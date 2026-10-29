import paths
import subprocess
import os
import re
import shutil
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
    except Exception:
        return 0.0


def slice_and_shift_words_for_segments(source_words: list[dict], segments: list[dict]) -> list[dict]:
    """
    Ricalcola i timestamp parola-per-parola estratti da .json3/.vtt/_inspection.json
    in base ai segmenti multipli tagliati e cuciti dall'Agente AI (0 MB RAM Whisper).
    """
    if not source_words or not segments:
        return []
    shifted = []
    cum_offset = 0.0
    for seg in segments:
        s_sec = parse_time_to_seconds(seg.get("start", 0))
        e_sec = parse_time_to_seconds(seg.get("end", 0))
        seg_dur = max(0.0, e_sec - s_sec)
        if seg_dur <= 0:
            continue
        for w in source_words:
            ws = float(w.get("start", 0))
            we = float(w.get("end", 0))
            if ws >= s_sec - 0.15 and we <= e_sec + 0.25:
                rel_s = max(0.0, ws - s_sec)
                rel_e = min(seg_dur, max(rel_s + 0.08, we - s_sec))
                shifted.append({
                    "word": w.get("word", ""),
                    "start": round(cum_offset + rel_s, 2),
                    "end": round(cum_offset + rel_e, 2),
                    "prob": w.get("prob", 1.0)
                })
        cum_offset += seg_dur
    return shifted


def load_source_words_for_video(input_video_path: Path) -> list[dict]:
    """
    Recupera le parole già estratte in <video_stem>_inspection.json o nei file .json3/.vtt
    accanto al video sorgente o in clipping_sources.
    """
    input_p = Path(input_video_path)
    search_dirs = [input_p.parent]
    for base_cand in [paths.PROJECT_ROOT / "clipping_sources", paths.PROJECT_ROOT.parent / "clipping_sources"]:
        if base_cand.exists():
            search_dirs.extend([d for d in base_cand.iterdir() if d.is_dir()])

    for d in search_dirs:
        insp_f = d / f"{input_p.stem}_inspection.json"
        if insp_f.exists():
            try:
                data = json.loads(insp_f.read_text(encoding="utf-8"))
                if data.get("words"):
                    return data["words"]
            except Exception:
                pass
        try:
            import video_inspector
            for ext in ("*.json3", "*.vtt", "*.srt"):
                subs = list(d.glob(f"{input_p.stem}*{ext[1:]}"))
                if subs:
                    w = video_inspector.parse_subtitle_file(subs[0])
                    if w:
                        return w
        except Exception:
            pass
    return []


def build_crop_filter(
    mode: str = "face_crop",
    center_x_ratio: float = 0.5,
    left_x: float = 0.28,
    right_x: float = 0.72,
    y_start_ratio: float = 0.0,
    height_ratio: float = 1.0,
    target_width: int = 1080,
    target_height: int = 1920,
    input_tag: str = "[0:v]"
) -> tuple[str, str]:
    """
    Costruisce il filtro FFmpeg 9:16 (1080x1920) pilotato dall'Agente AI:
    - 'face_crop' / 'center_crop': ritaglio verticale a tutto schermo centrato su center_x_ratio (0.0..1.0).
      Supporta anche y_start_ratio e height_ratio per ritagliare fuori cornici/sottotitoli pre-esistenti nel video 16:9.
    - 'split_screen': schermo diviso (metà superiore parlante sinistro, metà inferiore parlante destro)
    - 'zoomed_blur' / 'blur_background': sfondo sfocato + video centrale zoomato al 135% (1458px) per evitare l'effetto francobollo
    """
    cx = max(0.0, min(1.0, float(center_x_ratio)))
    ys = max(0.0, min(0.8, float(y_start_ratio)))
    hr = max(0.2, min(1.0 - ys, float(height_ratio)))
    out_tag = "[v_out]"

    if mode in ("face_crop", "center_crop"):
        pre_crop = ""
        if ys > 0.001 or hr < 0.999:
            pre_crop = f"crop=iw:ih*{hr:.3f}:0:ih*{ys:.3f},"
        filter_str = (
            f"{input_tag}{pre_crop}scale=-2:{target_height}:force_original_aspect_ratio=increase,"
            f"crop={target_width}:{target_height}:(iw-{target_width})*{cx:.3f}:(ih-{target_height})/2{out_tag}"
        )
        return filter_str, out_tag

    if mode == "split_screen":
        half_h = target_height // 2
        lx = max(0.0, min(1.0, float(left_x)))
        rx = max(0.0, min(1.0, float(right_x)))
        filter_str = (
            f"{input_tag}split=2[v_top_in][v_bot_in];"
            f"[v_top_in]scale=-2:{half_h}:force_original_aspect_ratio=increase,"
            f"crop={target_width}:{half_h}:(iw-{target_width})*{lx:.3f}:(ih-{half_h})/2[v_top];"
            f"[v_bot_in]scale=-2:{half_h}:force_original_aspect_ratio=increase,"
            f"crop={target_width}:{half_h}:(iw-{target_width})*{rx:.3f}:(ih-{half_h})/2[v_bot];"
            f"[v_top][v_bot]vstack=inputs=2{out_tag}"
        )
        return filter_str, out_tag

    # Default: zoomed_blur (135% zoom on foreground = 1458px scaled width cropped to 1080px)
    zoom_w = int(round(target_width * 1.35))  # 1458 for 1080
    filter_str = (
        f"{input_tag}split=2[v_bg_in][v_fg_in];"
        f"[v_bg_in]scale={target_width}:{target_height}:force_original_aspect_ratio=increase,"
        f"crop={target_width}:{target_height},boxblur=24:6[bg];"
        f"[v_fg_in]scale={zoom_w}:-2,crop={target_width}:ih:(iw-{target_width})*{cx:.3f}:0[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2{out_tag}"
    )
    return filter_str, out_tag


def build_multisegment_ffmpeg_cmd(
    input_video_path: Path,
    segments: list[dict],
    output_video_path: Path,
    mode: str = "face_crop",
    center_x_ratio: float = 0.5,
    y_start_ratio: float = 0.0,
    height_ratio: float = 1.0,
    logo_path: str = None,
    target_width: int = 1080,
    target_height: int = 1920
) -> list[str]:
    """
    Costruisce il comando FFmpeg che taglia e cuce (concat) i segmenti scelti dall'Agente AI
    (es. Teaser + Corpo 1 + Corpo 2 saltando le parti noiose) e li formatta in 9:16.
    """
    input_p = Path(input_video_path)
    output_p = Path(output_video_path)

    valid_segments = []
    for seg in (segments or []):
        s_sec = parse_time_to_seconds(seg.get("start", 0))
        e_sec = parse_time_to_seconds(seg.get("end", 0))
        if e_sec > s_sec + 0.2:
            valid_segments.append((s_sec, e_sec))

    if not valid_segments:
        valid_segments = [(0.0, 30.0)]

    n_segs = len(valid_segments)
    trim_parts = []
    concat_inputs = []

    for idx, (s_sec, e_sec) in enumerate(valid_segments):
        trim_parts.append(
            f"[0:v]trim=start={s_sec:.2f}:end={e_sec:.2f},setpts=PTS-STARTPTS[v{idx}];"
            f"[0:a]atrim=start={s_sec:.2f}:end={e_sec:.2f},asetpts=PTS-STARTPTS[a{idx}]"
        )
        concat_inputs.append(f"[v{idx}][a{idx}]")

    concat_filter = ";".join(trim_parts) + f";{''.join(concat_inputs)}concat=n={n_segs}:v=1:a=1[v_cat][a_cat]"
    crop_filter, last_v_tag = build_crop_filter(
        mode=mode,
        center_x_ratio=center_x_ratio,
        y_start_ratio=y_start_ratio,
        height_ratio=height_ratio,
        target_width=target_width,
        target_height=target_height,
        input_tag="[v_cat]"
    )

    filter_complex = f"{concat_filter};{crop_filter}"

    extra_inputs = []
    if logo_path and Path(logo_path).exists():
        extra_inputs = ["-i", str(logo_path)]
        filter_complex += f";[1:v]scale=180:-1[logo];{last_v_tag}[logo]overlay=W-w-40:60[final_v]"
        last_v_tag = "[final_v]"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_p),
    ] + extra_inputs + [
        "-filter_complex", filter_complex,
        "-map", last_v_tag,
        "-map", "[a_cat]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_p)
    ]
    return cmd


def process_clip_ffmpeg(
    input_video_path,
    start_time=None,
    end_time=None,
    output_video_path=None,
    mode="face_crop",
    center_x_ratio=0.5,
    y_start_ratio=0.0,
    height_ratio=1.0,
    segments=None,
    logo_path=None,
    hook_text=None,
    cta_text=None,
    brand_mention=None,
    target_width=1080,
    target_height=1920,
    logger=None
):
    """
    Esegue il montaggio della clip 9:16 (1080x1920) seguendo le istruzioni dell'Agente AI:
    - Supporta sia `segments` multipli (Taglia & Cuci + Cold-Open Teaser) sia `start_time`/`end_time` singoli.
    - Applica Smart Crop 9:16, Hook Card temporanea (3.2s), sottotitoli dinamici e CTA specifica della campagna.
    """
    input_p = Path(input_video_path)
    output_p = Path(output_video_path)
    output_p.parent.mkdir(parents=True, exist_ok=True)

    if segments and isinstance(segments, list) and len(segments) > 0:
        seg_list = segments
    else:
        s_sec = parse_time_to_seconds(start_time or 0)
        e_sec = parse_time_to_seconds(end_time or (s_sec + 35))
        seg_list = [{"start": s_sec, "end": e_sec, "role": "body"}]

    total_dur = sum(
        max(0.0, parse_time_to_seconds(s.get("end", 0)) - parse_time_to_seconds(s.get("start", 0)))
        for s in seg_list
    )

    msg_start = f"✂️ [FFMPEG-AI] Montaggio {len(seg_list)} segmenti per {input_p.name} (Durata totale: {total_dur:.1f}s, Mode: {mode}, X: {center_x_ratio})"
    print(f"[+] {msg_start}")
    if logger:
        logger(msg_start)

    if len(seg_list) == 1:
        s_sec = parse_time_to_seconds(seg_list[0].get("start", 0))
        e_sec = parse_time_to_seconds(seg_list[0].get("end", s_sec + 30))
        duration = max(e_sec - s_sec, 1.0)
        crop_filter, last_v_tag = build_crop_filter(
            mode=mode,
            center_x_ratio=center_x_ratio,
            y_start_ratio=y_start_ratio,
            height_ratio=height_ratio,
            target_width=target_width,
            target_height=target_height,
            input_tag="[0:v]"
        )
        extra_inputs = []
        if logo_path and Path(logo_path).exists():
            extra_inputs = ["-i", str(logo_path)]
            crop_filter += f";[1:v]scale=180:-1[logo];{last_v_tag}[logo]overlay=W-w-40:60[final_v]"
            last_v_tag = "[final_v]"

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(s_sec),
            "-i", str(input_p),
        ] + extra_inputs + [
            "-t", str(duration),
            "-filter_complex", crop_filter,
            "-map", last_v_tag,
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            str(output_p)
        ]
    else:
        cmd = build_multisegment_ffmpeg_cmd(
            input_video_path=input_p,
            segments=seg_list,
            output_video_path=output_p,
            mode=mode,
            center_x_ratio=center_x_ratio,
            y_start_ratio=y_start_ratio,
            height_ratio=height_ratio,
            logo_path=logo_path,
            target_width=target_width,
            target_height=target_height
        )

    if logger:
        logger("⚙️ [FFMPEG] Rendering 9:16 in corso...")

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
        if res.returncode == 0 and output_p.exists():
            temp_raw = output_p.parent / f"raw_cut_{output_p.name}"
            try:
                import video_captioner
                if logger:
                    logger("💬 [CAPTIONER] Applicazione sottotitoli animati, Hook (3.2s) e CTA dinamica...")
                if output_p.exists():
                    source_words = load_source_words_for_video(input_p)
                    shifted_words = slice_and_shift_words_for_segments(source_words, seg_list) if source_words else None
                    shutil.move(str(output_p), str(temp_raw))
                    video_captioner.burn_captions_to_video(
                        temp_raw,
                        output_video=output_p,
                        style_key="hormozi_gold",
                        custom_hook=hook_text,
                        brand_cta=cta_text,
                        brand_mention=brand_mention,
                        precomputed_words=shifted_words
                    )
            except Exception as cap_err:
                print(f"[CAPTIONER WARNING] Impossibile applicare sottotitoli: {cap_err}")
            finally:
                if not output_p.exists() and temp_raw.exists():
                    shutil.move(str(temp_raw), str(output_p))
                elif temp_raw.exists():
                    temp_raw.unlink()

            fsize_mb = output_p.stat().st_size / (1024 * 1024)
            msg_ok = f"✅ [FFMPEG] Clip esportata: {output_p.name} ({fsize_mb:.2f} MB)"
            print(f"[SUCCESS] {msg_ok}")
            if logger:
                logger(msg_ok)
            return True
        else:
            err_snip = res.stderr[-300:] if res.stderr else "Errore sconosciuto"
            msg_err = f"❌ [FFMPEG] Errore di rendering: {err_snip}"
            print(f"[-] {msg_err}")
            if logger:
                logger(msg_err)
            return False
    except Exception as e:
        msg_exc = f"❌ [FFMPEG] Eccezione: {e}"
        print(f"[-] {msg_exc}")
        if logger:
            logger(msg_exc)
        return False


def split_long_video_if_needed(input_video_path, max_duration_seconds=900, chunk_duration=600):
    input_p = Path(input_video_path)
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
