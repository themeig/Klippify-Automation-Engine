import paths
import json
import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime

# Force UTF-8 on Windows stdout/stderr
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import clip_processor
import video_inspector


def load_ai_director_cuts(cuts_file: Path, video_name: str = None, campaign_id: str = None) -> list[dict]:
    """
    Carica il piano di montaggio scritto dall'Agente AI di Antigravity (ai_director_cuts.json).
    Restituisce la lista di clip (con segments multipli, crop_mode, center_x_ratio, hook_text, tiktok_caption).
    """
    if not cuts_file:
        return []
    p = Path(cuts_file)
    if not p.exists() or not p.is_file():
        return []

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[AI-DIRECTOR] Errore lettura {p}: {e}")
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        file_camp = str(data.get("campaign_id", ""))
        file_vid = Path(str(data.get("video_file", ""))).name
        if campaign_id and file_camp and file_camp != str(campaign_id):
            return []
        if video_name and file_vid and file_vid.lower() != Path(video_name).name.lower():
            return []
        clips = data.get("clips", [])
        if isinstance(clips, list):
            return clips

    return []


def purge_legacy_blind_clips(root_dir: Path = None) -> dict:
    """
    Rimuove da clip_metadata.json e da campaign_schedules.json tutte le vecchie clip
    tagliate alla cieca dal fallback (identificate da transcript == 'Estratto dal video originale').
    """
    root = Path(root_dir) if root_dir else paths.PROJECT_ROOT
    meta_file = root / "clip_metadata.json"
    sched_file = root / "campaign_schedules.json"

    removed_clips = set()
    if meta_file.exists():
        try:
            meta_data = json.loads(meta_file.read_text(encoding="utf-8"))
            cleaned_meta = {}
            for fname, info in meta_data.items():
                if isinstance(info, dict) and info.get("transcript") == "Estratto dal video originale":
                    removed_clips.add(fname)
                else:
                    cleaned_meta[fname] = info
            meta_file.write_text(json.dumps(cleaned_meta, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"[PURGE] Errore pulizia {meta_file}: {e}")

    if sched_file.exists() and removed_clips:
        try:
            sched_data = json.loads(sched_file.read_text(encoding="utf-8"))
            for cid, cinfo in sched_data.items():
                if isinstance(cinfo, dict) and "slots" in cinfo:
                    for slot in cinfo.get("slots", []):
                        if slot.get("video") in removed_clips:
                            slot["video"] = ""
            sched_file.write_text(json.dumps(sched_data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"[PURGE] Errore pulizia {sched_file}: {e}")

    return {"removed_count": len(removed_clips), "removed_files": sorted(removed_clips)}


def run_clipping_workflow(campaign_id, video_source_path=None, is_auto=True, task_logger=None, cuts_file=None):
    root = paths.PROJECT_ROOT

    # 1. Carica i dati della campagna attiva
    classified_file = root / "active_campaigns_classified.json"
    camp_data = {}
    if classified_file.exists():
        try:
            with open(classified_file, "r", encoding="utf-8") as f:
                all_class = json.load(f)
                for c in all_class:
                    cid = c.get("id") or c.get("campaign_token") or c.get("campaign_id")
                    cname = c.get("name") or c.get("campaign_name") or ""
                    if str(cid) == str(campaign_id) or cname.lower() == str(campaign_id).lower():
                        camp_data = c
                        break
        except Exception:
            pass

    camp_name = camp_data.get("name") or camp_data.get("campaign_name") or str(campaign_id)
    print("\n=======================================================", flush=True)
    print(f"🎬 AVVIO PIPELINE CLIPPING AI-PILOTED PER: {camp_name}", flush=True)
    print("=======================================================\n", flush=True)
    if task_logger:
        task_logger(f"🎬 Avvio clipping per la campagna: {camp_name}")

    # 2. Localizza il video sorgente
    source_file = None
    if video_source_path:
        p = Path(video_source_path)
        if not p.is_absolute():
            for cand in [
                root / "generated_videos" / str(campaign_id) / "raw" / video_source_path,
                root / "clipping_sources" / str(campaign_id) / video_source_path,
                root / "clipping_sources" / re.sub(r'[^a-zA-Z0-9_]', '_', str(campaign_id)) / video_source_path,
                root / "clipping_sources" / re.sub(r'[^a-zA-Z0-9_]', '_', camp_name) / video_source_path,
                root / "generated_videos" / str(campaign_id) / video_source_path,
                root / "generated_videos" / video_source_path,
                root / video_source_path
            ]:
                if cand.exists() and cand.is_file():
                    p = cand
                    break
        if p.exists() and p.is_file():
            source_file = p
            print(f"[+] Video sorgente specificato trovato: {source_file.name}", flush=True)
            if task_logger:
                task_logger(f"[+] Video sorgente: {source_file.name}")

    if not source_file:
        search_dirs = [
            root / "generated_videos" / str(campaign_id) / "raw",
            root / "clipping_sources" / str(campaign_id),
            root / "clipping_sources" / re.sub(r'[^a-zA-Z0-9_]', '_', str(campaign_id)),
            root / "clipping_sources" / re.sub(r'[^a-zA-Z0-9_]', '_', camp_name),
            root / "generated_videos" / str(campaign_id),
            root / "clipping_sources"
        ]

        all_found = []
        for sdir in search_dirs:
            if sdir.exists():
                for ext in ["*.mp4", "*.mov", "*.mkv", "*.avi", "*.webm"]:
                    all_found.extend(list(sdir.glob(ext)))

        unique_videos = list({v.resolve(): v for v in all_found}.values())
        if unique_videos:
            unique_videos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            source_file = unique_videos[0]
            print(f"[+] Trovato video sorgente più recente: {source_file.name} ({source_file.stat().st_size / (1024*1024):.2f} MB)", flush=True)
            if task_logger:
                task_logger(f"[+] Video sorgente più recente selezionato: {source_file.name}")
        else:
            print("[!] Nessun video sorgente trovato.", flush=True)
            if task_logger:
                task_logger(f"[!] Nessun video sorgente trovato per {camp_name}")
            return {"status": "error", "message": f"Nessun video trovato per la campagna {camp_name}"}

    # 3. Cerca il piano di montaggio deciso dall'Agente AI di Antigravity (ai_director_cuts.json)
    candidate_cuts_files = []
    if cuts_file:
        cf_path = Path(cuts_file)
        candidate_cuts_files.append(cf_path if cf_path.is_absolute() else root / cf_path)
    candidate_cuts_files.extend([
        source_file.parent / f"{source_file.stem}_ai_cuts.json",
        root / "data" / "ai_director_cuts.json",
        root / "ai_director_cuts.json"
    ])

    analysis_results = []
    for cf in candidate_cuts_files:
        loaded = load_ai_director_cuts(cf, video_name=source_file.name, campaign_id=str(campaign_id))
        if loaded:
            analysis_results = loaded
            print(f"[+] Caricato piano di regia AI da '{cf.name}' ({len(analysis_results)} clip multi-segmento)!", flush=True)
            if task_logger:
                task_logger(f"🧠 Piano di regia AI caricato ({len(analysis_results)} clip decise dall'Agente AI).")
            break

    # VIETATO TAGLIARE A CASO: se l'Agente AI non ha ancora scritto il piano di montaggio,
    # prepara il pacchetto di ispezione (trascrizione + Storyboard JPG) e attendi la regia AI!
    if not analysis_results:
        print("[AI-DIRECTOR] Nessun piano di taglio AI trovato per questo video. Preparo trascrizione e Storyboard JPG per l'Agente AI...", flush=True)
        if task_logger:
            task_logger("🔍 Preparazione trascrizione e Storyboard JPG per la regia dell'Agente AI di Antigravity...")
        insp = video_inspector.inspect_video(source_file, campaign_id=str(campaign_id))
        return {
            "status": "awaiting_ai_director",
            "campaign_id": str(campaign_id),
            "campaign_name": camp_name,
            "video_file": str(source_file),
            "inspection_file": insp.get("inspection_file"),
            "storyboards": insp.get("storyboards", []),
            "message": "Ispezione completata. In attesa che l'Agente AI di Antigravity decida i segmenti in ai_director_cuts.json."
        }

    # 4. Esecuzione Montaggio Multi-Segmento 9:16 FFmpeg seguendo le decisioni dell'AI
    camp_clips_dir = root / "generated_videos" / str(campaign_id) / "clips"
    camp_clips_dir.mkdir(parents=True, exist_ok=True)

    root_gen_dir = root / "generated_videos"
    root_gen_dir.mkdir(exist_ok=True)

    processed_clips = []
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_short_name = re.sub(r'[^a-zA-Z0-9]', '', camp_name)[:12]

    camp_cta = camp_data.get("call_to_action") or "Guarda il video completo sul profilo!"
    hashtags_list = camp_data.get("mandatory_hashtags") or ["#klippify"]
    mentions_list = camp_data.get("mandatory_mentions") or []
    hashtags_str = " ".join([h if h.startswith('#') else f"#{h}" for h in hashtags_list])
    mentions_str = " ".join([m if m.startswith('@') else f"@{m}" for m in mentions_list])
    primary_mention = mentions_list[0] if mentions_list else None

    import clipping_queue_manager

    for idx, clip in enumerate(analysis_results):
        out_filename = f"clip_{sanitized_short_name}_slot{idx+1}_{timestamp_str}.mp4"
        out_path = camp_clips_dir / out_filename

        segments = clip.get("segments")
        start_t = clip.get("start_time") or (segments[0].get("start") if segments else "00:00")
        end_t = clip.get("end_time") or (segments[-1].get("end") if segments else "00:30")
        hook_t = clip.get("hook_text") or clip.get("concept") or ""
        concept_t = clip.get("concept") or f"Clip {idx+1} - {camp_name}"
        crop_mode = clip.get("crop_mode") or "face_crop"
        center_x = float(clip.get("center_x_ratio", 0.5))
        y_start_r = float(clip.get("y_start_ratio", 0.0))
        height_r = float(clip.get("height_ratio", 1.0))

        raw_caption = clip.get("tiktok_caption") or hook_t or concept_t
        final_caption_parts = [raw_caption]
        if camp_cta and camp_cta.lower() not in raw_caption.lower():
            final_caption_parts.append(camp_cta)
        if mentions_str and mentions_str not in raw_caption:
            final_caption_parts.append(mentions_str)
        if hashtags_str and hashtags_str not in raw_caption:
            final_caption_parts.append(hashtags_str)

        full_clip_caption = " ".join(final_caption_parts).strip()

        print(f"\n[+] Montaggio AI clip {idx+1}/{len(analysis_results)} ({crop_mode}, X={center_x}, Y={y_start_r}, H={height_r})...")
        print(f"    🎣 Hook (3.2s): {hook_t}")
        print(f"    📢 CTA finale: {camp_cta}")
        print(f"    📝 Caption: {full_clip_caption}")

        if task_logger:
            task_logger(f"✂️ [FFMPEG-AI] Montaggio Clip [{idx+1}/{len(analysis_results)}] ({crop_mode})...")

        success = clip_processor.process_clip_ffmpeg(
            input_video_path=source_file,
            start_time=start_t,
            end_time=end_t,
            output_video_path=out_path,
            mode=crop_mode,
            center_x_ratio=center_x,
            y_start_ratio=y_start_r,
            height_ratio=height_r,
            segments=segments,
            hook_text=hook_t,
            cta_text=camp_cta,
            brand_mention=primary_mention,
            logger=task_logger
        )

        if success:
            clip["video_filename"] = out_filename
            clip["tiktok_caption"] = full_clip_caption
            processed_clips.append(clip)
            if task_logger:
                task_logger(f"💾 Clip AI salvata nel magazzino: {out_filename}")

            clip_meta = {
                "filename": out_filename,
                "campaign_id": str(campaign_id),
                "campaign_name": camp_name,
                "raw_source_video": source_file.name,
                "concept": concept_t,
                "hook_text": hook_t,
                "crop_mode": crop_mode,
                "center_x_ratio": center_x,
                "segments": segments,
                "transcript": clip.get("transcript", ""),
                "tiktok_caption": full_clip_caption,
                "start_time": start_t,
                "end_time": end_t,
                "directed_by": "antigravity_ai_director",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            clipping_queue_manager.save_clip_metadata(out_filename, clip_meta)
            print(f"    [OK] Clip e metadati salvati: {out_filename}")

    # 5. Aggiorna lo schedulatore slot per la campagna
    try:
        schedules_file = root / "campaign_schedules.json"
        sched_data = {}
        if schedules_file.exists():
            with open(schedules_file, "r", encoding="utf-8") as sf:
                sched_data = json.load(sf)

        cid_str = str(campaign_id)
        if cid_str not in sched_data:
            sched_data[cid_str] = {"target_count": 3, "slots": [], "autopilot_enabled": True}

        current_slots = sched_data[cid_str].get("slots", [])
        times = ["15:00", "17:00", "20:00", "22:00"]
        for idx, clip in enumerate(processed_clips):
            t = times[idx] if idx < len(times) else "18:00"
            if idx < len(current_slots):
                if not current_slots[idx].get("video"):
                    current_slots[idx]["video"] = clip.get("video_filename", "")
            else:
                current_slots.append({"time": t, "video": clip.get("video_filename", "")})

        sched_data[cid_str]["slots"] = current_slots
        sched_data[cid_str]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(schedules_file, "w", encoding="utf-8") as sf:
            json.dump(sched_data, sf, indent=2, ensure_ascii=False)
        print("[+] Slot e magazzino aggiornati in campaign_schedules.json!")
    except Exception as e:
        print(f"[!] Errore salvataggio slot: {e}")

    print(f"\n[SUCCESS] Elaborate con successo {len(processed_clips)} clip 9:16 pilotate dall'AI!")

    if processed_clips and source_file:
        try:
            import storage_manager
            storage_manager.delete_raw_source_after_clipping(source_file, campaign_id=campaign_id, logger=task_logger)
        except Exception as st_err:
            print(f"[STORAGE WARNING] Impossibile eliminare video sorgente: {st_err}")

    return {
        "status": "success",
        "campaign_id": campaign_id,
        "campaign_name": camp_name,
        "clips": processed_clips
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI-Piloted Master Clipping Pipeline')
    parser.add_argument('campaign_id', nargs='?', type=str, help='ID o nome della campagna attiva')
    parser.add_argument('--video', type=str, default=None, help='Percorso o nome del file video sorgente')
    parser.add_argument('--cuts', type=str, default=None, help='Percorso al file JSON dei tagli decisi dall\'AI (ai_director_cuts.json)')
    parser.add_argument('--purge-blind-clips', action='store_true', help='Rimuove tutte le vecchie clip tagliate alla cieca dal fallback')
    args = parser.parse_args()

    if args.purge_blind_clips:
        res = purge_legacy_blind_clips()
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.campaign_id:
        run_clipping_workflow(args.campaign_id, video_source_path=args.video, cuts_file=args.cuts)
    else:
        parser.print_help()
