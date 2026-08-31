import paths
import subprocess
import os
import re
from pathlib import Path

def parse_time_to_seconds(t_str):
    """Converte 'MM:SS' o 'HH:MM:SS' o float/int in secondi."""
    if isinstance(t_str, (int, float)):
        return float(t_str)
    t_str = str(t_str).strip()
    parts = t_str.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    try:
        return float(t_str)
    except:
        return 0.0

def process_clip_ffmpeg(
    input_video_path,
    start_time,
    end_time,
    output_video_path,
    mode="blur_background",  # 'blur_background' o 'center_crop'
    logo_path=None,
    hook_text=None,
    cta_text=None,
    target_width=1080,
    target_height=1920,
    logger=None
):
    """
    Taglia un segmento del video e lo converte in formato verticale 9:16 (1080x1920) per TikTok,
    applicando sfondo sfocato, overlay hook nei primi secondi e CTA obbligatoria Klippify.
    """
    input_p = Path(input_video_path)
    output_p = Path(output_video_path)
    output_p.parent.mkdir(parents=True, exist_ok=True)
    
    start_sec = parse_time_to_seconds(start_time)
    end_sec = parse_time_to_seconds(end_time)
    duration = max(end_sec - start_sec, 1.0)
    
    msg_start = f"✂️ [FFMPEG] Elaborazione clip: {input_p.name} | Da {start_sec:.1f}s a {end_sec:.1f}s (Durata: {duration:.1f}s, 9:16 1080x1920)"
    print(f"[+] {msg_start}")
    if logger: logger(msg_start)
    
    # Costruisci il filtro video FFmpeg per 9:16
    if mode == "blur_background":
        # Sfondo sfocato + video originale centrato e nitido
        filter_complex = (
            f"[0:v]scale={target_width}:{target_height}:force_original_aspect_ratio=increase,crop={target_width}:{target_height},boxblur=20:5[bg];"
            f"[0:v]scale={target_width}:-1:force_original_aspect_ratio=decrease[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2[v_out]"
        )
    else:
        # Center crop classico
        filter_complex = f"[0:v]scale=-1:{target_height},crop={target_width}:{target_height}[v_out]"
        
    last_v_tag = "[v_out]"
    
    # Se presente un logo, aggiungilo in overlay (angolo in alto a destra)
    extra_inputs = []
    if logo_path and Path(logo_path).exists():
        extra_inputs = ["-i", str(logo_path)]
        filter_complex += f";[1:v]scale=180:-1[logo];{last_v_tag}[logo]overlay=W-w-40:60[final_v]"
        last_v_tag = "[final_v]"

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-i", str(input_p),
    ] + extra_inputs + [
        "-t", str(duration),
        "-filter_complex", filter_complex,
        "-map", last_v_tag,
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_p)
    ]
    
    if logger: logger(f"⚙️ [FFMPEG] Taglio video 9:16 verticale in corso...")
    
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
        if res.returncode == 0 and output_p.exists():
            # Applica i sottotitoli virali TikTok e la Hook Card con video_captioner
            try:
                import video_captioner
                if logger: logger(f"💬 [CAPTIONER] Applicazione sottotitoli animati e Hook Card Sticker...")
                temp_raw = output_p.parent / f"raw_cut_{output_p.name}"
                if output_p.exists():
                    import shutil
                    shutil.move(output_p, temp_raw)
                    cap_res = video_captioner.burn_captions_to_video(
                        temp_raw,
                        output_video=output_p,
                        style_key="hormozi_gold",
                        custom_hook=hook_text
                    )
                    if temp_raw.exists():
                        temp_raw.unlink()
            except Exception as cap_err:
                print(f"[CAPTIONER WARNING] Impossibile applicare sottotitoli: {cap_err}")

            fsize_mb = output_p.stat().st_size / (1024 * 1024)
            msg_ok = f"✅ [FFMPEG] Clip con sottotitoli esportata: {output_p.name} ({fsize_mb:.2f} MB)"
            print(f"[SUCCESS] {msg_ok}")
            if logger: logger(msg_ok)
            return True
        else:
            err_snip = res.stderr[-300:] if res.stderr else "Errore sconosciuto"
            msg_err = f"❌ [FFMPEG] Errore di rendering: {err_snip}"
            print(f"[-] {msg_err}")
            if logger: logger(msg_err)
            return False
    except Exception as e:
        msg_exc = f"❌ [FFMPEG] Eccezione: {e}"
        print(f"[-] {msg_exc}")
        if logger: logger(msg_exc)
        return False

def split_long_video_if_needed(input_video_path, max_duration_seconds=900, chunk_duration=600):
    """
    Se un video supera max_duration_seconds (es. 15 minuti),
    lo suddivide in parti da chunk_duration (es. 10 minuti) in /temp_chunks/.
    """
    input_p = Path(input_video_path)
    
    # Calcola la durata con ffprobe
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(input_p)
    ]
    try:
        out = subprocess.check_output(probe_cmd, text=True).strip()
        total_duration = float(out)
    except Exception as e:
        print(f"[!] Impossibile determinare la durata: {e}")
        return [str(input_p)]
        
    if total_duration <= max_duration_seconds:
        return [str(input_p)]
        
    print(f"[+] Video lungo rilevato ({total_duration/60:.1f} min). Suddivisione in parti da {chunk_duration/60:.1f} min...")
    chunks_dir = input_p.parent / "chunks"
    chunks_dir.mkdir(exist_ok=True)
    
    chunk_paths = []
    chunk_idx = 1
    current_start = 0
    
    while current_start < total_duration:
        chunk_out = chunks_dir / f"{input_p.stem}_part{chunk_idx}.mp4"
        split_cmd = [
            "ffmpeg", "-y",
            "-ss", str(current_start),
            "-i", str(input_p),
            "-t", str(chunk_duration),
            "-c", "copy",
            str(chunk_out)
        ]
        subprocess.run(split_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if chunk_out.exists():
            chunk_paths.append(str(chunk_out))
            print(f"   Part {chunk_idx}: {chunk_out.name} ({current_start/60:.1f}m - {(current_start+chunk_duration)/60:.1f}m)")
        chunk_idx += 1
        current_start += chunk_duration
        
    return chunk_paths