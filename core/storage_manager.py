import paths
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# UTF-8 encoding support on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = paths.PROJECT_ROOT
SETTINGS_FILE = BASE_DIR / "storage_settings.json"

DEFAULT_SETTINGS = {
    "auto_delete_raw_sources": True,
    "auto_delete_published_clips": True,
    "auto_delete_temp_files": True,
    "total_freed_mb": 0.0,
    "total_deleted_files_count": 0,
    "last_cleanup_timestamp": None
}

def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[STORAGE ERROR] Impossibile salvare storage_settings.json: {e}")

def record_freed_space(freed_bytes, count=1):
    settings = load_settings()
    mb = freed_bytes / (1024 * 1024)
    settings["total_freed_mb"] = round(settings.get("total_freed_mb", 0.0) + mb, 2)
    settings["total_deleted_files_count"] = settings.get("total_deleted_files_count", 0) + count
    settings["last_cleanup_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_settings(settings)

def delete_raw_source_after_clipping(source_file_path, campaign_id=None, logger=None):
    """
    Elimina il file video grezzo/lungo una volta che le clip 9:16
    sono state estratte con successo e salvate nel magazzino.
    """
    settings = load_settings()
    if not settings.get("auto_delete_raw_sources", True):
        return False

    if not source_file_path:
        return False

    p = Path(source_file_path)
    if p.exists() and p.is_file():
        try:
            size_bytes = p.stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            p.unlink()
            record_freed_space(size_bytes, 1)
            msg = f"🧹 [STORAGE] Video lungo eliminato dopo il clipping: '{p.name}' (Liberati {size_mb:.2f} MB)"
            print(msg)
            if logger: logger(msg)
            return True
        except Exception as e:
            err = f"⚠️ [STORAGE] Impossibile eliminare video lungo '{p.name}': {e}"
            print(err)
            if logger: logger(err)
            return False
    return False

def delete_published_clip(clip_filename, campaign_id=None, logger=None):
    """
    Elimina il file .mp4 della singola clip una volta pubblicata
    con successo su TikTok e inviata a Klippify.
    """
    settings = load_settings()
    if not settings.get("auto_delete_published_clips", True):
        return False

    if not clip_filename:
        return False

    candidates = []
    if campaign_id:
        candidates.append(BASE_DIR / "generated_videos" / str(campaign_id) / "clips" / clip_filename)
        candidates.append(BASE_DIR / "generated_videos" / str(campaign_id) / clip_filename)

    candidates.append(BASE_DIR / "generated_videos" / clip_filename)
    
    # Cerca ricorsivamente in generated_videos se non trovato
    for cand in candidates:
        if cand.exists() and cand.is_file():
            try:
                size_bytes = cand.stat().st_size
                size_mb = size_bytes / (1024 * 1024)
                cand.unlink()
                record_freed_space(size_bytes, 1)
                msg = f"🧹 [STORAGE] Clip pubblicata eliminata dal disco: '{cand.name}' (Liberati {size_mb:.2f} MB)"
                print(msg)
                if logger: logger(msg)
                return True
            except Exception as e:
                err = f"⚠️ [STORAGE] Impossibile eliminare clip pubblicata '{cand.name}': {e}"
                print(err)
                if logger: logger(err)
                return False

    # Ricerca fallback
    gen_dir = BASE_DIR / "generated_videos"
    if gen_dir.exists():
        for f in gen_dir.rglob(clip_filename):
            if f.is_file():
                try:
                    size_bytes = f.stat().st_size
                    size_mb = size_bytes / (1024 * 1024)
                    f.unlink()
                    record_freed_space(size_bytes, 1)
                    msg = f"🧹 [STORAGE] Clip pubblicata eliminata: '{f.name}' (Liberati {size_mb:.2f} MB)"
                    print(msg)
                    if logger: logger(msg)
                    return True
                except Exception as e:
                    print(f"[-] Errore: {e}")
                    return False
    return False

def clean_temporary_files(logger=None):
    """
    Elimina file intermedi .ass, raw_cut_*, temp_*, .f136, .f137, .f140.
    """
    deleted_count = 0
    freed_bytes = 0

    patterns = [
        "*.ass", "temp_*", "raw_cut_*", "*.f136.mp4", "*.f137.mp4", "*.f140-1.m4a", "*.f140.m4a", "*.part", "*.ytdl"
    ]

    search_dirs = [
        BASE_DIR / "clipping_sources",
        BASE_DIR / "generated_videos"
    ]

    for sdir in search_dirs:
        if sdir.exists():
            for pat in patterns:
                for f in sdir.rglob(pat):
                    if f.is_file():
                        try:
                            sz = f.stat().st_size
                            freed_bytes += sz
                            f.unlink()
                            deleted_count += 1
                        except Exception:
                            pass

    if deleted_count > 0:
        record_freed_space(freed_bytes, deleted_count)
        msg = f"🧹 [STORAGE] Puliti {deleted_count} file temporanei (Liberati {freed_bytes / (1024*1024):.2f} MB)"
        print(msg)
        if logger: logger(msg)

    return {"deleted_count": deleted_count, "freed_mb": round(freed_bytes / (1024 * 1024), 2)}

def run_full_storage_cleanup(logger=None):
    """
    Scansiona ed esegue la pulizia completa:
    1. Clip già pubblicate rimaste su disco
    2. File video lunghi già completamente processati
    3. File temporanei / intermedi
    """
    deleted_files = []
    total_bytes = 0

    # 1. Pulisci file temporanei
    temp_res = clean_temporary_files(logger=logger)

    # 2. Pulisci clip storiche già pubblicate
    sched_file = BASE_DIR / "campaign_schedules.json"
    published_filenames = set()
    if sched_file.exists():
        try:
            with open(sched_file, "r", encoding="utf-8") as sf:
                schedules = json.load(sf)
                for cid, cdata in schedules.items():
                    for p in cdata.get("published_clips", []):
                        published_filenames.add(p)
        except Exception:
            pass

    pub_hist_file = BASE_DIR / "published_content.json"
    if pub_hist_file.exists():
        try:
            with open(pub_hist_file, "r", encoding="utf-8") as pf:
                pdata = json.load(pf)
                for item in pdata:
                    fn = item.get("filename")
                    if fn:
                        published_filenames.add(fn)
        except Exception:
            pass

    gen_dir = BASE_DIR / "generated_videos"
    if gen_dir.exists():
        for pclip in published_filenames:
            for f in gen_dir.rglob(pclip):
                if f.is_file():
                    try:
                        sz = f.stat().st_size
                        total_bytes += sz
                        f.unlink()
                        deleted_files.append(f.name)
                    except Exception:
                        pass

    if total_bytes > 0:
        record_freed_space(total_bytes, len(deleted_files))

    freed_mb = round((total_bytes / (1024 * 1024)) + temp_res.get("freed_mb", 0.0), 2)
    tot_count = len(deleted_files) + temp_res.get("deleted_count", 0)

    summary = {
        "status": "success",
        "freed_mb": freed_mb,
        "deleted_count": tot_count,
        "deleted_published_clips": deleted_files
    }
    msg_fin = f"✅ [STORAGE CLEANUP] Pulizia completata: {tot_count} file eliminati, Liberati {freed_mb:.2f} MB!"
    print(msg_fin)
    if logger: logger(msg_fin)
    return summary

def get_storage_inventory_stats():
    """
    Restituisce un riepilogo dello spazio attualmente occupato sul disco.
    """
    def get_dir_size_and_count(dpath, pattern="*.*"):
        if not dpath.exists():
            return 0, 0
        total_sz = 0
        cnt = 0
        for f in dpath.rglob(pattern):
            if f.is_file():
                try:
                    total_sz += f.stat().st_size
                    cnt += 1
                except Exception:
                    pass
        return cnt, round(total_sz / (1024 * 1024), 2)

    raw_count, raw_mb = get_dir_size_and_count(BASE_DIR / "clipping_sources")
    clips_count, clips_mb = get_dir_size_and_count(BASE_DIR / "generated_videos", "*.mp4")
    
    settings = load_settings()

    return {
        "raw_sources_count": raw_count,
        "raw_sources_mb": raw_mb,
        "clips_count": clips_count,
        "clips_mb": clips_mb,
        "total_occupied_mb": round(raw_mb + clips_mb, 2),
        "total_freed_lifetime_mb": settings.get("total_freed_mb", 0.0),
        "total_deleted_files_lifetime": settings.get("total_deleted_files_count", 0),
        "auto_delete_raw_sources": settings.get("auto_delete_raw_sources", True),
        "auto_delete_published_clips": settings.get("auto_delete_published_clips", True)
    }