import os
import sys
import re
import json
import time
import uuid
import shutil
import urllib.parse
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"c:\Users\HP\Desktop\contenuti klippify")
HISTORY_FILE = BASE_DIR / "downloaded_sources_history.json"
SOURCES_CONFIG_FILE = BASE_DIR / "campaign_sources.json"

def get_history():
    if not HISTORY_FILE.exists():
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_to_history(video_id, metadata):
    history = get_history()
    history[str(video_id)] = {
        **metadata,
        "downloaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        tmp = HISTORY_FILE.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        tmp.replace(HISTORY_FILE)
    except Exception as e:
        print(f"[HISTORY] Errore salvataggio storico: {e}")

def is_video_downloaded(video_id_or_url):
    history = get_history()
    if str(video_id_or_url) in history:
        return True
    for vid, meta in history.items():
        if meta.get("url") == video_or_url_clean(video_id_or_url):
            return True
    return False

def video_or_url_clean(u):
    return str(u).strip().split("&")[0].split("?")[0] if "youtube.com" not in str(u) else str(u).strip()

def detect_platform(url):
    url_l = url.lower()
    if "youtube.com" in url_l or "youtu.be" in url_l:
        return "youtube"
    elif "tiktok.com" in url_l:
        return "tiktok"
    elif "instagram.com" in url_l:
        return "instagram"
    elif "drive.google.com" in url_l:
        return "gdrive"
    elif "twitch.tv" in url_l:
        return "twitch"
    elif "facebook.com" in url_l or "fb.watch" in url_l:
        return "facebook"
    elif "twitter.com" in url_l or "x.com" in url_l:
        return "twitter"
    return "generic"

def format_duration(seconds):
    if not seconds:
        return "N/D"
    try:
        sec = int(seconds)
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}h {m:02d}m {s:02d}s"
        return f"{m:02d}m {s:02d}s"
    except Exception:
        return str(seconds)

def inspect_source(url, limit=10):
    """
    Estrae rapidamente metadati dei video da un URL (canale YouTube, profilo TikTok, Instagram, ecc.)
    SENZA scaricare il video.
    """
    import yt_dlp
    
    url = url.strip()
    platform = detect_platform(url)
    
    # Normalizza URL canale YouTube se non ha /videos
    if platform == "youtube":
        if "@" in url and not url.endswith(("/videos", "/shorts", "/streams", "/playlists")):
            url = url.rstrip("/") + "/videos"

    ydl_opts = {
        'extract_flat': 'in_playlist',
        'playlistend': limit,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'skip_download': True,
    }

    results = {
        "platform": platform,
        "source_url": url,
        "channel_title": "",
        "entries": [],
        "total_found": 0
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return {"error": "Impossibile recuperare informazioni dall'URL specificato."}

            results["channel_title"] = info.get("uploader") or info.get("channel") or info.get("title") or "Fonte Sconosciuta"

            raw_entries = info.get("entries") or [info]
            history = get_history()

            for entry in raw_entries:
                if not entry:
                    continue
                
                vid_id = entry.get("id") or str(uuid.uuid4().hex[:8])
                vid_url = entry.get("url") or entry.get("webpage_url") or (f"https://www.youtube.com/watch?v={vid_id}" if platform == "youtube" else url)
                
                # Se è un video YouTube:
                if platform == "youtube" and not str(vid_url).startswith("http"):
                    vid_url = f"https://www.youtube.com/watch?v={vid_id}"

                title = entry.get("title") or entry.get("description") or f"Video {vid_id}"
                title = title.split("\n")[0][:120]

                duration = entry.get("duration") or 0
                views = entry.get("view_count") or 0
                upload_date = entry.get("upload_date") or ""
                if upload_date and len(upload_date) == 8:
                    upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

                thumbnails = entry.get("thumbnails") or []
                thumbnail_url = entry.get("thumbnail") or (thumbnails[-1].get("url") if thumbnails else "")

                already_downloaded = str(vid_id) in history or any(h.get("url") == vid_url for h in history.values())

                results["entries"].append({
                    "id": str(vid_id),
                    "title": title,
                    "url": vid_url,
                    "duration_sec": duration,
                    "duration_str": format_duration(duration),
                    "view_count": views,
                    "upload_date": upload_date,
                    "thumbnail": thumbnail_url,
                    "platform": platform,
                    "already_downloaded": already_downloaded
                })

            results["total_found"] = len(results["entries"])
            return results

    except Exception as e:
        return {"error": f"Errore durante l'ispezione dell'URL ({platform}): {str(e)}"}

def download_source_video(url, campaign_id="general", custom_title=None, progress_logger=None):
    """
    Scarica il video specificato e lo salva in clipping_sources/<campaign_id>/
    """
    import yt_dlp

    sanitized_camp = re.sub(r'[^a-zA-Z0-9_]', '_', str(campaign_id))
    target_dir = BASE_DIR / "clipping_sources" / sanitized_camp
    target_dir.mkdir(parents=True, exist_ok=True)

    def log(msg):
        safe_msg = str(msg).encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')
        print(f"[SOURCE-DOWNLOADER] {safe_msg}")
        if progress_logger:
            try:
                progress_logger(msg)
            except Exception:
                pass

    log(f"Inizio download video da: {url} per campagna {campaign_id}...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_template = str(target_dir / f"%(title).60s_%(id)s_{timestamp}.%(ext)s")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': out_template,
        'merge_output_format': 'mp4',
        'windowsfilenames': True,
        'restrictfilenames': True,
        'quiet': False,
        'no_warnings': True,
        'ignoreerrors': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                return {"status": "error", "message": "Nessun flusso video trovato."}

            vid_id = info.get("id") or timestamp
            raw_title = info.get("title") or custom_title or f"video_{vid_id}"
            title = re.sub(r'[^\w\s\-\.\(\)]', '', raw_title).strip()
            
            downloaded_files = sorted(
                list(target_dir.glob(f"*{vid_id}*.mp4")) + list(target_dir.glob(f"*{timestamp}*.mp4")),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            if not downloaded_files:
                all_mp4 = sorted(list(target_dir.glob("*.mp4")), key=lambda p: p.stat().st_mtime, reverse=True)
                downloaded_file = all_mp4[0] if all_mp4 else None
            else:
                downloaded_file = downloaded_files[0]

            if not downloaded_file or not downloaded_file.exists():
                return {"status": "error", "message": "File video non trovato su disco dopo il download."}

            file_size_mb = round(downloaded_file.stat().st_size / (1024 * 1024), 2)
            fname = downloaded_file.name

            raw_target_dir = BASE_DIR / "generated_videos" / sanitized_camp / "raw"
            raw_target_dir.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(downloaded_file, raw_target_dir / fname)
            except Exception:
                pass

            save_to_history(vid_id, {
                "title": title,
                "filename": fname,
                "campaign_id": campaign_id,
                "url": url,
                "file_size_mb": file_size_mb,
                "duration": info.get("duration", 0)
            })

            log(f"Download completato con successo: '{fname}' ({file_size_mb} MB) salvato in {sanitized_camp}!")

            try:
                import clipping_queue_manager
                clipping_queue_manager.add_video_to_queue(campaign_id, fname, file_size_mb=file_size_mb)
                clipping_queue_manager.start_auto_clipping_for_campaign(campaign_id)
            except Exception as qe:
                print(f"[SOURCE-DOWNLOADER] Nota aggiunta a coda clipping: {qe}")

            return {
                "status": "success",
                "video_id": vid_id,
                "filename": fname,
                "file_path": str(downloaded_file),
                "file_size_mb": file_size_mb,
                "title": title,
                "duration": info.get("duration", 0)
            }

    except Exception as e:
        err_msg = f"Errore durante il download da {url}: {str(e)}"
        log(f"{err_msg}")
        return {"status": "error", "message": err_msg}

def get_campaign_sources():
    if not SOURCES_CONFIG_FILE.exists():
        return {}
    try:
        with open(SOURCES_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_campaign_source(campaign_id, source_url, auto_download=True):
    sources = get_campaign_sources()
    cid = str(campaign_id)
    if cid not in sources:
        sources[cid] = {"sources": [], "auto_download": auto_download}
    
    current_list = sources[cid].get("sources", [])
    if source_url not in current_list:
        current_list.append(source_url)
    
    sources[cid]["sources"] = current_list
    sources[cid]["auto_download"] = auto_download
    sources[cid]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(SOURCES_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(sources, f, indent=2, ensure_ascii=False)
        return {"status": "ok", "sources": sources[cid]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def remove_campaign_source(campaign_id, source_url):
    sources = get_campaign_sources()
    cid = str(campaign_id)
    if cid in sources:
        current_list = sources[cid].get("sources", [])
        if source_url in current_list:
            current_list.remove(source_url)
            sources[cid]["sources"] = current_list
            with open(SOURCES_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(sources, f, indent=2, ensure_ascii=False)
    return {"status": "ok", "sources": sources.get(cid, {})}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--inspect":
        test_url = sys.argv[2]
        res = inspect_source(test_url, limit=5)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif len(sys.argv) > 3 and sys.argv[1] == "--download":
        test_url = sys.argv[2]
        camp = sys.argv[3]
        res = download_source_video(test_url, campaign_id=camp)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("Usage:")
        print("  python source_downloader.py --inspect <URL>")
        print("  python source_downloader.py --download <URL> <CAMPAIGN_ID>")
