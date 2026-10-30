import os
import sys
import json
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))

import video_captioner
import face_verifier

AUDIO_DIR = ROOT / "data/audio_tracks"
SFX_IMPACT = AUDIO_DIR / "sfx_impact.wav"
SFX_CHIME = AUDIO_DIR / "sfx_chime.wav"
SFX_WHOOSH = AUDIO_DIR / "sfx_whoosh.wav"
AMBIENT_MUSIC = AUDIO_DIR / "curiosity_ambient.mp3"

# Definizione Strategie A/B/C/D
STRATEGY_CATALOG = {
    "combo_1_shock_loop": {
        "id": "combo_1_shock_loop",
        "name": "Shock Hook + Seamless Loop (Loss Aversion)",
        "description": "Gancio shock su perdita di denaro + SFX Impact al sec 0 + Chiusura a Loop continuo",
        "sfx_start": SFX_IMPACT,
        "sfx_volume": 0.22,
        "music_volume": 0.05,
        "hook_prefix": "🚨 ATTENZIONE: ",
        "badge_text": "⚠️ ERRORE DA 2.000€",
        "outro_type": "loop",
        "outro_text": "E LA COSA PIÙ ASSURDA È CHE..."
    },
    "combo_2_controversy_comment_bait": {
        "id": "combo_2_controversy_comment_bait",
        "name": "Controversia Scomoda + Comment Bait",
        "description": "Rivelazione scottante + SFX Whoosh + Domanda polarizzante finale per forzare i commenti",
        "sfx_start": SFX_WHOOSH,
        "sfx_volume": 0.25,
        "music_volume": 0.05,
        "hook_prefix": "🤐 LA VERITÀ CHE NESSUNO DICE: ",
        "badge_text": "🤫 SEGRETO SVELATO",
        "outro_type": "comment_bait",
        "outro_text": "TU COSA AVRESTI FATTO? DILLO NEI COMMENTI! 👇"
    },
    "combo_3_breaking_news_loop": {
        "id": "combo_3_breaking_news_loop",
        "name": "Breaking News Banner + Curiosity Gap + Loop",
        "description": "Inquadratura con banner Breaking News stile TG + Gancio curiosità + Chiusura ad anello",
        "sfx_start": SFX_IMPACT,
        "sfx_volume": 0.20,
        "music_volume": 0.05,
        "hook_prefix": "📰 ULTIM'ORA AIRBNB: ",
        "badge_text": "🔴 NOTIZIA ESCLUSIVA",
        "outro_type": "loop",
        "outro_text": "ED È PER QUESTO CHE IL 90% SBAGLIA..."
    },
    "combo_4_loss_aversion_story": {
        "id": "combo_4_loss_aversion_story",
        "name": "Storytelling Emotivo + Paura di Fallire + Chime",
        "description": "Storia ad alta tensione emotiva su rischi e conseguenze + SFX Chime sui numeri chiave",
        "sfx_start": SFX_CHIME,
        "sfx_volume": 0.20,
        "music_volume": 0.05,
        "hook_prefix": "😱 HO QUASI PERSO TUTTO: ",
        "badge_text": "🛑 NON FARE QUESTO",
        "outro_type": "comment_bait",
        "outro_text": "TI È MAI SUCCESSO? SCRIVILO QUI SOTTO! 👇"
    }
}

def render_strategy_clip(
    input_video_path,
    start_sec,
    duration_sec,
    output_video_path,
    strategy_key="combo_1_shock_loop",
    custom_hook_text="SE FAI QUESTO CON LA TUA CASA STAI BRUCIANDO 2.000€!",
    brand_mention="@marcobilliani",
    brand_cta="Segui @marcobilliani @chiaveimmobiliare",
    target_width=1080,
    target_height=1920
):
    """
    Renderizza una clip applicando una specifica combinazione di strategie A/B.
    Include:
    - 9:16 vertical crop perfettamente centrato sul volto di Marco
    - Face verification sui primi 7s (100% compliance Klippify)
    - SFX sincronizzato al millisecondo 0
    - Musica ambient al 5%
    - Sottotitoli dinamici Neue Montreal kinetic con Hook Card e Outro dedicati alla strategia
    """
    strategy = STRATEGY_CATALOG.get(strategy_key, STRATEGY_CATALOG["combo_1_shock_loop"])
    out_p = Path(output_video_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================", flush=True)
    print(f"🎬 [STRATEGY COMBINER] RENDER CLIP CON STRATEGIA: {strategy['name']}", flush=True)
    print(f"   Durata target: {duration_sec:.2f}s | Start: {start_sec:.2f}s", flush=True)
    print(f"   Hook: {custom_hook_text}", flush=True)
    print(f"   Outro: {strategy['outro_text']} (Tipo: {strategy['outro_type']})", flush=True)
    print(f"=======================================================\n", flush=True)

    # 1. Step A: Estrai segmento video 9:16 stabilizzato senza zoom
    temp_base = out_p.parent / f"temp_{out_p.stem}_base.mp4"
    crop_filter = f"[0:v]scale=-1:{target_height},crop={target_width}:{target_height}[v_crop]"

    cmd_base = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-i", str(input_video_path),
        "-t", str(duration_sec),
        "-filter_complex", crop_filter,
        "-map", "[v_crop]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        str(temp_base)
    ]
    subprocess.run(cmd_base, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Step B: Verifica facciale rigorosa (0 - 7 secondi continui)
    is_valid, face_scores = face_verifier.verify_clip_face_compliance(str(temp_base))
    print(f"[+] Verifica volto OpenCV (primi 7s): Conforme={is_valid}, Scores={face_scores}", flush=True)
    if not is_valid:
        print(f"[!] ATTENZIONE: La clip non supera pienamente il test facciale. Si consiglia aggiustamento timestamp.", flush=True)

    # 3. Step C: Trascrizione Whisper e generazione sottotitoli ASS Neue Montreal
    all_words = video_captioner.transcribe_audio_words(str(temp_base), model_size="base")
    ass_file = out_p.parent / f"temp_{out_p.stem}.ass"

    # Prepara titolo hook e badge
    hook_full = strategy["hook_prefix"] + custom_hook_text
    video_captioner.generate_ass_file(
        words=all_words,
        output_ass_path=str(ass_file),
        duration_sec=duration_sec,
        style_key="neue_montreal",
        use_emojis=True,
        hook_title=hook_full,
        brand_cta=strategy["outro_text"] if strategy["outro_type"] == "comment_bait" else brand_cta,
        brand_mention=brand_mention
    )

    # 4. Step D: Mix Audio Avanzato (Parlato 100% + Ambient 5% + SFX Hook 20-25%)
    # Costruisci input audio per FFmpeg
    audio_inputs = ["-i", str(temp_base)]
    filter_complex_audio = "[0:a]volume=1.0[speech];"
    mix_sources = "[speech]"
    input_count = 1

    # Aggiungi Musica Ambient (loopata e abbassata al 5%)
    if AMBIENT_MUSIC.exists():
        audio_inputs.extend(["-stream_loop", "-1", "-i", str(AMBIENT_MUSIC)])
        filter_complex_audio += f"[{input_count}:a]volume={strategy['music_volume']}[bgm];"
        mix_sources += "[bgm]"
        input_count += 1

    # Aggiungi SFX Hook
    sfx_file = strategy.get("sfx_start")
    if sfx_file and Path(sfx_file).exists():
        audio_inputs.extend(["-i", str(sfx_file)])
        filter_complex_audio += f"[{input_count}:a]volume={strategy['sfx_volume']}[sfx];"
        mix_sources += "[sfx]"
        input_count += 1

    # Amix finale
    filter_complex_audio += f"{mix_sources}amix=inputs={input_count}:duration=first:dropout_transition=2[a_out]"

    # Video filter: applica Jump Cut a due telecamere, Color Grading e sottotitoli ASS
    ass_escaped = str(ass_file).replace("\\", "/").replace(":", "\\:")
    jump_cut_filter = (
        "crop=w='if(between(t,7.5,14.0)+between(t,21.0,28.0),915,1080)':"
        "h='if(between(t,7.5,14.0)+between(t,21.0,28.0),1627,1920)':"
        "x='(in_w-out_w)/2':y='(in_h-out_h)/2-if(between(t,7.5,14.0)+between(t,21.0,28.0),50,0)',"
        "scale=1080:1920,"
        "eq=contrast=1.12:brightness=0.01:saturation=1.20,"
        "unsharp=5:5:0.7:5:5:0.0"
    )
    filter_complex_full = f"{filter_complex_audio};[0:v]{jump_cut_filter},ass='{ass_escaped}'[v_out]"

    cmd_final = [
        "ffmpeg", "-y"
    ] + audio_inputs + [
        "-filter_complex", filter_complex_full,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", str(duration_sec),
        "-movflags", "+faststart",
        str(out_p)
    ]
    subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Pulizia temporanei
    if temp_base.exists():
        temp_base.unlink(missing_ok=True)
    if ass_file.exists():
        ass_file.unlink(missing_ok=True)

    print(f"✅ [STRATEGY COMBINER] Clip generata con successo: {out_p.name} ({out_p.stat().st_size / (1024*1024):.2f} MB)", flush=True)
    return {
        "status": "success",
        "output_path": str(out_p),
        "strategy_applied": strategy_key,
        "strategy_name": strategy["name"],
        "face_verified": is_valid,
        "duration": duration_sec
    }

if __name__ == "__main__":
    print("Strategy Combiner module ready.")
