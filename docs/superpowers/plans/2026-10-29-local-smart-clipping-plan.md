# Antigravity AI-Piloted Video Editing & Multi-Segment Clipping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sostituire qualsiasi taglio automatico/casuale in Python con un motore di montaggio multi-segmento ("Taglia & Cuci") pilotato interamente dall'Agente AI di Antigravity, dotato di ispezione visiva (Storyboard JPG) + trascrizione timestampata e auto-configurazione portabile multi-PC tramite `GEMINI.md` e `.agents/skills/`.

**Architecture:** Il sistema separa nettamente **Percezione**, **Decisione (Regia AI)** ed **Esecuzione FFmpeg**:
1. **Percezione (`core/video_inspector.py` + `core/source_downloader.py`):** estrae dal video sorgente la trascrizione parola-per-parola coi timestamp (`.json3`/`.vtt` nativi da YouTube o `Faster-Whisper` int8) e genera **Storyboard JPG** (griglie di fotogrammi con timestamp `MM:SS` sovraimpresso + coordinate volti OpenCV) salvando tutto in `<video_stem>_inspection.json`.
2. **Decisione (`GEMINI.md` + `.agents/skills/klippify-ai-director/SKILL.md` + Cronjob Antigravity):** l'Agente AI di Antigravity legge `<video_stem>_inspection.json`, guarda le Storyboard JPG tramite `read_file`, decide **cosa tenere e cosa buttare** (anche componendo una singola clip da più segmenti staccati `segments: [{"start": ..., "end": ...}, ...]`) e scrive `data/ai_director_cuts.json`.
3. **Esecuzione (`core/clip_processor.py` + `core/video_captioner.py` + `core/clipping_pipeline.py`):** esegue alla lettera il piano `ai_director_cuts.json`, ritagliando in 9:16 secondo `crop_mode`/`center_x_ratio` indicati dall'AI, cucendo i segmenti, mostrando l'Hook solo nei primi `3.2s` e la CTA dinamica negli ultimi `3.0s`. Se un video non ha ancora il piano `ai_director_cuts.json`, non viene mai tagliato a caso ma preparato per l'AI (`status="awaiting_ai_director"`).

**Tech Stack:** Python 3.x, FFmpeg/FFprobe, `yt-dlp`, `faster-whisper` (int8 CPU), `opencv-python-headless`, `pytest`.

**Spec:** `docs/superpowers/specs/2026-10-29-local-smart-clipping-design.md`

## Global Constraints

- **Vietato qualsiasi taglio a caso o euristico autonomo:** Python non decide mai i tagli da solo; esegue esclusivamente i `segments` scritti dall'Agente AI in `ai_director_cuts.json` (se assenti, prepara `<video_stem>_inspection.json` + Storyboard JPG e restituisce `status="awaiting_ai_director"`).
- **Supporto Multi-Segmento ("Taglia & Cuci"):** ogni clip in `ai_director_cuts.json` può contenere una lista di `segments` (`[{"start": "02:14.2", "end": "02:17.1", "role": "teaser"}, {"start": "00:42.5", "end": "00:58.3", "role": "body"}, ...]`) per tenere solo le parti forti e scartare le parti noiose in mezzo.
- Il banner Hook superiore in `core/video_captioner.py` deve durare **solo i primi `3.2` secondi** (`persistent=False`), mai per tutto il video.
- La slide Outro CTA finale (ultimi `3.0s`–`3.5s`) deve usare dinamicamente la CTA e la menzione `@` della campagna attiva, rimuovendo l'hardcoding fisso su `@saradizdari_ecom`.
- Gli script `.bat` nella root devono usare `cd /d "%~dp0"` anziché percorsi cablati ad altri PC.

## Review Focus

1. **Sottotitoli `.json3`/`.vtt` con eventi vuoti o newline:** `parse_subtitle_file()` deve filtrare i token vuoti e produrre segmenti leggibili dall'AI con timestamp `[MM:SS.cc -> MM:SS.cc]`.
2. **Montaggio multi-segmento con lista `segments` di 2+ parti non contigue:** `build_multisegment_ffmpeg_cmd()` deve ritagliare ciascun segmento in 9:16 e concatenare video e audio (`concat=n=K:v=1:a=1`) senza desincronizzare l'audio.
3. **Campagna diversa da Sara Dizdari (o senza `@mention`):** `generate_ass_file()` non deve mai mostrare `@saradizdari_ecom` o `"SUL PROFILO DI SARA"` su altre campagne.
4. **Chiamata a `run_clipping_workflow` quando l'AI non ha ancora scritto `ai_director_cuts.json`:** non deve usare il vecchio fallback `00:10-00:45`, ma invocare `video_inspector.inspect_video()` e restituire `{"status": "awaiting_ai_director", "inspection_file": ...}`.
5. **Clonazione della repo su un altro PC con Antigravity:** `setup_antigravity_cron.py` deve generare `sidecar.json` con il percorso reale del PC corrente e `GEMINI.md` deve istruire l'agente ad auto-eseguirlo.

---

### Task 1: Portabilità `.bat`, Dipendenze e Modulo `core/video_inspector.py` (Trascrizione + Storyboard JPG per l'AI)

**Files:**
- Create: `requirements.txt`
- Create: `Installa_Dipendenze.bat`
- Modify: `AVVIA_KLIPPIFY_24H.bat:1-10`
- Modify: `core/source_downloader.py:170-260`
- Create: `core/video_inspector.py`
- Test: `tests/test_video_inspector.py`

**Interfaces:**
- Consumes: `yt_dlp`, `subprocess`, `json`, `cv2` (opzionale)
- Produces:
  - `video_inspector.parse_subtitle_file(sub_path: Path) -> list[dict]` (`[{"word": str, "start": float, "end": float}]`)
  - `video_inspector.group_words_into_timed_lines(words: list[dict], pause_sec: float = 0.4) -> list[dict]` (`[{"start": float, "end": float, "start_str": str, "end_str": str, "text": str}]`)
  - `video_inspector.generate_storyboards(video_path: Path, output_dir: Path, interval_sec: int = 12) -> list[str]`
  - `video_inspector.inspect_video(video_path: Path, campaign_id: str = "general") -> dict` (genera `<video_stem>_inspection.json` + `<video_stem>_storyboard_*.jpg` e restituisce il dizionario d'ispezione completo pronto da leggere per l'Agente AI)

- [ ] **Step 1: Write the failing test in `tests/test_video_inspector.py`**

```python
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import video_inspector

def test_parse_json3_and_group_into_timed_lines(tmp_path):
    sample_json3 = {
        "events": [
            {"tStartMs": 0, "dDurationMs": 1000, "segs": [{"utf8": "\n"}]},
            {
                "tStartMs": 1500,
                "dDurationMs": 1800,
                "segs": [
                    {"utf8": "Nel "},
                    {"utf8": "primo ", "tOffsetMs": 400},
                    {"utf8": "mese ", "tOffsetMs": 800},
                    {"utf8": "3.200€.", "tOffsetMs": 1200}
                ]
            },
            {
                "tStartMs": 5000,
                "dDurationMs": 1500,
                "segs": [
                    {"utf8": "Senza "},
                    {"utf8": "esperienza!", "tOffsetMs": 600}
                ]
            }
        ]
    }
    sub_file = tmp_path / "video.it.json3"
    sub_file.write_text(json.dumps(sample_json3), encoding="utf-8")

    words = video_inspector.parse_subtitle_file(sub_file)
    assert len(words) == 6
    lines = video_inspector.group_words_into_timed_lines(words, pause_sec=0.5)
    assert len(lines) == 2
    assert lines[0]["text"] == "Nel primo mese 3.200€."
    assert lines[0]["start"] == 1.5
    assert lines[1]["text"] == "Senza esperienza!"
    assert lines[1]["start"] == 5.0

def test_parse_vtt_subtitles(tmp_path):
    vtt = """WEBVTT

00:00:10.000 --> 00:00:13.000
Ecco cosa tenere nel montaggio.
"""
    vtt_file = tmp_path / "video.it.vtt"
    vtt_file.write_text(vtt, encoding="utf-8")
    words = video_inspector.parse_subtitle_file(vtt_file)
    assert [w["word"] for w in words] == ["Ecco", "cosa", "tenere", "nel", "montaggio."]
    assert words[0]["start"] == 10.0
    assert round(words[-1]["end"], 1) == 13.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_video_inspector.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'video_inspector'`

- [ ] **Step 3: Create `requirements.txt`, `Installa_Dipendenze.bat`, update `AVVIA_KLIPPIFY_24H.bat` and `core/source_downloader.py`, and implement `core/video_inspector.py`**

- Fix `AVVIA_KLIPPIFY_24H.bat` to use `cd /d "%~dp0"`.
- In `core/source_downloader.py`, add `'writesubtitles': True, 'writeautomaticsub': True, 'subtitleslangs': ['it', 'en'], 'subtitlesformat': 'json3/vtt'` to `ydl_opts` in `download_source_video()`, and automatically call `video_inspector.inspect_video(downloaded_file, campaign_id=campaign_id)` right after download.
- In `core/video_inspector.py`, implement:
  - `parse_subtitle_file(sub_path)` (`.json3` and `.vtt`/`.srt`);
  - `group_words_into_timed_lines(words, pause_sec=0.4)` grouping words into readable timestamped sentences for the AI Director;
  - `generate_storyboards(video_path, output_dir, interval_sec=12)` using FFmpeg (`fps=1/12,scale=320:180,drawtext=...:text='%{pts\:hms}',tile=4x4`) to create lightweight contact-sheet `.jpg` grids + sampling face coordinates (`center_x_ratio`) via OpenCV Haar cascade;
  - `inspect_video(video_path, campaign_id="general")` saving `<video_stem>_inspection.json` with `duration_sec`, `suggested_crop`, `storyboards`, `timed_lines` (`[MM:SS.d -> MM:SS.d] text`), and `words`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_video_inspector.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add requirements.txt Installa_Dipendenze.bat AVVIA_KLIPPIFY_24H.bat core/source_downloader.py core/video_inspector.py tests/test_video_inspector.py
git commit -m "feat(inspector): add video_inspector with timestamped transcript & storyboard generation for AI Director"
```

---

### Task 2: Esecutore FFmpeg Multi-Segmento ("Taglia & Cuci" AI) & Sottotitoli Puliti (`clip_processor.py` & `video_captioner.py`)

**Files:**
- Modify: `core/clip_processor.py:1-130`
- Modify: `core/video_captioner.py:130-315`
- Test: `tests/test_clip_and_captions.py`

**Interfaces:**
- Consumes: `subprocess`, `video_captioner`
- Produces:
  - `clip_processor.build_crop_filter(mode: str = "face_crop", center_x_ratio: float = 0.5, left_x: float = 0.3, right_x: float = 0.7, target_width: int = 1080, target_height: int = 1920) -> tuple[str, str]`
  - `clip_processor.build_multisegment_ffmpeg_cmd(input_video_path: Path, segments: list[dict], output_video_path: Path, mode: str = "face_crop", center_x_ratio: float = 0.5, logo_path: str = None) -> list[str]`
  - `clip_processor.process_clip_ffmpeg(input_video_path, start_time=None, end_time=None, output_video_path=None, mode="face_crop", center_x_ratio=0.5, segments=None, logo_path=None, hook_text=None, cta_text=None, brand_mention=None, target_width=1080, target_height=1920, logger=None) -> bool`
  - `video_captioner.format_hook_card(hook_title: str, style_active_color: str = "&H0000E6FF", persistent: bool = False, duration_sec: float = 3.2) -> list[str]`
  - `video_captioner.generate_ass_file(words, output_ass_path, duration_sec=35.0, style_key="hormozi_gold", use_emojis=True, hook_title=None, brand_cta=None, brand_mention=None)`

- [ ] **Step 1: Write the failing test in `tests/test_clip_and_captions.py`**

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import clip_processor
import video_captioner

def test_hook_card_disappears_after_3_2_seconds():
    events = video_captioner.format_hook_card("3.200€ NEL PRIMO MESE")
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
        {"word": "risultato", "start": 0.8, "end": 1.4},
    ]
    video_captioner.generate_ass_file(
        words=words,
        output_ass_path=ass_file,
        duration_sec=30.0,
        hook_title="IL RISULTATO REALE",
        brand_cta="Guarda il video completo al link in bio!",
        brand_mention="@millionhospitality"
    )
    content = ass_file.read_text(encoding="utf-8")
    assert "GUARDA IL VIDEO COMPLETO AL LINK IN BIO!" in content
    assert "@millionhospitality" in content
    assert "@saradizdari_ecom" not in content

def test_build_multisegment_ffmpeg_cmd_concatenates_ai_selected_segments(tmp_path):
    dummy_in = tmp_path / "in.mp4"
    dummy_out = tmp_path / "out.mp4"
    segments = [
        {"start": "02:10.5", "end": "02:13.0", "role": "teaser"},
        {"start": "00:30.0", "end": "00:45.0", "role": "body"},
        {"start": "01:12.0", "end": "01:28.5", "role": "payoff"}
    ]
    cmd = clip_processor.build_multisegment_ffmpeg_cmd(
        input_video_path=dummy_in,
        segments=segments,
        output_video_path=dummy_out,
        mode="face_crop",
        center_x_ratio=0.55
    )
    cmd_str = " ".join(cmd)
    assert "concat=n=3:v=1:a=1" in cmd_str
    assert "crop=" in cmd_str
    assert "-preset veryfast" in cmd_str

def test_build_crop_filter_supports_face_crop_split_screen_and_zoomed_blur():
    f_face, _ = clip_processor.build_crop_filter(mode="face_crop", center_x_ratio=0.6)
    assert "crop=1080:1920" in f_face

    f_split, _ = clip_processor.build_crop_filter(mode="split_screen", left_x=0.25, right_x=0.75)
    assert "vstack" in f_split

    f_zoom, _ = clip_processor.build_crop_filter(mode="zoomed_blur")
    assert "boxblur" in f_zoom and "1458" in f_zoom
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_clip_and_captions.py -v`
Expected: FAIL (`AssertionError` on `1:00:00.00` and missing functions in `clip_processor`)

- [ ] **Step 3: Implement updates in `core/video_captioner.py` and `core/clip_processor.py`**

In `core/video_captioner.py`:
- Change `format_hook_card(hook_title, style_active_color="&H0000E6FF", persistent=False, duration_sec=3.2)` so `end_time = "1:00:00.00" if persistent else format_ass_time(duration_sec)`, removing `"SUL PROFILO DI SARA"` hardcoding.
- Update `STYLES` `pos_y` to `1320` (TikTok safe zone).
- Update `generate_ass_file` and `burn_captions_to_video` to accept `brand_cta=None` and `brand_mention=None`, replacing `"👉 Trovi il link su @saradizdari_ecom"` with `f"👉 Segui {brand_mention}" if brand_mention else "👉 Scopri di più sul profilo ufficiale"`.

In `core/clip_processor.py`:
- Implement `build_crop_filter(mode="face_crop", center_x_ratio=0.5, left_x=0.3, right_x=0.7, target_width=1080, target_height=1920)` supporting:
  - `face_crop`: full-screen 9:16 vertical crop centered at `center_x_ratio`;
  - `split_screen`: top `1080x960` on `left_x` and bottom `1080x960` on `right_x` stacked vertically (`vstack`);
  - `zoomed_blur`: blurred 9:16 background + foreground zoomed to `1458` width (`135%`) cropped to `1080` width.
- Implement `build_multisegment_ffmpeg_cmd(input_video_path, segments, output_video_path, mode="face_crop", center_x_ratio=0.5, logo_path=None)` using `trim=start=...:end=...,setpts=PTS-STARTPTS` and `atrim=start=...:end=...,asetpts=PTS-STARTPTS` for each segment in `segments`, concatenating them with `concat=n=K:v=1:a=1[v_cat][a_cat]`, then applying the 9:16 crop filter and `-preset veryfast`.
- Update `process_clip_ffmpeg` to support `segments` list (or single `start_time`/`end_time`), `center_x_ratio`, and `brand_mention`, forwarding `brand_cta=cta_text` and `brand_mention=brand_mention` to `video_captioner.burn_captions_to_video()`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_clip_and_captions.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/clip_processor.py core/video_captioner.py tests/test_clip_and_captions.py
git commit -m "feat(render): add AI-piloted multi-segment FFmpeg cutter, 9:16 face crop and clean captions"
```

---

### Task 3: Pipeline Pilotata dall'AI (`clipping_pipeline.py`) & Pulizia delle 68 Clip Cieche

**Files:**
- Modify: `core/clipping_pipeline.py:1-254`
- Modify: `data/clip_metadata.json`
- Modify: `data/campaign_schedules.json`
- Test: `tests/test_clipping_pipeline.py`

**Interfaces:**
- Consumes: `video_inspector.inspect_video`, `clip_processor.process_clip_ffmpeg`
- Produces:
  - `clipping_pipeline.load_ai_director_cuts(cuts_file: Path, video_name: str = None, campaign_id: str = None) -> list[dict]`
  - `clipping_pipeline.purge_legacy_blind_clips(root_dir: Path = None) -> dict`
  - `clipping_pipeline.run_clipping_workflow(campaign_id, video_source_path=None, is_auto=True, task_logger=None, cuts_file=None) -> dict`

- [ ] **Step 1: Write the failing test in `tests/test_clipping_pipeline.py`**

```python
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
import clipping_pipeline

def test_purge_legacy_blind_clips_removes_all_hardcoded_fallback_entries(tmp_path):
    meta_file = tmp_path / "clip_metadata.json"
    sched_file = tmp_path / "campaign_schedules.json"

    meta_data = {
        "blind_1.mp4": {
            "filename": "blind_1.mp4",
            "campaign_id": "camp1",
            "transcript": "Estratto dal video originale",
            "start_time": "00:10",
            "end_time": "00:45"
        },
        "ai_directed_1.mp4": {
            "filename": "ai_directed_1.mp4",
            "campaign_id": "camp1",
            "transcript": "In 30 giorni abbiamo raggiunto 3.200 euro.",
            "segments": [{"start": "02:10", "end": "02:13"}, {"start": "00:40", "end": "01:08"}]
        }
    }
    sched_data = {
        "camp1": {
            "target_count": 2,
            "slots": [
                {"time": "15:00", "video": "blind_1.mp4"},
                {"time": "18:00", "video": "ai_directed_1.mp4"}
            ]
        }
    }
    meta_file.write_text(json.dumps(meta_data), encoding="utf-8")
    sched_file.write_text(json.dumps(sched_data), encoding="utf-8")

    res = clipping_pipeline.purge_legacy_blind_clips(tmp_path)
    assert res["removed_count"] == 1
    cleaned_meta = json.loads(meta_file.read_text(encoding="utf-8"))
    assert "blind_1.mp4" not in cleaned_meta
    assert "ai_directed_1.mp4" in cleaned_meta

def test_workflow_without_ai_cuts_does_not_cut_blindly_and_prepares_inspection(tmp_path, monkeypatch):
    monkeypatch.setattr(clipping_pipeline.paths, "PROJECT_ROOT", tmp_path)
    raw_dir = tmp_path / "clipping_sources" / "camp_test"
    raw_dir.mkdir(parents=True)
    dummy_vid = raw_dir / "source_video.mp4"
    dummy_vid.write_bytes(b"00" * 1024)

    monkeypatch.setattr(
        clipping_pipeline.video_inspector,
        "inspect_video",
        lambda vp, campaign_id="general": {"inspection_file": str(tmp_path / "source_video_inspection.json")}
    )

    res = clipping_pipeline.run_clipping_workflow("camp_test", video_source_path=str(dummy_vid))
    assert res["status"] == "awaiting_ai_director"
    assert "inspection_file" in res
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_clipping_pipeline.py -v`
Expected: FAIL (`AttributeError: module 'clipping_pipeline' has no attribute 'purge_legacy_blind_clips'`)

- [ ] **Step 3: Implement `core/clipping_pipeline.py` and run `purge_legacy_blind_clips()` on `data/`**

In `core/clipping_pipeline.py`:
- Remove `import gemini_analysis_bot` and remove the blind fallback (`00:10-00:45`, `01:00-01:35`, `02:00-02:35`).
- Import `video_inspector`.
- Implement `load_ai_director_cuts(cuts_file, video_name=None, campaign_id=None)`.
- Implement `purge_legacy_blind_clips(root_dir=None)`.
- In `run_clipping_workflow(campaign_id, video_source_path=None, is_auto=True, task_logger=None, cuts_file=None)`:
  - Look for AI Director cuts in `cuts_file` or `root / "ai_director_cuts.json"`.
  - If no AI cuts exist for this video/campaign, run `insp = video_inspector.inspect_video(source_file, campaign_id=str(campaign_id))` and return `{"status": "awaiting_ai_director", "campaign_id": campaign_id, "video_file": str(source_file), "inspection_file": insp.get("inspection_file")}` — **never** cutting blindly!
  - When AI cuts exist, iterate through `analysis_results` passing `segments=clip.get("segments")`, `mode=clip.get("crop_mode", "face_crop")`, `center_x_ratio=clip.get("center_x_ratio", 0.5)`, `hook_text=hook_t`, `cta_text=camp_cta`, and `brand_mention=mentions_list[0] if mentions_list else None` to `clip_processor.process_clip_ffmpeg()`.
  - Only delete the raw source video (`storage_manager.delete_raw_source_after_clipping`) after AI-directed clips have actually been rendered.
- Run `python core/clipping_pipeline.py --purge-blind-clips` to clean the 68 blind entries from `data/clip_metadata.json` and `data/campaign_schedules.json`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_clipping_pipeline.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/clipping_pipeline.py data/clip_metadata.json data/campaign_schedules.json tests/test_clipping_pipeline.py
git commit -m "feat(pipeline): enforce AI-director-only cuts, add multi-segment support and purge 68 blind clips"
```

---

### Task 4: Auto-Riconoscimento Multi-PC su Antigravity (`GEMINI.md`, `AGENTS.md`, `.agents/skills/klippify-ai-director/SKILL.md`, `core/setup_antigravity_cron.py`)

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
    fake_repo = tmp_path / "KlippifyOnOldLaptop"
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
    assert "ai_director_cuts.json" in skill_text
    assert "setup_antigravity_cron.py" in gemini_md.read_text(encoding="utf-8")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_antigravity_setup.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'setup_antigravity_cron'`

- [ ] **Step 3: Implement `core/setup_antigravity_cron.py`, `GEMINI.md`, `AGENTS.md`, `.agents/skills/klippify-ai-director/SKILL.md`, and update `watcher_instructions.md`**

- Implement `core/setup_antigravity_cron.py` so running `python core/setup_antigravity_cron.py` creates/updates `~/.gemini/config/sidecars/klippify-ai-director/sidecar.json` dynamically using the local repository path on whichever PC it runs on.
- Write `GEMINI.md` and `AGENTS.md` in the repo root instructing any Antigravity agent that opens this workspace to:
  1. Check if `~/.gemini/config/sidecars/klippify-ai-director/sidecar.json` matches the current workspace path; if not, run `python core/setup_antigravity_cron.py`;
  2. Never allow blind cuts; always act as the **AI Video Director** following `.agents/skills/klippify-ai-director/SKILL.md`: inspect `<video_stem>_inspection.json` + view `<video_stem>_storyboard_*.jpg` with `read_file`, decide which exact segments (`segments`) to keep and which to discard, write `data/ai_director_cuts.json`, and run `python core/clipping_pipeline.py <campaign_id> --video <video_path> --cuts data/ai_director_cuts.json`.
- Write `.agents/skills/klippify-ai-director/SKILL.md` and update `watcher_instructions.md`.

- [ ] **Step 4: Run the full test suite to verify everything passes**

Run: `python -m pytest tests/ -v`
Expected: ALL TESTS PASS

- [ ] **Step 5: Commit and push to GitHub**

```bash
git add core/setup_antigravity_cron.py GEMINI.md AGENTS.md .agents/skills/klippify-ai-director/SKILL.md watcher_instructions.md tests/test_antigravity_setup.py
git commit -m "feat(antigravity): add portable GEMINI.md rules, klippify-ai-director skill and auto cron setup"
```
