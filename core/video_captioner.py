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

# Palette ASS in formato &HAABBGGRR (BGR esadecimale)
STYLES = {
    "hormozi_gold": {
        "name": "Hormozi Gold (Creator & E-Commerce)",
        "font": "Arial Black",
        "fontsize": 68,
        "primary_color": "&H00FFFFFF",
        "active_color": "&H0000D4FF",      # Oro caldo (#FFD400)
        "power_color": "&H0066FF33",       # Verde Smeraldo (#33FF66) per numeri/€
        "kicker_color": "&H0000D4FF",
        "outline_color": "&H00000000",
        "outline_width": 4.8,
        "shadow_width": 0.0,
        "pos_y": 1380
    },
    "executive_fin": {
        "name": "Executive Finance (Saikoo / B2B / Dati)",
        "font": "Arial Black",
        "fontsize": 66,
        "primary_color": "&H00FFFFFF",
        "active_color": "&H000AD6FF",      # Financial Gold (#FFD60A)
        "power_color": "&H00B9FF10",       # Cyber Mint (#10FFB9) per metriche/bilanci
        "kicker_color": "&H00F8BD38",      # Sky Cyan (#38BDF8)
        "outline_color": "&H00000000",
        "outline_width": 4.8,
        "shadow_width": 0.0,
        "pos_y": 1380
    },
    "docu_crimson": {
        "name": "Investigative Docu (Theory / Caso Studio)",
        "font": "Arial Black",
        "fontsize": 68,
        "primary_color": "&H00FFFFFF",
        "active_color": "&H0000CCFF",      # High-Alert Amber (#FFCC00)
        "power_color": "&H004444FF",       # Crimson Red (#FF4444)
        "kicker_color": "&H004444FF",
        "outline_color": "&H00000000",
        "outline_width": 4.8,
        "shadow_width": 0.0,
        "pos_y": 1380
    },
    "viral_emerald": {
        "name": "Viral Emerald (Trading & Mindset)",
        "font": "Arial Black",
        "fontsize": 68,
        "primary_color": "&H00FFFFFF",
        "active_color": "&H0055FF00",      # Neon Emerald (#00FF55)
        "power_color": "&H0000E6FF",       # Gold (#FFE600)
        "kicker_color": "&H0055FF00",
        "outline_color": "&H00000000",
        "outline_width": 4.8,
        "shadow_width": 0.0,
        "pos_y": 1380
    },
    "cyber_cyan": {
        "name": "Cyber Cyan (Tech & AI)",
        "font": "Arial Black",
        "fontsize": 66,
        "primary_color": "&H00FFFFFF",
        "active_color": "&H00FFFF00",      # Cyan (#00FFFF)
        "power_color": "&H0000D4FF",       # Gold (#FFD400)
        "kicker_color": "&H00FFFF00",
        "outline_color": "&H00000000",
        "outline_width": 4.8,
        "shadow_width": 0.0,
        "pos_y": 1380
    }
}

POWER_KEYWORDS = (
    "EURO", "€", "%", "ZERO", "RECORD", "SEGRETO", "ERRORE", "MAI", "VERITÀ",
    "GIORNI", "MESI", "MILIONI", "MILIARDI", "BILANCIO", "BILANCI", "FATTURATO",
    "UTILE", "UTILI", "6M+", "SAIKOO", "SHOPIFY", "ECOMMERCE", "GRATIS", "GRATUITA"
)

def resolve_campaign_visual_profile(campaign_id=None, campaign_name=None, brand_cta=None, brand_mention=None, hook_title=None, default_style="hormozi_gold"):
    """
    Seleziona automaticamente il profilo estetico, i colori delle parole-chiave e i testi
    di cornice (Kicker / Callout finale) adattandoli alla campagna specifica.
    Zero emoji rotte, zero box neri amatoriali.
    """
    cid = str(campaign_id or "").strip().lower()
    cname = str(campaign_name or "").strip().lower()
    cta_l = str(brand_cta or "").strip().lower()
    ment_l = str(brand_mention or "").strip().lower()
    hook_l = str(hook_title or "").strip().lower()
    combined = f"{cid} {cname} {cta_l} {ment_l} {hook_l}"

    # 1. Saikoo x Theory SPA (Finanza, Bilanci Aziendali, B2B)
    if "6a91676284a29ab01b754c33" in cid or "saikoo" in combined or "bilanci" in combined:
        return {
            "style_key": "executive_fin",
            "hook_kicker": "DATI UFFICIALI  •  ANALISI AZIENDALE",
            "outro_kicker": "VUOI VEDERE I NUMERI REALI DI OGNI AZIENDA?",
            "outro_headline": brand_cta.strip() if brand_cta and str(brand_cta).strip() else "Cerca gratis i bilanci di 6M+ aziende su Saikoo.ai",
            "outro_action_prefix": "PROVALO ORA  ▸ "
        }

    # 2. Sara Dizdari Academy (E-Commerce, Negozi Digitali, Shopify)
    if "6a71c6f7245627c68999eae2" in cid or "dizdari" in combined or "negozi digitali" in combined or "shopify" in combined:
        return {
            "style_key": "hormozi_gold",
            "hook_kicker": "CASO STUDIO  •  E-COMMERCE ITALIA",
            "outro_kicker": "VUOI AVVIARE IL TUO NEGOZIO DIGITALE?",
            "outro_headline": brand_cta.strip() if brand_cta and str(brand_cta).strip() else "Guarda la lezione gratuita sul profilo di Sara",
            "outro_action_prefix": "VAI SUL PROFILO  ▸ "
        }

    # 3. Le 9 Bugie di FitActive / Alex Theory (Inchiesta, Business Caso Studio)
    if "6a719c80a2d57190f5d7a38b" in cid or "fitactive" in combined or "bugie" in combined or "alextheory" in combined:
        return {
            "style_key": "docu_crimson",
            "hook_kicker": "DIETRO LE QUINTE  •  CASO STUDIO",
            "outro_kicker": "VUOI SCOPRIRE TUTTA LA VERITÀ?",
            "outro_headline": brand_cta.strip() if brand_cta and str(brand_cta).strip() else "Guarda l'inchiesta completa sul profilo ufficiale",
            "outro_action_prefix": "SEGUI IL CANALE  ▸ "
        }

    # 4. Aldo Masolo (Trading, Mindset, Performance)
    if "6a7628ca922613d297f2e2c5" in cid or "masolo" in combined:
        return {
            "style_key": "viral_emerald",
            "hook_kicker": "MINDSET  •  STRATEGIA OPERATIVA",
            "outro_kicker": "VUOI APPROFONDIRE IL METODO COMPLETO?",
            "outro_headline": brand_cta.strip() if brand_cta and str(brand_cta).strip() else "Scopri la strategia completa sul profilo di Aldo Masolo",
            "outro_action_prefix": "PROFILO UFFICIALE  ▸ "
        }

    # 5. Fallback dinamico intelligente per qualsiasi nuova campagna Klippify
    return {
        "style_key": default_style if default_style in STYLES else "hormozi_gold",
        "hook_kicker": "ESTRATTO ESCLUSIVO  •  FOCUS",
        "outro_kicker": "VUOI APPROFONDIRE QUESTO ARGOMENTO?",
        "outro_headline": brand_cta.strip() if brand_cta and str(brand_cta).strip() else "Guarda il video completo sul profilo ufficiale!",
        "outro_action_prefix": "SEGUI ORA  ▸ "
    }


def format_ass_time(seconds):
    seconds = max(0.0, float(seconds))
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


def _strip_broken_emojis(text: str) -> str:
    """Rimuove emoji Unicode che su Windows libass vengono renderizzate come quadratini o glifi rotti."""
    if not text:
        return ""
    return re.sub(r"[\U00010000-\U0010ffff\u2600-\u27bf\ufe0f]", "", str(text)).strip()


def wrap_balanced_lines(text: str, max_chars_per_line: int = 24) -> list[str]:
    """Spezza un titolo o una CTA lunga in 2 righe bilanciate per evitare scritte schiacciate."""
    clean = re.sub(r"\s+", " ", _strip_broken_emojis(text)).strip()
    if len(clean) <= max_chars_per_line:
        return [clean]
    words = clean.split()
    if len(words) <= 2:
        return [clean]
    # Se non supera 2 righe, dividi vicino alla metà dei caratteri
    total_len = len(clean)
    if total_len <= max_chars_per_line * 2.2:
        target = total_len // 2
        best_idx = 1
        best_diff = 9999
        running = 0
        for idx in range(1, len(words)):
            running += len(words[idx - 1]) + (1 if idx > 1 else 0)
            diff = abs(running - target)
            if diff < best_diff:
                best_diff = diff
                best_idx = idx
        return [" ".join(words[:best_idx]), " ".join(words[best_idx:])]
    # Altrimenti costruisci righe fino a max_chars_per_line
    lines = []
    curr = []
    curr_len = 0
    for w in words:
        if curr and curr_len + 1 + len(w) > max_chars_per_line:
            lines.append(" ".join(curr))
            curr = [w]
            curr_len = len(w)
        else:
            curr.append(w)
            curr_len += len(w) + (1 if len(curr) > 1 else 0)
    if curr:
        lines.append(" ".join(curr))
    return lines[:3]


def colorize_viral_words(text: str, active_color: str = "&H0000D4FF", power_color: str = "&H0066FF33", base_color: str = "&H00FFFFFF") -> str:
    """Evidenzia numeri, valute, siti web (.ai/.it/.com) e parole chiave ad alto impatto."""
    words = text.split()
    out = []
    for w in words:
        w_up = w.upper()
        if any(ch.isdigit() for ch in w_up) or "€" in w_up or "%" in w_up or ".AI" in w_up or ".IT" in w_up or ".COM" in w_up:
            out.append(rf"{{\c{active_color}}}" + w + rf"{{\c{base_color}}}")
        elif any(kw in w_up for kw in POWER_KEYWORDS):
            out.append(rf"{{\c{power_color}}}" + w + rf"{{\c{base_color}}}")
        else:
            out.append(w)
    return " ".join(out)


def format_hook_card(hook_title, style_active_color="&H0000D4FF", persistent=False, duration_sec=3.2, kicker_text="ESTRATTO ESCLUSIVO  •  FOCUS", power_color="&H0066FF33"):
    """
    Genera l'Hook editoriale nei primi 3.2 secondi del video:
    - Niente box neri rettangolari o emoji rotte.
    - Tipografia su 2 righe bilanciate con animazione pop-in e ombreggiatura morbida cinematografica.
    """
    clean = _strip_broken_emojis(hook_title).upper().strip() if hook_title else "GUARDA COSA SUCCEDE"
    end_time = "1:00:00.00" if persistent else format_ass_time(duration_sec)

    lines = wrap_balanced_lines(clean, max_chars_per_line=22)
    styled_lines = [
        colorize_viral_words(ln, active_color=style_active_color, power_color=power_color, base_color="&H00FFFFFF")
        for ln in lines
    ]
    title_formatted = r"\N".join(styled_lines)
    kicker_clean = _strip_broken_emojis(kicker_text).upper()

    pop_anim = r"\fscx92\fscy92\t(0,160,\fscx100\fscy100)"
    badge_event = (
        rf"Dialogue: 2,0:00:00.00,{end_time},HookBadge,,0,0,0,,"
        rf"{{\an5\pos(540,245)\fad(120,240){pop_anim}}}{kicker_clean}"
    )
    card_event = (
        rf"Dialogue: 3,0:00:00.00,{end_time},HookCardBox,,0,0,0,,"
        rf"{{\an5\pos(540,335)\fad(120,240){pop_anim}}}{title_formatted}"
    )

    return [badge_event, card_event]


def _is_power_word(word_text: str) -> bool:
    w_up = word_text.upper()
    if any(ch.isdigit() for ch in w_up) or "€" in w_up or "%" in w_up:
        return True
    return any(kw in w_up for kw in POWER_KEYWORDS)


def generate_ass_file(
    words,
    output_ass_path,
    duration_sec=35.0,
    style_key="hormozi_gold",
    use_emojis=False,
    hook_title=None,
    brand_cta=None,
    brand_mention=None,
    campaign_id=None,
    campaign_name=None
):
    profile = resolve_campaign_visual_profile(
        campaign_id=campaign_id,
        campaign_name=campaign_name,
        brand_cta=brand_cta,
        brand_mention=brand_mention,
        hook_title=hook_title,
        default_style=style_key
    )
    resolved_style_key = profile["style_key"] if style_key == "hormozi_gold" else style_key
    style = STYLES.get(resolved_style_key, STYLES["hormozi_gold"])
    pos_y = style["pos_y"]

    # Quando il video ha una durata sufficiente (> 6s), riserviamo gli ultimi 2.7s alla Call-To-Action
    # disattivando i sottotitoli parlati in quella finestra per evitare qualsiasi sovrapposizione visiva!
    has_outro = bool(duration_sec and duration_sec > 4.0)
    outro_start = max(0.0, duration_sec - 2.8) if has_outro else 999999.0
    sub_cutoff_sec = max(0.0, outro_start - 0.12) if (duration_sec and duration_sec > 6.5) else 999999.0

    # BorderStyle=1 (contorno nitido + ombra profonda morbida) su TUTTI gli stili:
    # elimina i rettangoli neri "AI slop" (BorderStyle=3) che coprivano il volto del parlante!
    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTokSubGlow,{style['font']},{style['fontsize']},&H00000000,&H000000FF,&H50000000,&H00000000,-1,0,0,0,100,100,1.5,0,1,12.0,0.0,5,50,50,50,1
Style: TikTokSub,{style['font']},{style['fontsize']},{style['primary_color']},&H000000FF,{style['outline_color']},&H80000000,-1,0,0,0,100,100,1.5,0,1,{style['outline_width']},2.5,5,50,50,50,1
Style: HookBadge,Arial Black,26,{style['kicker_color']},&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,3.0,0,1,4.0,2.0,5,40,40,40,1
Style: HookCardBox,{style['font']},52,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1.0,0,1,5.2,3.5,5,50,50,40,1
Style: OutroGlow,{style['font']},50,&H00000000,&H000000FF,&H45000000,&H00000000,-1,0,0,0,100,100,1.0,0,1,16.0,0.0,5,60,60,40,1
Style: OutroBadge,Arial Black,27,{style['kicker_color']},&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2.5,0,1,4.2,2.5,5,50,50,40,1
Style: OutroCardBox,{style['font']},50,&H00FFFFFF,&H000000FF,&H00000000,&H95000000,-1,0,0,0,100,100,1.0,0,1,5.5,4.0,5,60,60,40,1
Style: OutroSub,Arial Black,31,{style['active_color']},&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2.0,0,1,4.5,2.5,5,50,50,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    dialogue_lines = []

    # 1. Hook Card Superiore (temporanea, primi 3.2 secondi, 2 righe bilanciate)
    if hook_title:
        hook_events = format_hook_card(
            hook_title,
            style_active_color=style["active_color"],
            persistent=False,
            duration_sec=3.2,
            kicker_text=profile["hook_kicker"],
            power_color=style["power_color"]
        )
        dialogue_lines.extend(hook_events)

    # 2. Sottotitoli parlati parola-per-parola con raggruppamento naturale per pause/punteggiatura e pop dinamico
    if words:
        clean_words = []
        for w in words:
            w_txt = _strip_broken_emojis(re.sub(r">>+|\[.*?\]", "", str(w.get("word", "")))).strip()
            if not w_txt:
                continue
            ws = float(w.get("start", 0.0))
            if ws >= sub_cutoff_sec:
                continue
            we = min(sub_cutoff_sec, float(w.get("end", ws + 0.18)))
            if we <= ws:
                we = min(sub_cutoff_sec, ws + 0.16)
            if we <= ws:
                continue
            clean_words.append({"word": w_txt, "start": ws, "end": we})

        for i in range(len(clean_words) - 1):
            next_s = clean_words[i + 1]["start"]
            if next_s <= clean_words[i]["start"]:
                next_s = round(clean_words[i]["start"] + 0.08, 2)
                clean_words[i + 1]["start"] = next_s
                if clean_words[i + 1]["end"] <= next_s:
                    clean_words[i + 1]["end"] = round(next_s + 0.15, 2)
            if clean_words[i]["end"] > next_s:
                clean_words[i]["end"] = next_s
            elif next_s - clean_words[i]["start"] >= 0.18 and clean_words[i]["end"] - clean_words[i]["start"] < 0.18:
                clean_words[i]["end"] = min(next_s, round(clean_words[i]["start"] + 0.18, 2))

        # Raggruppamento intelligente: spezza sulle pause vocali (>0.32s) o sulla punteggiatura forte
        groups = []
        current_group = []
        for idx, w in enumerate(clean_words):
            current_group.append(w)
            w_str = w["word"]
            has_punct = w_str.endswith((".", "!", "?", ",", ";", ":"))
            next_gap = (clean_words[idx + 1]["start"] - w["end"]) if (idx + 1 < len(clean_words)) else 0.0
            char_sum = sum(len(x["word"]) for x in current_group)
            if (
                len(current_group) >= 3
                or (len(current_group) >= 2 and (char_sum >= 14 or has_punct or next_gap >= 0.30))
                or (len(current_group) == 1 and (len(w_str) >= 12 or has_punct or next_gap >= 0.45))
            ):
                groups.append(current_group)
                current_group = []
        if current_group:
            groups.append(current_group)

        for group in groups:
            for active_idx, active_word in enumerate(group):
                w_start = float(active_word["start"])
                w_end = float(active_word["end"])
                if w_end <= w_start:
                    w_end = round(w_start + 0.05, 2)

                t_start_str = format_ass_time(w_start)
                t_end_str = format_ass_time(w_end)

                formatted_words = []
                plain_words = []
                for idx, item in enumerate(group):
                    word_text = item["word"].upper()
                    plain_words.append(word_text)
                    is_pwr = _is_power_word(word_text)

                    if idx == active_idx:
                        hl_col = style["power_color"] if is_pwr else style["active_color"]
                        # Pop leggero (+10% scale) sulla parola pronunciata in questo istante
                        formatted_words.append(
                            rf"{{\c{hl_col}\fscx110\fscy110}}" + word_text + rf"{{\fscx100\fscy100\c{style['primary_color']}}}"
                        )
                    else:
                        idle_col = style["active_color"] if is_pwr else style["primary_color"]
                        formatted_words.append(rf"{{\c{idle_col}}}" + word_text + rf"{{\c{style['primary_color']}}}")

                line_text = " ".join(formatted_words)
                plain_line = " ".join(plain_words)
                # Layer 0: Alone scuro morbido (blur) per contrasto perfetto su camicie bianche o sfondi chiari
                dialogue_lines.append(
                    f"Dialogue: 0,{t_start_str},{t_end_str},TikTokSubGlow,,0,0,0,,{{\\an5\\pos(540,{pos_y})\\blur5}}{plain_line}"
                )
                # Layer 1: Testo nitido principale con parola attiva animata
                dialogue_lines.append(
                    f"Dialogue: 1,{t_start_str},{t_end_str},TikTokSub,,0,0,0,,{{\\an5\\pos(540,{pos_y})}}{line_text}"
                )

    # 3. OUTRO CALLOUT VIRALE ADATTATO ALLA CAMPAGNA (Negli ultimi 2.8s, nella zona focalizzata in basso)
    cta_raw = _strip_broken_emojis(profile["outro_headline"])
    mention_clean = _strip_broken_emojis(brand_mention) if brand_mention and str(brand_mention).strip() else ""
    if mention_clean and not mention_clean.startswith("@"):
        mention_clean = f"@{mention_clean}"
    outro_sub_text = (
        f"{profile['outro_action_prefix']}{mention_clean}"
        if mention_clean
        else f"{profile['outro_action_prefix']}LINK SUL PROFILO UFFICIALE"
    )

    if has_outro:
        outro_end = duration_sec + 0.5
        o_start_str = format_ass_time(outro_start)
        o_end_str = format_ass_time(outro_end)

        cta_upper = cta_raw.upper()
        cta_lines = wrap_balanced_lines(cta_upper, max_chars_per_line=25)
        cta_plain_multiline = r"\N".join(cta_lines)
        cta_styled_multiline = r"\N".join(
            colorize_viral_words(
                ln,
                active_color=style["active_color"],
                power_color=style["power_color"],
                base_color="&H00FFFFFF"
            )
            for ln in cta_lines
        )

        # Commento metadato con il testo lineare integrale per ispezione/test
        dialogue_lines.append(f"Comment: 0,{o_start_str},{o_end_str},OutroCardBox,,0,0,0,,{cta_upper}")

        pop_outro = r"\fscx88\fscy88\t(0,180,\fscx100\fscy100)"
        # Posizionato a y=1180..1390 (zona lower-third pulita, non copre mai gli occhi/volto del parlante!)
        dialogue_lines.append(
            f"Dialogue: 4,{o_start_str},{o_end_str},OutroBadge,,0,0,0,,"
            f"{{\\an5\\pos(540,1170)\\fad(200,0){pop_outro}}}{profile['outro_kicker']}"
        )
        dialogue_lines.append(
            f"Dialogue: 4,{o_start_str},{o_end_str},OutroGlow,,0,0,0,,"
            f"{{\\an5\\pos(540,1265)\\fad(200,0)\\blur6{pop_outro}}}{cta_plain_multiline}"
        )
        dialogue_lines.append(
            f"Dialogue: 5,{o_start_str},{o_end_str},OutroCardBox,,0,0,0,,"
            f"{{\\an5\\pos(540,1265)\\fad(200,0){pop_outro}}}{cta_styled_multiline}"
        )
        dialogue_lines.append(
            f"Dialogue: 4,{o_start_str},{o_end_str},OutroSub,,0,0,0,,"
            f"{{\\an5\\pos(540,1375)\\fad(200,0){pop_outro}}}{outro_sub_text}"
        )

    full_ass_content = ass_header + "\n".join(dialogue_lines) + "\n"

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(full_ass_content)

    print(f"[CAPTIONER] File .ASS generato ({style['name']}): Hook (3.2s), Sottotitoli dinamici e Callout finale pronti.")


def extract_smart_hook(video_filename_or_words):
    if isinstance(video_filename_or_words, list) and video_filename_or_words:
        first_words = [w.get("word", "") for w in video_filename_or_words[:7]]
        candidate = " ".join(first_words).strip().upper()
        if candidate:
            return candidate
    name = str(video_filename_or_words)
    clean_stem = re.sub(r"[_\\-]+", " ", Path(name).stem).upper()
    tokens = [t for t in clean_stem.split() if not t.startswith("SLOT") and not t.startswith("CLIP") and not t.isdigit()]
    if tokens:
        return " ".join(tokens[:6])
    return "GUARDA FINO ALLA FINE"


def burn_captions_to_video(
    input_video,
    output_video=None,
    style_key="hormozi_gold",
    use_emojis=False,
    custom_hook=None,
    brand_cta=None,
    brand_mention=None,
    model_size="base",
    precomputed_words=None,
    campaign_id=None,
    campaign_name=None
):
    inp = Path(input_video)
    if not inp.exists():
        return {"status": "error", "message": f"File video '{input_video}' non trovato."}

    if not output_video:
        output_video = inp.parent / f"{inp.stem}_captioned_v4{inp.suffix}"
    outp = Path(output_video)

    ass_temp = inp.parent / f"temp_{inp.stem}_{int(time.time())}.ass"

    try:
        duration_sec = get_video_duration(inp)
        if precomputed_words is not None and len(precomputed_words) > 0:
            words = precomputed_words
            print(f"[CAPTIONER] Uso {len(words)} parole già sincronizzate dall'ispezione AI (0 MB RAM Whisper).")
        else:
            try:
                words = transcribe_audio_words(inp, model_size=model_size)
            except Exception as w_err:
                print(f"[CAPTIONER WARNING] Trascrizione Whisper non disponibile ({w_err}), procedo con Hook e CTA.")
                words = []
        hook = custom_hook if custom_hook else extract_smart_hook(words or inp.name)

        generate_ass_file(
            words,
            ass_temp,
            duration_sec=duration_sec,
            style_key=style_key,
            use_emojis=use_emojis,
            hook_title=hook,
            brand_cta=brand_cta,
            brand_mention=brand_mention,
            campaign_id=campaign_id,
            campaign_name=campaign_name
        )

        print(f"[CAPTIONER] Rendering con Hook (3.2s), Sottotitoli dinamici e Callout finale...")
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

        print(f"[CAPTIONER] ✅ Video finale generato in {t_render_elapsed}s: '{outp.name}' ({round(outp.stat().st_size/(1024*1024), 2)} MB)!")

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
