# Design: Regia Video Pilotata dall'AI di Antigravity ("AI Director" Multi-Segmento)

**Data:** 2026-10-29  
**Progetto:** `Klippify-Automation-Engine` (`C:\Users\Leo\Desktop\automazione-klippify`)  
**Dimensione:** Progetto (Sostituzione del taglio automatico cieco con montaggio "Taglia & Cuci" pilotato interamente dall'Agente AI di Antigravity)

---

## 1. Intento e Motivazione (Il "Perché")

Il sistema precedente ha generato ~200 video senza mai superare le 1.000 visualizzazioni perché:
1. `core/gemini_analysis_bot.py` falliva nel caricare file `.mp4` via browser (`"clips": []`) e `core/clipping_pipeline.py` ripiegava su un fallback cieco (`00:10-00:45`, `01:00-01:35`, `02:00-02:35`).
2. Anche quando tagliava un segmento, prendeva un blocco unico contiguo di 35 secondi senza poter tagliare via le frasi noiose in mezzo, rimpiccioliva il 16:9 al centro su sfondo sfocato e teneva fisso per tutto il video il banner promozionale `🎓 LEZIONE GRATUITA / SUL PROFILO DI SARA`.

**Cosa vuole l'utente:**
- **Zero scelte "a caso" o euristiche in Python:** gli script Python locali **non** devono decidere da soli cosa tagliare.
- **È l'Agente AI di Antigravity (svegliato da un Cronjob o su comando) a pilotare il video e decidere cosa tenere e cosa buttare**, leggendo la trascrizione parola-per-parola e guardando i fotogrammi del video tramite i suoi strumenti nativi.
- **Portabilità Totale Multi-PC:** scaricando la stessa repository da GitHub su un altro computer con Antigravity (il portatile dedicato), l'agente su quel PC deve capire immediatamente e in automatico cosa fare grazie a `GEMINI.md` e `.agents/skills/`.

---

## 2. Obiettivi, Non-Obiettivi e Anti-Obiettivi

### Obiettivi (Goals)
- **Regia 100% guidata dall'AI di Antigravity:** nessuna clip viene generata senza una decisione esplicita dell'Agente AI salvata nel piano di montaggio (`data/ai_director_cuts.json`).
- **Ispezione Audio + Visiva per l'Agente (`core/video_inspector.py`):** fornire all'Agente AI il trascritto completo coi timestamp al centesimo di secondo e le **Storyboard JPG (griglie di fotogrammi col timestamp sovraimpresso)** così l'Agente AI vede chi parla, dove si trova nello schermo e cosa succede in ogni secondo del video.
- **Montaggio Multi-Segmento ("Taglia & Cuci" chirurgico):** permettere all'Agente AI di comporre una singola clip cucendo insieme più segmenti non contigui del video (`segments: [{"start": ..., "end": ...}, ...]`), così da:
  - mettere in testa (`00:00`) i 2–3 secondi più forti come *Teaser*,
  - tenere solo le frasi ad altissima ritenzione e **buttare via le frasi deboli, le digressioni o le pause** anche se si trovano a metà discorso!
- **Inquadratura 9:16 pilotata dall'AI + Grafica Pulita:**
  - L'AI, guardando la Storyboard JPG (coadiuvata dalle coordinate rilevate da OpenCV), indica per ciascun segmento il crop 9:16 (`face_crop` con coordinata X del parlante, `split_screen` per 2 persone, o `zoomed_blur` ingrandito al 135%).
  - Hook testuale mostrato **solo nei primi 3.2 secondi** (mai fisso per tutto il video).
  - Slide Outro CTA mostrata **solo negli ultimi 3 secondi** con i dati reali della campagna attiva (rimosso l'hardcoding su `@saradizdari_ecom`).
- **Auto-Riconoscimento su qualsiasi Antigravity (`GEMINI.md` + `.agents/skills/` + `setup_antigravity_cron.py`):** clonando la repo su un altro PC, l'agente Antigravity locale carica automaticamente le regole e la skill del Regista AI e configura il proprio cronjob con i percorsi del nuovo PC.

### Anti-Obiettivi
- **Vietato qualsiasi taglio automatico "di ripiego" o a caso:** se l'AI di Antigravity non ha ancora scritto il piano di taglio per un video, lo script Python **non** deve inventare timestamp con regole fisse né usare fallback `00:10-00:45`; deve preparare il pacchetto di ispezione e attendere la regia dell'AI.

---

## 3. Architettura Dettagliata della Soluzione

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. VIDEO INSPECTOR (core/video_inspector.py)                                │
│    - Estrae trascrizione parola-per-parola coi timestamp (.json3/vtt/whisper)│
│    - Genera Storyboard JPG (griglie di frame col timestamp + coord. volti)   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ 2. AGENTE AI ANTIGRAVITY (Cronjob + .agents/skills/klippify-ai-director)    │
│    - Legge il copione timestampato e GUARDA le Storyboard JPG (read_file)    │
│    - Decide esattamente COSA TENERE e COSA BUTTARE (lista di `segments`)     │
│    - Sceglie Teaser, Crop 9:16, Hook e Caption -> salva `ai_director_cuts`  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ 3. ESECUTORE FFMPEG MULTI-SEGMENTO (core/clip_processor.py + captioner)     │
│    - Taglia e cuce insieme i `segments` scelti dall'AI in 9:16              │
│    - Applica Hook (solo primi 3.2s), Sottotitoli e CTA dinamica (ultimi 3s) │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Modulo 1: `core/video_inspector.py` (Occhi e Orecchie per l'AI)
Quando viene scaricato un nuovo video sorgente (o tramite `python core/video_inspector.py <video_path>`):
1. **Estrazione Trascrizione Precisa:**
   - Se `source_downloader.py` ha scaricato i sottotitoli nativi YouTube (`.json3` / `.vtt`), li converte istantaneamente (0s CPU) in segmenti e parole timestampate.
   - Se il video non ha sottotitoli nativi, esegue `Faster-Whisper (int8, vad_filter=True)` salvando la trascrizione in `<video_stem>_inspection.json`.
2. **Generazione Storyboard Visiva per l'AI (`<video_stem>_storyboard_1.jpg`, ...):**
   - Estrae 1 fotogramma ogni 10–15 secondi con FFmpeg stampando su ciascun fotogramma il timestamp esatto (`MM:SS`) e una griglia graduata X (`0.0 ... 0.5 ... 1.0`), componendoli in 1–2 immagini Storyboard compatte (`4x4` tile).
   - Se OpenCV è presente, annota nel file `<video_stem>_inspection.json` anche le coordinate medie dei volti rilevati (`suggested_center_x_ratio`), così l'Agente AI vede sia a occhio nudo nelle Storyboard sia numericamente dove si trova chi parla.

### 3.2 Modulo 2: Schema di Regia Multi-Segmento (`data/ai_director_cuts.json`)
L'Agente AI di Antigravity pilota il montaggio scrivendo `data/ai_director_cuts.json` con questo formato:
```json
{
  "campaign_id": "6a71c6f7245627c68999eae2",
  "video_file": "nome_video_sorgente.mp4",
  "directed_by": "antigravity_ai_director",
  "clips": [
    {
      "clip_number": 1,
      "concept": "Come ha generato i primi 3.200€ partendo da zero",
      "hook_text": "3.200€ NEL PRIMO MESE PARTENDO DA ZERO",
      "crop_mode": "face_crop",
      "center_x_ratio": 0.52,
      "segments": [
        {"start": "02:14.20", "end": "02:17.10", "role": "teaser"},
        {"start": "00:42.50", "end": "00:58.30", "role": "body"},
        {"start": "01:15.00", "end": "01:31.40", "role": "payoff"}
      ],
      "tiktok_caption": "Ha iniziato con 0 esperienza e 2 ore la sera... Ecco cosa è successo in 30 giorni! 🚀 Scopri la lezione gratuita sul profilo di @saradizdari_ecom #saradizdari #ecommerce #klippify"
    }
  ]
}
```
Grazie all'array `segments`, l'AI può:
- mettere come primo elemento il **Teaser** (2–3s presi dal momento clou);
- saltare qualsiasi parte debole, saluto o digressione a metà discorso, **tenendo solo le frasi che contano** e cucendole insieme senza tempi morti.

### 3.3 Modulo 3: Esecutore FFmpeg Multi-Segmento & Sottotitoli Puliti (`core/clip_processor.py` + `core/video_captioner.py`)
1. **Taglia & Cuci Multi-Segmento (`process_clip_ffmpeg`):**
   - Accetta sia `segments=[{"start": ..., "end": ...}, ...]` (modalità multi-segmento AI) sia `start_time`/`end_time` singoli.
   - Per ogni segmento in `segments`, estrae e ritaglia in 9:16 (`1080x1920`) secondo `crop_mode` (`face_crop` centrato su `center_x_ratio`, `split_screen` o `zoomed_blur` ingrandito al 135%) e li concatena in un unico flusso fluido con FFmpeg (`concat=n=K:v=1:a=1`, `-preset veryfast`).
2. **Sottotitoli e Grafica Anti-Spot (`video_captioner.py`):**
   - L'Hook Card superiore (`hook_text`) compare a `0:00:00.00` e **scompare a `0:00:03.20`** (`persistent=False`).
   - I sottotitoli dinamici parola-per-parola vengono generati sull'audio già montato della clip finale (così i timestamp delle parole combaciano al millisecondo anche dopo aver cucito più segmenti diversi!).
   - La slide Outro CTA compare solo negli ultimi `3.0s` usando dinamicamente la CTA e la menzione `@` della campagna attiva.

### 3.4 Modulo 4: Blocco Anti-Taglio Cieco (`core/clipping_pipeline.py`)
- Rimosso completamente il fallback cieco (`00:10-00:45`, `01:00-01:35`, `02:00-02:35`) e rimosso `gemini_analysis_bot.py` basato su Playwright.
- Quando viene chiamato `run_clipping_workflow(campaign_id, video_source_path, cuts_file=None)`:
  - Se esiste il piano di taglio dell'AI (`cuts_file` o `data/ai_director_cuts.json` corrispondente al video), esegue immediatamente il montaggio multi-segmento FFmpeg delle clip decise dall'AI.
  - Se il video **non** è ancora stato analizzato dall'AI di Antigravity, esegue automaticamente `video_inspector.inspect_video(source_file)` per preparare trascrizione e Storyboard JPG e restituisce `"status": "awaiting_ai_director"` (senza mai tagliare a caso!).
- Include inoltre `purge_legacy_blind_clips()` per ripulire da `data/clip_metadata.json` e `data/campaign_schedules.json` le 68 vecchie clip tagliate a `00:10-00:45`.

### 3.5 Modulo 5: Portabilità Automatica Multi-PC (`GEMINI.md`, `AGENTS.md`, `.agents/skills/klippify-ai-director/SKILL.md`, `core/setup_antigravity_cron.py`)
- **`GEMINI.md` e `AGENTS.md` (nella radice Git):** caricati automaticamente da qualsiasi Antigravity appena clona la repository. Istruiscono l'agente a verificare/installare il cronjob locale (`python core/setup_antigravity_cron.py`) e a usare la skill `.agents/skills/klippify-ai-director/SKILL.md`.
- **`.agents/skills/klippify-ai-director/SKILL.md`:** istruisce l'Agente AI passo-passo su come:
  1. Controllare rifiuti e views in `data/klippify_submissions.json`;
  2. Scaricare nuovi video e lanciare `python core/video_inspector.py <video_path>`;
  3. Leggere `<video_stem>_inspection.json` e guardare con `read_file` le `<video_stem>_storyboard_*.jpg`;
  4. Decidere cosa tenere e cosa buttare scrivendo `data/ai_director_cuts.json` (con `segments` multipli, `crop_mode`, `center_x_ratio`, `hook_text`, `tiktok_caption`);
  5. Lanciare `python core/clipping_pipeline.py <campaign_id> --video <video_path> --cuts data/ai_director_cuts.json` per produrre i `.mp4` finiti e metterli in coda all'autopilota.
