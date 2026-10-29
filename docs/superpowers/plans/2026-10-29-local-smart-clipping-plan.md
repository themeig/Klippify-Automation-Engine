# Local Smart Clipping & Antigravity AI Director Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sostituire il taglio cieco (`00:10-00:45`) e l'upload browser fallimentare con un motore di montaggio video intelligente 100% locale e leggero per CPU datate, integrato con un Cronjob Regista AI su Antigravity auto-configurante su qualsiasi PC tramite `GEMINI.md` e `.agents/skills/`.

**Architecture:** Il sistema opera su due livelli complementari: (1) un livello locale leggero (`source_downloader.py` + `local_viral_analyzer.py` + `clip_processor.py` + `video_captioner.py`) che estrae sottotitoli timestampati nativi (`.json3`/`.vtt`) o hotspot vocali FFmpeg, calcola i punteggi di viralità per frase, applica un *Cold-Open Teaser* nei primi 2.5s, esegue Smart Crop 9:16 sul volto campionando 10 frame con OpenCV, taglia i silenzi `> 0.45s` e mostra l'Hook solo nei primi 3.2s e la CTA dinamica negli ultimi 3s; (2) un livello "AI Director" basato su `GEMINI.md`, `.agents/skills/klippify-ai-director/SKILL.md` e `setup_antigravity_cron.py` che permette a qualsiasi istanza di Antigravity (su questo PC o sul portatile vecchio) di auto-configurare il cronjob pianificato e guidare il montaggio leggendo copioni e frame JPG.

**Tech Stack:** Python 3.x, FFmpeg/FFprobe, `yt-dlp`, `faster-whisper` (int8 CPU), `opencv-python-headless` (Haar Cascade), `pytest`.

**Spec:** `docs/superpowers/specs/2026-10-29-local-smart-clipping-design.md`

## Global Constraints

- Tutte le operazioni devono funzionare **100% in locale** senza richiedere chiavi API esterne o apertura di Chrome/Playwright per Gemini Web.
- Ottimizzato per **portatile vecchio (solo CPU)**: vietato trascrivere con Whisper video interi > 10 minuti senza prima usare i sottotitoli nativi YouTube (`.json3`/`.vtt`) o il pre-filtro energetico FFmpeg (`astats`).
- `core/clipping_pipeline.py` deve mantenere la firma compatibile `run_clipping_workflow(campaign_id, video_source_path=None, is_auto=True, task_logger=None, cuts_file=None)`.
- Il banner Hook superiore in `core/video_captioner.py` deve durare **solo i primi `3.2` secondi** (`persistent=False`), mai per tutto il video.
- La slide Outro CTA finale (ultimi `3.0s`–`3.5s`) deve usare dinamicamente la CTA e la menzione `@` della campagna attiva, rimuovendo l'hardcoding fisso su `@saradizdari_ecom`.
- Gli script `.bat` nella root devono usare `cd /d "%~dp0"` anziché percorsi cablati ad altri PC.

## Review Focus

1. **Sottotitoli YouTube `.json3`/`.vtt` con eventi vuoti, newline o timestamp sovrapposti:** `parse_subtitle_file()` deve ignorare eventi solo-musica/vuoti, normalizzare i ritorni a capo e restituire parole con `start < end` monotoni.
2. **Video sorgente breve (`< 60s`) o con pochissimo parlato:** `analyze_transcript_for_clips()` non deve andare in crash o restituire liste vuote se il parlato dura 30–50s, ma adattare la finestra per estrarre comunque clip valide a frase compiuta.
3. **Campagna senza `mandatory_mentions` o `call_to_action` esplicita:** `generate_ass_file()` non deve mai stampare `@saradizdari_ecom` se la campagna è un'altra (es. *Million Hospitality* o *Gabriele Vagnato*), ma usare la menzione della campagna o il testo generico `"👉 Segui il profilo ufficiale per saperne di più"`.
4. **Clip con zero volti rilevati (es. screencast e-commerce o b-roll):** `detect_smart_crop_mode()` deve restituire `mode="zoomed_blur"` (con foreground ingrandito al 135% anziché francobollo piccolo) senza sollevare eccezioni OpenCV.
5. **Clonazione della repo su un altro PC con nome utente Windows diverso:** `setup_antigravity_cron.py` deve calcolare dinamicamente `Path(__file__).resolve().parent.parent` e `Path.home() / ".gemini" / "config"`, sovrascrivendo eventuali percorsi obsoleti nel `sidecar.json`.

---

### Task 1: Portabilità Ambiente, Dipendenze ed Estrazione Sottotitoli/Frame (`source_downloader.py`)

**Files:**
- Create: `requirements.txt`
- Create: `Installa_Dipendenze.bat`
- Modify: `AVVIA_KLIPPIFY_24H.bat:1-10`
- Modify: `core/source_downloader.py:170-328`
- Test: `tests/test_source_downloader.py`

**Interfaces:**
- Consumes: `yt_dlp`, `subprocess`, `json`, `pathlib.Path`
- Produces:
  - `source_downloader.parse_subtitle_file(sub_path: Path) -> list[dict]` (returns `[{"word": str, "start": float, "end": float, "prob": float}]`)
  - `source_downloader.extract_sample_frames(video_path: Path, output_dir: Path, count: int = 6) -> list[str]`
  - `source_downloader.prepare_video_for_ai(video_path: Path, campaign_id: str = "general") -> dict` (returns `{"video_path": str, "transcript_path": str, "words_count": int, "sample_frames": list[str]}`)

- [ ] **Step 1: Write the failing test in `tests/test_source_downloader.py`**

```python
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import source_downloader

def test_parse_json3_subtitles_extracts_words_and_skips_empty(tmp_path):
    sample_json3 = {
        "events": [
            {"tStartMs": 0, "dDurationMs": 1000, "segs": [{"utf8": "\n"}]},
            {
                "tStartMs": 1500,
                "dDurationMs": 2000,
                "segs": [
                    {"utf8": "Oggi "},
                    {"utf8": "vediamo ", "tOffsetMs": 500},
                    {"utf8": "10.000€!", "tOffsetMs": 1200}
                ]
            }
        ]
    }
    sub_file = tmp_path / "test.it.json3"
    sub_file.write_text(json.dumps(sample_json3), encoding="utf-8")

    words = source_downloader.parse_subtitle_file(sub_file)
    assert len(words) == 3
    assert words[0]["word"] == "Oggi"
    assert words[0]["start"] == 1.5
    assert words[1]["word"] == "vediamo"
    assert words[1]["start"] == 2.0
    assert words[2]["word"] == "10.000€!"
    assert words[2]["end"] > words[2]["start"]

def test_parse_vtt_subtitles_interpolates_word_timestamps(tmp_path):
    vtt_content = """WEBVTT

00:00:02.000 --> 00:00:05.000
Questo metodo ha generato 3000 euro
"""
    vtt_file = tmp_path / "test.it.vtt"
    vtt_file.write_text(vtt_content, encoding="utf-8")

    words = source_downloader.parse_subtitle_file(vtt_file)
    assert [w["word"] for w in words] == ["Questo", "metodo", "ha", "generato", "3000", "euro"]
    assert words[0]["start"] == 2.0
    assert round(words[-1]["end"], 2) == 5.0
    for w in words:
        assert w["end"] > w["start"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_source_downloader.py -v`
Expected: FAIL with `AttributeError: module 'source_downloader' has no attribute 'parse_subtitle_file'`

- [ ] **Step 3: Create `requirements.txt`, `Installa_Dipendenze.bat`, fix `AVVIA_KLIPPIFY_24H.bat`, and implement `parse_subtitle_file`, `extract_sample_frames`, and `prepare_video_for_ai` in `core/source_downloader.py`**

In `AVVIA_KLIPPIFY_24H.bat`, replace `cd /d "c:\Users\HP\Desktop\contenuti klippify"` with `cd /d "%~dp0"`.
In `core/source_downloader.py`:
- Implement `parse_subtitle_file(sub_path: Path) -> list[dict]` supporting both `.json3` (`events` -> `segs` with `tStartMs` + `tOffsetMs`) and `.vtt` / `.srt` (regex timestamp cues split into evenly timed words across the cue duration, stripping `<c>` tags and empty tokens).
- Implement `extract_sample_frames(video_path: Path, output_dir: Path, count: int = 6) -> list[str]` using `ffprobe` for duration and `ffmpeg -ss <t> -i <video> -vframes 1 -vf scale=-1:480 -q:v 4 <frame.jpg>`.
- Update `download_source_video` `ydl_opts` to include `'writesubtitles': True, 'writeautomaticsub': True, 'subtitleslangs': ['it', 'en'], 'subtitlesformat': 'json3/vtt'` and automatically parse any downloaded subtitle file into `<video_stem>_transcript.json`.
- Add CLI flag `--prepare-for-ai <video_path>` in `source_downloader.py`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_source_downloader.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add requirements.txt Installa_Dipendenze.bat AVVIA_KLIPPIFY_24H.bat core/source_downloader.py tests/test_source_downloader.py
git commit -m "feat(sourcing): add portable bat paths and instant json3/vtt subtitle & frame extraction"
```

---

### Task 2: Motore Locale di Viral Scoring, Cold-Open Teaser & Hook Contestuali (`core/local_viral_analyzer.py`)

**Files:**
- Create: `core/local_viral_analyzer.py`
- Test: `tests/test_local_viral_analyzer.py`

**Interfaces:**
- Consumes: `source_downloader.parse_subtitle_file`
- Produces:
  - `local_viral_analyzer.segment_words_into_sentences(words: list[dict], pause_threshold: float = 0.35) -> list[dict]`
  - `local_viral_analyzer.is_greeting_or_preamble(sentence_text: str) -> bool`
  - `local_viral_analyzer.score_sentence_virality(sentence: dict) -> float`
  - `local_viral_analyzer.extract_contextual_hook(text: str, campaign_name: str = "") -> str`
  - `local_viral_analyzer.analyze_transcript_for_clips(words: list[dict], campaign_data: dict = None, min_clips: int = 3, max_clips: int = 5) -> list[dict]`
  - `local_viral_analyzer.analyze_video_locally(video_path: Path, campaign_data: dict = None, task_logger=None) -> list[dict]`

- [ ] **Step 1: Write the failing test in `tests/test_local_viral_analyzer.py`**

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import local_viral_analyzer

def _make_words_from_timed_sentences(timed_sentences):
    words = []
    for text, start_t, end_t in timed_sentences:
        tokens = text.split()
        dur = (end_t - start_t) / max(len(tokens), 1)
        for i, tok in enumerate(tokens):
            words.append({
                "word": tok,
                "start": round(start_t + i * dur, 2),
                "end": round(start_t + (i + 1) * dur - 0.02, 2),
                "prob": 0.99
            })
    return words

def test_greeting_preamble_is_detected_and_excluded():
    assert local_viral_analyzer.is_greeting_or_preamble("Ciao a tutti ragazzi e bentornati sul mio canale!") is True
    assert local_viral_analyzer.is_greeting_or_preamble("In soli due mesi ho generato 12.400 euro partendo da zero.") is False

def test_analyze_transcript_extracts_complete_sentence_clips_with_teaser_and_custom_hook():
    sentences = [
        ("Ciao a tutti e benvenuti in questo nuovo video con Marco.", 0.0, 6.0),
        ("Il più grande errore che fa il 95% delle persone è aspettare il momento perfetto.", 6.5, 14.0),
        ("Quando ho aperto il primo store avevo zero esperienza e solo due ore la sera.", 14.5, 23.0),
        ("Nel primo mese sono arrivati i primi 3.200 euro di fatturato reale senza magazzino.", 23.5, 32.5),
        ("E dopo sessanta giorni abbiamo superato 15.000 euro cambiando completamente la mia vita.", 33.0, 41.5),
        ("Ora vi spiego i tre passaggi fondamentali che nessuno vi dice mai.", 42.0, 50.0),
        ("Il primo passaggio è scegliere un prodotto che risolve un problema urgente.", 50.5, 59.0),
        ("Il secondo passaggio è testare le creatività video senza buttare budget.", 59.5, 68.0),
        ("Chi applica questo metodo evita di bruciare migliaia di euro in test inutili.", 68.5, 77.0),
        ("Alla fine chi agisce oggi costruisce una seconda entrata solida in poche settimane.", 77.5, 86.0),
    ]
    words = _make_words_from_timed_sentences(sentences)
    camp = {
        "name": "Test Brand",
        "call_to_action": "Scopri il training sul profilo",
        "mandatory_hashtags": ["#testbrand", "#klippify"],
        "mandatory_mentions": ["@testbrand_official"]
    }
    clips = local_viral_analyzer.analyze_transcript_for_clips(words, camp, min_clips=2, max_clips=4)
    assert len(clips) >= 2
    first = clips[0]
    # Must NOT start at 0.0 (greeting skipped) and must NOT be hardcoded 00:10-00:45
    assert first["start_seconds"] >= 6.4
    assert 22.0 <= (first["end_seconds"] - first["start_seconds"]) <= 55.0
    assert "teaser_start" in first and "teaser_end" in first
    assert first["teaser_end"] > first["teaser_start"]
    assert first["hook_text"] != "POV: quello che nessuno ti dice su Test Brand 🤫"
    assert first["transcript"] != "Estratto dal video originale"
    assert "@testbrand_official" in first["tiktok_caption"]

def test_short_video_under_60s_still_returns_valid_clip():
    sentences = [
        ("Ho guadagnato 4.500 euro in 30 giorni facendo esattamente questa mossa.", 1.0, 12.0),
        ("Prima lavoravo dieci ore al giorno e non avevo mai tempo per la famiglia.", 12.5, 22.0),
        ("Oggi gestisco tutto dal portatile in due ore al giorno.", 22.5, 31.0),
    ]
    words = _make_words_from_timed_sentences(sentences)
    clips = local_viral_analyzer.analyze_transcript_for_clips(words, {"name": "ShortCamp"}, min_clips=1, max_clips=3)
    assert len(clips) >= 1
    assert clips[0]["end_seconds"] - clips[0]["start_seconds"] >= 18.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_local_viral_analyzer.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'local_viral_analyzer'`

- [ ] **Step 3: Implement `core/local_viral_analyzer.py`**

Implement:
- `segment_words_into_sentences(words, pause_threshold=0.35)` grouping words into sentence dicts `{"text": str, "start": float, "end": float, "words": list[dict]}` when a word ends with `.`, `!`, `?` or the gap to the next word is `>= pause_threshold` (and sentence has `>= 4` words).
- `is_greeting_or_preamble(sentence_text)` matching Italian/English intro clichés (`r"\b(ciao a tutti|bentornat|benvenut|in questo video|mi chiamo|oggi parliamo|buongiorno a tutti|iscriviti al canale)\b"`).
- `score_sentence_virality(sentence)` scoring numbers/currency (`€`, `euro`, `%`, `\d+`), high-retention Italian/English trigger words (`errore`, `segreto`, `nessuno`, `verità`, `problema`, `fatturato`, `guadagn`, `zero`, `giorni`, `mesi`, `libertà`, `rischio`, `vita`, `metodo`, `milioni`, `mila`, `stipendio`, `clienti`), and speech pace (`words / duration` between `2.2` and `4.0` wps).
- `extract_contextual_hook(text, campaign_name="")` extracting the punchiest 5–8 words containing numbers/triggers in uppercase (e.g. `"3.200€ NEL PRIMO MESE SENZA MAGAZZINO"` or the core clause of the teaser sentence).
- `analyze_transcript_for_clips(words, campaign_data=None, min_clips=3, max_clips=5)` sliding over sentence boundaries to build 25–52s non-overlapping windows (or 18–52s for short videos), selecting the highest-scoring sentence inside each window as `teaser_start` / `teaser_end` (clamped to `1.8s–3.5s`), and formatting `start_time` / `end_time` as `MM:SS.d` plus `start_seconds` / `end_seconds`.
- `detect_audio_hotspots_ffmpeg(video_path, top_k=4, window_sec=75.0)` and `analyze_video_locally(video_path, campaign_data=None, task_logger=None)` which:
  1. Checks `<video_stem>_transcript.json` or `.json3`/`.vtt` next to the video;
  2. If not present, finds audio energy hotspots with FFmpeg `silencedetect`/`astats` and runs `faster_whisper` (`int8`) only on the hotspots (or falls back to sentence-paced energy windows if `faster_whisper` is not installed yet), caching `<video_stem>_transcript.json`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_local_viral_analyzer.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/local_viral_analyzer.py tests/test_local_viral_analyzer.py
git commit -m "feat(analyzer): add 100% local viral clip & cold-open teaser analyzer"
```

---

### Task 3: Smart Crop 9:16 "10-Frame Sample", Teaser, Jump-Cut & Sottotitoli Anti-Spot (`clip_processor.py` & `video_captioner.py`)

**Files:**
- Modify: `core/clip_processor.py:1-130`
- Modify: `core/video_captioner.py:130-315`
- Test: `tests/test_clip_and_captions.py`

**Interfaces:**
- Consumes: `cv2` (optional with graceful fallback), `subprocess`
- Produces:
  - `clip_processor.detect_smart_crop_mode(video_path: Path, start_sec: float, duration: float) -> dict` (returns `{"mode": "face_crop" | "split_screen" | "zoomed_blur", "center_x_ratio": float, "faces_detected": int}`)
  - `clip_processor.compute_active_speech_segments(words: list[dict], start_sec: float, end_sec: float, max_silence: float = 0.45) -> list[tuple[float, float]]`
  - `clip_processor.build_ffmpeg_filter_complex(crop_info: dict, target_width: int = 1080, target_height: int = 1920, logo_path: str = None) -> tuple[str, str]`
  - `video_captioner.format_hook_card(hook_title: str, style_active_color: str = "&H0000E6FF", persistent: bool = False, duration_sec: float = 3.2) -> list[str]`
  - `video_captioner.generate_ass_file(words, output_ass_path, duration_sec=35.0, style_key="hormozi_gold", use_emojis=True, hook_title=None, brand_cta=None, brand_mention=None)`

- [ ] **Step 1: Write the failing test in `tests/test_clip_and_captions.py`**

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import clip_processor
import video_captioner

def test_hook_card_is_temporary_not_permanent():
    events = video_captioner.format_hook_card("DA ZERO A 10.000€ IN 2 MESI")
    assert len(events) == 2
    for ev in events:
        assert "0:00:00.00,0:00:03.20" in ev
        assert "1:00:00.00" not in ev
        assert "SUL PROFILO DI SARA" not in ev

def test_generate_ass_file_uses_dynamic_campaign_cta_and_mention(tmp_path):
    ass_file = tmp_path / "test.ass"
    words = [
        {"word": "Ecco", "start": 0.2, "end": 0.6},
        {"word": "il", "start": 0.6, "end": 0.8},
        {"word": "segreto", "start": 0.8, "end": 1.4},
    ]
    video_captioner.generate_ass_file(
        words=words,
        output_ass_path=ass_file,
        duration_sec=30.0,
        hook_title="IL SEGRETO DEL LUXURY",
        brand_cta="Guarda il video completo al link in bio!",
        brand_mention="@millionhospitality"
    )
    content = ass_file.read_text(encoding="utf-8")
    assert "GUARDA IL VIDEO COMPLETO AL LINK IN BIO!" in content
    assert "@millionhospitality" in content
    assert "@saradizdari_ecom" not in content

def test_generate_ass_file_without_mention_does_not_leak_sara_dizdari(tmp_path):
    ass_file = tmp_path / "test_nomention.ass"
    video_captioner.generate_ass_file(
        words=[{"word": "Ciao", "start": 0.1, "end": 0.5}],
        output_ass_path=ass_file,
        duration_sec=25.0,
        hook_title="TEST HOOK",
        brand_cta="Scopri di più sul profilo!",
        brand_mention=None
    )
    content = ass_file.read_text(encoding="utf-8")
    assert "@saradizdari_ecom" not in content
    assert "Sara" not in content

def test_compute_active_speech_segments_removes_long_silences():
    words = [
        {"word": "Prima", "start": 10.0, "end": 10.5},
        {"word": "frase.", "start": 10.5, "end": 11.2},
        # 1.8s silence gap here!
        {"word": "Seconda", "start": 13.0, "end": 13.5},
        {"word": "frase!", "start": 13.5, "end": 14.2},
    ]
    segs = clip_processor.compute_active_speech_segments(words, 10.0, 14.5, max_silence=0.45)
    assert len(segs) == 2
    assert segs[0][0] <= 10.0 and segs[0][1] < 12.0
    assert segs[1][0] > 12.5 and segs[1][1] >= 14.2

def test_build_ffmpeg_filter_complex_modes():
    fc_face, tag = clip_processor.build_ffmpeg_filter_complex({"mode": "face_crop", "center_x_ratio": 0.6})
    assert "crop=" in fc_face and "1080:1920" in fc_face

    fc_zoom, _ = clip_processor.build_ffmpeg_filter_complex({"mode": "zoomed_blur", "center_x_ratio": 0.5})
    assert "boxblur" in fc_zoom and "1458" in fc_zoom  # 135% zoom width (1080 * 1.35 = 1458)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_clip_and_captions.py -v`
Expected: FAIL (`AssertionError` on `1:00:00.00` and missing functions in `clip_processor`)

- [ ] **Step 3: Implement updates in `core/video_captioner.py` and `core/clip_processor.py`**

In `core/video_captioner.py`:
- Change `format_hook_card(hook_title, style_active_color="&H0000E6FF", persistent=False, duration_sec=3.2)` so `end_time = "1:00:00.00" if persistent else format_ass_time(duration_sec)`, removing the hardcoded `"SUL PROFILO DI SARA"` check and using a clean hook badge (`🔥 FOCUS` + `hook_title`).
- Change `POS_Y` in `STYLES` from `1420` to `1320` (TikTok safe zone).
- Update `generate_ass_file` and `burn_captions_to_video` to accept `brand_cta=None` and `brand_mention=None`, replacing `"👉 Trovi il link su @saradizdari_ecom"` with `f"👉 Segui {brand_mention}" if brand_mention else "👉 Guarda il link in bio sul profilo ufficiale"`, and defaulting `cta_text` to `"Guarda il video completo sul profilo!"` when `brand_cta` is empty.

In `core/clip_processor.py`:
- Implement `detect_smart_crop_mode(video_path, start_sec, duration)` sampling up to 8 frames with `ffmpeg` and checking faces with `cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')` if `cv2` is installed:
  - 1 dominant face cluster -> `{"mode": "face_crop", "center_x_ratio": median_x_ratio, "faces_detected": 1}`
  - 2 well-separated faces (`abs(x1 - x2) > 0.32`) in `>= 40%` of frames -> `{"mode": "split_screen", "left_x": x1, "right_x": x2, "faces_detected": 2}`
  - 0 faces or fallback -> `{"mode": "zoomed_blur", "center_x_ratio": 0.5, "faces_detected": 0}`
- Implement `compute_active_speech_segments(words, start_sec, end_sec, max_silence=0.45)` merging words separated by `<= max_silence` with `0.12s` padding around each spoken chunk.
- Implement `build_ffmpeg_filter_complex(crop_info, target_width=1080, target_height=1920, logo_path=None)`:
  - `face_crop`: `scale=-2:1920,crop=1080:1920:clamp((iw-1080)*center_x_ratio,0,iw-1080):0`
  - `split_screen`: top half `1080x960` on left speaker + bottom half `1080x960` on right speaker via `vstack`
  - `zoomed_blur`: blurred background `1080x1920` + foreground scaled to `1458:-2` (`135%` zoom) cropped to `1080` width so the center video fills ~65% of the vertical screen instead of a tiny postage stamp.
- Update `process_clip_ffmpeg` to accept `teaser_start=None, teaser_end=None, brand_mention=None, words_transcript=None`, prepending the `teaser_start..teaser_end` segment at `00:00` when provided, using `-preset veryfast`, and forwarding `brand_cta=cta_text` and `brand_mention=brand_mention` to `video_captioner.burn_captions_to_video()`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_clip_and_captions.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/clip_processor.py core/video_captioner.py tests/test_clip_and_captions.py
git commit -m "feat(render): add 9:16 smart crop, cold-open teaser, jump-cuts and clean non-persistent hook/CTA"
```

---

### Task 4: Pipeline di Clipping Intelligente e Pulizia Clip Cieche (`core/clipping_pipeline.py`)

**Files:**
- Modify: `core/clipping_pipeline.py:1-254`
- Test: `tests/test_clipping_pipeline.py`

**Interfaces:**
- Consumes: `local_viral_analyzer.analyze_video_locally`, `clip_processor.process_clip_ffmpeg`
- Produces:
  - `clipping_pipeline.load_ai_director_cuts(cuts_file: Path, video_name: str = None, campaign_id: str = None) -> list[dict]`
  - `clipping_pipeline.purge_legacy_blind_clips(root_dir: Path = None) -> dict` (removes blind fallback clips with `"transcript": "Estratto dal video originale"` from `clip_metadata.json` and `campaign_schedules.json`)
  - `clipping_pipeline.run_clipping_workflow(campaign_id, video_source_path=None, is_auto=True, task_logger=None, cuts_file=None) -> dict`

- [ ] **Step 1: Write the failing test in `tests/test_clipping_pipeline.py`**

```python
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import clipping_pipeline

def test_purge_legacy_blind_clips_cleans_metadata_and_schedules(tmp_path):
    meta_file = tmp_path / "clip_metadata.json"
    sched_file = tmp_path / "campaign_schedules.json"

    meta_data = {
        "blind_clip_1.mp4": {
            "filename": "blind_clip_1.mp4",
            "campaign_id": "camp1",
            "transcript": "Estratto dal video originale",
            "start_time": "00:10",
            "end_time": "00:45"
        },
        "smart_clip_1.mp4": {
            "filename": "smart_clip_1.mp4",
            "campaign_id": "camp1",
            "transcript": "Nel primo mese abbiamo generato 3.200 euro reali.",
            "start_time": "00:23.5",
            "end_time": "00:54.0"
        }
    }
    sched_data = {
        "camp1": {
            "target_count": 2,
            "slots": [
                {"time": "15:00", "video": "blind_clip_1.mp4"},
                {"time": "18:00", "video": "smart_clip_1.mp4"}
            ]
        }
    }
    meta_file.write_text(json.dumps(meta_data), encoding="utf-8")
    sched_file.write_text(json.dumps(sched_data), encoding="utf-8")

    res = clipping_pipeline.purge_legacy_blind_clips(tmp_path)
    assert res["removed_count"] == 1

    cleaned_meta = json.loads(meta_file.read_text(encoding="utf-8"))
    assert "blind_clip_1.mp4" not in cleaned_meta
    assert "smart_clip_1.mp4" in cleaned_meta

    cleaned_sched = json.loads(sched_file.read_text(encoding="utf-8"))
    assert cleaned_sched["camp1"]["slots"][0]["video"] == ""
    assert cleaned_sched["camp1"]["slots"][1]["video"] == "smart_clip_1.mp4"

def test_load_ai_director_cuts_reads_valid_json(tmp_path):
    cuts_path = tmp_path / "ai_director_cuts.json"
    cuts_payload = {
        "campaign_id": "camp1",
        "video_file": "source.mp4",
        "clips": [
            {
                "clip_number": 1,
                "start_time": "00:18.5",
                "end_time": "00:51.0",
                "teaser_start": "00:35.0",
                "teaser_end": "00:37.8",
                "hook_text": "12.400€ IN 60 GIORNI DA ZERO",
                "concept": "Risultato concreto",
                "transcript": "In sessanta giorni siamo arrivati a 12.400 euro.",
                "tiktok_caption": "Storia incredibile!"
            }
        ]
    }
    cuts_path.write_text(json.dumps(cuts_payload), encoding="utf-8")
    loaded = clipping_pipeline.load_ai_director_cuts(cuts_path, video_name="source.mp4", campaign_id="camp1")
    assert len(loaded) == 1
    assert loaded[0]["hook_text"] == "12.400€ IN 60 GIORNI DA ZERO"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_clipping_pipeline.py -v`
Expected: FAIL with `AttributeError: module 'clipping_pipeline' has no attribute 'purge_legacy_blind_clips'`

- [ ] **Step 3: Implement `load_ai_director_cuts`, `purge_legacy_blind_clips`, and update `run_clipping_workflow` in `core/clipping_pipeline.py`**

In `core/clipping_pipeline.py`:
- Implement `load_ai_director_cuts(cuts_file: Path, video_name: str = None, campaign_id: str = None) -> list[dict]`.
- Implement `purge_legacy_blind_clips(root_dir: Path = None) -> dict` which removes entries where `transcript == "Estratto dal video originale"` from `clip_metadata.json`, clears their slot assignments in `campaign_schedules.json`, and archives/deletes those blind `.mp4` files so the autopilot only publishes smart clips.
- In `run_clipping_workflow`:
  1. Check `cuts_file` (or `root / "ai_director_cuts.json"`) first;
  2. Otherwise call `local_viral_analyzer.analyze_video_locally(source_file, camp_data=camp_data, task_logger=task_logger)` (completely replacing the Playwright `gemini_analysis_bot` call and the blind `00:10-00:45` fallback!);
  3. Pass `teaser_start=clip.get("teaser_start")`, `teaser_end=clip.get("teaser_end")`, `cta_text=camp_cta`, `brand_mention=mentions_list[0] if mentions_list else None`, and `mode=clip.get("crop_mode", "auto")` to `clip_processor.process_clip_ffmpeg()`.
  4. Add CLI options `--cuts <file>` and `--purge-blind-clips` to `clipping_pipeline.py`.
- Execute `purge_legacy_blind_clips()` once on `C:\Users\Leo\Desktop\automazione-klippify\data` to clean the 68 legacy blind entries from `data/clip_metadata.json`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_clipping_pipeline.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/clipping_pipeline.py data/clip_metadata.json data/campaign_schedules.json tests/test_clipping_pipeline.py
git commit -m "feat(pipeline): wire AI director cuts & local viral analyzer and purge 68 legacy blind clips"
```

---

### Task 5: Auto-Riconoscimento Multi-PC su Antigravity (`GEMINI.md`, `AGENTS.md`, `.agents/skills/`, `setup_antigravity_cron.py`)

**Files:**
- Create: `core/setup_antigravity_cron.py`
- Create: `GEMINI.md`
- Create: `AGENTS.md`
- Create: `.agents/skills/klippify-ai-director/SKILL.md`
- Modify: `watcher_instructions.md`
- Test: `tests/test_antigravity_setup.py`

**Interfaces:**
- Consumes: `pathlib.Path`, `json`
- Produces:
  - `setup_antigravity_cron.install_or_update_sidecar(repo_root: Path = None, config_dir: Path = None, cron_expr: str = "CRON_TZ=Europe/Rome 0 */4 * * *") -> Path`
  - `GEMINI.md` and `AGENTS.md` in repository root
  - `.agents/skills/klippify-ai-director/SKILL.md`

- [ ] **Step 1: Write the failing test in `tests/test_antigravity_setup.py`**

```python
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))
import setup_antigravity_cron

def test_install_or_update_sidecar_writes_valid_portable_config(tmp_path):
    fake_repo = tmp_path / "MyKlippifyRepo"
    fake_repo.mkdir()
    fake_config = tmp_path / ".gemini" / "config"

    sidecar_path = setup_antigravity_cron.install_or_update_sidecar(
        repo_root=fake_repo,
        config_dir=fake_config,
        cron_expr="CRON_TZ=Europe/Rome 0 */4 * * *"
    )
    assert sidecar_path.exists()
    data = json.loads(sidecar_path.read_text(encoding="utf-8"))
    assert data["builtin"] == "schedule"
    assert data["restart_policy"] == "always"
    assert data["display_name"] == "Klippify AI Director (4h)"
    assert data["args"][0] == "CRON_TZ=Europe/Rome 0 */4 * * *"
    assert data["args"][1:4] == ["agentapi", "new-conversation", "--"]
    assert str(fake_repo).replace("\\", "/") in data["args"][4].replace("\\", "/")
    assert any(str(fake_repo).replace("\\", "/") in u.replace("\\", "/") for u in data["agent_permissions"]["workspace_uris"])

def test_workspace_rules_and_skill_files_exist_and_have_valid_frontmatter():
    gemini_md = REPO_ROOT / "GEMINI.md"
    agents_md = REPO_ROOT / "AGENTS.md"
    skill_md = REPO_ROOT / ".agents" / "skills" / "klippify-ai-director" / "SKILL.md"

    assert gemini_md.exists()
    assert agents_md.exists()
    assert skill_md.exists()

    skill_text = skill_md.read_text(encoding="utf-8")
    assert skill_text.startswith("---\nname: klippify-ai-director\n")
    assert "setup_antigravity_cron.py" in gemini_md.read_text(encoding="utf-8")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_antigravity_setup.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'setup_antigravity_cron'`

- [ ] **Step 3: Implement `core/setup_antigravity_cron.py`, `GEMINI.md`, `AGENTS.md`, `.agents/skills/klippify-ai-director/SKILL.md`, and update `watcher_instructions.md`**

1. In `core/setup_antigravity_cron.py`:
   - Implement `install_or_update_sidecar(repo_root=None, config_dir=None, cron_expr="CRON_TZ=Europe/Rome 0 */4 * * *") -> Path` writing `<config_dir>/sidecars/klippify-ai-director/sidecar.json` with:
     - `"builtin": "schedule"`
     - `"restart_policy": "always"`
     - `"display_name": "Klippify AI Director (4h)"`
     - `"args"` invoking `agentapi new-conversation --` with a self-contained prompt that points to `<repo_root>/.agents/skills/klippify-ai-director/SKILL.md`.
     - `"agent_permissions"` granting `workspace_uris` for `repo_root` and `access_grants` (`command(python)`, `command(ffmpeg)`, `command(ffprobe)`, `read_file(<repo_root>)`, `write_file(<repo_root>)`).
   - Run `install_or_update_sidecar()` when invoked from CLI (`python core/setup_antigravity_cron.py`).
2. Create `GEMINI.md` and `AGENTS.md` in the repo root explaining:
   - Automatic multi-PC bootstrap: whenever Antigravity opens this repository on any computer, check if `~/.gemini/config/sidecars/klippify-ai-director/sidecar.json` points to the current repo path; if not, run `python core/setup_antigravity_cron.py`.
   - How the AI Director workflow works and how to activate `.agents/skills/klippify-ai-director/SKILL.md`.
3. Create `.agents/skills/klippify-ai-director/SKILL.md` with YAML frontmatter (`name: klippify-ai-director`, `description: ...`) and the 4-step AI Director runbook:
   - Step 1: Audit rejections & analyze top-performing views in `data/klippify_submissions.json`;
   - Step 2: Inspect channels & run `python core/source_downloader.py --prepare-for-ai <video_path>` to get `<stem>_transcript.json` + 6 JPG sample frames;
   - Step 3: Read `<stem>_transcript.json` and view the sample frames with `read_file`, then write `data/ai_director_cuts.json` (with `teaser_start`, `teaser_end`, `start_time`, `end_time`, `crop_mode`, `hook_text`, `tiktok_caption`);
   - Step 4: Run `python core/clipping_pipeline.py <campaign_id> --video <video_path> --cuts data/ai_director_cuts.json`.

- [ ] **Step 4: Run all tests across the suite to verify everything passes**

Run: `python -m pytest tests/ -v`
Expected: ALL TESTS PASS

- [ ] **Step 5: Commit**

```bash
git add core/setup_antigravity_cron.py GEMINI.md AGENTS.md .agents/skills/klippify-ai-director/SKILL.md watcher_instructions.md tests/test_antigravity_setup.py
git commit -m "feat(antigravity): add portable GEMINI.md rules, klippify-ai-director skill and auto cron setup"
```
