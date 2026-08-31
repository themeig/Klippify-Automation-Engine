import paths
import os
import sys
import re
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = paths.PROJECT_ROOT

EMOJI_KEYWORDS = {
    r"\b(euro|€|soldi|guadagn|fatturat|sold)\w*": "💰",
    r"\b(negozi|shop|store|ecommerce|e-commerce)\w*": "🛒",
    r"\b(zero|inizi|partit|primo|prima)\w*": "🎯",
    r"\b(mesi|mese|giorn|tempo|ann|settiman)\w*": "⏳",
    r"\b(esperienza|risultat|crescit|scal)\w*": "🚀",
    r"\b(metodo|strategi|segret|chiav)\w*": "🔑",
    r"\b(lavor|online|digital|computer)\w*": "💻",
    r"\b(fuoco|viral|incredibil|pazzesc|top)\w*": "🔥",
    r"\b(libert|vit|cambiat|svolt)\w*": "✨"
}

STYLES = {
    "hormozi_gold": {
        "name": "Hormozi Gold",
        "font": "Impact",
        "fontsize": 52,
        "primary_color": "&H00FFFFFF",
        "active_color": "&H0000E6FF",
        "outline_color": "&H00000000",
        "outline_width": 4.2,
        "shadow_width": 2.0,
        "pos_y": 1420
    },
    "viral_emerald": {
        "name": "Viral Emerald",
        "font": "Impact",
        "fontsize": 52,
        "primary_color": "&H00FFFFFF",
        "active_color": "&H0033FF00",
        "outline_color": "&H00000000",
        "outline_width": 4.2,
        "shadow_width": 2.0,
        "pos_y": 1420
    },
    "cyber_cyan": {
        "name": "Cyber Cyan",
        "font": "Impact",
        "fontsize": 52,
        "primary_color": "&H00FFFFFF",
        "active_color": "&H00FFFF00",
        "outline_color": "&H00000000",
        "outline_width": 4.2,
        "shadow_width": 2.0,
        "pos_y": 1420
    }
}

def format_ass_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centisecs = int(round((seconds - int(seconds)) * 100))
    if centisecs >= 100:
        centisecs = 99
    return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

def get_video_duration(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(res.stdout.strip())
    except Exception:
        return 35.0

def transcribe_audio_words(video_path, model_size="base"):
    from faster_whisper import WhisperModel

    print(f"[CAPTIONER] Caricamento Faster-Whisper ({model_size})...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"[CAPTIONER] Trascrizione audio per: '{Path(video_path).name}'...")
    start_t = time.time()
    segments, info = model.transcribe(
        str(video_path),
        language="it",
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=250)
    )

    all_words = []
    for segment in segments:
        if segment.words:
            for w in segment.words:
                word_clean = w.word.strip()
                if not word_clean:
                    continue
                all_words.append({
                    "word": word_clean,
                    "start": w.start,
                    "end": w.end,
                    "prob": getattr(w, "probability", 1.0)
                })

    elapsed = round(time.time() - start_t, 2)
    print(f"[CAPTIONER] Trascrizione completata in {elapsed}s: {len(all_words)} parole.")
    return all_words

def inject_emoji(word):
    w_clean = re.sub(r"[^\w€]", "", word.lower())
    for pattern, emoji in EMOJI_KEYWORDS.items():
        if re.search(pattern, w_clean):
            return f"{word} {emoji}"
    return word

def format_hook_card(hook_title, style_active_color="&H0000E6FF", persistent=True):
    clean = hook_title.upper().strip() if hook_title else "LEZIONE GRATUITA SUL PROFILO DI SARA"
    
    if "LEZIONE" in clean or "SITO" in clean or "PROFILO" in clean or "SARA" in clean:
        end_time = "1:00:00.00" if persistent else "0:00:05.00"
        badge_event = rf"Dialogue: 2,0:00:00.00,{end_time},HookBadge,,0,0,0,,{{\an5\pos(540,290)\fad(200,0)}}🎓 LEZIONE GRATUITA"
        card_event = rf"Dialogue: 1,0:00:00.00,{end_time},HookCardBox,,0,0,0,,{{\an5\pos(540,360)\fad(200,0)}}🔗 SUL PROFILO DI SARA"
        return [badge_event, card_event]
    
    words = clean.split()
    highlighted_words = []
    for w in words:
        if any(kw in w for kw in ["3000", "6000", "10.000", "20.000", "1.277", "EURO", "€", "RECORD", "METODO", "ONLINE", "GRATIS", "GRATUITA"]):
            highlighted_words.append(r"{\c" + style_active_color + r"}" + w + r"{\c&H00FFFFFF&}")
        else:
            highlighted_words.append(w)
    
    title_formatted = " ".join(highlighted_words)
    end_time = "1:00:00.00" if persistent else "0:00:05.00"

    badge_event = rf"Dialogue: 2,0:00:00.00,{end_time},HookBadge,,0,0,0,,{{\an5\pos(540,290)\fad(200,0)}}🔴 STORIA REALE"
    card_event = rf"Dialogue: 1,0:00:00.00,{end_time},HookCardBox,,0,0,0,,{{\an5\pos(540,360)\fad(200,0)}}" + title_formatted

    return [badge_event, card_event]

def generate_ass_file(words, output_ass_path, duration_sec=35.0, style_key="hormozi_gold", use_emojis=True, hook_title=None, brand_cta=None):
    style = STYLES.get(style_key, STYLES["hormozi_gold"])
    pos_y = style["pos_y"]

    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTokSub,{style['font']},{style['fontsize']},{style['primary_color']},&H000000FF,{style['outline_color']},{style['outline_color']},-1,0,0,0,100,100,2,0,1,{style['outline_width']},{style['shadow_width']},5,40,40,40,1
Style: HookBadge,Arial Black,24,&H00000000,&H000000FF,{style['active_color']},{style['active_color']},-1,0,0,0,100,100,2,0,3,6.0,0.0,5,30,30,30,1
Style: HookCardBox,{style['font']},44,&H00FFFFFF,&H000000FF,&H00000000,&HB0000000,-1,0,0,0,100,100,1,0,3,10.0,3.0,5,30,30,30,1
Style: OutroBadge,Arial Black,28,&H00000000,&H000000FF,{style['active_color']},{style['active_color']},-1,0,0,0,100,100,2,0,3,8.0,0.0,5,30,30,30,1
Style: OutroCardBox,{style['font']},48,&H00FFFFFF,&H000000FF,&H00000000,&HD0000000,-1,0,0,0,100,100,1,0,3,14.0,6.0,5,30,30,30,1
Style: OutroSub,Arial,30,&H0038BDF8,&H000000FF,&H00000000,&HB0000000,-1,0,0,0,100,100,1,0,3,6.0,2.0,5,30,30,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    dialogue_lines = []

    # 1. Hook Card Superiore
    if hook_title:
        hook_events = format_hook_card(hook_title, style_active_color=style["active_color"])
        dialogue_lines.extend(hook_events)

    # 2. Sottotitoli parlati
    if words:
        groups = []
        current_group = []
        for w in words:
            current_group.append(w)
            if len(current_group) >= 3 or (len(current_group) >= 2 and len(w["word"]) > 7):
                groups.append(current_group)
                current_group = []
        if current_group:
            groups.append(current_group)

        for group in groups:
            for active_idx, active_word in enumerate(group):
                w_start = active_word["start"]
                w_end = active_word["end"]
                
                if w_end - w_start < 0.18:
                    w_end = w_start + 0.18

                t_start_str = format_ass_time(w_start)
                t_end_str = format_ass_time(w_end)

                formatted_words = []
                for idx, item in enumerate(group):
                    word_text = item["word"].upper()
                    if use_emojis:
                        word_text = inject_emoji(word_text)

                    if idx == active_idx:
                        formatted_words.append(r"{\c" + style['active_color'] + r"}" + word_text + r"{\c" + style['primary_color'] + r"}")
                    else:
                        formatted_words.append(r"{\c" + style['primary_color'] + r"}" + word_text)

                line_text = " ".join(formatted_words)
                dialogue_lines.append(f"Dialogue: 0,{t_start_str},{t_end_str},TikTokSub,,0,0,0,,{{\\an5\\pos(540,{pos_y})}}{line_text}")

    # 3. OUTRO SLIDE FINALE OBBLIGATORIA (Negli ultimi 3.5s)
    cta_text = brand_cta.strip() if brand_cta else "La lezione gratuita sul profilo di Sara"
    if duration_sec and duration_sec > 4.0:
        outro_start = max(0.0, duration_sec - 3.5)
        outro_end = duration_sec + 0.5
        o_start_str = format_ass_time(outro_start)
        o_end_str = format_ass_time(outro_end)
        
        dialogue_lines.append(f"Dialogue: 4,{o_start_str},{o_end_str},OutroBadge,,0,0,0,,{{\\an5\\pos(540,820)\\fad(250,0)}}🎓 CALL TO ACTION")
        dialogue_lines.append(f"Dialogue: 5,{o_start_str},{o_end_str},OutroCardBox,,0,0,0,,{{\\an5\\pos(540,940)\\fad(250,0)}}{cta_text.upper()}")
        dialogue_lines.append(f"Dialogue: 4,{o_start_str},{o_end_str},OutroSub,,0,0,0,,{{\\an5\\pos(540,1070)\\fad(250,0)}}👉 Trovi il link su @saradizdari_ecom")

    full_ass_content = ass_header + "\n".join(dialogue_lines) + "\n"
    
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(full_ass_content)

    print(f"[CAPTIONER] File .ASS generato: Hook Card, Sottotitoli e Outro CTA Card pronti.")

def extract_smart_hook(video_filename_or_words):
    name = str(video_filename_or_words)
    if "sara" in name.lower() or "dizdari" in name.lower():
        return "LEZIONE GRATUITA SUL PROFILO DI SARA"
    elif "6000" in name or "6.000" in name:
        return "DA 0 A 6.000€ IN UN SOLO MESE"
    elif "3000" in name or "3.000" in name:
        return "3.000€ CON IL SUO PRIMO SHOP"
    elif "10.000" in name or "10000" in name:
        return "OLTRE 10.000€ IN SOLI 4 MESI"
    elif "1277" in name:
        return "I SUOI PRIMI 1.277€ ONLINE"
    return "LEZIONE GRATUITA SUL PROFILO DI SARA"

def burn_captions_to_video(input_video, output_video=None, style_key="hormozi_gold", use_emojis=True, custom_hook=None, brand_cta="La lezione gratuita sul profilo di Sara", model_size="base"):
    inp = Path(input_video)
    if not inp.exists():
        return {"status": "error", "message": f"File video '{input_video}' non trovato."}

    if not output_video:
        output_video = inp.parent / f"{inp.stem}_captioned_v4{inp.suffix}"
    outp = Path(output_video)

    ass_temp = inp.parent / f"temp_{inp.stem}_{int(time.time())}.ass"

    try:
        duration_sec = get_video_duration(inp)
        words = transcribe_audio_words(inp, model_size=model_size)
        hook = custom_hook if custom_hook else extract_smart_hook(inp.name)
        
        generate_ass_file(
            words,
            ass_temp,
            duration_sec=duration_sec,
            style_key=style_key,
            use_emojis=use_emojis,
            hook_title=hook,
            brand_cta=brand_cta
        )

        print(f"[CAPTIONER] Rendering con Hook Card, Sottotitoli e Outro CTA Slide...")
        ass_path_escaped = str(ass_temp.resolve()).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")

        cmd = [
            "ffmpeg", "-y",
            "-i", str(inp),
            "-vf", f"ass='{ass_path_escaped}'",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "19",
            "-c:a", "copy",
            str(outp)
        ]

        t_render_start = time.time()
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        t_render_elapsed = round(time.time() - t_render_start, 2)

        if res.returncode != 0:
            print(f"[CAPTIONER ERROR] FFmpeg err: {res.stderr}")
            return {"status": "error", "message": f"Errore rendering FFmpeg: {res.stderr[-300:]}"}

        print(f"[CAPTIONER] ✅ Video finale con Outro CTA Slide generato in {t_render_elapsed}s: '{outp.name}' ({round(outp.stat().st_size/(1024*1024), 2)} MB)!")

        return {
            "status": "success",
            "output_path": str(outp),
            "filename": outp.name,
            "style": style_key,
            "hook_title": hook,
            "words_count": len(words) if words else 0
        }

    except Exception as e:
        print(f"[CAPTIONER EXCEPTION] {e}")
        return {"status": "error", "message": str(e)}
    finally:
        if ass_temp.exists():
            try:
                ass_temp.unlink()
            except Exception:
                pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_vid = sys.argv[1]
        style = sys.argv[2] if len(sys.argv) > 2 else "hormozi_gold"
        hook = sys.argv[3] if len(sys.argv) > 3 else None
        res = burn_captions_to_video(test_vid, style_key=style, custom_hook=hook)
        print(json.dumps(res, indent=2, ensure_ascii=False))