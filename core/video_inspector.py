import paths
import json
import os
import re
import sys
import subprocess
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def format_mmss(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins:02d}:{secs:05.2f}"


def _parse_vtt_time(t_str: str) -> float:
    t_str = t_str.strip().replace(",", ".")
    parts = t_str.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    return float(parts[0])


def parse_subtitle_file(sub_path: Path) -> list[dict]:
    """
    Parsa un file di sottotitoli (.json3, .vtt, .srt) ed estrae la lista di parole
    con timestamp precisi [{"word": str, "start": float, "end": float, "prob": float}].
    """
    p = Path(sub_path)
    if not p.exists():
        return []

    raw_text = p.read_text(encoding="utf-8", errors="ignore")
    suffix = p.suffix.lower()

    if suffix == ".json3" or raw_text.lstrip().startswith("{"):
        try:
            data = json.loads(raw_text)
        except Exception:
            return []

        words = []
        events = data.get("events", [])
        for ev in events:
            segs = ev.get("segs")
            if not segs:
                continue
            ev_start_ms = float(ev.get("tStartMs", 0))
            ev_dur_ms = float(ev.get("dDurationMs", 1500))
            ev_end_ms = ev_start_ms + ev_dur_ms

            parsed_segs = []
            for seg in segs:
                txt = seg.get("utf8", "")
                txt_clean = re.sub(r"\s+", " ", txt).strip()
                if not txt_clean or txt_clean in ("[Musica]", "[Music]", "[Applausi]"):
                    continue
                offset_ms = float(seg.get("tOffsetMs", 0))
                parsed_segs.append((ev_start_ms + offset_ms, txt_clean))

            for idx, (seg_start_ms, txt_clean) in enumerate(parsed_segs):
                next_ms = parsed_segs[idx + 1][0] if idx + 1 < len(parsed_segs) else ev_end_ms
                seg_dur_ms = max(120.0, next_ms - seg_start_ms)
                tokens = [t for t in txt_clean.split(" ") if t]
                if not tokens:
                    continue
                tok_dur_ms = seg_dur_ms / len(tokens)
                for t_idx, tok in enumerate(tokens):
                    w_start = round((seg_start_ms + t_idx * tok_dur_ms) / 1000.0, 2)
                    w_end = round((seg_start_ms + (t_idx + 1) * tok_dur_ms) / 1000.0, 2)
                    if w_end <= w_start:
                        w_end = round(w_start + 0.12, 2)
                    words.append({
                        "word": tok,
                        "start": w_start,
                        "end": w_end,
                        "prob": 1.0
                    })
        return words

    # VTT / SRT parser
    words = []
    cue_pattern = re.compile(
        r"(\d{1,2}:\d{2}:\d{2}[\.,]\d{1,3}|\d{2}:\d{2}[\.,]\d{1,3})\s*-->\s*(\d{1,2}:\d{2}:\d{2}[\.,]\d{1,3}|\d{2}:\d{2}[\.,]\d{1,3})[^\n]*\n(.*?)(?=\n\n|\Z)",
        re.DOTALL
    )
    for match in cue_pattern.finditer(raw_text):
        c_start = _parse_vtt_time(match.group(1))
        c_end = _parse_vtt_time(match.group(2))
        if c_end <= c_start:
            c_end = c_start + 1.0
        body = match.group(3)
        # Strip HTML/VTT inline tags like <c>, <00:00:01.000>
        body_clean = re.sub(r"<[^>]+>", " ", body)
        body_clean = re.sub(r"\s+", " ", body_clean).strip()
        if not body_clean:
            continue
        tokens = [t for t in body_clean.split(" ") if t]
        if not tokens:
            continue
        dur = max(0.2, c_end - c_start)
        step = dur / len(tokens)
        for i, tok in enumerate(tokens):
            w_start = round(c_start + i * step, 2)
            w_end = round(c_start + (i + 1) * step, 2)
            if w_end <= w_start:
                w_end = round(w_start + 0.1, 2)
            words.append({
                "word": tok,
                "start": w_start,
                "end": w_end,
                "prob": 1.0
            })
    return words


def group_words_into_timed_lines(words: list[dict], pause_sec: float = 0.4) -> list[dict]:
    """
    Raggruppa la lista di parole in frasi leggibili con timestamp di inizio e fine
    per l'ispezione da parte dell'Agente AI di Antigravity.
    """
    if not words:
        return []

    lines = []
    curr = []

    for idx, w in enumerate(words):
        curr.append(w)
        word_str = str(w.get("word", ""))
        ends_punct = word_str.endswith((".", "!", "?"))
        has_pause = False
        if idx + 1 < len(words):
            gap = float(words[idx + 1]["start"]) - float(w["end"])
            if gap >= pause_sec:
                has_pause = True

        if ends_punct or has_pause or len(curr) >= 16:
            s_t = float(curr[0]["start"])
            e_t = float(curr[-1]["end"])
            text_str = " ".join(x["word"] for x in curr).strip()
            if text_str:
                lines.append({
                    "start": round(s_t, 2),
                    "end": round(e_t, 2),
                    "start_str": format_mmss(s_t),
                    "end_str": format_mmss(e_t),
                    "text": text_str
                })
            curr = []

    if curr:
        s_t = float(curr[0]["start"])
        e_t = float(curr[-1]["end"])
        text_str = " ".join(x["word"] for x in curr).strip()
        if text_str:
            lines.append({
                "start": round(s_t, 2),
                "end": round(e_t, 2),
                "start_str": format_mmss(s_t),
                "end_str": format_mmss(e_t),
                "text": text_str
            })

    return lines


def get_video_duration_sec(video_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        return float(res.stdout.strip())
    except Exception:
        return 60.0


def detect_face_crop_suggestion(frame_paths: list[str]) -> dict:
    """
    Se OpenCV è disponibile, ispeziona i frame estratti per suggerire all'Agente AI
    la posizione orizzontale del volto (center_x_ratio in 0.0..1.0) e la modalità.
    """
    try:
        import cv2
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(cascade_path)
        x_centers = []
        two_face_frames = 0

        for fp in frame_paths:
            if not Path(fp).exists():
                continue
            img = cv2.imread(str(fp))
            if img is None:
                continue
            h, w = img.shape[:2]
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(30, 30))
            if len(faces) == 1:
                fx, fy, fw, fh = faces[0]
                x_centers.append((fx + fw / 2.0) / float(w))
            elif len(faces) >= 2:
                sorted_f = sorted(faces, key=lambda b: b[0])
                c1 = (sorted_f[0][0] + sorted_f[0][2] / 2.0) / float(w)
                c2 = (sorted_f[-1][0] + sorted_f[-1][2] / 2.0) / float(w)
                if abs(c2 - c1) >= 0.30:
                    two_face_frames += 1
                else:
                    x_centers.append((c1 + c2) / 2.0)

        if two_face_frames >= 2 and two_face_frames >= len(x_centers):
            return {"suggested_mode": "split_screen", "center_x_ratio": 0.5}
        if x_centers:
            x_centers.sort()
            med = round(x_centers[len(x_centers) // 2], 3)
            return {"suggested_mode": "face_crop", "center_x_ratio": med}
    except Exception:
        pass

    return {"suggested_mode": "zoomed_blur", "center_x_ratio": 0.5}


def generate_storyboards(video_path: Path, output_dir: Path, interval_sec: int = 15) -> tuple[list[str], list[str]]:
    """
    Estrae sia una griglia Storyboard JPG (4x3 tile) sia 6 fotogrammi chiave singoli
    affinché l'Agente AI di Antigravity possa guardare il video con `read_file`.
    """
    video_p = Path(video_path)
    out_d = Path(output_dir)
    out_d.mkdir(parents=True, exist_ok=True)

    duration = get_video_duration_sec(video_p)
    step = max(3.0, duration / 7.0)
    sample_frames = []

    for i in range(1, 7):
        t_sec = round(min(duration - 0.5, i * step), 1)
        if t_sec < 0:
            t_sec = 0.0
        frame_out = out_d / f"{video_p.stem}_frame_{i}_{int(t_sec)}s.jpg"
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(t_sec),
            "-i", str(video_p),
            "-vframes", "1",
            "-vf", "scale=640:-1",
            "-q:v", "4",
            str(frame_out)
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
            if frame_out.exists():
                sample_frames.append(str(frame_out))
        except Exception:
            pass

    storyboard_out = out_d / f"{video_p.stem}_storyboard.jpg"
    fps_interval = max(2, int(duration / 12)) if duration > 24 else 2
    sb_cmd = [
        "ffmpeg", "-y",
        "-i", str(video_p),
        "-vf", f"fps=1/{fps_interval},scale=320:180,tile=4x3",
        "-frames:v", "1",
        "-q:v", "4",
        str(storyboard_out)
    ]
    storyboards = []
    try:
        subprocess.run(sb_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        if storyboard_out.exists():
            storyboards.append(str(storyboard_out))
    except Exception:
        pass

    return storyboards, sample_frames


def inspect_video(video_path: Path, campaign_id: str = "general") -> dict:
    """
    Prepara il pacchetto completo di ispezione (<video_stem>_inspection.json + Storyboard JPG)
    affinché l'Agente AI di Antigravity possa leggere ogni frase coi timestamp, guardare i frame
    e decidere esattamente quali segmenti tenere e quali scartare.
    """
    video_p = Path(video_path).resolve()
    if not video_p.exists():
        return {"status": "error", "message": f"Video non trovato: {video_p}"}

    inspection_file = video_p.parent / f"{video_p.stem}_inspection.json"
    if inspection_file.exists():
        try:
            cached = json.loads(inspection_file.read_text(encoding="utf-8"))
            if cached.get("timed_lines"):
                return cached
        except Exception:
            pass

    # 1. Cerca sottotitoli nativi (.json3 / .vtt / .srt) scaricati da yt-dlp
    words = []
    for ext in ("*.json3", "*.vtt", "*.srt"):
        sub_cands = list(video_p.parent.glob(f"{video_p.stem}*{ext[1:]}"))
        if sub_cands:
            words = parse_subtitle_file(sub_cands[0])
            if words:
                break

    # 2. Se non ci sono sottotitoli scaricati, trascrivi con Faster-Whisper (int8)
    if not words:
        try:
            import video_captioner
            words = video_captioner.transcribe_audio_words(video_p, model_size="base")
        except Exception as e:
            print(f"[VIDEO-INSPECTOR] Avviso trascrizione: {e}")
            words = []

    timed_lines = group_words_into_timed_lines(words, pause_sec=0.4)
    duration_sec = get_video_duration_sec(video_p)

    frames_dir = video_p.parent / f"{video_p.stem}_frames"
    storyboards, sample_frames = generate_storyboards(video_p, frames_dir)
    crop_suggestion = detect_face_crop_suggestion(sample_frames)

    inspection_data = {
        "status": "ready_for_ai_director",
        "campaign_id": str(campaign_id),
        "video_file": str(video_p),
        "video_name": video_p.name,
        "duration_sec": round(duration_sec, 2),
        "inspection_file": str(inspection_file),
        "storyboards": storyboards,
        "sample_frames": sample_frames,
        "crop_suggestion": crop_suggestion,
        "words_count": len(words),
        "timed_lines": timed_lines,
        "words": words,
        "inspected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    inspection_file.write_text(json.dumps(inspection_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[VIDEO-INSPECTOR] Pacchetto ispezione AI pronto: {inspection_file} ({len(timed_lines)} righe timestampate)")
    return inspection_data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        v_path = Path(sys.argv[1])
        c_id = sys.argv[2] if len(sys.argv) > 2 else "general"
        res = inspect_video(v_path, campaign_id=c_id)
        summary = {k: v for k, v in res.items() if k != "words"}
        print(json.dumps(summary, indent=2, ensure_ascii=False))
