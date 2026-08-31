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
    except:
        pass

# Import local modules
import clip_processor
import gemini_analysis_bot

def run_clipping_workflow(campaign_id, video_source_path=None, is_auto=True, task_logger=None):
    root = Path(r"c:\Users\HP\Desktop\contenuti klippify")
    
    # 1. Carica i dati della campagna attiva
    classified_file = root / "active_campaigns_classified.json"
    camp_data = {}
    if classified_file.exists():
        with open(classified_file, "r", encoding="utf-8") as f:
            all_class = json.load(f)
            for c in all_class:
                cid = c.get("id") or c.get("campaign_token") or c.get("campaign_id")
                cname = c.get("name") or c.get("campaign_name") or ""
                if str(cid) == str(campaign_id) or cname.lower() == str(campaign_id).lower():
                    camp_data = c
                    break
                    
    camp_name = camp_data.get("name") or camp_data.get("campaign_name") or str(campaign_id)
    print(f"\n=======================================================", flush=True)
    print(f"🎬 AVVIO PIPELINE CLIPPING PER: {camp_name}", flush=True)
    print(f"=======================================================\n", flush=True)
    if task_logger: task_logger(f"🎬 Avvio clipping per la campagna: {camp_name}")
    
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
            if task_logger: task_logger(f"[+] Video sorgente: {source_file.name}")

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
            print(f"[+] Trovato video sorgente piu recente: {source_file.name} ({source_file.stat().st_size / (1024*1024):.2f} MB)", flush=True)
            if task_logger: task_logger(f"[+] Video sorgente piu recente selezionato: {source_file.name}")
        else:
            print(f"[!] Nessun video sorgente trovato.", flush=True)
            if task_logger: task_logger(f"[!] Nessun video sorgente trovato per {camp_name}")
            return {"status": "error", "message": f"Nessun video trovato per la campagna {camp_name}"}
            
    # 3. Suddivisione video se troppo lungo
    print(f"\n[+] Verifica durata video sorgente: {source_file.name}...", flush=True)
    video_parts = clip_processor.split_long_video_if_needed(source_file, max_duration_seconds=900, chunk_duration=600)
    video_to_analyze = video_parts[0] if video_parts else source_file
    
    # 4. Upload e analisi con Gemini Bot nella chat 'analisi video klippify'
    print(f"\n[+] Avvio bot per upload e analisi su Gemini ('analisi video klippify')...", flush=True)
    if task_logger: task_logger("[+] Apertura bot Gemini per analisi del video...")
    analysis_results = gemini_analysis_bot.run_analysis(video_to_analyze, is_auto=is_auto, task_logger=task_logger)
    
    if not analysis_results:
        print("[-] Nessun timestamp estratto da Gemini o bot in attesa. Generazione fallback di 3 clip salienti...")
        analysis_results = [
            {"clip_number": 1, "start_time": "00:10", "end_time": "00:45", "concept": f"Punto Chiave 1 - {camp_name}", "hook_text": f"POV: quello che nessuno ti dice su {camp_name} 🤫", "transcript": "Estratto dal video originale"},
            {"clip_number": 2, "start_time": "01:00", "end_time": "01:35", "concept": f"Punto Chiave 2 - {camp_name}", "hook_text": "Non fare questo errore se vuoi guadagnare!", "transcript": "Estratto dal video originale"},
            {"clip_number": 3, "start_time": "02:00", "end_time": "02:35", "concept": f"Punto Chiave 3 - {camp_name}", "hook_text": "Guarda cosa succede alla fine...", "transcript": "Estratto dal video originale"}
        ]
        
    # 5. Taglio FFmpeg 9:16 per ciascuna clip salvato nella cartella isolata della campagna
    camp_clips_dir = root / "generated_videos" / str(campaign_id) / "clips"
    camp_clips_dir.mkdir(parents=True, exist_ok=True)
    
    root_gen_dir = root / "generated_videos"
    root_gen_dir.mkdir(exist_ok=True)
    
    processed_clips = []
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_short_name = re.sub(r'[^a-zA-Z0-9]', '', camp_name)[:12]
    
    # Determina la CTA, tag e hashtag obbligatori della campagna
    camp_cta = camp_data.get("call_to_action", "")
    if not camp_cta and "Sara Dizdari" in camp_name:
        camp_cta = "La lezione gratuita sul profilo di Sara"
        
    hashtags_list = camp_data.get("mandatory_hashtags") or ["#klippify"]
    mentions_list = camp_data.get("mandatory_mentions") or []
    hashtags_str = " ".join([h if h.startswith('#') else f"#{h}" for h in hashtags_list])
    mentions_str = " ".join([m if m.startswith('@') else f"@{m}" for m in mentions_list])

    # Importa il gestore metadati
    import clipping_queue_manager

    for idx, clip in enumerate(analysis_results):
        out_filename = f"clip_{sanitized_short_name}_slot{idx+1}_{timestamp_str}.mp4"
        out_path = camp_clips_dir / out_filename
        
        start_t = clip.get("start_time", f"00:{idx*40}")
        end_t = clip.get("end_time", f"00:{idx*40 + 35}")
        hook_t = clip.get("hook_text") or clip.get("concept") or ""
        concept_t = clip.get("concept") or f"Clip {idx+1} - {camp_name}"
        
        # Costruisce la didascalia specifica e fedele per questa clip
        raw_caption = clip.get("tiktok_caption") or hook_t or concept_t
        final_caption_parts = [raw_caption]
        if camp_cta and camp_cta.lower() not in raw_caption.lower():
            final_caption_parts.append(camp_cta)
        if mentions_str and mentions_str not in raw_caption:
            final_caption_parts.append(mentions_str)
        if hashtags_str and hashtags_str not in raw_caption:
            final_caption_parts.append(hashtags_str)
            
        full_clip_caption = " ".join(final_caption_parts).strip()
        
        print(f"\n[+] Taglio clip {idx+1}/{len(analysis_results)}: da {start_t} a {end_t} in formato 9:16 vertical TikTok...")
        print(f"    🎣 Hook: {hook_t}")
        print(f"    📢 CTA: {camp_cta}")
        print(f"    📝 Caption: {full_clip_caption}")
        
        if task_logger:
            task_logger(f"✂️ [FFMPEG] Avvio ritaglio Clip [{idx+1}/{len(analysis_results)}] (da {start_t} a {end_t})...")
            if hook_t: task_logger(f"   🎣 Hook visivo: {hook_t}")
            if camp_cta: task_logger(f"   📢 CTA: {camp_cta}")
        
        success = clip_processor.process_clip_ffmpeg(
            input_video_path=source_file,
            start_time=start_t,
            end_time=end_t,
            output_video_path=out_path,
            mode="blur_background",
            hook_text=hook_t,
            cta_text=camp_cta,
            logger=task_logger
        )
        
        if success:
            clip["video_filename"] = out_filename
            clip["tiktok_caption"] = full_clip_caption
            processed_clips.append(clip)
            if task_logger: task_logger(f"💾 Clip e metadati salvati nel magazzino: {out_filename}")
            
            # Salva i metadati persistenti per questa specifica clip
            clip_meta = {
                "filename": out_filename,
                "campaign_id": str(campaign_id),
                "campaign_name": camp_name,
                "raw_source_video": source_file.name,
                "concept": concept_t,
                "hook_text": hook_t,
                "transcript": clip.get("transcript", ""),
                "tiktok_caption": full_clip_caption,
                "start_time": start_t,
                "end_time": end_t,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            clipping_queue_manager.save_clip_metadata(out_filename, clip_meta)
            print(f"    [OK] Clip e metadati salvati: {out_filename}")
            
    # 6. Aggiorna lo schedulatore slot per la campagna (assegnazione iniziale slot se vuoti)
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

    print(f"\n[SUCCESS] Elaborate con successo {len(processed_clips)} clip 9:16 pronte per TikTok!")

    # 7. Pulizia automatica file sorgente lungo completato (risparmio spazio disco)
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
    parser = argparse.ArgumentParser(description='Master Clipping Pipeline')
    parser.add_argument('campaign_id', type=str, help='ID o nome della campagna attiva')
    parser.add_argument('--video', type=str, default=None, help='Percorso o nome del file video sorgente')
    args = parser.parse_args()
    
    run_clipping_workflow(args.campaign_id, video_source_path=args.video)
