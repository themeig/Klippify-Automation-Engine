import paths
import threading
import time
import os
import sys
import json
import re
import shutil
from datetime import datetime
import urllib.parse
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from klippify_scraper import fetch_klippify_campaigns, analyze_and_rank_campaigns, fetch_klippify_dashboard_data, fetch_klippify_submissions
from generate_report import generate_html_report, HTML_REPORT_PATH
import subprocess
from tiktok_manager import get_user_stats, upload_video, get_video_stats, get_all_user_videos
from process_manager import process_manager
import autopilot_engine
import clipping_queue_manager
import source_downloader

BASE_DIR = paths.PROJECT_ROOT
LOCAL_CAMPAIGN_DIR = BASE_DIR / "alestark campain"
PORT = 5000

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle each HTTP request in a separate thread to prevent blocking."""
    daemon_threads = True

class KlippifyServerHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Clean logging
        print(f"[SERVER] {self.address_string()} - {format % args}")

    def serve_video_file(self, filepath):
        """
        Serve video file with full HTTP 206 Partial Content (Range requests)
        support for seamless video scrubbing, seeking forward and backward.
        """
        if not filepath.exists() or not filepath.is_file():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        file_size = filepath.stat().st_size
        range_header = self.headers.get("Range")
        content_type = "video/mp4" if filepath.suffix.lower() == ".mp4" else "application/octet-stream"

        if range_header:
            match = re.match(r"bytes=(\d+)-(\d*)", range_header.strip())
            if match:
                start_str, end_str = match.groups()
                start = int(start_str)
                end = int(end_str) if end_str else file_size - 1
                if start >= file_size:
                    self.send_response(416)  # Range Not Satisfiable
                    self.send_header("Content-Range", f"bytes */{file_size}")
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()
                    return

                end = min(end, file_size - 1)
                content_length = end - start + 1

                self.send_response(206)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(content_length))
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()

                try:
                    with open(filepath, "rb") as f:
                        f.seek(start)
                        remaining = content_length
                        while remaining > 0:
                            chunk_size = min(remaining, 128 * 1024)
                            data = f.read(chunk_size)
                            if not data:
                                break
                            self.wfile.write(data)
                            remaining -= len(data)
                except (ConnectionResetError, BrokenPipeError):
                    # Normal when user scrubs/jumps to a new timestamp
                    pass
                return

        # Standard 200 OK
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(file_size))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        try:
            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(128 * 1024)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except (ConnectionResetError, BrokenPipeError):
            pass

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            # Ensure cache is fresh & pre-render HTML server-side
            raw_camps = fetch_klippify_campaigns(use_cache_if_available=True)
            ranked = analyze_and_rank_campaigns(raw_camps)
            dash_data = fetch_klippify_dashboard_data(use_cache_if_available=True)
            subs_data = fetch_klippify_submissions(use_cache_if_available=True)
            generate_html_report(ranked, dash_data, subs_data)

            with open(HTML_REPORT_PATH, "rb") as f:
                self.wfile.write(f.read())

        elif path == "/api/campaigns":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            raw_camps = fetch_klippify_campaigns(use_cache_if_available=True)
            ranked = analyze_and_rank_campaigns(raw_camps)
            self.wfile.write(json.dumps(ranked, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            dash_data = fetch_klippify_dashboard_data(use_cache_if_available=True)
            self.wfile.write(json.dumps(dash_data, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/local-media":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            media_info = []
            if LOCAL_CAMPAIGN_DIR.exists():
                for folder in LOCAL_CAMPAIGN_DIR.iterdir():
                    if folder.is_dir() and not folder.name.startswith("_"):
                        files = [f.name for f in folder.iterdir() if f.is_file()]
                        media_info.append({
                            "folder_name": folder.name,
                            "file_count": len(files),
                            "files": files[:10]
                        })
            
            self.wfile.write(json.dumps(media_info, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/videos" or path.startswith("/api/videos?"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            query_params = urllib.parse.parse_qs(parsed_path.query)
            target_campaign = query_params.get("campaign_id", [None])[0]

            videos_dir = BASE_DIR / "generated_videos"
            video_files = []
            seen_filenames = set()

            def scan_dir(sdir, camp_id, folder_tag="general"):
                if not sdir.exists():
                    return
                for ext in ["*.mp4", "*.mov", "*.mkv", "*.webm"]:
                    for f in sdir.glob(ext):
                        if f.is_file() and f.name not in seen_filenames:
                            seen_filenames.add(f.name)
                            # Create relative path for serving
                            rel_to_gen = ""
                            try:
                                rel_to_gen = f.relative_to(videos_dir).as_posix()
                            except:
                                rel_to_gen = f.name
                            video_files.append({
                                "filename": f.name,
                                "size": f.stat().st_size,
                                "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                                "mtime": f.stat().st_mtime,
                                "campaign_id": camp_id,
                                "rel_url": f"/generated_videos/{rel_to_gen}",
                                "folder": folder_tag,
                                "is_clip": f.name.startswith("clip_") or "clip" in f.name.lower()
                            })

            if target_campaign:
                # 1. Scansiona cartelle specifiche per questa campagna
                camp_gen = videos_dir / str(target_campaign)
                scan_dir(camp_gen / "clips", str(target_campaign), "clips")
                scan_dir(camp_gen / "raw", str(target_campaign), "raw")
                scan_dir(camp_gen / "ai", str(target_campaign), "ai")
                scan_dir(camp_gen, str(target_campaign), "general")

                # Scansiona cartella clipping_sources specifica
                camp_src = BASE_DIR / "clipping_sources" / str(target_campaign)
                scan_dir(camp_src, str(target_campaign), "sources")

                # Fallback: scan root generated_videos solo per file con tag esplicito di questa campagna
                if videos_dir.exists():
                    for ext in ["*.mp4", "*.mov"]:
                        for f in videos_dir.glob(ext):
                            fname = f.name
                            # Verifica se il nome corrisponde alla campagna specifica
                            if str(target_campaign) in fname:
                                if f.name not in seen_filenames:
                                    scan_dir(f.parent, str(target_campaign), "clips" if f.name.startswith("clip_") else "general")
                            elif "6a71c6f7245627c68999eae2" == str(target_campaign) and ("SaraDizdari" in fname or "Sara" in fname or any(k in fname for k in ["CRISTINA", "ELISABETTA", "FEDRA"])):
                                scan_dir(f.parent, str(target_campaign), "clips" if f.name.startswith("clip_") else "raw")
                            elif "6a426231e6a21896f769dc80" == str(target_campaign) and ("Dose" in fname or "dose" in fname):
                                scan_dir(f.parent, str(target_campaign), "clips" if f.name.startswith("clip_") else "raw")
            else:
                # Scansiona tutte le cartelle e associa alla campagna corretta
                if videos_dir.exists():
                    for camp_folder in videos_dir.iterdir():
                        if camp_folder.is_dir():
                            cid = camp_folder.name
                            scan_dir(camp_folder / "clips", cid, "clips")
                            scan_dir(camp_folder / "raw", cid, "raw")
                            scan_dir(camp_folder / "ai", cid, "ai")
                            scan_dir(camp_folder, cid, "general")
                    
                    # File root generated_videos
                    for ext in ["*.mp4", "*.mov"]:
                        for f in videos_dir.glob(ext):
                            if f.name not in seen_filenames:
                                cid = "general"
                                if "SaraDizdari" in f.name or "Sara" in f.name or any(k in f.name for k in ["CRISTINA", "ELISABETTA", "FEDRA"]):
                                    cid = "6a71c6f7245627c68999eae2"
                                elif "Dose" in f.name or "dose" in f.name:
                                    cid = "6a426231e6a21896f769dc80"
                                seen_filenames.add(f.name)
                                video_files.append({
                                    "filename": f.name,
                                    "size": f.stat().st_size,
                                    "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
                                    "mtime": f.stat().st_mtime,
                                    "campaign_id": cid,
                                    "rel_url": f"/generated_videos/{f.name}",
                                    "folder": "clips" if f.name.startswith("clip_") else "general",
                                    "is_clip": f.name.startswith("clip_") or "clip" in f.name.lower()
                                })

            # Ordina dal più recente al più vecchio
            video_files.sort(key=lambda x: x.get("mtime", 0), reverse=True)
            self.wfile.write(json.dumps(video_files, ensure_ascii=False).encode("utf-8"))

        elif path.startswith("/video/"):
            # Serve video direttamente per nome file con ricerca automatica ricorsiva
            raw_fname = urllib.parse.unquote(path[len("/video/"):])
            fname = Path(raw_fname).name
            filepath = None
            for candidate in (BASE_DIR / "generated_videos").rglob(fname):
                if candidate.is_file():
                    filepath = candidate
                    break
            if not filepath:
                for candidate in (BASE_DIR / "clipping_sources").rglob(fname):
                    if candidate.is_file():
                        filepath = candidate
                        break
            if filepath and filepath.is_file():
                self.serve_video_file(filepath)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Video File Not Found")

        elif path.startswith("/generated_videos/"):
            # Serve static MP4 files with recursive campaign subfolder resolution
            rel = urllib.parse.unquote(path[len("/generated_videos/"):])
            filepath = BASE_DIR / "generated_videos" / rel
            if not filepath.exists() or not filepath.is_file():
                # Cerca ricorsivamente in generated_videos
                fname = Path(rel).name
                found = False
                for candidate in (BASE_DIR / "generated_videos").rglob(fname):
                    if candidate.is_file():
                        filepath = candidate
                        found = True
                        break
                if not found:
                    for candidate in (BASE_DIR / "clipping_sources").rglob(fname):
                        if candidate.is_file():
                            filepath = candidate
                            found = True
                            break
            self.serve_video_file(filepath)

        elif path.startswith("/clipping_sources/"):
            rel = urllib.parse.unquote(path[len("/clipping_sources/"):])
            filepath = BASE_DIR / "clipping_sources" / rel
            if not filepath.exists() or not filepath.is_file():
                fname = Path(rel).name
                for candidate in (BASE_DIR / "clipping_sources").rglob(fname):
                    if candidate.is_file():
                        filepath = candidate
                        break
            self.serve_video_file(filepath)

        elif path == "/api/generated-content":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            gc_path = BASE_DIR / "generated_content.json"
            if gc_path.exists():
                with open(gc_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = []
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/clip-metadata":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = clipping_queue_manager.load_clip_metadata()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/tiktok/stats":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                stats = get_user_stats()
                self.wfile.write(json.dumps(stats, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif path == "/api/tiktok/videos":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                videos = get_all_user_videos(limit=50)
                self.wfile.write(json.dumps({"status": "ok", "videos": videos}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e), "videos": []}, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/klippify/submissions":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                parsed = urllib.parse.parse_qs(parsed_path.query)
                camp_id = parsed.get("campaign_id", [None])[0]
                subs = fetch_klippify_submissions(use_cache_if_available=True)
                if camp_id:
                    subs = [s for s in subs if s.get("campaign_id") == camp_id]
                self.wfile.write(json.dumps(subs, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e), "submissions": []}, ensure_ascii=False).encode("utf-8"))
        elif path in ["/api/klippify/sync", "/api/sync/klippify"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                task_id = process_manager.create_task("klippify_sync", "🔄 Sincronizzazione Catalogo & Campagne Klippify")
                process_manager.log(task_id, "Avvio scraping aggiornato da Klippify con Playwright...")
                raw_camps = fetch_klippify_campaigns(use_cache_if_available=False)
                dash_data = fetch_klippify_dashboard_data(use_cache_if_available=False)
                subs_data = fetch_klippify_submissions(use_cache_if_available=False)
                ranked = analyze_and_rank_campaigns(raw_camps)
                generate_html_report(ranked, dash_data, subs_data)
                process_manager.log(task_id, f"Sincronizzate con successo {len(raw_camps)} campagne LIVE e rigenerato il report.")
                process_manager.finish_task(task_id, status="completed")
                self.wfile.write(json.dumps({"status": "ok", "message": f"Sincronizzazione completata: {len(raw_camps)} campagne aggiornate.", "count": len(raw_camps)}, ensure_ascii=False).encode("utf-8"))
            except Exception as ex:
                if 'task_id' in locals():
                    process_manager.finish_task(task_id, status="error", error=str(ex))
                self.wfile.write(json.dumps({"status": "error", "message": str(ex)}, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/tiktok/video-stats":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                parsed = urllib.parse.parse_qs(parsed_path.query)
                video_filename = parsed.get("filename", [None])[0]
                
                # Check Klippify real submissions first
                subs = fetch_klippify_submissions(use_cache_if_available=True)
                matched_sub = None
                if video_filename:
                    t = str(video_filename).lower()
                    for s in subs:
                        if s.get("id") == video_filename or t in str(s.get("post_url", "")).lower() or t in str(s.get("campaign_name", "")).lower():
                            matched_sub = s
                            break
                
                if matched_sub:
                    resp_data = {
                        "id": matched_sub.get("id"),
                        "post_url": matched_sub.get("post_url"),
                        "thumbnail_url": matched_sub.get("thumbnail_url"),
                        "view_count": matched_sub.get("views", 0),
                        "like_count": matched_sub.get("likes", 0),
                        "comment_count": matched_sub.get("comments", 0),
                        "share_count": matched_sub.get("shares", 0),
                        "earnings": matched_sub.get("earnings", 0.0),
                        "status": matched_sub.get("status", "accepted"),
                        "is_ai_verified": matched_sub.get("is_ai_verified", True),
                        "ai_reasoning": matched_sub.get("ai_reasoning", "")
                    }
                else:
                    stats = get_video_stats(video_filename)
                    resp_data = stats

                self.wfile.write(json.dumps(resp_data, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/campaign/total-performance" or path.startswith("/api/campaign/total-performance?"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                parsed = urllib.parse.parse_qs(parsed_path.query)
                camp_id = parsed.get("campaign_id", [None])[0]
                sync_live = parsed.get("sync_live", ["false"])[0].lower() in ["1", "true", "yes"]

                # 1. Recupera o sincronizza i video da TikTok API
                tiktok_videos = []
                try:
                    if sync_live:
                        tiktok_videos = get_all_user_videos(limit=50)
                except Exception as tk_err:
                    print(f"[SERVER] Errore sync live TikTok: {tk_err}")

                # 2. Carica le submission Klippify
                subs = fetch_klippify_submissions(use_cache_if_available=not sync_live)
                
                # Filtra per la campagna specificata (o tutte se non specificata)
                camp_subs = []
                for s in subs:
                    cid = s.get("campaign_id") or s.get("campaign_token")
                    cname = s.get("campaign_name", "")
                    if not camp_id or str(cid) == str(camp_id) or (cname and str(camp_id).lower() in cname.lower()):
                        if tiktok_videos:
                            for tv in tiktok_videos:
                                if tv.get("share_url") and tv.get("share_url") in str(s.get("post_url", "")) or tv.get("id") in str(s.get("post_url", "")):
                                    s["views"] = tv.get("view_count", s.get("views", 0))
                                    s["likes"] = tv.get("like_count", s.get("likes", 0))
                                    s["comments"] = tv.get("comment_count", s.get("comments", 0))
                                    s["shares"] = tv.get("share_count", s.get("shares", 0))
                        camp_subs.append(s)

                # 3. Calcolo metriche aggregate totali
                total_views = sum(s.get("views", 0) for s in camp_subs)
                total_likes = sum(s.get("likes", 0) for s in camp_subs)
                total_comments = sum(s.get("comments", 0) for s in camp_subs)
                total_shares = sum(s.get("shares", 0) for s in camp_subs)
                total_earnings = sum(s.get("earnings", 0.0) for s in camp_subs)
                
                total_videos = len(camp_subs)
                accepted = sum(1 for s in camp_subs if s.get("status") == "accepted")
                rejected = sum(1 for s in camp_subs if s.get("status") == "rejected")
                pending = sum(1 for s in camp_subs if s.get("status") not in ["accepted", "rejected"])
                
                avg_views = round(total_views / max(1, total_videos), 1) if total_videos > 0 else 0
                approval_rate = round((accepted / max(1, total_videos)) * 100, 1) if total_videos > 0 else 0

                resp_data = {
                    "status": "success",
                    "campaign_id": camp_id,
                    "total_views": total_views,
                    "total_likes": total_likes,
                    "total_comments": total_comments,
                    "total_shares": total_shares,
                    "total_earnings": round(total_earnings, 2),
                    "total_videos_published": total_videos,
                    "accepted_count": accepted,
                    "rejected_count": rejected,
                    "pending_count": pending,
                    "avg_views_per_video": avg_views,
                    "approval_rate": approval_rate,
                    "submissions": camp_subs
                }
                self.wfile.write(json.dumps(resp_data, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/storage/stats":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                import storage_manager
                stats = storage_manager.get_storage_inventory_stats()
                self.wfile.write(json.dumps(stats, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/storage/cleanup":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                import storage_manager
                res = storage_manager.run_full_storage_cleanup()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/campaign/schedules":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            sched_path = BASE_DIR / "campaign_schedules.json"
            if sched_path.exists():
                with open(sched_path, "r", encoding="utf-8") as sf:
                    sched_data = json.load(sf)
            else:
                sched_data = {}
            self.wfile.write(json.dumps(sched_data, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/clipping/classified-active":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            class_path = BASE_DIR / "active_campaigns_classified.json"
            if class_path.exists():
                with open(class_path, "r", encoding="utf-8") as cf:
                    class_data = json.load(cf)
            else:
                class_data = []
            self.wfile.write(json.dumps(class_data, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/debug/tasks":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            tasks = process_manager.get_tasks_list()
            self.wfile.write(json.dumps(tasks, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/autopilot/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            state = autopilot_engine.load_state()
            state["next_scheduled_run"] = autopilot_engine.compute_next_run(state)
            self.wfile.write(json.dumps(state, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/sources/get-campaign-sources" or path.startswith("/api/sources/get-campaign-sources?"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            sources = source_downloader.get_campaign_sources()
            self.wfile.write(json.dumps(sources, ensure_ascii=False).encode("utf-8"))

        elif path.startswith("/api/autopilot/campaign-status"):
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            camp_id = query_params.get("campaign_id", [""])[0]
            status_data = autopilot_engine.get_campaign_autopilot_status(camp_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(json.dumps(status_data, ensure_ascii=False).encode("utf-8"))

        elif path.startswith("/api/clipping/queue"):
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            camp_id = query_params.get("campaign_id", [""])[0]
            queue_data = clipping_queue_manager.get_campaign_queue(camp_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(json.dumps(queue_data, ensure_ascii=False).encode("utf-8"))

        elif path.startswith("/video/"):
            raw_filename = urllib.parse.unquote(path[len("/video/"):])
            found_file = None
            gen_dir = BASE_DIR / "generated_videos"
            if gen_dir.exists():
                for candidate in gen_dir.rglob(raw_filename):
                    if candidate.is_file():
                        found_file = candidate
                        break
            
            if not found_file:
                src_dir = BASE_DIR / "clipping_sources"
                if src_dir.exists():
                    for candidate in src_dir.rglob(raw_filename):
                        if candidate.is_file():
                            found_file = candidate
                            break
            
            if not found_file:
                candidate = BASE_DIR / raw_filename
                if candidate.is_file():
                    found_file = candidate

            if found_file:
                self.serve_video_file(found_file)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(f"404 Video '{raw_filename}' not found".encode("utf-8"))

        elif path.startswith("/generated_videos/"):
            rel_subpath = urllib.parse.unquote(path[len("/generated_videos/"):])
            target_path = BASE_DIR / "generated_videos" / rel_subpath
            if target_path.is_file():
                self.serve_video_file(target_path)
            else:
                fname = Path(rel_subpath).name
                found_file = None
                gen_dir = BASE_DIR / "generated_videos"
                if gen_dir.exists():
                    for candidate in gen_dir.rglob(fname):
                        if candidate.is_file():
                            found_file = candidate
                            break
                if found_file:
                    self.serve_video_file(found_file)
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"404 Video Not Found")

        elif path.startswith("/clipping_sources/"):
            rel_subpath = urllib.parse.unquote(path[len("/clipping_sources/"):])
            target_path = BASE_DIR / "clipping_sources" / rel_subpath
            if target_path.is_file():
                self.serve_video_file(target_path)
            else:
                fname = Path(rel_subpath).name
                found_file = None
                src_dir = BASE_DIR / "clipping_sources"
                if src_dir.exists():
                    for candidate in src_dir.rglob(fname):
                        if candidate.is_file():
                            found_file = candidate
                            break
                if found_file:
                    self.serve_video_file(found_file)
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"404 Source Video Not Found")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        if self.path == "/api/refresh":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            # Force Playwright live scrape
            raw_camps = fetch_klippify_campaigns(use_cache_if_available=False)
            ranked = analyze_and_rank_campaigns(raw_camps)
            dash_data = fetch_klippify_dashboard_data(use_cache_if_available=False)
            generate_html_report(ranked, dash_data)
            
            response = {"status": "ok", "count": len(ranked), "data": ranked, "dashboard": dash_data}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/save-selection":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                selected_ids = json.loads(post_data.decode('utf-8'))
                with open(BASE_DIR / "campagne_selezionate.json", "w", encoding="utf-8") as f:
                    json.dump(selected_ids, f, indent=2, ensure_ascii=False)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/delete-campaign":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                
                # 1. Remove from campagne_selezionate.json
                sel_path = BASE_DIR / "campagne_selezionate.json"
                if sel_path.exists():
                    with open(sel_path, "r", encoding="utf-8") as f:
                        selected = json.load(f)
                    selected = [c for c in selected if c != camp_id]
                    with open(sel_path, "w", encoding="utf-8") as f:
                        json.dump(selected, f, indent=2, ensure_ascii=False)
                
                # 2. Remove from generated_content.json
                gen_path = BASE_DIR / "generated_content.json"
                if gen_path.exists():
                    with open(gen_path, "r", encoding="utf-8") as f:
                        generated = json.load(f)
                    generated = [g for g in generated if g.get("campaign_id") != camp_id]
                    with open(gen_path, "w", encoding="utf-8") as f:
                        json.dump(generated, f, indent=2, ensure_ascii=False)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/campaign/save-schedule":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                target_count = payload.get("target_count", 3)
                slots = payload.get("slots", [])
                # Ordina automaticamente gli slot in ordine cronologico crescente
                slots = sorted(slots, key=lambda s: s.get("time", "99:99"))

                sched_path = BASE_DIR / "campaign_schedules.json"
                sched_data = {}
                if sched_path.exists():
                    try:
                        with open(sched_path, "r", encoding="utf-8") as sf:
                            sched_data = json.load(sf)
                    except:
                        sched_data = {}
                
                existing_entry = sched_data.get(camp_id, {})
                existing_entry.update({
                    "target_count": target_count,
                    "slots": slots,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                sched_data[camp_id] = existing_entry

                with open(sched_path, "w", encoding="utf-8") as sf:
                    json.dump(sched_data, sf, indent=2, ensure_ascii=False)

                # Riassegna le clip a scalare secondo il nuovo ordine cronologico
                try:
                    autopilot_engine.advance_campaign_slots(camp_id)
                except Exception as adv_e:
                    print(f"[SERVER] Nota advance_campaign_slots: {adv_e}")

                if sched_path.exists():
                    try:
                        with open(sched_path, "r", encoding="utf-8") as sf:
                            sched_data = json.load(sf)
                    except:
                        pass
                updated_entry = sched_data.get(camp_id, {})

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "campaign_data": updated_entry,
                    "slots": updated_entry.get("slots", [])
                }).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/campaign/add-slot":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                new_time = payload.get("time", "12:00")
                new_video = payload.get("video", "")

                sched_path = BASE_DIR / "campaign_schedules.json"
                sched_data = {}
                if sched_path.exists():
                    try:
                        with open(sched_path, "r", encoding="utf-8") as sf:
                            sched_data = json.load(sf)
                    except:
                        sched_data = {}

                camp_entry = sched_data.get(camp_id, {"slots": [], "target_count": 3})
                slots = camp_entry.get("slots", [])
                slots.append({"time": new_time, "video": new_video})
                # Ordina automaticamente tutti gli slot in ordine cronologico crescente
                slots = sorted(slots, key=lambda s: s.get("time", "99:99"))
                camp_entry["slots"] = slots
                camp_entry["target_count"] = len(slots)
                camp_entry["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sched_data[camp_id] = camp_entry

                with open(sched_path, "w", encoding="utf-8") as sf:
                    json.dump(sched_data, sf, indent=2, ensure_ascii=False)

                # Riassegna le clip a scalare secondo il nuovo ordine orario
                try:
                    autopilot_engine.advance_campaign_slots(camp_id)
                except Exception as adv_e:
                    print(f"[SERVER] Nota advance_campaign_slots: {adv_e}")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "slots": slots, "target_count": len(slots)}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/campaign/remove-slot":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                slot_index = int(payload.get("slot_index", -1))

                sched_path = BASE_DIR / "campaign_schedules.json"
                sched_data = {}
                if sched_path.exists():
                    try:
                        with open(sched_path, "r", encoding="utf-8") as sf:
                            sched_data = json.load(sf)
                    except:
                        sched_data = {}

                camp_entry = sched_data.get(camp_id, {"slots": [], "target_count": 3})
                slots = camp_entry.get("slots", [])
                if 0 <= slot_index < len(slots):
                    slots.pop(slot_index)
                camp_entry["slots"] = slots
                camp_entry["target_count"] = max(1, len(slots))
                camp_entry["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sched_data[camp_id] = camp_entry

                with open(sched_path, "w", encoding="utf-8") as sf:
                    json.dump(sched_data, sf, indent=2, ensure_ascii=False)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "slots": slots, "target_count": len(slots)}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path in ["/api/klippify/sync", "/api/sync/klippify"]:
            try:
                task_id = process_manager.create_task("klippify_sync", "🔄 Sincronizzazione Catalogo & Campagne Klippify")
                process_manager.log(task_id, "Avvio scraping aggiornato da Klippify con Playwright...")
                raw_camps = fetch_klippify_campaigns(use_cache_if_available=False)
                dash_data = fetch_klippify_dashboard_data(use_cache_if_available=False)
                subs_data = fetch_klippify_submissions(use_cache_if_available=False)
                ranked = analyze_and_rank_campaigns(raw_camps)
                generate_html_report(ranked, dash_data, subs_data)
                process_manager.log(task_id, f"Sincronizzate con successo {len(raw_camps)} campagne LIVE e rigenerato il report.")
                process_manager.finish_task(task_id, status="completed")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "message": f"Sincronizzazione completata: {len(raw_camps)} campagne aggiornate.", "count": len(raw_camps)}, ensure_ascii=False).encode("utf-8"))
            except Exception as ex:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(ex)}).encode("utf-8"))

        elif self.path == "/api/campaign/reset-published-clips":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                sched_path = BASE_DIR / "campaign_schedules.json"
                if sched_path.exists():
                    try:
                        with open(sched_path, "r", encoding="utf-8") as sf:
                            sched_data = json.load(sf)
                        if camp_id in sched_data:
                            sched_data[camp_id]["published_clips"] = []
                        with open(sched_path, "w", encoding="utf-8") as sf:
                            json.dump(sched_data, sf, indent=2, ensure_ascii=False)
                    except Exception as ex:
                        print(f"Errore reset published_clips schedule: {ex}")
                
                # Filter out from published_content.json for this campaign
                pub_file = BASE_DIR / "published_content.json"
                if pub_file.exists():
                    try:
                        with open(pub_file, "r", encoding="utf-8") as pf:
                            pub_data = json.load(pf)
                        pub_data = [p for p in pub_data if p.get("campaign_id") != camp_id]
                        with open(pub_file, "w", encoding="utf-8") as pf:
                            json.dump(pub_data, pf, indent=2, ensure_ascii=False)
                    except Exception as ex:
                        print(f"Errore reset published_content.json: {ex}")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/campaign/add-custom-prompt":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                prompt_text = payload.get("prompt", "")
                caption_text = payload.get("caption", "")
                concept_name = payload.get("concept_name", "Nuova Variante")

                gen_path = BASE_DIR / "generated_content.json"
                gen_data = []
                if gen_path.exists():
                    try:
                        with open(gen_path, "r", encoding="utf-8") as gcf:
                            gen_data = json.load(gcf)
                    except:
                        gen_data = []
                
                found = False
                for camp in gen_data:
                    if camp.get("campaign_id") == camp_id:
                        if "scripts" not in camp or not isinstance(camp["scripts"], list):
                            camp["scripts"] = []
                        camp["scripts"].append({
                            "concept_name": concept_name,
                            "video_prompt_gemini": prompt_text,
                            "tiktok_caption": caption_text,
                            "storyboard": [
                                {"duration": "0-3s", "description": "Hook iniziale dinamico", "text_overlay": "Attenzione!"},
                                {"duration": "3-10s", "description": "Sviluppo contenuto", "text_overlay": "Scopri di più"},
                                {"duration": "10-15s", "description": "Call to action finale", "text_overlay": "Link in bio!"}
                            ]
                        })
                        found = True
                        break
                
                if not found:
                    gen_data.append({
                        "campaign_id": camp_id,
                        "scripts": [{
                            "concept_name": concept_name,
                            "video_prompt_gemini": prompt_text,
                            "tiktok_caption": caption_text,
                            "storyboard": []
                        }]
                    })

                with open(gen_path, "w", encoding="utf-8") as gcf:
                    json.dump(gen_data, gcf, indent=2, ensure_ascii=False)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "count": len(gen_data)}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/clipping/upload-source":
            try:
                filename = self.headers.get('X-Filename', f"source_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
                filename = urllib.parse.unquote(filename)
                camp_id = self.headers.get('X-Campaign-Id', 'general')
                
                content_length = int(self.headers.get('Content-Length', 0))
                file_bytes = self.rfile.read(content_length)
                
                # Trova o crea le cartelle di destinazione isolate per la campagna
                sanitized_camp = re.sub(r'[^a-zA-Z0-9_]', '_', camp_id)
                target_src_dir = BASE_DIR / "clipping_sources" / sanitized_camp
                target_src_dir.mkdir(parents=True, exist_ok=True)
                
                out_path = target_src_dir / filename
                with open(out_path, "wb") as out_f:
                    out_f.write(file_bytes)
                
                # Salva anche nella sottocartella raw della campagna
                camp_raw_dir = BASE_DIR / "generated_videos" / sanitized_camp / "raw"
                camp_raw_dir.mkdir(parents=True, exist_ok=True)
                raw_path = camp_raw_dir / filename
                with open(raw_path, "wb") as raw_f:
                    raw_f.write(file_bytes)
                
                # Aggiungi automaticamente alla coda clipping della campagna
                size_mb = len(file_bytes) / (1024 * 1024)
                queue_res = clipping_queue_manager.add_video_to_queue(camp_id, filename, file_size_mb=size_mb)
                
                # Avvia subito in background il processo continuo di clipping a cascata
                clipping_queue_manager.start_auto_clipping_for_campaign(camp_id)
                
                print(f"[SERVER] Video caricato con successo in {out_path} ({size_mb:.2f} MB) e organizzato nella cartella {sanitized_camp}. Clipping avviato!")
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "filename": filename, "path": str(out_path), "queue": queue_res}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/clipping/queue/remove":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                video_id = payload.get("id") or payload.get("filename")
                res = clipping_queue_manager.remove_video_from_queue(camp_id, video_id)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "queue": res}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/clipping/queue/process-all":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                camp_id = payload.get("campaign_id")
                
                started = clipping_queue_manager.start_auto_clipping_for_campaign(camp_id)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "started": started,
                    "message": "Elaborazione coda avviata" if started else "Processo di clipping già in esecuzione"
                }).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/sources/inspect":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                url = payload.get("url", "")
                limit = int(payload.get("limit", 8))
                
                res = source_downloader.inspect_source(url, limit=limit)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/sources/download":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                url = payload.get("url", "")
                camp_id = payload.get("campaign_id", "general")
                title = payload.get("title", "")
                
                task_id = process_manager.create_task(
                    "source_download",
                    f"📥 Download Fonte ({title[:30] if title else url[:30]})"
                )
                
                def run_dl():
                    def task_log(m):
                        process_manager.log(task_id, str(m))
                    res = source_downloader.download_source_video(url, campaign_id=camp_id, custom_title=title, progress_logger=task_log)
                    if res.get("status") == "success":
                        process_manager.finish_task(task_id, status="completed")
                    else:
                        process_manager.finish_task(task_id, status="error", error=res.get("message"))
                
                threading.Thread(target=run_dl, daemon=True).start()
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "task_id": task_id, "message": "Download avviato in background"}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/sources/save-campaign-source":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                camp_id = payload.get("campaign_id", "general")
                source_url = payload.get("url", "")
                auto_download = payload.get("auto_download", True)
                
                res = source_downloader.save_campaign_source(camp_id, source_url, auto_download=auto_download)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/sources/remove-campaign-source":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                camp_id = payload.get("campaign_id", "general")
                source_url = payload.get("url", "")
                
                res = source_downloader.remove_campaign_source(camp_id, source_url)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/open-local-folder":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                camp_id = payload.get("campaign_id", "")
                sanitized_camp = re.sub(r'[^a-zA-Z0-9_]', '_', camp_id) if camp_id else ""
                
                # Apri prioritariamente la cartella isolata dei contenuti della campagna
                target_dir = BASE_DIR / "generated_videos" / sanitized_camp if sanitized_camp else BASE_DIR / "generated_videos"
                if not target_dir.exists():
                    target_dir = BASE_DIR / "clipping_sources" / sanitized_camp if sanitized_camp else BASE_DIR / "clipping_sources"
                (target_dir / "clips").mkdir(parents=True, exist_ok=True)
                (target_dir / "raw").mkdir(parents=True, exist_ok=True)
                
                print(f"[SERVER] Apertura cartella Esplora Risorse: {target_dir}")
                subprocess.Popen(["explorer.exe", str(target_dir)])
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "folder": str(target_dir)}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/debug/kill":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                task_id = payload.get("task_id")
                kill_all = payload.get("kill_all", False)
                if kill_all:
                    killed_count = process_manager.kill_all_active_tasks()
                    res = {"status": "ok", "message": f"Terminati {killed_count} processi attivi"}
                elif task_id:
                    ok, msg = process_manager.kill_task(task_id)
                    res = {"status": "ok" if ok else "error", "message": msg}
                else:
                    res = {"status": "error", "message": "Nessun task_id specificato"}
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/debug/clear":
            try:
                process_manager.clear_finished()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/clipping/run-pipeline":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                video_name = payload.get("video_name") or payload.get("video_path")
                
                print(f"[SERVER] Avvio Pipeline Clipping per campagna {camp_id} (video: {video_name})...")
                
                if video_name:
                    clipping_queue_manager.update_video_status(camp_id, video_name, status="processing")

                import clipping_pipeline
                task_id = process_manager.create_task(
                    "clipping",
                    f"🎬 Clipping 9:16 - {video_name or camp_id} ({camp_id})"
                )

                def run_clip_job():
                    try:
                        def tlog(msg):
                            process_manager.log(task_id, str(msg))
                        res = clipping_pipeline.run_clipping_workflow(
                            campaign_id=camp_id,
                            video_source_path=video_name,
                            is_auto=True,
                            task_logger=tlog
                        )
                        if res.get("status") == "success" and res.get("clips"):
                            clip_names = [c.get("video_filename") for c in res.get("clips") if c.get("video_filename")]
                            if video_name:
                                clipping_queue_manager.update_video_status(camp_id, video_name, status="completed", generated_clips=clip_names)
                            process_manager.finish_task(task_id, status="completed")
                        else:
                            err = res.get("message", "Nessuna clip generata")
                            if video_name:
                                clipping_queue_manager.update_video_status(camp_id, video_name, status="error", error_message=err)
                            process_manager.finish_task(task_id, status="error", error=err)
                    except Exception as e:
                        if video_name:
                            clipping_queue_manager.update_video_status(camp_id, video_name, status="error", error_message=str(e))
                        process_manager.finish_task(task_id, status="error", error=str(e))

                threading.Thread(target=run_clip_job, daemon=True).start()

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "task_id": task_id, "message": "Pipeline clipping avviata"}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/generate-video":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                prompt = payload.get("prompt", "")
                if not prompt:
                    raise ValueError("Prompt vuoto.")
                
                # Salva il prompt in un file di testo temporaneo
                prompt_file = BASE_DIR / "pending_prompt.txt"
                with open(prompt_file, "w", encoding="utf-8") as f:
                    f.write(prompt)
                
                print(f"[SERVER] Avvio bot Gemini per elaborare il prompt...")
                task_id = process_manager.start_subprocess_task(
                    "gemini",
                    f"🤖 Scrittura & Generazione Gemini AI ({prompt[:30]}...)",
                    ["cmd.exe", "/c", "Avvia_Bot.bat", "--auto"],
                    shell=True,
                    meta={"prompt": prompt}
                )
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "task_id": task_id, "message": "Bot avviato e tracciato nel Debug!"}).encode("utf-8"))
                    
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/tiktok/upload":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                filename = payload.get("filename", "")
                title = payload.get("title", "")
                cover_time_ms = payload.get("cover_time_ms", 1000)
                campaign_id = payload.get("campaign_id", "unknown")
                if not filename:
                    raise ValueError("Filename mancante.")

                # Verifica se esiste una didascalia specifica e fedele salvata nei metadati della clip
                clip_meta = clipping_queue_manager.get_clip_metadata(filename)
                if clip_meta and clip_meta.get("tiktok_caption"):
                    title = clip_meta["tiktok_caption"]

                filepath = BASE_DIR / "generated_videos" / filename
                if not filepath.exists() or not filepath.is_file():
                    camp_clip = BASE_DIR / "generated_videos" / str(campaign_id) / "clips" / filename
                    if camp_clip.exists():
                        filepath = camp_clip
                    else:
                        for cand in (BASE_DIR / "generated_videos").rglob(filename):
                            if cand.is_file():
                                filepath = cand
                                break
                upload_script = paths.CORE_DIR / "tiktok_uploader.py"
                
                payload_file = BASE_DIR / "upload_payload.json"
                with open(payload_file, "w", encoding="utf-8") as f:
                    json.dump({
                        "video": str(filepath),
                        "title": title,
                        "cover": cover_time_ms / 1000.0,
                        "campaign_id": campaign_id
                    }, f)

                # Avviamo il processo tracciato in process_manager
                cmd = [sys.executable, "-u", str(upload_script), "--payload", str(payload_file)]
                task_id = process_manager.start_subprocess_task(
                    "tiktok",
                    f"🚀 Upload TikTok & Invio Klippify ({filename})",
                    cmd,
                    meta={"filename": filename, "campaign_id": campaign_id, "title": title}
                )
                
                pub_file = BASE_DIR / "published_content.json"
                try:
                    pub_data = []
                    if pub_file.exists():
                        with open(pub_file, "r", encoding="utf-8") as f:
                            pub_data = json.load(f)
                    
                    pub_data.append({
                        "campaign_id": campaign_id,
                        "filename": filename,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "title": title
                    })
                    
                    with open(pub_file, "w", encoding="utf-8") as f:
                        json.dump(pub_data, f, indent=2, ensure_ascii=False)
                except Exception as ex:
                    print(f"Errore nel salvare published_content.json: {ex}")

                # Sincronizza anche campaign_schedules.json e avanza gli slot
                try:
                    autopilot_engine.mark_clip_as_published(campaign_id, filename)
                    autopilot_engine.advance_campaign_slots(campaign_id)
                except Exception as adv_ex:
                    print(f"Nota avanzamento slot da /api/tiktok/upload: {adv_ex}")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "task_id": task_id, "id": "playwright_bot"}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/klippify/submit-content":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                campaign_id = payload.get("campaign_id")
                content_url = payload.get("content_url")
                platform = payload.get("platform", "tiktok")

                if not campaign_id or not content_url:
                    raise ValueError("campaign_id e content_url sono obbligatori.")

                from klippify_scraper import submit_video_to_klippify
                res = submit_video_to_klippify(campaign_id, content_url, platform=platform)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/toggle":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                enable_val = payload.get("enable", None)
                new_state = autopilot_engine.toggle_engine(enable_val)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "is_enabled": new_state}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/settings":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                state = autopilot_engine.update_settings(payload)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "settings": state}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/queue/add":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                campaign_id = payload.get("campaign_id")
                source_video = payload.get("source_video")
                item_type = payload.get("type", "clipping")
                custom_caption = payload.get("caption", None)
                concept_name = payload.get("concept_name", None)
                
                item = autopilot_engine.add_queue_item(
                    campaign_id=campaign_id,
                    source_video=source_video,
                    item_type=item_type,
                    custom_caption=custom_caption,
                    concept_name=concept_name
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "item": item}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/queue/remove":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                item_id = payload.get("item_id")
                autopilot_engine.remove_queue_item(item_id)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/queue/reorder":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                item_ids = payload.get("item_ids", [])
                autopilot_engine.reorder_queue(item_ids)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/run-now":
            try:
                res = autopilot_engine.trigger_run_now()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(res).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/campaign-toggle":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                enable_val = payload.get("enable", None)
                new_state = autopilot_engine.toggle_campaign_autopilot(camp_id, enable_val)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "is_enabled": new_state}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/campaign-queue-slots":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                added = autopilot_engine.queue_campaign_slots(camp_id)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "added_count": len(added), "items": added}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/campaign-run-now":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                camp_id = payload.get("campaign_id")
                res = autopilot_engine.trigger_campaign_run_now(camp_id)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(res).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/campaign-pause":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                camp_id = payload.get("campaign_id")
                days = float(payload.get("days", 1))
                until_iso = payload.get("until_iso", None)
                res = autopilot_engine.pause_campaign(camp_id, days=days, until_iso=until_iso)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/campaign-end":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                camp_id = payload.get("campaign_id")
                res = autopilot_engine.end_campaign(camp_id)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        elif self.path == "/api/autopilot/campaign-resume":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8')) if body else {}
                camp_id = payload.get("campaign_id")
                res = autopilot_engine.resume_campaign(camp_id)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))



def background_klippify_monitor():
    while True:
        try:
            print('[Monitor] Avvio controllo periodico Klippify (ogni 30 min)...')
            # Fetch without cache to update campaigns_data.json
            fetch_klippify_campaigns(use_cache_if_available=False)
            fetch_klippify_dashboard_data(use_cache_if_available=False)
            print('[Monitor] Dati Klippify aggiornati con successo.')
        except Exception as e:
            print(f'[Monitor] Errore durante aggiornamento: {e}')
        # Dorme 30 minuti (1800 secondi)
        time.sleep(1800)


def run_server():
    server_address = ('', PORT)
    httpd = ThreadedHTTPServer(server_address, KlippifyServerHandler)

    monitor_thread = threading.Thread(target=background_klippify_monitor, daemon=True)
    monitor_thread.start()

    # Avvia il motore di Autopilota in background
    autopilot_engine.start_autopilot_engine()

    url = f"http://localhost:{PORT}"
    print("=" * 60)
    print(f"  [+] Klippify Server Running on {url}")
    print("=" * 60)
    
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Server stopped cleanly.")

if __name__ == "__main__":
    run_server()