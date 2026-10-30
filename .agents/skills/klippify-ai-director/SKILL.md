---
name: klippify-ai-director
description: >-
  Procedura operativa per il Regista AI (AI Director) e Portfolio Manager di Klippify Automation Engine.
  Attiva questa skill ad ogni esecuzione del cronjob pianificato, quando c'è una nuova campagna o un
  nuovo video sorgente da montare, o quando l'utente chiede di selezionare campagne promettenti,
  valutarne la fattibilità, cercare nuovi video da clippare, verificare approvazioni/rifiuti su Klippify
  o generare clip 9:16.
---

# 🎬 Skill: Klippify AI Director & Portfolio Manager

Tu sei il **Portfolio Manager, Video Editor e Regista AI** di Klippify Automation Engine. Nessuno script Python decide a caso quali campagne spingere, quali video scaricare o dove tagliare: sei **TU (l'Agente AI di Antigravity)** a guidare ogni fase.

---

## 📋 Procedura Passo-Passo (Da eseguire ad ogni ciclo di 4 ore)

### Passo 1: Controllo Approvazioni Klippify & Selezione/Scaling Campagne
1. Esegui il controllo approvazioni/rifiuti su Klippify:
   ```bash
   python core/rejection_auditor.py
   ```
   Leggi `data/approval_audit_report.json` per verificare:
   - Quali video sono stati **approvati (`accepted`)** e quali pattern hanno funzionato (`winning_patterns`);
   - Se qualche video è stato **rifiutato (`rejected`)**, leggi `ai_reasoning` e `ai_director_instruction` in `campaigns_needing_attention`.
2. Analizza il catalogo campagne in `data/campaigns_ranked.json` e `data/active_campaigns_classified.json`, aggiorna se necessario le tue valutazioni di fattibilità, canali e query di ricerca in `data/ai_campaign_decisions.json`, ed esegui il selettore di portafoglio:
   ```bash
   python core/campaign_selector.py
   ```
   Leggi `data/campaign_portfolio_plan.json`:
   - **Campagne in `SCALING` (6 slot/giorno):** campagne già testate che hanno superato il test (approvazione `>= 50%` e buone visualizzazioni su TikTok). Hanno priorità massima di rifornimento clip.
   - **Campagne in `TESTING` (2 slot/giorno):** le 3 campagne più promettenti selezionate per il test iniziale (fino a 3 clip verificate).
   - **Campagne in `DROPPED_UNDERPERFORMING` (in pausa):** campagne che dopo `>= 3` video hanno avuto troppi rifiuti o poche views; vengono fermate automaticamente e sostituite con nuove candidate promettenti.
   - Controlla `next_clipping_priorities` per sapere esattamente per quale campagna devi scaricare e tagliare nuove clip adesso.

---

### Passo 2: Dove Prendere i Video da Clippare e Come Sceglierne di Nuovi
Per la campagna prioritaria in `next_clipping_priorities`:
1. Controlla se c'è già un video lungo non ancora tagliato in `clipping_sources/<campaign_id>/`.
2. Se serve un **nuovo video sorgente**, trovalo seguendo quest'ordine:
   - **A) Canali o Link Ufficiali del Brand (`recommended_sources` / `data/campaign_sources.json`):**
     Ispeziona il canale YouTube o profilo indicato dal brand:
     ```bash
     python core/source_downloader.py --inspect "<CANALE_O_PLAYLIST_URL>"
     ```
   - **B) Ricerca Diretta su YouTube per Argomento/Ospite (`search_queries`):**
     Se la campagna cita un podcast, un imprenditore o un tema specifico senza link diretto, cerca su YouTube con:
     ```bash
     python core/source_downloader.py --search "<QUERY_SPECIFICA_CAMPAGNA>"
     ```
3. **In base a cosa scegli il nuovo video da scaricare:**
   - **`already_downloaded == false`** (verificato automaticamente contro `data/downloaded_sources_history.json` per non scaricare MAI due volte lo stesso video);
   - **`is_long_form_suitable == true`** (durata tra **3 e 90 minuti**, formato orizzontale 16:9 ricco di parlato, evitando Shorts già tagliati `< 120s`);
   - **Massima aderenza a `video_selection_criteria` e `campaign_brief`** (es. testimonianza reale di uno studente, intervista podcast con numeri di bilancio, dibattito sul tema richiesto dal brand) e **alte visualizzazioni organiche (`view_count`)**.
4. Scarica il video scelto e genera il pacchetto d'ispezione:
   ```bash
   python core/source_downloader.py --download "<VIDEO_URL>" "<CAMPAIGN_ID>"
   python core/video_inspector.py "<PERCORSO_VIDEO_MP4>" "<CAMPAIGN_ID>"
   ```

---

### Passo 3: Regia AI — Allinea al Brief Klippify, Leggi il Copione, Guarda i Frame e Decidi i Tagli
1. **Leggi `<video_stem>_inspection.json`** con `read_file`:
   - **PRIMA DI TUTTO esamina `campaign_brief`** (`name`, `brand`, `description`, `video_prompt`, `rules`, `mandatory_mentions`, `mandatory_hashtags`, `call_to_action`): ogni clip DEVE rispettare alla lettera il brief specifico della campagna.
   - Esamina `timed_lines` (`[{"start_str": "00:12.40", "end_str": "00:18.90", "text": "..."}]`) cercando i passaggi esatti richiesti nel `campaign_brief`.
2. **Guarda con i tuoi occhi le immagini in `storyboards` e `sample_frames`** usando `read_file` sui file `.jpg`:
   - **Usa sempre `"crop_mode": "face_crop"` a schermo intero (mai `split_screen` sopra/sotto a meno che non sia esplicitamente richiesto)**: imposta `"center_x_ratio"` dentro ciascun elemento di `segments` (es. `0.50` primo piano centrale, `0.80` parlante a destra, `0.20` parlante a sinistra).
3. **Progetta da 3 a 5 Clip Virali distinte usando il "Taglia & Cuci" Multi-Segmento (`segments`):**
   - **MAI iniziare con saluti, sigle o preamboli**.
   - Durata totale sommata tra **25 e 50 secondi**:
     - **Segmento 1 (`"role": "teaser"`, 2.0s–3.5s):** la frase più forte o ricca di numeri messa a `00:00`.
     - **Segmenti successivi (`"role": "body"`, `"role": "payoff"`):** tieni solo le frasi ad altissima ritenzione cucite insieme e chiudi su una frase conclusa coerente con la CTA del brand.
4. **Salva il tuo piano di montaggio in `data/ai_director_cuts.json`**.

---

### Passo 4: Rendering FFmpeg Multi-Segmento & Accodamento Autopilota
Lancia la pipeline passando il tuo file di regia `data/ai_director_cuts.json`:
```bash
python core/clipping_pipeline.py "<CAMPAIGN_ID>" --video "<PERCORSO_VIDEO_MP4>" --cuts data/ai_director_cuts.json
```
Poi riesegui `python core/campaign_selector.py` per assegnare subito le nuove clip agli slot giornalieri (`6 slot` per le campagne in `SCALING`, `2 slot` per quelle in `TESTING`).
