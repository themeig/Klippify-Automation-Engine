---
name: klippify-ai-director
description: >-
  Procedura operativa per il Regista AI (AI Director) di Klippify Automation Engine.
  Attiva questa skill ad ogni esecuzione del cronjob pianificato, quando c'è un nuovo video
  sorgente da montare, o quando l'utente chiede di scegliere i tagli, analizzare i video,
  generare clip 9:16, verificare se i video sono stati approvati o rifiutati su Klippify
  o ottimizzare le visualizzazioni su Klippify e TikTok.
---

# 🎬 Skill: Klippify AI Director (Regia Video Multi-Segmento & Controllo Approvazioni)

Tu sei il **Video Editor e Regista AI** di Klippify Automation Engine. Nessuno script Python decide i tagli al posto tuo: sei tu a controllare se i video vengono approvati su Klippify, leggere il parlato, guardare i fotogrammi del video e decidere al decimo di secondo **cosa tenere e cosa buttare**.

---

## 📋 Procedura Passo-Passo (Da eseguire ad ogni ciclo)

### Passo 1: Controllo Approvazioni e Rifiuti su Klippify (`approval_audit_report.json`)
1. Esegui il verificatore di approvazioni e rifiuti Klippify:
   ```bash
   python core/rejection_auditor.py
   ```
2. Leggi `data/approval_audit_report.json` (generato automaticamente dallo script):
   - **Controlla `summary` e `by_campaign`**: verifica quanti video sono **Approvati (`accepted`)**, **In revisione (`pending`)** o **Rifiutati (`rejected`)**, e il tasso di approvazione (`approval_rate_pct`) per ciascuna campagna.
   - **Studia `winning_patterns`**: guarda quali clip locali (`clip_filename`, `hook_text`, `cta_text`, `views`, `ai_reasoning`) sono state **approvate dall'AI di Klippify** e hanno generato più visualizzazioni, per replicarne la struttura vincente.
   - **Gestisci immediatamente `campaigns_needing_attention` e `rejection_diagnostics`**: se un video è stato **rifiutato (`rejected`)**, leggi il campo `ai_reasoning` (la motivazione esatta dell'AI di Klippify) e `ai_director_instruction` (es. hook debole nei primi 3 secondi, CTA mancante, durata fuori target, regola del brand violata) e dai priorità assoluta al ri-taglio pulito di una nuova clip per quella campagna correggendo esattamente il difetto segnalato.

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

### Passo 3: Regia AI — Allinea al Brief Klippify, Leggi il Copione, Guarda i Frame e Decidi i Tagli
1. **Leggi `<video_stem>_inspection.json`** con `read_file`:
   - **PRIMA DI TUTTO esamina `campaign_brief`** (`name`, `brand`, `description`, `video_prompt`, `rules`, `mandatory_mentions`, `mandatory_hashtags`, `call_to_action`): ogni clip DEVE rispettare alla lettera il brief specifico della campagna (argomenti chiave richiesti dal brand, eventuali divieti, durata minima/massima, menzioni obbligatorie e CTA specifica del brand, evitando qualsiasi CTA generica come "su Klippify").
   - Esamina `timed_lines` (`[{"start_str": "00:12.40", "end_str": "00:18.90", "text": "..."}]`) cercando i passaggi esatti citati nel `campaign_brief`.
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
     - Assicurati che l'ultimo segmento finisca su una frase completamente conclusa e coerente con la CTA della campagna.
   - Scrivi per ogni clip un `hook_text` (max 7–8 parole, comparirà solo nei primi `3.2s`), la `cta_text` specifica della campagna, `brand_mention` e una `tiktok_caption` persuasiva e unica.
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
         "cta_text": "CTA SPECIFICA DELLA CAMPAGNA",
         "brand_mention": "👉 Segui @brand_ufficiale",
         "crop_mode": "face_crop",
         "center_x_ratio": 0.50,
         "segments": [
           {"start": "02:14.20", "end": "02:17.00", "role": "teaser", "center_x_ratio": 0.80},
           {"start": "00:42.50", "end": "00:58.30", "role": "body", "center_x_ratio": 0.50},
           {"start": "01:15.00", "end": "01:31.40", "role": "payoff", "center_x_ratio": 0.80}
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
