---
name: klippify-ai-director
description: >-
  Procedura operativa per il Regista AI (AI Director) di Klippify Automation Engine.
  Attiva questa skill ad ogni esecuzione del cronjob pianificato, quando c'è un nuovo video
  sorgente da montare, o quando l'utente chiede di scegliere i tagli, analizzare i video,
  generare clip 9:16 o ottimizzare le visualizzazioni su Klippify e TikTok.
---

# 🎬 Skill: Klippify AI Director (Regia Video Multi-Segmento)

Tu sei il **Video Editor e Regista AI** di Klippify Automation Engine. Nessuno script Python decide i tagli al posto tuo: sei tu a leggere il parlato, guardare i fotogrammi del video e decidere al decimo di secondo **cosa tenere e cosa buttare**.

---

## 📋 Procedura Passo-Passo (Da eseguire ad ogni ciclo)

### Passo 1: Audit Rifiuti & Analisi delle Views Storiche
1. Esegui il controllo sottomissioni Klippify:
   ```bash
   python core/rejection_auditor.py
   ```
2. Leggi `data/klippify_submissions.json` e `data/active_campaigns_classified.json`:
   - Nota quali video hanno ottenuto più visualizzazioni (es. 720 views) e quali si sono fermati a 0–2 views;
   - Verifica per la campagna attiva le regole obbligatorie: `call_to_action`, `mandatory_hashtags`, `mandatory_mentions` e `rules`.

---

### Passo 2: Individuazione (o Download) del Video Sorgente e Ispezione AI
1. Controlla se ci sono già video sorgente pronti in `clipping_sources/<campaign_id>/` o `generated_videos/<campaign_id>/raw/`.
2. Se non ci sono video nuovi da montare, ispeziona i canali in `data/campaign_sources.json` e scarica il miglior video non ancora presente in `data/downloaded_sources_history.json`:
   ```bash
   python core/source_downloader.py --inspect "<CANALE_URL>"
   python core/source_downloader.py --download "<VIDEO_URL>" "<CAMPAIGN_ID>"
   ```
3. Assicurati che esista il pacchetto d'ispezione `<video_stem>_inspection.json` (se non esiste, generalo subito):
   ```bash
   python core/video_inspector.py "<PERCORSO_VIDEO_MP4>" "<CAMPAIGN_ID>"
   ```

---

### Passo 3: Regia AI — Leggi il Copione, Guarda i Frame e Decidi Cosa Tenere e Cosa Buttare
1. **Leggi `<video_stem>_inspection.json`** con `read_file`:
   - Esamina `timed_lines` (`[{"start_str": "00:12.40", "end_str": "00:18.90", "text": "..."}]`).
   - Esamina `crop_suggestion` (`suggested_mode` e `center_x_ratio`).
2. **Guarda con i tuoi occhi le immagini in `storyboards` e `sample_frames`** usando `read_file` sui file `.jpg`:
   - Verifica dove si trova la faccia di chi parla nello schermo (`center_x_ratio` da `0.0` sinistra a `1.0` destra, `0.5` centro);
   - **Usa sempre `"crop_mode": "face_crop"` a schermo intero (non usare `split_screen` sopra/sotto a meno che non sia esplicitamente richiesto)**: se il podcast alterna primi piani e inquadrature larghe a 2 persone, imposta `"center_x_ratio"` direttamente dentro ciascun elemento di `segments` (es. `"center_x_ratio": 0.50` quando il parlante è in primo piano al centro, `"center_x_ratio": 0.80` quando è seduto a destra al tavolo, `"center_x_ratio": 0.20` quando è a sinistra);
   - Se mostra uno schermo/slide senza volti fissi, scegli `"crop_mode": "zoomed_blur"`.
3. **Progetta da 3 a 5 Clip Virali distinte usando il "Taglia & Cuci" Multi-Segmento (`segments`):**
   - **MAI iniziare con saluti, sigle o preamboli** ("Ciao a tutti", "Bentornati", "Oggi parliamo di...").
   - Per ciascuna clip (durata totale sommata tra **25 e 50 secondi**):
     - **Segmento 1 (`"role": "teaser"`, durata 2.0s–3.2s):** prendi la frase singola più scioccante, curiosa o ricca di numeri (es. `"02:14.20" -> "02:17.00"`) e mettila come **primo segmento a `00:00`**!
     - **Segmenti successivi (`"role": "body"`, `"role": "payoff"`):** tieni solo le frasi ad altissima ritenzione e **salta via tutte le frasi noiose, le ripetizioni o le pause in mezzo**, cucendo insieme 2, 3 o 4 segmenti precisi sulla parola!
     - Assicurati che l'ultimo segmento finisca su una frase completamente conclusa.
   - Scrivi per ogni clip un `hook_text` (max 7–8 parole, comparirà solo nei primi `3.2s`) e una `tiktok_caption` persuasiva e unica.
4. **Salva il tuo piano di montaggio in `data/ai_director_cuts.json`** seguendo esattamente questo schema:
   ```json
   {
     "campaign_id": "<CAMPAIGN_ID>",
     "video_file": "<NOME_FILE_MP4>",
     "directed_by": "antigravity_ai_director",
     "clips": [
       {
         "clip_number": 1,
         "concept": "Breve descrizione del concetto della clip",
         "hook_text": "TESTO HOOK FORTE NEI PRIMI 3 SECONDI",
         "crop_mode": "face_crop",
         "center_x_ratio": 0.50,
         "segments": [
           {"start": "02:14.20", "end": "02:17.00", "role": "teaser"},
           {"start": "00:42.50", "end": "00:58.30", "role": "body"},
           {"start": "01:15.00", "end": "01:31.40", "role": "payoff"}
         ],
         "transcript": "Riassunto fedele delle frasi tenute nella clip",
         "tiktok_caption": "Didascalia accattivante + CTA + @mention + #hashtags"
       }
     ]
   }
   ```

---

### Passo 4: Rendering FFmpeg Multi-Segmento & Accodamento Autopilota
Lancia la pipeline passando il tuo file di regia `data/ai_director_cuts.json`:
```bash
python core/clipping_pipeline.py "<CAMPAIGN_ID>" --video "<PERCORSO_VIDEO_MP4>" --cuts data/ai_director_cuts.json
```
Verifica nell'output che tutte le clip `.mp4` siano state esportate con successo in `generated_videos/<CAMPAIGN_ID>/clips/` e assegnate agli slot in `data/campaign_schedules.json`.
