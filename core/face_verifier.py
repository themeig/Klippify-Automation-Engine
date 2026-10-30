import os
import sys
import cv2
import numpy as np
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

_CASCADE = None

def get_cascade():
    global _CASCADE
    if _CASCADE is None:
        casc_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        _CASCADE = cv2.CascadeClassifier(casc_path)
    return _CASCADE

def extract_frame_at_sec(video_path, sec):
    """
    Estrae un fotogramma esatto al secondo specificato usando ffmpeg e cv2.imdecode
    per preservare correttamente l'aspect ratio (16:9 / 9:16) ed evitare distorsioni di buffer.
    """
    cmd = [
        "ffmpeg", "-ss", str(sec),
        "-i", str(video_path),
        "-frames:v", "1",
        "-f", "image2pipe",
        "-vcodec", "mjpeg",
        "pipe:1"
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10)
        raw_bytes = proc.stdout
        if not raw_bytes:
            return None
        np_arr = np.frombuffer(raw_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"[FACE_VERIFIER ERROR] Estrazione frame fallita a {sec}s: {e}")
        return None

def detect_face_in_frame(frame, min_size=(45, 45), active_crop_only=True):
    """
    Rileva se un volto è presente nel frame, considerando l'area 9:16 verticale centrale.
    """
    if frame is None:
        return False
    
    h, w = frame.shape[:2]
    if active_crop_only:
        crop_w = int(h * 9 / 16)
        x1 = max(0, int((w - crop_w) / 2))
        x2 = min(w, x1 + crop_w)
        crop_frame = frame[:, x1:x2]
    else:
        crop_frame = frame
        
    gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
    casc = get_cascade()
    faces = casc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=min_size)
    return len(faces) > 0

def verify_clip_face_compliance(clip_path, sample_seconds=None):
    """
    Verifica se il volto del creator è presente ininterrottamente nei primi 7 secondi (Klippify AI Rule 1).
    Controlla i sample temporali 0.8s, 2.0s, 3.5s, 5.0s, 6.5s.
    """
    vp = Path(clip_path)
    if not vp.exists():
        return False, {"error": "Clip non trovata", "is_compliant": False}

    if sample_seconds is None:
        sample_seconds = [0.8, 2.0, 3.5, 5.0, 6.5]

    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(vp)]
    res = subprocess.run(cmd_dur, capture_output=True, text=True)
    dur = float(res.stdout.strip() or 0)

    detected_at = {}
    for s in sample_seconds:
        frame = extract_frame_at_sec(vp, s)
        has_face = detect_face_in_frame(frame, min_size=(45, 45), active_crop_only=True)
        detected_at[s] = has_face

    face_count = sum(1 for v in detected_at.values() if v)
    continuous_face = detected_at.get(0.8, False) and detected_at.get(2.0, False) and detected_at.get(3.5, False) and (detected_at.get(5.0, False) or detected_at.get(6.5, False))
    is_compliant = continuous_face and (face_count >= 4)

    return is_compliant, {
        "clip_name": vp.name,
        "is_compliant": is_compliant,
        "duration": dur,
        "samples": detected_at,
        "face_detections_count": face_count,
        "total_samples": len(sample_seconds),
        "continuous_face": continuous_face
    }

def scan_source_for_face_segments(source_video_path, target_clips_count=3, clip_duration=38.0):
    """
    Scansiona il video sorgente per individuare segmenti temporali con volto garantito nei primi 7 secondi.
    """
    src_p = Path(source_video_path)
    if not src_p.exists():
        return []

    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(src_p)]
    res = subprocess.run(cmd_dur, capture_output=True, text=True)
    total_dur = float(res.stdout.strip() or 0)
    if total_dur < clip_duration:
        return []

    valid_segments = []
    step = 20.0
    curr_t = 15.0

    while curr_t + clip_duration <= total_dur and len(valid_segments) < target_clips_count:
        f1 = extract_frame_at_sec(src_p, curr_t + 0.8)
        f2 = extract_frame_at_sec(src_p, curr_t + 2.0)
        f3 = extract_frame_at_sec(src_p, curr_t + 3.5)
        f4 = extract_frame_at_sec(src_p, curr_t + 5.0)
        f5 = extract_frame_at_sec(src_p, curr_t + 6.5)

        has_f1 = detect_face_in_frame(f1, min_size=(45, 45), active_crop_only=True)
        has_f2 = detect_face_in_frame(f2, min_size=(45, 45), active_crop_only=True)
        has_f3 = detect_face_in_frame(f3, min_size=(45, 45), active_crop_only=True)
        has_f4 = detect_face_in_frame(f4, min_size=(45, 45), active_crop_only=True)
        has_f5 = detect_face_in_frame(f5, min_size=(45, 45), active_crop_only=True)

        if has_f1 and has_f2 and has_f3 and (has_f4 or has_f5):
            start_m, start_s = divmod(int(curr_t), 60)
            end_sec = curr_t + clip_duration
            end_m, end_s = divmod(int(end_sec), 60)

            valid_segments.append({
                "clip_number": len(valid_segments) + 1,
                "start_time": f"{start_m:02d}:{start_s:02d}",
                "end_time": f"{end_m:02d}:{end_s:02d}",
                "start_sec": curr_t,
                "end_sec": end_sec,
                "concept": f"Segmento verificato - Parte {len(valid_segments) + 1}",
                "hook_text": "Non fare questo errore se vuoi guadagnare! 💡",
                "transcript": "Estratto con volto verificato e continuo del creator (0-7s)"
            })
            curr_t += clip_duration + 30.0
        else:
            curr_t += step

    return valid_segments

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_video = sys.argv[1]
        comp, info = verify_clip_face_compliance(test_video)
        print("Risultato verifica:", comp)
        print("Dettagli:", info)
