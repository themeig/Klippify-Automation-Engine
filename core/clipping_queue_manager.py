import paths
import os
import sys
import json
import uuid
import re
import threading
from pathlib import Path
from datetime import datetime

BASE_DIR = paths.PROJECT_ROOT
QUEUE_FILE = BASE_DIR / "clipping_queue.json"
METADATA_FILE = BASE_DIR / "clip_metadata.json"
_lock = threading.Lock()

def load_clip_metadata():
    with _lock:
        if not METADATA_FILE.exists():
            return {}
        try:
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[METADATA] Errore lettura {METADATA_FILE}: {e}")
            return {}

def save_clip_metadata(clip_filename, meta_dict):
    with _lock:
        try:
            data = {}
            if METADATA_FILE.exists():
                try:
                    with open(METADATA_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            
            data[str(clip_filename)] = meta_dict
            tmp = METADATA_FILE.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            tmp.replace(METADATA_FILE)
        except Exception as e:
            print(f"[METADATA] Errore salvataggio {METADATA_FILE}: {e}")

def get_clip_metadata(clip_filename):
    data = load_clip_metadata()
    return data.get(str(clip_filename), {})

def _load_all_queues():
    with _lock:
        if not QUEUE_FILE.exists():
            return {}
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[CLIPPING_QUEUE] Errore lettura {QUEUE_FILE}: {e}")
            return {}

def _save_all_queues(data):
    with _lock:
        try:
            tmp = QUEUE_FILE.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            tmp.replace(QUEUE_FILE)
        except Exception as e:
            print(f"[CLIPPING_QUEUE] Errore salvataggio {QUEUE_FILE}: {e}")

def get_campaign_queue(campaign_id):
    """
    Restituisce la coda video per la campagna specificata,
    sincronizzandosi automaticamente con i file fisici presenti in clipping_sources.
    """
    all_q = _load_all_queues()
    cid = str(campaign_id)
    queue = all_q.get(cid, [])

    # Sincronizza con la cartella fisica clipping_sources/<campaign_id>
    sanitized_camp = re.sub(r'[^a-zA-Z0-9_]', '_', cid)
    sources_dir = BASE_DIR / "clipping_sources" / sanitized_camp
    if not sources_dir.exists():
        sources_dir = BASE_DIR / "clipping_sources" / cid

    existing_filenames = set(item.get("filename") for item in queue)
    
    if sources_dir.exists():
        for ext in ["*.mp4", "*.mov", "*.mkv", "*.avi", "*.webm"]:
            for fpath in sources_dir.glob(ext):
                fname = fpath.name
                if fname not in existing_filenames:
                    size_mb = fpath.stat().st_size / (1024 * 1024)
                    queue.append({
                        "id": f"cq_{uuid.uuid4().hex[:8]}",
                        "filename": fname,
                        "file_size_mb": round(size_mb, 2),
                        "uploaded_at": datetime.fromtimestamp(fpath.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "queued",
                        "error_message": None,
                        "generated_clips": [],
                        "processed_at": None
                    })
                    existing_filenames.add(fname)

    all_q[cid] = queue
    _save_all_queues(all_q)
    return queue

def add_video_to_queue(campaign_id, filename, file_size_mb=0):
    """Aggiunge o aggiorna un video nella coda di clipping della campagna."""
    all_q = _load_all_queues()
    cid = str(campaign_id)
    queue = all_q.get(cid, [])

    # Controlla se esiste già
    found = False
    for item in queue:
        if item.get("filename") == filename:
            item["status"] = "queued"
            item["error_message"] = None
            item["uploaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if file_size_mb > 0:
                item["file_size_mb"] = round(file_size_mb, 2)
            found = True
            break

    if not found:
        new_item = {
            "id": f"cq_{uuid.uuid4().hex[:8]}",
            "filename": filename,
            "file_size_mb": round(file_size_mb, 2),
            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "queued",
            "error_message": None,
            "generated_clips": [],
            "processed_at": None
        }
        queue.append(new_item)

    all_q[cid] = queue
    _save_all_queues(all_q)
    return queue

def remove_video_from_queue(campaign_id, item_id_or_filename):
    """Rimuove un video dalla coda."""
    all_q = _load_all_queues()
    cid = str(campaign_id)
    queue = all_q.get(cid, [])
    queue = [it for it in queue if it.get("id") != item_id_or_filename and it.get("filename") != item_id_or_filename]
    all_q[cid] = queue
    _save_all_queues(all_q)
    return queue

def update_video_status(campaign_id, filename, status, generated_clips=None, error_message=None):
    """Aggiorna lo stato di un video nella coda."""
    all_q = _load_all_queues()
    cid = str(campaign_id)
    queue = all_q.get(cid, [])
    for item in queue:
        if item.get("filename") == filename or item.get("id") == filename:
            item["status"] = status
            if generated_clips is not None:
                item["generated_clips"] = generated_clips
            if error_message is not None:
                item["error_message"] = error_message
            if status == "completed":
                item["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    all_q[cid] = queue
    _save_all_queues(all_q)

def process_campaign_queue_sequential(campaign_id, task_id=None):
    """
    Esegue in sequenza tutti i video con status 'queued' nella coda della campagna.
    Per ciascun video invoca clipping_pipeline e aggiorna lo stato.
    """
    from process_manager import process_manager
    import clipping_pipeline

    queue = get_campaign_queue(campaign_id)
    queued_items = [it for it in queue if it.get("status") in ["queued", "error", "processing"]]

    if not queued_items:
        if task_id:
            process_manager.log(task_id, f"Nessun video in coda da elaborare per la campagna {campaign_id}.")
            process_manager.finish_task(task_id, status="completed")
        return {"status": "ok", "processed_count": 0, "message": "Nessun video in coda."}

    total = len(queued_items)
    if task_id:
        process_manager.log(task_id, f"🎬 Avvio elaborazione sequenziale di {total} video in coda per la campagna {campaign_id}...")

    processed_count = 0
    all_generated_clips = []

    def task_log(m):
        if task_id:
            process_manager.log(task_id, str(m))

    for idx, item in enumerate(queued_items):
        fname = item.get("filename")
        task_log(f"[{idx+1}/{total}] ⏳ Inizio analisi Gemini & ritaglio per '{fname}'...")

        update_video_status(campaign_id, fname, status="processing")

        try:
            res = clipping_pipeline.run_clipping_workflow(
                campaign_id=campaign_id,
                video_source_path=fname,
                is_auto=True,
                task_logger=task_log
            )

            if res.get("status") == "success" and res.get("clips"):
                clips = res.get("clips")
                clip_names = [c.get("video_filename") for c in clips if c.get("video_filename")]
                all_generated_clips.extend(clip_names)
                update_video_status(campaign_id, fname, status="completed", generated_clips=clip_names)
                processed_count += 1
                if task_id:
                    process_manager.log(task_id, f"[{idx+1}/{total}] ✅ Video '{fname}' completato! Generate {len(clip_names)} clip 9:16.")
            else:
                err = res.get("message", "Nessuna clip generata")
                update_video_status(campaign_id, fname, status="error", error_message=err)
                if task_id:
                    process_manager.log(task_id, f"[{idx+1}/{total}] ❌ Errore su '{fname}': {err}")

        except Exception as e:
            update_video_status(campaign_id, fname, status="error", error_message=str(e))
            if task_id:
                process_manager.log(task_id, f"[{idx+1}/{total}] ❌ Eccezione durante il clipping di '{fname}': {e}")

    if task_id:
        process_manager.log(task_id, f"🎉 Sequenza di clipping completata: {processed_count}/{total} video elaborati.")
        process_manager.finish_task(task_id, status="completed" if processed_count > 0 else "completed")

    return {"status": "ok", "processed_count": processed_count, "clips": all_generated_clips}

_active_clipping_campaigns = set()
_clipping_lock = threading.Lock()

def is_campaign_clipping(campaign_id):
    with _clipping_lock:
        return str(campaign_id) in _active_clipping_campaigns

def start_auto_clipping_for_campaign(campaign_id):
    """Avvia in background l'elaborazione automatica a cascata dei video in coda per la campagna."""
    cid = str(campaign_id)
    with _clipping_lock:
        if cid in _active_clipping_campaigns:
            return False
        _active_clipping_campaigns.add(cid)

    def worker():
        task_id = None
        try:
            from process_manager import process_manager
            task_id = process_manager.create_task(
                "clipping_queue",
                f"🎬 Clipping Automatico Continuo ({cid})"
            )
            process_campaign_queue_sequential(cid, task_id=task_id)
        except Exception as e:
            print(f"[AUTO-CLIPPING WORKER ERROR] {cid}: {e}")
            if task_id:
                try:
                    process_manager.finish_task(task_id, status="error", error=str(e))
                except Exception:
                    pass
        finally:
            if task_id:
                try:
                    # Se il task è ancora in stato 'running', chiudilo come completato
                    if task_id in process_manager.tasks and process_manager.tasks[task_id].get("status") == "running":
                        process_manager.finish_task(task_id, status="completed")
                except Exception:
                    pass
            with _clipping_lock:
                _active_clipping_campaigns.discard(cid)

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return True