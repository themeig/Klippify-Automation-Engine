# 🧠 Klippify Automation Engine — Istruzioni Automatiche per l'Agente Antigravity

Questo file (`GEMINI.md`) viene caricato **automaticamente** da qualsiasi istanza di Antigravity su qualsiasi computer non appena apri o cloni questa repository da GitHub.

## ⚡ 1. Auto-Configurazione Multi-PC (Esegui subito su un nuovo computer)
Quando apri questa repository su un nuovo computer (es. il portatile dedicato):
1. Verifica se il cronjob nativo di Antigravity `~/.gemini/config/sidecars/klippify-ai-director/sidecar.json` esiste e punta al percorso assoluto di questa cartella su questo PC.
2. Se non esiste o punta al percorso di un altro computer, esegui immediatamente:
   ```bash
   python core/setup_antigravity_cron.py
   ```
   Questo comando registra l'automazione **`Klippify AI Director (4h)`** adattando automaticamente tutti i percorsi al PC corrente.

## 🎬 2. Regola Fondamentale: L'Agente AI è l'Unico Video Editor (Vietati i Tagli Ciechi)
- **Nessuno script Python locale deve decidere da solo o a caso dove tagliare i video.**
- Sei **TU (l'Agente AI di Antigravity)** a pilotare il montaggio video leggendo la trascrizione parola-per-parola e guardando le Storyboard JPG del video tramite `read_file`.
- Quando l'utente ti chiede di analizzare/montare un video, o quando vieni attivato dal Cronjob ogni 4 ore, **leggi e segui sempre la skill di progetto**:
  👉 [`.agents/skills/klippify-ai-director/SKILL.md`](.agents/skills/klippify-ai-director/SKILL.md)

## 🛠️ 3. Architettura Rapida del Motore AI-Piloted
1. **Ispezione Video (`core/video_inspector.py`):**
   ```bash
   python core/video_inspector.py "<percorso_video.mp4>" "<campaign_id>"
   ```
   Genera `<video_stem>_inspection.json` (con tutte le frasi timestampate `[MM:SS.cc -> MM:SS.cc]`) e le griglie visive `<video_stem>_storyboard.jpg` + 6 frame JPG campione.
2. **Decisione Regia AI (`data/ai_director_cuts.json`):**
   Tu leggi `<video_stem>_inspection.json`, guardi i frame JPG con `read_file` e scrivi `data/ai_director_cuts.json` specificando per ciascuna clip:
   - `segments`: lista di segmenti da **tenere e cucire insieme** (`[{"start": "...", "end": "...", "role": "teaser"}, {"start": "...", "end": "...", "role": "body"}, ...]`), saltando saluti, parti noiose, pause o digressioni anche a metà discorso;
   - `crop_mode`: `"face_crop"` (con `center_x_ratio` tra `0.0` e `1.0` centrato sul volto visto nei frame), `"split_screen"` (per 2 persone), oppure `"zoomed_blur"` (zoom 135%);
   - `hook_text`: titolo punchline (visibile **solo nei primi 3.2 secondi**, mai fisso per tutto il video);
   - `tiktok_caption`: didascalia completa con CTA, `@mention` e `#hashtag` della campagna.
3. **Esecuzione Taglia & Cuci FFmpeg (`core/clipping_pipeline.py`):**
   ```bash
   python core/clipping_pipeline.py "<campaign_id>" --video "<percorso_video.mp4>" --cuts data/ai_director_cuts.json
   ```
   Esegue il montaggio multi-segmento 9:16 con FFmpeg (`-preset veryfast`), applica i sottotitoli dinamici e la slide CTA finale (ultimi 3s) e carica le clip negli slot di `autopilot_engine.py`.
