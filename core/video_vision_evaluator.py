import os
import sys
import cv2
import numpy as np
import subprocess
from pathlib import Path

# UTF-8 support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))

import face_verifier

def evaluate_segment_visual_energy(video_path, start_sec, duration_sec=38.0, sample_interval=1.0):
    """
    Analizza la 'Vision' del segmento video per determinare l'energia visiva del creator:
    1. Espressività e movimento gestuale (Frame differencing / Optical Motion)
    2. Luminosità e contrasto del volto (evita scene buie o piatte)
    3. Stabilità e centratura dello sguardo (Eye Contact)
    Restituisce un punteggio da 0 a 100 e le metriche dettagliate.
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return 0.0, {"error": "Video non apribile"}

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    start_frame = int(start_sec * fps)
    end_frame = int((start_sec + duration_sec) * fps)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if start_frame >= total_frames:
        cap.release()
        return 0.0, {"error": "Timestamp oltre la durata"}

    motion_scores = []
    contrast_scores = []
    brightness_scores = []
    face_presence_count = 0
    total_sampled = 0

    prev_gray = None
    step_frames = int(fps * sample_interval)

    for f_idx in range(start_frame, min(end_frame, total_frames), step_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
        ret, frame = cap.read()
        if not ret or frame is None:
            continue

        h, w = frame.shape[:2]
        crop_w = int(h * 9 / 16)
        x1 = max(0, int((w - crop_w) / 2))
        x2 = min(w, x1 + crop_w)
        crop_frame = frame[:, x1:x2]

        gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
        total_sampled += 1

        casc = face_verifier.get_cascade()
        faces = casc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(45, 45))
        if len(faces) > 0:
            face_presence_count += 1
            fx, fy, fw, fh = faces[0]
            face_roi = gray[fy:fy+fh, fx:fx+fw]
            brightness_scores.append(float(np.mean(face_roi)))
            contrast_scores.append(float(np.std(face_roi)))

        if prev_gray is not None:
            diff = cv2.absdiff(gray, prev_gray)
            motion_val = float(np.mean(diff))
            motion_scores.append(motion_val)
        prev_gray = gray

    cap.release()

    if total_sampled == 0:
        return 0.0, {"error": "Nessun frame campionato"}

    face_ratio = face_presence_count / total_sampled
    avg_motion = float(np.mean(motion_scores)) if motion_scores else 0.0
    avg_contrast = float(np.mean(contrast_scores)) if contrast_scores else 0.0
    avg_brightness = float(np.mean(brightness_scores)) if brightness_scores else 0.0

    norm_face = min(1.0, face_ratio / 0.85) * 40.0
    norm_motion = min(1.0, max(0.0, (avg_motion - 1.5) / 10.0)) * 35.0
    norm_contrast = min(1.0, max(0.0, (avg_contrast - 20.0) / 35.0)) * 25.0

    total_score = round(norm_face + norm_motion + norm_contrast, 1)

    return total_score, {
        "visual_score": total_score,
        "face_presence_ratio": round(face_ratio, 2),
        "motion_energy": round(avg_motion, 2),
        "face_contrast": round(avg_contrast, 1),
        "face_brightness": round(avg_brightness, 1),
        "is_visually_engaging": (total_score >= 60.0)
    }

def find_most_engaging_segments(video_path, clip_duration=38.0, step_sec=15.0, top_k=3):
    """
    Scansiona l'intero video sorgente e ordina i segmenti temporali
    dal più espressivo ed energico a quello più piatto, garantendo conformità Klippify.
    """
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    total_sec = total_frames / fps
    cap.release()

    candidates = []
    curr = 10.0

    print(f"\n🔍 [VIDEO VISION] Scansione visiva intelligente di: {Path(video_path).name} ({total_sec:.1f}s)", flush=True)

    while curr + clip_duration <= total_sec - 5.0:
        score, details = evaluate_segment_visual_energy(video_path, curr, clip_duration)
        if details.get("face_presence_ratio", 0) >= 0.70:
            candidates.append({
                "start_sec": curr,
                "end_sec": curr + clip_duration,
                "score": score,
                "details": details
            })
        curr += step_sec

    candidates.sort(key=lambda x: x["score"], reverse=True)
    best = candidates[:top_k]

    print(f"[+] Trovati {len(candidates)} segmenti validi. Top {len(best)} per energia visiva:")
    for idx, c in enumerate(best, 1):
        print(f"   {idx}. Da {c['start_sec']:.1f}s a {c['end_sec']:.1f}s | Score: {c['score']}/100 (Motion: {c['details']['motion_energy']}, Face: {c['details']['face_presence_ratio']*100:.0f}%)")

    return best

if __name__ == "__main__":
    print("Video Vision Evaluator module ready.")
