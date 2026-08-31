import paths
import os
import sys
import json
import time
import uuid
import threading
from pathlib import Path
from datetime import datetime, timedelta

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = paths.PROJECT_ROOT
STATE_FILE = BASE_DIR / "autopilot_state.json"
CAMPAIGNS_CLASSIFIED_FILE = BASE_DIR / "active_campaigns_classified.json"
CAMPAIGNS_RANKED_FILE = BASE_DIR / "campaigns_ranked.json"
GENERATED_CONTENT_FILE = BASE_DIR / "generated_content.json"

import clipping_queue_manager

_lock = threading.Lock()
_engine_thread = None
_engine_running = False

DEFAULT_STATE = {
    "is_enabled": False,
    "mode": "interval",               # "interval" oppure "fixed_times"
    "interval_minutes": 180,           # default: pubblica ogni 3 ore (180 minuti)
    "fixed_times": ["12:00", "15:30", "19:00", "22:00"],
    "max_daily_uploads": 5,
    "today_uploads_count": 0,
    "last_upload_date": "",
    "last_upload_timestamp": None,
    "next_scheduled_run": None,
    "current_working_task": None,
    "queue": [],
    "history": []
}

def load_state():
    with _lock:
        if not STATE_FILE.exists():
            save_state_unlocked(DEFAULT_STATE)
            return DEFAULT_STATE.copy()
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure all default keys exist
                for k, v in DEFAULT_STATE.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception as e:
            print(f"[AUTOPILOT ERROR] Impossibile leggere {STATE_FILE}: {e}")
            return DEFAULT_STATE.copy()

def save_state_unlocked(data):
    try:
        temp_file = STATE_FILE.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        temp_file.replace(STATE_FILE)
    except Exception as e:
        print(f"[AUTOPILOT ERROR] Impossibile salvare {STATE_FILE}: {e}")

def save_state(data):
    with _lock:
        save_state_unlocked(data)

def get_campaign_info(campaign_id):
    """Recupera nome, cta, hashtag e menzioni per la campagna specificata."""
    c_info = {
        "id": campaign_id,
        "name": str(campaign_id),
        "cta": "Guarda il video completo sul profilo!",
        "hashtags": ["#klippify", "#fyp", "#viral"],
        "mentions": []
    }
    
    # 1. Cerca in active_campaigns_classified.json
    if CAMPAIGNS_CLASSIFIED_FILE.exists():
        try:
            with open(CAMPAIGNS_CLASSIFIED_FILE, "r", encoding="utf-8") as f:
                camps = json.load(f)
                for c in camps:
                    cid = c.get("id") or c.get("campaign_token") or c.get("campaign_id")
                    if str(cid) == str(campaign_id) or (c.get("name") and c.get("name").lower() == str(campaign_id).lower()):
                        c_info["name"] = c.get("name") or c_info["name"]
                        c_info["cta"] = c.get("call_to_action") or c_info["cta"]
                        if c.get("mandatory_hashtags"):
                            c_info["hashtags"] = c.get("mandatory_hashtags")
                        if c.get("mandatory_mentions"):
                            c_info["mentions"] = c.get("mandatory_mentions")
                        return c_info
        except Exception:
            pass

    # 2. Cerca in campaigns_ranked.json
    if CAMPAIGNS_RANKED_FILE.exists():
        try:
            with open(CAMPAIGNS_RANKED_FILE, "r", encoding="utf-8") as f:
                camps = json.load(f)
                for c in camps:
                    cid = c.get("id") or c.get("campaign_token")
                    if str(cid) == str(campaign_id) or (c.get("name") and c.get("name").lower() == str(campaign_id).lower()):
                        c_info["name"] = c.get("name") or c_info["name"]
                        c_info["cta"] = c.get("call_to_action") or c_info["cta"]
                        if c.get("mandatory_hashtags"):
                            c_info["hashtags"] = c.get("mandatory_hashtags")
                        if c.get("mandatory_mentions"):
                            c_info["mentions"] = c.get("mandatory_mentions")
                        return c_info
        except Exception:
            pass

    return c_info

def compute_next_run(state):
    """Calcola il prossimo orario di pubblicazione pianificato."""
    if not state.get("is_enabled"):
        return None
    
    # Reset conteggio giornaliero se è cambiato giorno
    today_str = datetime.now().strftime("%Y-%m-%d")
    if state.get("last_upload_date") != today_str:
        state["today_uploads_count"] = 0
        state["last_upload_date"] = today_str

    if state.get("today_uploads_count", 0) >= state.get("max_daily_uploads", 5):
        # Limite giornaliero raggiunto, programma per domani alle prima fascia oraria
        tomorrow = datetime.now() + timedelta(days=1)
        first_time = state.get("fixed_times", ["12:00"])[0] if state.get("mode") == "fixed_times" else "12:00"
        return f"{tomorrow.strftime('%Y-%m-%d')} {first_time}:00"

    now = datetime.now()
    queue = state.get("queue", [])
    
    # 1. Se ci sono clip pronte con orario di slot specifico per oggi
    upcoming_slots = []
    has_due_slot = False
    for it in queue:
        if it.get("status") in ["ready", "queued"] and it.get("scheduled_time"):
            try:
                h, m = map(int, it["scheduled_time"].split(":"))
                slot_dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if slot_dt <= now and it.get("status") == "ready":
                    has_due_slot = True
                elif slot_dt > now:
                    upcoming_slots.append(slot_dt)
            except Exception:
                pass
                
    if has_due_slot:
        return now.strftime("%Y-%m-%d %H:%M:%S")
        
    if upcoming_slots:
        earliest = min(upcoming_slots)
        return earliest.strftime("%Y-%m-%d %H:%M:%S")

    mode = state.get("mode", "interval")

    if mode == "interval":
        interval_min = state.get("interval_minutes", 180)
        last_ts_str = state.get("last_upload_timestamp")
        if last_ts_str:
            try:
                last_dt = datetime.fromisoformat(last_ts_str)
                next_dt = last_dt + timedelta(minutes=interval_min)
                if next_dt <= now:
                    return now.strftime("%Y-%m-%d %H:%M:%S")
                return next_dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
        # Nessun upload precedente registrato: pronto subito!
        return now.strftime("%Y-%m-%d %H:%M:%S")

    elif mode == "fixed_times":
        fixed_times = state.get("fixed_times", ["12:00", "16:00", "20:00"])
        # Trova il prossimo orario oggi
        for t_str in sorted(fixed_times):
            try:
                h, m = map(int, t_str.split(":"))
                slot_dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if slot_dt > now:
                    return slot_dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                continue
        # Se tutti gli orari di oggi sono passati, programma per il primo orario di domani
        first_t = sorted(fixed_times)[0]
        h, m = map(int, first_t.split(":"))
        tomorrow_slot = (now + timedelta(days=1)).replace(hour=h, minute=m, second=0, microsecond=0)
        return tomorrow_slot.strftime("%Y-%m-%d %H:%M:%S")

    return (now + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

def add_queue_item(campaign_id, source_video, item_type="clipping", custom_caption=None, concept_name=None, scheduled_time=None):
    """Aggiunge un video o una richiesta di clipping alla coda di lavoro."""
    camp_info = get_campaign_info(campaign_id)
    item_id = str(uuid.uuid4())[:8]
    
    # Se non specificata, genera la caption TikTok ottimizzata
    if not custom_caption:
        tags_str = " ".join(camp_info["hashtags"])
        mentions_str = " ".join(camp_info["mentions"])
        cta_str = camp_info["cta"]
        custom_caption = f"Guarda fino alla fine! 🚀 {cta_str} 💡 {mentions_str} {tags_str}".strip()

    new_item = {
        "id": item_id,
        "campaign_id": campaign_id,
        "campaign_name": camp_info["name"],
        "type": item_type,                  # "clipping" (da ritagliare) oppure "ready_clip" (già 9:16)
        "source_video": source_video,
        "concept_name": concept_name or f"Clip per {camp_info['name']}",
        "generated_clip": source_video if item_type == "ready_clip" else None,
        "caption": custom_caption,
        "scheduled_time": scheduled_time,
        "status": "ready" if item_type == "ready_clip" else "queued",
        "error_message": None,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "published_at": None,
        "tiktok_url": None,
        "klippify_status": None
    }

    state = load_state()
    state["queue"].append(new_item)
    state["next_scheduled_run"] = compute_next_run(state)
    save_state(state)
    print(f"[AUTOPILOT] Aggiunto elemento alla coda: {new_item['concept_name']} (ID: {item_id}, Tipo: {item_type})")
    return new_item

def remove_queue_item(item_id):
    """Rimuove un elemento dalla coda."""
    state = load_state()
    state["queue"] = [it for it in state.get("queue", []) if it.get("id") != item_id]
    state["next_scheduled_run"] = compute_next_run(state)
    save_state(state)
    return True

def reorder_queue(item_ids_list):
    """Riordina gli elementi nella coda in base alla lista di ID fornita."""
    state = load_state()
    current_q = {it.get("id"): it for it in state.get("queue", [])}
    new_q = []
    for iid in item_ids_list:
        if iid in current_q:
            new_q.append(current_q[iid])
            del current_q[iid]
    # Aggiungi eventuali elementi rimanenti
    new_q.extend(current_q.values())
    state["queue"] = new_q
    state["next_scheduled_run"] = compute_next_run(state)
    save_state(state)
    return True

def toggle_engine(enable=None):
    """Attiva o mette in pausa il pilota automatico."""
    state = load_state()
    if enable is None:
        state["is_enabled"] = not state.get("is_enabled", False)
    else:
        state["is_enabled"] = bool(enable)
    state["next_scheduled_run"] = compute_next_run(state)
    save_state(state)
    print(f"[AUTOPILOT] Stato Pilota Automatico cambiato in: {'🟢 ATTIVO' if state['is_enabled'] else '⏸ IN PAUSA'}")
    return state["is_enabled"]

def update_settings(settings_dict):
    """Aggiorna le impostazioni di programmazione e limiti."""
    state = load_state()
    if "mode" in settings_dict and settings_dict["mode"] in ["interval", "fixed_times"]:
        state["mode"] = settings_dict["mode"]
    if "interval_minutes" in settings_dict:
        state["interval_minutes"] = max(15, int(settings_dict["interval_minutes"]))
    if "fixed_times" in settings_dict and isinstance(settings_dict["fixed_times"], list):
        state["fixed_times"] = settings_dict["fixed_times"]
    if "max_daily_uploads" in settings_dict:
        state["max_daily_uploads"] = max(1, int(settings_dict["max_daily_uploads"]))
    state["next_scheduled_run"] = compute_next_run(state)
    save_state(state)
    return state

# ==========================================
# CAMPAIGN-SPECIFIC AUTOPILOT HELPERS
# ==========================================

def get_campaign_autopilot_status(campaign_id):
    """Restituisce lo stato dell'autopilota filtrato per la specifica campagna."""
    state = load_state()
    sched_file = BASE_DIR / "campaign_schedules.json"
    camp_sched = {}
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as f:
                schedules = json.load(f)
                camp_sched = schedules.get(campaign_id, {})
        except Exception:
            pass

    camp_queue = [it for it in state.get("queue", []) if str(it.get("campaign_id")) == str(campaign_id)]
    camp_history = [it for it in state.get("history", []) if str(it.get("campaign_id")) == str(campaign_id)]
    
    # La verità ufficiale per la singola campagna è SEMPRE autopilot_enabled in campaign_schedules.json
    is_campaign_active = bool(camp_sched.get("autopilot_enabled", False))
    
    ready_clips = [it for it in camp_queue if it.get("status") == "ready"]
    next_clip = ready_clips[0] if ready_clips else (camp_queue[0] if camp_queue else None)

    pause_until_str = camp_sched.get("pause_until")
    is_paused = False
    if pause_until_str:
        try:
            p_dt = datetime.strptime(pause_until_str, "%Y-%m-%d %H:%M:%S")
            if datetime.now() < p_dt:
                is_paused = True
            else:
                camp_sched["pause_until"] = None
                camp_sched["is_paused"] = False
        except Exception:
            pass

    is_ended = bool(camp_sched.get("is_ended", False))

    return {
        "campaign_id": campaign_id,
        "is_enabled": is_campaign_active and not is_paused and not is_ended,
        "is_paused": is_paused,
        "pause_until": pause_until_str if is_paused else None,
        "is_ended": is_ended,
        "ended_at": camp_sched.get("ended_at"),
        "queue": camp_queue,
        "history": camp_history,
        "next_clip": next_clip,
        "ready_count": len(ready_clips),
        "total_queued": len(camp_queue),
        "target_count": camp_sched.get("target_count", 3),
        "slots": camp_sched.get("slots", [])
    }

def pause_campaign(campaign_id, days=1, until_iso=None):
    """
    Mette in pausa temporanea la campagna per un numero specificato di giorni (default: 1 giorno).
    Allo scadere della pausa, il motore riprenderà automaticamente le pubblicazioni standard.
    """
    sched_file = BASE_DIR / "campaign_schedules.json"
    schedules = {}
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as f:
                schedules = json.load(f)
        except Exception:
            schedules = {}

    if campaign_id not in schedules:
        schedules[campaign_id] = {"target_count": 3, "slots": [], "autopilot_enabled": True}

    if until_iso:
        pause_until_str = until_iso
    else:
        now = datetime.now()
        pause_until_dt = now + timedelta(days=float(days))
        pause_until_str = pause_until_dt.strftime("%Y-%m-%d %H:%M:%S")

    schedules[campaign_id]["pause_until"] = pause_until_str
    schedules[campaign_id]["is_paused"] = True
    schedules[campaign_id]["is_ended"] = False
    schedules[campaign_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(sched_file, "w", encoding="utf-8") as f:
            json.dump(schedules, f, indent=2, ensure_ascii=False)
        print(f"[AUTOPILOT] ⏸️ Campagna '{campaign_id}' messa in PAUSA fino al {pause_until_str} ({days} giorno/i).")
    except Exception as e:
        print(f"[AUTOPILOT ERROR] Errore salvataggio pausa {sched_file}: {e}")

    # Rimuovi task pendenti in coda
    state = load_state()
    state["queue"] = [it for it in state.get("queue", []) if str(it.get("campaign_id")) != str(campaign_id)]
    save_state(state)

    return {
        "status": "ok",
        "campaign_id": campaign_id,
        "is_paused": True,
        "pause_until": pause_until_str
    }

def end_campaign(campaign_id):
    """
    Termina definitivamente la campagna. La pubblicazione viene interrotta per sempre.
    """
    sched_file = BASE_DIR / "campaign_schedules.json"
    schedules = {}
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as f:
                schedules = json.load(f)
        except Exception:
            schedules = {}

    if campaign_id not in schedules:
        schedules[campaign_id] = {"target_count": 3, "slots": []}

    schedules[campaign_id]["autopilot_enabled"] = False
    schedules[campaign_id]["is_ended"] = True
    schedules[campaign_id]["is_paused"] = False
    schedules[campaign_id]["pause_until"] = None
    schedules[campaign_id]["ended_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    schedules[campaign_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(sched_file, "w", encoding="utf-8") as f:
            json.dump(schedules, f, indent=2, ensure_ascii=False)
        print(f"[AUTOPILOT] 🛑 Campagna '{campaign_id}' TERMINATA per sempre.")
    except Exception as e:
        print(f"[AUTOPILOT ERROR] Errore salvataggio termina campagna {sched_file}: {e}")

    state = load_state()
    state["queue"] = [it for it in state.get("queue", []) if str(it.get("campaign_id")) != str(campaign_id)]
    save_state(state)

    return {
        "status": "ok",
        "campaign_id": campaign_id,
        "is_ended": True,
        "autopilot_enabled": False
    }

def resume_campaign(campaign_id):
    """
    Riprende immediatamente la campagna rimuovendo pause o stato terminato.
    """
    sched_file = BASE_DIR / "campaign_schedules.json"
    schedules = {}
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as f:
                schedules = json.load(f)
        except Exception:
            schedules = {}

    if campaign_id not in schedules:
        schedules[campaign_id] = {"target_count": 3, "slots": []}

    schedules[campaign_id]["autopilot_enabled"] = True
    schedules[campaign_id]["is_paused"] = False
    schedules[campaign_id]["is_ended"] = False
    schedules[campaign_id]["pause_until"] = None
    schedules[campaign_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(sched_file, "w", encoding="utf-8") as f:
            json.dump(schedules, f, indent=2, ensure_ascii=False)
        print(f"[AUTOPILOT] ▶️ Campagna '{campaign_id}' RIPRESA regolarmente.")
    except Exception as e:
        print(f"[AUTOPILOT ERROR] Errore ripresa {sched_file}: {e}")

    toggle_engine(True)
    queue_campaign_slots(campaign_id)

    return {
        "status": "ok",
        "campaign_id": campaign_id,
        "is_paused": False,
        "is_ended": False,
        "autopilot_enabled": True
    }

def toggle_campaign_autopilot(campaign_id, enable=None):
    """Attiva o disattiva il pilota automatico per una specifica campagna."""
    sched_file = BASE_DIR / "campaign_schedules.json"
    schedules = {}
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as f:
                schedules = json.load(f)
        except Exception:
            schedules = {}

    if campaign_id not in schedules:
        schedules[campaign_id] = {"target_count": 3, "slots": [], "autopilot_enabled": False}

    current_val = schedules[campaign_id].get("autopilot_enabled", False)
    new_val = not current_val if enable is None else bool(enable)
    schedules[campaign_id]["autopilot_enabled"] = new_val
    if new_val:
        schedules[campaign_id]["is_ended"] = False
        schedules[campaign_id]["is_paused"] = False
        schedules[campaign_id]["pause_until"] = None

    try:
        with open(sched_file, "w", encoding="utf-8") as f:
            json.dump(schedules, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[AUTOPILOT ERROR] Errore salvataggio {sched_file}: {e}")

    state = load_state()

    # Se attivato, assicurati che il motore globale sia attivo e che gli slot siano accodati
    if new_val:
        toggle_engine(True)
        # Se non ci sono elementi in coda per questa campagna, accoda gli slot
        has_items = any(str(it.get("campaign_id")) == str(campaign_id) for it in state.get("queue", []))
        if not has_items:
            queue_campaign_slots(campaign_id)
    else:
        # Se disattivato, rimuovi tutti gli elementi in coda per questa campagna
        state["queue"] = [it for it in state.get("queue", []) if str(it.get("campaign_id")) != str(campaign_id)]
        
        # Se nessuna altra campagna ha l'autopilota abilitato, metti in pausa anche il motore globale
        any_active_camp = any(v.get("autopilot_enabled", False) for k, v in schedules.items() if isinstance(v, dict))
        if not any_active_camp:
            state["is_enabled"] = False
        
        save_state(state)

    return new_val

def mark_clip_as_published(campaign_id, clip_filename):
    """Registra in modo permanente la clip come pubblicata e non più riutilizzabile."""
    if not clip_filename:
        return
    sched_file = BASE_DIR / "campaign_schedules.json"
    schedules = {}
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as f:
                schedules = json.load(f)
        except Exception:
            schedules = {}
    
    if campaign_id not in schedules:
        schedules[campaign_id] = {"target_count": 3, "slots": [], "published_clips": []}
    
    pub_list = schedules[campaign_id].get("published_clips", [])
    if clip_filename not in pub_list:
        pub_list.append(clip_filename)
        schedules[campaign_id]["published_clips"] = pub_list
        try:
            with open(sched_file, "w", encoding="utf-8") as f:
                json.dump(schedules, f, indent=2, ensure_ascii=False)
            print(f"[AUTOPILOT] Clip '{clip_filename}' registrata come PUBBLICATA (non riutilizzabile) per campagna {campaign_id}.")
        except Exception as e:
            print(f"[AUTOPILOT ERROR] Errore salvataggio published_clips: {e}")

def get_available_virgin_clips(campaign_id):
    """Restituisce le clip 9:16 disponibili escludendo quelle già pubblicate per la campagna."""
    sched_file = BASE_DIR / "campaign_schedules.json"
    pub_clips = set()
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as f:
                schedules = json.load(f)
                pub_clips = set(schedules.get(campaign_id, {}).get("published_clips", []))
        except Exception:
            pass

    # Aggiungi anche dal file storico globale published_content.json
    pub_file = BASE_DIR / "published_content.json"
    if pub_file.exists():
        try:
            with open(pub_file, "r", encoding="utf-8") as f:
                pub_data = json.load(f)
                for p in pub_data:
                    if p.get("filename") and (p.get("tiktok_url") or p.get("content_url") or p.get("status") in ["published", "accepted"]):
                        pub_clips.add(p["filename"])
        except Exception:
            pass

    # Elenca i file video verticali appartenenti RIGOROSAMENTE a questa specifica campagna
    gen_dir = BASE_DIR / "generated_videos"
    camp_files = []
    seen = set()

    def add_files_from(sdir):
        if sdir.exists():
            for item in sorted(sdir.iterdir(), key=lambda x: x.stat().st_mtime):
                if item.is_file() and item.suffix.lower() in [".mp4", ".mov"]:
                    if item.name not in seen:
                        seen.add(item.name)
                        camp_files.append(item.name)

    if campaign_id:
        cid_str = str(campaign_id)
        # 1. Cerca nella sottocartella clips della campagna
        add_files_from(gen_dir / cid_str / "clips")
        add_files_from(gen_dir / cid_str)
        add_files_from(BASE_DIR / "clipping_sources" / cid_str / "clips")
        add_files_from(BASE_DIR / "clipping_sources" / cid_str)

        # 2. Cerca nella root di generated_videos SOLO se il nome corrisponde alla campagna
        if gen_dir.exists():
            for item in sorted(gen_dir.iterdir(), key=lambda x: x.stat().st_mtime):
                if item.is_file() and item.suffix.lower() in [".mp4", ".mov"]:
                    fname = item.name
                    if cid_str in fname and fname not in seen:
                        seen.add(fname)
                        camp_files.append(fname)
                    elif cid_str == "6a71c6f7245627c68999eae2" and ("SaraDizdari" in fname or "Sara" in fname) and fname not in seen:
                        seen.add(fname)
                        camp_files.append(fname)
                    elif cid_str == "6a426231e6a21896f769dc80" and ("Dose" in fname or "dose" in fname) and fname not in seen:
                        seen.add(fname)
                        camp_files.append(fname)
    else:
        # Fallback generale
        add_files_from(gen_dir)

    # Filtra: clip 9:16, dimensione valida (> 0.8MB) e NON presenti nello storico pubblicato
    import subprocess
    virgin = []
    for f in camp_files:
        if (f.startswith("clip_") or "clip" in f.lower()) and f not in pub_clips:
            # Verifica che il file non sia corrotto o incompleto (< 0.8 MB)
            f_path = None
            for cand_p in [gen_dir / (str(campaign_id) if campaign_id else "") / "clips" / f, gen_dir / (str(campaign_id) if campaign_id else "") / f, gen_dir / f]:
                if cand_p.exists():
                    f_path = cand_p
                    break
            if f_path and f_path.stat().st_size >= 800 * 1024:
                try:
                    chk = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(f_path)], capture_output=True, text=True, timeout=2)
                    if chk.stdout.strip():
                        virgin.append(f)
                except Exception:
                    virgin.append(f)
    return virgin, pub_clips

def advance_campaign_slots(campaign_id, force_new_day=False):
    """
    Fa scorrere da sola la catena di montaggio:
    - A ogni nuovo giorno (mezzanotte), ricarica tutti gli slot con le prossime clip 9:16 vergini disponibili.
    - Durante la giornata, assegna le clip vergini agli slot liberi.
    """
    sched_file = BASE_DIR / "campaign_schedules.json"
    schedules = {}
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as f:
                schedules = json.load(f)
        except Exception:
            schedules = {}

    camp_sched = schedules.get(campaign_id, {"target_count": 4, "slots": [], "autopilot_enabled": True})
    current_slots = camp_sched.get("slots", [])
    sorted_slots = sorted(current_slots, key=lambda s: s.get("time", "99:99"))
    target_count = max(camp_sched.get("target_count", 4), len(sorted_slots))
    default_times = ["12:00", "15:00", "18:00", "20:00", "21:30"]

    today_str = datetime.now().strftime("%Y-%m-%d")
    last_sched_date = camp_sched.get("schedule_date", "")
    is_new_day = (last_sched_date != today_str) or force_new_day

    virgin_clips, pub_clips = get_available_virgin_clips(campaign_id)
    print(f"[AUTOPILOT ADVANCE] Campagna {campaign_id}: {len(virgin_clips)} vergini, {len(pub_clips)} pubblicate. (Nuovo giorno: {is_new_day})")

    new_slots = []
    assigned_vids = set()
    v_idx = 0

    for i in range(target_count):
        slot_time = (sorted_slots[i].get("time") if i < len(sorted_slots) and sorted_slots[i].get("time") else default_times[i] if i < len(default_times) else "15:00")
        existing_vid = sorted_slots[i].get("video") if i < len(sorted_slots) else ""

        if is_new_day:
            # Nuovo giorno: popola tutti gli slot con le prossime clip vergini disponibili
            while v_idx < len(virgin_clips) and virgin_clips[v_idx] in assigned_vids:
                v_idx += 1
            if v_idx < len(virgin_clips):
                assigned_video = virgin_clips[v_idx]
                assigned_vids.add(assigned_video)
                v_idx += 1
            else:
                assigned_video = ""
        else:
            # Stesso giorno: mantieni lo storico di quanto già pubblicato oggi
            if existing_vid and existing_vid in pub_clips:
                assigned_video = existing_vid
            elif existing_vid and existing_vid in virgin_clips and existing_vid not in assigned_vids:
                assigned_video = existing_vid
                assigned_vids.add(assigned_video)
            else:
                while v_idx < len(virgin_clips) and virgin_clips[v_idx] in assigned_vids:
                    v_idx += 1
                if v_idx < len(virgin_clips):
                    assigned_video = virgin_clips[v_idx]
                    assigned_vids.add(assigned_video)
                    v_idx += 1
                else:
                    assigned_video = ""

        new_slots.append({
            "time": slot_time,
            "video": assigned_video
        })

    new_slots = sorted(new_slots, key=lambda s: s.get("time", "99:99"))
    camp_sched["target_count"] = len(new_slots)
    camp_sched["slots"] = new_slots
    camp_sched["schedule_date"] = today_str
    camp_sched["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    schedules[campaign_id] = camp_sched

    try:
        with open(sched_file, "w", encoding="utf-8") as f:
            json.dump(schedules, f, indent=2, ensure_ascii=False)
        print(f"[AUTOPILOT ADVANCE] Slot aggiornati con successo per {campaign_id}: {[s['video'] for s in new_slots]}")
    except Exception as e:
        print(f"[AUTOPILOT ERROR] Errore salvataggio slot in {sched_file}: {e}")

    return new_slots

def queue_campaign_slots(campaign_id):
    """Fa avanzare automaticamente le clip vergini negli slot e li accoda per la pubblicazione autonoma."""
    # 1. Assegnazione automatica a scorrimento delle clip non pubblicate
    advance_campaign_slots(campaign_id)

    sched_file = BASE_DIR / "campaign_schedules.json"
    schedules = {}
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as f:
                schedules = json.load(f)
        except Exception:
            schedules = {}

    camp_sched = schedules.get(campaign_id, {})
    slots = camp_sched.get("slots", [])
    valid_slots = [s for s in slots if s.get("video")]

    # Recupera didascalie personalizzate da generated_content.json se presenti
    scripts = []
    if GENERATED_CONTENT_FILE.exists():
        try:
            with open(GENERATED_CONTENT_FILE, "r", encoding="utf-8") as gcf:
                gen_data = json.load(gcf)
                for c in gen_data:
                    if str(c.get("campaign_id")) == str(campaign_id):
                        scripts = c.get("scripts", [])
                        break
        except Exception:
            scripts = []

    camp_info = get_campaign_info(campaign_id)

    added_items = []
    if valid_slots:
        for idx, s in enumerate(valid_slots):
            caption = None
            if idx < len(scripts) and scripts[idx].get("tiktok_caption"):
                caption = scripts[idx]["tiktok_caption"]
            
            item = add_queue_item(
                campaign_id=campaign_id,
                source_video=s.get("video"),
                item_type="ready_clip",
                custom_caption=caption,
                concept_name=f"Slot {idx+1} ({s.get('time', '12:00')}) - {s.get('video')}",
                scheduled_time=s.get("time")
            )
            added_items.append(item)
    else:
        # Accoda richiesta di clipping automatico
        item = add_queue_item(
            campaign_id=campaign_id,
            source_video="source_video",
            item_type="clipping",
            concept_name=f"Clipping & Generazione Slot Automatici ({camp_info['name']})"
        )
        added_items.append(item)

    # Assicurati che l'autopilota sia attivo per questa campagna
    if campaign_id in schedules:
        schedules[campaign_id]["autopilot_enabled"] = True
        try:
            with open(sched_file, "w", encoding="utf-8") as f:
                json.dump(schedules, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    toggle_engine(True)
    return added_items

def trigger_campaign_run_now(campaign_id):
    """Forza l'esecuzione immediata del prossimo video per la campagna specificata."""
    state = load_state()
    queue = state.get("queue", [])
    
    # 1. Cerca la prima clip pronta specifica di QUESTA campagna
    camp_ready_item = next((it for it in queue if str(it.get("campaign_id")) == str(campaign_id) and it.get("status") == "ready"), None)
    
    if camp_ready_item:
        for it in state["queue"]:
            if it.get("id") == camp_ready_item.get("id"):
                it["status"] = "publishing"
        save_state(state)
        threading.Thread(target=execute_publish_step, args=(camp_ready_item,), daemon=True).start()
        return {"status": "ok", "message": f"Pubblicazione avviata per '{camp_ready_item.get('concept_name')}'!"}

    # 2. Se non c'è una clip pronta, cerca se c'è un task di clipping in coda per questa campagna
    camp_clip_item = next((it for it in queue if str(it.get("campaign_id")) == str(campaign_id) and it.get("status") == "queued"), None)
    if camp_clip_item:
        threading.Thread(target=execute_clipping_step, args=(camp_clip_item,), daemon=True).start()
        return {"status": "ok", "message": f"Clipping avviato per '{camp_clip_item.get('concept_name')}'!"}

    # 3. Se non c'è nulla in coda, accoda gli slot configurati ed esegui subito il primo
    added = queue_campaign_slots(campaign_id)
    if added:
        first_item = added[0]
        state = load_state()
        if first_item.get("type") == "ready_clip":
            for it in state["queue"]:
                if it.get("id") == first_item.get("id"):
                    it["status"] = "publishing"
            save_state(state)
            threading.Thread(target=execute_publish_step, args=(first_item,), daemon=True).start()
            return {"status": "ok", "message": f"Pubblicazione avviata per '{first_item.get('concept_name')}'!"}
        else:
            threading.Thread(target=execute_clipping_step, args=(first_item,), daemon=True).start()
            return {"status": "ok", "message": f"Clipping avviato per '{first_item.get('concept_name')}'!"}

    return {"status": "error", "message": "Nessun video o slot disponibile per questa campagna."}


# ==========================================
# ESECUZIONE TASK AUTONOMI (WORKER)
# ==========================================

def execute_clipping_step(item):
    """Esegue il clipping di un video sorgente usando clipping_pipeline."""
    import process_manager
    task_id = process_manager.create_task(
        "clipping",
        f"✂️ Autopilota: Clipping video '{item.get('source_video')}' ({item.get('campaign_name')})"
    )
    
    try:
        process_manager.log(task_id, f"Inizio elaborazione clipping per la campagna {item.get('campaign_id')}...")
        import clipping_pipeline
        
        camp_id = item.get("campaign_id")
        source_v = item.get("source_video")
        
        res = clipping_pipeline.run_clipping_workflow(campaign_id=camp_id, video_source_path=source_v, is_auto=True)
        
        if res.get("status") == "success" and res.get("clips"):
            clips = res.get("clips")
            first_clip = clips[0]
            clip_file = first_clip.get("video_filename")
            
            # Aggiorna l'elemento corrente con la prima clip generata
            state = load_state()
            for it in state.get("queue", []):
                if it.get("id") == item.get("id"):
                    it["generated_clip"] = clip_file
                    it["status"] = "ready"
                    if first_clip.get("hook_text"):
                        camp_info = get_campaign_info(camp_id)
                        it["caption"] = f"{first_clip['hook_text']} 🚀 {camp_info['cta']} {' '.join(camp_info['mentions'])} {' '.join(camp_info['hashtags'])}"
                    break
            
            # Se sono state generate altre clip (es. slot 2, slot 3), le accoda automaticamente come 'ready'
            for extra_clip in clips[1:]:
                extra_file = extra_clip.get("video_filename")
                extra_hook = extra_clip.get("hook_text") or "Guarda cosa succede!"
                camp_info = get_campaign_info(camp_id)
                extra_caption = f"{extra_hook} 🚀 {camp_info['cta']} {' '.join(camp_info['mentions'])} {' '.join(camp_info['hashtags'])}"
                
                extra_item = {
                    "id": str(uuid.uuid4())[:8],
                    "campaign_id": camp_id,
                    "campaign_name": item.get("campaign_name"),
                    "type": "ready_clip",
                    "source_video": source_v,
                    "concept_name": f"{item.get('campaign_name')} - Slot Generato",
                    "generated_clip": extra_file,
                    "caption": extra_caption,
                    "status": "ready",
                    "error_message": None,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "published_at": None,
                    "tiktok_url": None,
                    "klippify_status": None
                }
                state["queue"].append(extra_item)

            state["next_scheduled_run"] = compute_next_run(state)
            save_state(state)
            process_manager.log(task_id, f"✅ Clipping completato: generate {len(clips)} clip 9:16 pronte!")
            process_manager.finish_task(task_id, status="completed")
            return True
        else:
            err_msg = res.get("message", "Nessuna clip generata")
            process_manager.finish_task(task_id, status="error", error=err_msg)
            # Segna come fallito
            state = load_state()
            for it in state.get("queue", []):
                if it.get("id") == item.get("id"):
                    it["status"] = "failed"
                    it["error_message"] = err_msg
            save_state(state)
            return False

    except Exception as ex:
        process_manager.finish_task(task_id, status="error", error=str(ex))
        state = load_state()
        for it in state.get("queue", []):
            if it.get("id") == item.get("id"):
                it["status"] = "failed"
                it["error_message"] = str(ex)
        save_state(state)
        return False

def execute_publish_step(item):
    import process_manager
    import clipping_queue_manager
    clip_filename = item.get("generated_clip") or item.get("source_video")
    camp_id = item.get("campaign_id", "unknown")
    caption = item.get("caption", "Video automatico da Klippify")

    # Verifica se esiste la didascalia specifica salvata nei metadati
    clip_meta = clipping_queue_manager.get_clip_metadata(clip_filename)
    if clip_meta and clip_meta.get("tiktok_caption"):
        caption = clip_meta["tiktok_caption"]

    # Localizza il percorso reale del file
    video_full_path = None
    candidates = [
        BASE_DIR / "generated_videos" / str(camp_id) / "clips" / clip_filename,
        BASE_DIR / "generated_videos" / str(camp_id) / clip_filename,
        BASE_DIR / "generated_videos" / clip_filename,
        BASE_DIR / "clipping_sources" / str(camp_id) / clip_filename,
        BASE_DIR / clip_filename,
        Path(clip_filename)
    ]
    for cand in candidates:
        if cand.exists() and cand.is_file():
            video_full_path = cand
            break

    if not video_full_path and (BASE_DIR / "generated_videos").exists():
        for cand in (BASE_DIR / "generated_videos").rglob(clip_filename):
            if cand.is_file():
                video_full_path = cand
                break

    if not video_full_path:
        # Auto-recovery: cerca la prima clip vergine fisicamente esistente sul disco
        virgin_clips, _ = get_available_virgin_clips(camp_id)
        if virgin_clips:
            fallback_name = virgin_clips[0]
            for cand in [
                BASE_DIR / "generated_videos" / str(camp_id) / "clips" / fallback_name,
                BASE_DIR / "generated_videos" / str(camp_id) / fallback_name,
                BASE_DIR / "generated_videos" / fallback_name,
                BASE_DIR / "clipping_sources" / str(camp_id) / fallback_name,
                BASE_DIR / fallback_name,
            ]:
                if cand.exists() and cand.is_file():
                    video_full_path = cand
                    clip_filename = fallback_name
                    item["generated_clip"] = fallback_name
                    item["source_video"] = fallback_name
                    print(f"[AUTOPILOT AUTO-RECOVERY] Clip originale assente. Sostituita con clip vergine: {clip_filename}")
                    break

    if not video_full_path:
        state = load_state()
        for it in state.get("queue", []):
            if it.get("id") == item.get("id"):
                it["status"] = "failed"
                it["error_message"] = f"Nessuna clip valida trovata su disco per la campagna {camp_id}."
        save_state(state)
        return False

    # Esegui tiktok_uploader in modalità automatica con payload compatibile
    payload_data = {
        "video": str(video_full_path),
        "video_path": str(video_full_path),
        "title": caption,
        "cover": 1.0,
        "cover_time_sec": 1.0,
        "campaign_id": camp_id
    }
    
    payload_path = BASE_DIR / "upload_payload.json"
    with open(payload_path, "w", encoding="utf-8") as pf:
        json.dump(payload_data, pf, indent=2, ensure_ascii=False)

    cmd = [
        sys.executable, "-u",
        str(BASE_DIR / "tiktok_uploader.py"),
        "--payload", str(payload_path)
    ]

    task_id = process_manager.start_subprocess_task(
        "tiktok",
        f"🚀 Upload TikTok & Invio Klippify ({clip_filename})",
        cmd,
        meta={"filename": clip_filename, "campaign_id": camp_id, "title": caption}
    )

    # Salva in published_content.json per sincronizzazione UI
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pub_file = BASE_DIR / "published_content.json"
    try:
        pub_data = []
        if pub_file.exists():
            with open(pub_file, "r", encoding="utf-8") as f:
                pub_data = json.load(f)
        pub_data.append({
            "campaign_id": camp_id,
            "filename": clip_filename,
            "timestamp": now_str,
            "title": caption
        })
        with open(pub_file, "w", encoding="utf-8") as f:
            json.dump(pub_data, f, indent=2, ensure_ascii=False)
    except Exception as p_ex:
        print(f"[AUTOPILOT] Errore salvataggio published_content.json: {p_ex}")

    # Registra in modo permanente la clip come pubblicata e non riutilizzabile
    mark_clip_as_published(camp_id, clip_filename)

    # Fa avanzare in automatico la catena di montaggio e riassegna a scalare le prossime clip
    advance_campaign_slots(camp_id)

    # Aggiorna stato e storico
    state = load_state()
    state["queue"] = [it for it in state.get("queue", []) if it.get("id") != item.get("id")]
    
    item["status"] = "published"
    item["published_at"] = now_str
    item["klippify_status"] = "accepted_or_pending"
    
    state["history"].insert(0, item)
    state["today_uploads_count"] = state.get("today_uploads_count", 0) + 1
    state["last_upload_timestamp"] = datetime.now().isoformat()
    state["last_upload_date"] = datetime.now().strftime("%Y-%m-%d")
    state["next_scheduled_run"] = compute_next_run(state)
    save_state(state)

    # Se l'autopilota per questa campagna è attivo, mantieni la coda sempre rifornita con i nuovi slot
    try:
        sched_file = BASE_DIR / "campaign_schedules.json"
        if sched_file.exists():
            with open(sched_file, "r", encoding="utf-8") as sf:
                schedules = json.load(sf)
                if schedules.get(camp_id, {}).get("autopilot_enabled", False):
                    # Ri-accoda automaticamente i nuovi slot non ancora in coda
                    has_future_ready = any(str(it.get("campaign_id")) == str(camp_id) and it.get("status") == "ready" for it in state.get("queue", []))
                    if not has_future_ready:
                        queue_campaign_slots(camp_id)
    except Exception as q_ex:
        print(f"[AUTOPILOT] Errore ri-accodamento slot a scalare: {q_ex}")

    return True

def autopilot_worker_loop():
    """Ciclo principale del motore di autopilota."""
    global _engine_running
    print("[AUTOPILOT ENGINE] Motore avviato e in ascolto.")
    
    while _engine_running:
        try:
            state = load_state()

            # Controllo reset giornaliero a mezzanotte (00:00)
            today_str = datetime.now().strftime("%Y-%m-%d")
            if state.get("last_active_date") != today_str:
                print(f"[AUTOPILOT RESET 00:00] Inizio nuovo giorno {today_str}: reset conteggi e ricaricamento slot...")
                state["today_uploads_count"] = 0
                state["last_active_date"] = today_str
                try:
                    sched_file = BASE_DIR / "campaign_schedules.json"
                    if sched_file.exists():
                        with open(sched_file, "r", encoding="utf-8") as sf:
                            schedules = json.load(sf)
                            for cid, cdata in schedules.items():
                                if cdata.get("autopilot_enabled", False):
                                    advance_campaign_slots(cid)
                except Exception as r_ex:
                    print(f"[AUTOPILOT MIDNIGHT RESET ERROR] {r_ex}")
                save_state(state)

            # Controllo automatico continuo della Coda Video Grezzi (Materia Prima & Taglio)
            try:
                all_clip_queues = clipping_queue_manager._load_all_queues()
                for camp_id_key, q_list in all_clip_queues.items():
                    has_queued = any(v.get("status") in ["queued", "processing"] for v in q_list)
                    if has_queued and not clipping_queue_manager.is_campaign_clipping(camp_id_key):
                        print(f"[AUTOPILOT] Video grezzi in attesa per la campagna {camp_id_key}! Avvio clipping continuo in background...")
                        clipping_queue_manager.start_auto_clipping_for_campaign(camp_id_key)
            except Exception as cq_err:
                print(f"[AUTOPILOT QUEUE CHECK ERROR] {cq_err}")

            if not state.get("is_enabled"):
                time.sleep(5)
                continue

            # 1. FASE PUBBLICAZIONE AUTOMATICA DA SCHEDULAZIONE SLOTS (campaign_schedules.json)
            # Controlla sempre ogni 15s gli orari impostati dall'utente per tutte le campagne attive
            import process_manager
            active_tasks = process_manager.get_tasks_list()
            is_tiktok_running = any(t.get("type") == "tiktok" and t.get("status") == "running" for t in active_tasks)
            if is_tiktok_running:
                # Un upload è già in corso nel browser: attendi che finisca prima di avviare il prossimo
                time.sleep(10)
                continue

            try:
                sched_file = BASE_DIR / "campaign_schedules.json"
                if sched_file.exists():
                    with open(sched_file, "r", encoding="utf-8") as sf:
                        all_schedules = json.load(sf)
                    
                    now = datetime.now()
                    for cid, c_data in all_schedules.items():
                        if c_data.get("is_ended", False):
                            continue

                        if not c_data.get("autopilot_enabled", True):
                            continue

                        pause_until = c_data.get("pause_until")
                        if pause_until:
                            try:
                                p_dt = datetime.strptime(pause_until, "%Y-%m-%d %H:%M:%S")
                                if now < p_dt:
                                    # La campagna è in pausa temporanea: salta la pubblicazione
                                    continue
                                else:
                                    # La pausa è terminata: riprendi automaticamente!
                                    print(f"[AUTOPILOT] 🟢 Pausa completata per la campagna {cid}! Ripresa automatica delle pubblicazioni...")
                                    c_data["pause_until"] = None
                                    c_data["is_paused"] = False
                                    with open(sched_file, "w", encoding="utf-8") as sf:
                                        json.dump(all_schedules, sf, indent=2, ensure_ascii=False)
                            except Exception as pe:
                                print(f"[AUTOPILOT PAUSE CHECK ERROR] {pe}")
                        
                        slots = c_data.get("slots", [])
                        pub_clips = c_data.get("published_clips", [])
                        
                        # Cerca il primo slot valido con orario scaduto/raggiunto
                        for s_idx, slot in enumerate(slots):
                            v_name = slot.get("video")
                            s_time = slot.get("time")
                            if v_name and v_name not in pub_clips and s_time:
                                try:
                                    h, m = map(int, s_time.split(":"))
                                    slot_dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
                                    if now >= slot_dt:
                                        print(f"[AUTOPILOT SCHEDULE] ⏰ Orario {s_time} raggiunto per Slot {s_idx+1} ({cid})! Avvio pubblicazione: {v_name}...")
                                        
                                        camp_info = get_campaign_info(cid)
                                        # Recupera script o didascalia personalizzata se presente
                                        caption = f"Guarda fino alla fine! 🚀 {camp_info.get('cta', '')} {' '.join(camp_info.get('mentions', []))} {' '.join(camp_info.get('hashtags', []))}".strip()
                                        if GENERATED_CONTENT_FILE.exists():
                                            try:
                                                with open(GENERATED_CONTENT_FILE, "r", encoding="utf-8") as gcf:
                                                    gen_data = json.load(gcf)
                                                    for cg in gen_data:
                                                        if str(cg.get("campaign_id")) == str(cid):
                                                            scs = cg.get("scripts", [])
                                                            if s_idx < len(scs) and scs[s_idx].get("tiktok_caption"):
                                                                caption = scs[s_idx]["tiktok_caption"]
                                                            break
                                            except Exception:
                                                pass

                                        item = {
                                            "id": uuid.uuid4().hex[:8],
                                            "campaign_id": cid,
                                            "campaign_name": camp_info.get("name", cid),
                                            "type": "ready_clip",
                                            "source_video": v_name,
                                            "concept_name": f"Slot {s_idx+1} ({s_time}) - {v_name}",
                                            "generated_clip": v_name,
                                            "caption": caption,
                                            "scheduled_time": s_time,
                                            "status": "publishing"
                                        }
                                        pub_ok = execute_publish_step(item)
                                        if not pub_ok:
                                            print(f"[AUTOPILOT] Clip {v_name} non pubblicabile. Archiviazione slot e avanzamento automatico...")
                                            mark_clip_as_published(cid, v_name)
                                            advance_campaign_slots(cid)
                                        break
                                except Exception as s_ex:
                                    print(f"[AUTOPILOT SLOT CHECK ERROR] {s_ex}")
            except Exception as sch_err:
                print(f"[AUTOPILOT SCHEDULER ERROR] {sch_err}")

            # 2. FASE TASK CODA SECONDARIA (Clipping e code manuali se presenti)
            queue = state.get("queue", [])
            if queue:
                unclipped_item = next((it for it in queue if it.get("type") == "clipping" and it.get("status") == "queued"), None)
                if unclipped_item:
                    print(f"[AUTOPILOT] Avvio clipping per elemento: {unclipped_item['concept_name']}")
                    for it in state["queue"]:
                        if it.get("id") == unclipped_item.get("id"):
                            it["status"] = "clipping"
                    save_state(state)
                    execute_clipping_step(unclipped_item)

        except Exception as loop_ex:
            print(f"[AUTOPILOT WORKER ERROR] {loop_ex}")

        time.sleep(15)

def start_autopilot_engine():
    """Avvia il thread background del pilota automatico."""
    global _engine_thread, _engine_running
    if _engine_thread is None or not _engine_thread.is_alive():
        _engine_running = True
        _engine_thread = threading.Thread(target=autopilot_worker_loop, daemon=True)
        _engine_thread.start()
        print("[AUTOPILOT] Thread background avviato con successo.")

def trigger_run_now():
    """Forza l'esecuzione immediata della pubblicazione del primo video pronto."""
    state = load_state()
    queue = state.get("queue", [])
    ready_item = next((it for it in queue if it.get("status") == "ready"), None)
    if not ready_item:
        unclipped_item = next((it for it in queue if it.get("status") == "queued"), None)
        if unclipped_item:
            # Esegui clipping prima
            threading.Thread(target=execute_clipping_step, args=(unclipped_item,), daemon=True).start()
            return {"status": "ok", "message": "Avviato clipping immediato del video sorgente."}
        return {"status": "error", "message": "Nessun video pronto in coda da pubblicare."}

    # Avvia pubblicazione in background
    for it in state["queue"]:
        if it.get("id") == ready_item.get("id"):
            it["status"] = "publishing"
    save_state(state)

    threading.Thread(target=execute_publish_step, args=(ready_item,), daemon=True).start()
    return {"status": "ok", "message": f"Pubblicazione immediata avviata per '{ready_item.get('concept_name')}'!"}

if __name__ == "__main__":
    start_autopilot_engine()
    print("Autopilot Engine attivo in standalone. Premi Ctrl+C per uscire.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        _engine_running = False