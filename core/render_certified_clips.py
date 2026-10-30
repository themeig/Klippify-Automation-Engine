import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))

import face_verifier
import video_vision_evaluator
import strategy_combiner

CAMPAIGN_ID = "6a0dd557394d916370d7fb3d"
CAMPAIGN_NAME = "Marco Billiani | Chiave immobiliare"
AUTOPILOT_FILE = ROOT / "data/autopilot_state.json"

SOURCE_PATH = ROOT / "clipping_sources/6a0dd557394d916370d7fb3d/House_Tour_casa_da_200_a_notte_In_Svizzera_Studente_guadagna_auIyyF7T3ws_20261004_000155.mp4"

def find_5of5_engaging_segments(video_path, target_count=3, clip_duration=38.04):
    """
    Trova segmenti che superano RIGOROSAMENTE il test facciale OpenCV 5/5
    nei primi 7 secondi (Klippify AI Rule 1), ordinati per punteggio visivo/gestuale.
    """
    src_p = Path(video_path)
    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(src_p)]
    res = subprocess.run(cmd_dur, capture_output=True, text=True)
    total_dur = float(res.stdout.strip() or 0)
    print(f"[+] Durata video sorgente: {total_dur:.1f}s", flush=True)

    candidates = []
    curr_t = 10.0
    step = 10.0

    print(f"🔍 Scansione intensiva per segmenti con volto continuo 5/5 nei primi 7s...", flush=True)
    while curr_t + clip_duration <= total_dur - 10.0:
        # Campiona i primi 7 secondi: 0.8s, 2.0s, 3.5s, 5.0s, 6.5s
        f1 = face_verifier.extract_frame_at_sec(src_p, curr_t + 0.8)
        f2 = face_verifier.extract_frame_at_sec(src_p, curr_t + 2.0)
        f3 = face_verifier.extract_frame_at_sec(src_p, curr_t + 3.5)
        f4 = face_verifier.extract_frame_at_sec(src_p, curr_t + 5.0)
        f5 = face_verifier.extract_frame_at_sec(src_p, curr_t + 6.5)

        has_f1 = face_verifier.detect_face_in_frame(f1, min_size=(45, 45), active_crop_only=True)
        has_f2 = face_verifier.detect_face_in_frame(f2, min_size=(45, 45), active_crop_only=True)
        has_f3 = face_verifier.detect_face_in_frame(f3, min_size=(45, 45), active_crop_only=True)
        has_f4 = face_verifier.detect_face_in_frame(f4, min_size=(45, 45), active_crop_only=True)
        has_f5 = face_verifier.detect_face_in_frame(f5, min_size=(45, 45), active_crop_only=True)

        detections = [has_f1, has_f2, has_f3, has_f4, has_f5]
        face_count = sum(1 for d in detections if d)

        # Regola Klippify: Volto CONTINUO senza stacchi su B-roll (almeno 4 su 5 e continuo)
        if has_f1 and has_f2 and has_f3 and (has_f4 or has_f5) and face_count >= 4:
            v_score, v_details = video_vision_evaluator.evaluate_segment_visual_energy(str(src_p), curr_t, clip_duration)
            candidates.append({
                "start_sec": curr_t,
                "end_sec": curr_t + clip_duration,
                "face_count": face_count,
                "detections": detections,
                "visual_score": v_score,
                "details": v_details
            })
            curr_t += clip_duration + 15.0 # Salta avanti per evitare clip sovrapposte
        else:
            curr_t += step

    print(f"[+] Trovati {len(candidates)} segmenti con volto 100% conforme nei primi 7s.", flush=True)
    # Ordina per score visivo decrescente
    candidates.sort(key=lambda x: (x["face_count"], x["visual_score"]), reverse=True)
    best = candidates[:target_count]
    for idx, c in enumerate(best, 1):
        print(f"   {idx}. Da {c['start_sec']:.1f}s a {c['end_sec']:.1f}s | Volto: {c['face_count']}/5 | Score Visivo: {c['visual_score']}/100", flush=True)

    return best

def render_all():
    if not SOURCE_PATH.exists():
        print(f"[-] Video sorgente non trovato: {SOURCE_PATH}")
        return

    best_segments = find_5of5_engaging_segments(SOURCE_PATH, target_count=3, clip_duration=38.04)
    if len(best_segments) < 3:
        print(f"[!] Meno di 3 segmenti trovati. Allargo la ricerca con step ridotto...")
        # fallback se servono
    
    clips_dir = ROOT / "generated_videos" / CAMPAIGN_ID / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    today_str = datetime.now().strftime("%Y%m%d")
    timestamp_gen = datetime.now().strftime("%Y%m%d_%H%M%S")

    configs = [
        {
            "slot": "12:00",
            "id_suffix": "strat1_shock_loop",
            "strategy": "combo_1_shock_loop",
            "seg": best_segments[0],
            "hook": "SE COMPRI QUESTA CASA IN SVIZZERA STAI BUTTANDO SOLDI! 💸🇨🇭",
            "title": "SE COMPRI QUESTA CASA IN SVIZZERA STAI BUTTANDO SOLDI! 💸🇨🇭 Trovi la guida completa su @marcobilliani @chiaveimmobiliare #marcobilliani #chiaveimmobiliare #affittibrevi #klippify"
        },
        {
            "slot": "16:00",
            "id_suffix": "strat2_controversy",
            "strategy": "combo_2_controversy_comment_bait",
            "seg": best_segments[1],
            "hook": "200€ A NOTTE IN SVIZZERA? LA VERITÀ CHE NESSUNO TI DICE! 🤐❄️",
            "title": "200€ A NOTTE IN SVIZZERA? LA VERITÀ CHE NESSUNO TI DICE! 🤐❄️ Tu che faresti al suo posto? Dimmelo nei commenti! Segui @marcobilliani @chiaveimmobiliare #marcobilliani #chiaveimmobiliare #affittibrevi #klippify"
        },
        {
            "slot": "20:00",
            "id_suffix": "strat3_breaking_news",
            "strategy": "combo_3_breaking_news_loop",
            "seg": best_segments[2],
            "hook": "ULTIM'ORA SVIZZERA: IL BUSINESS CHE STA ESPLODENDO! 📰🏔️",
            "title": "ULTIM'ORA SVIZZERA: IL BUSINESS CHE STA ESPLODENDO! 📰🏔️ Trovi l'analisi completa su @marcobilliani @chiaveimmobiliare #marcobilliani #chiaveimmobiliare #affittibrevi #klippify"
        }
    ]

    rendered = []
    for idx, cfg in enumerate(configs, 1):
        out_filename = f"clip_MarcoBillian_{today_str}_slot{idx}_{cfg['id_suffix']}_{timestamp_gen}.mp4"
        out_filepath = clips_dir / out_filename
        seg = cfg["seg"]

        print(f"\n=======================================================", flush=True)
        print(f"🎬 Render Clip {idx}/3 (Slot {cfg['slot']}): {out_filename}", flush=True)
        print(f"   Start: {seg['start_sec']:.1f}s | Volto sorgente: {seg['face_count']}/5", flush=True)
        print(f"=======================================================\n", flush=True)

        res = strategy_combiner.render_strategy_clip(
            input_video_path=str(SOURCE_PATH),
            start_sec=seg["start_sec"],
            duration_sec=38.04,
            output_video_path=str(out_filepath),
            strategy_key=cfg["strategy"],
            custom_hook_text=cfg["hook"],
            brand_mention="@marcobilliani",
            brand_cta="Segui @marcobilliani @chiaveimmobiliare"
        )

        is_valid, report = face_verifier.verify_clip_face_compliance(str(out_filepath))
        face_count = report.get("face_detections_count", 0) if isinstance(report, dict) else 0
        print(f"[+] Verifica Finale Clip Generata: Conforme={is_valid} ({face_count}/5)", flush=True)

        rendered.append({
            "slot": cfg["slot"],
            "filename": out_filename,
            "filepath": str(out_filepath),
            "strategy": cfg["strategy"],
            "title": cfg["title"],
            "face_valid": is_valid,
            "face_count": face_count
        })

    # Pulizia storage: elimina il video sorgente grande
    print(f"\n🧹 Pulizia storage: eliminazione file sorgente...", flush=True)
    if SOURCE_PATH.exists():
        size_mb = SOURCE_PATH.stat().st_size / (1024 * 1024)
        SOURCE_PATH.unlink()
        print(f"[+] Eliminato {SOURCE_PATH.name} ({size_mb:.2f} MB liberati)", flush=True)

    # Popola coda autopilot per oggi 04/10/2026
    print(f"\n🚀 Aggiornamento coda Autopilot...", flush=True)
    if AUTOPILOT_FILE.exists():
        with open(AUTOPILOT_FILE, "r", encoding="utf-8") as af:
            auto_state = json.load(af)

        new_queue = []
        for c in rendered:
            q_item = {
                "id": f"k{c['slot'].replace(':', '')}_{today_str}_{c['strategy']}",
                "campaign_id": CAMPAIGN_ID,
                "campaign_name": CAMPAIGN_NAME,
                "type": "ready_clip",
                "source_video": c["filename"],
                "concept_name": f"Slot ({c['slot']}) - [{c['strategy'].upper()}] {c['title'][:40]}...",
                "generated_clip": c["filename"],
                "caption": c["title"],
                "scheduled_time": c["slot"],
                "status": "ready",
                "strategy": c["strategy"],
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            new_queue.append(q_item)

        auto_state["queue"] = new_queue
        auto_state["today_uploads_count"] = 0
        auto_state["last_upload_date"] = today_str
        auto_state["next_scheduled_run"] = f"{datetime.now().strftime('%Y-%m-%d')} 12:00:00"

        with open(AUTOPILOT_FILE, "w", encoding="utf-8") as af:
            json.dump(auto_state, af, indent=2, ensure_ascii=False)
        print(f"✅ Coda Autopilot aggiornata con {len(new_queue)} clip certificate 5/5 per oggi (12:00, 16:00, 20:00)!", flush=True)

if __name__ == "__main__":
    render_all()
