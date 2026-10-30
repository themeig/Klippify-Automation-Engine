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

### Passo 1: Controllo Approvazioni Klippify & Selezione Campagne (Portfolio AI)
1. **Sincronizza il catalogo live da Klippify** (stato, sezione `Iscritte`/`Nuove`, budget residuo):
   ```bash
   python -c "import sys; sys.path.insert(0,'core'); import klippify_scraper; klippify_scraper.fetch_klippify_campaigns(use_cache_if_available=False)"
   ```
   Se `data/klippify_config.json` contiene ancora l'email segnaposto, la sync live NON avviene e i dati sono vecchi: **avvisa l'utente**.
2. Controlla approvazioni/rifiuti: `python core/rejection_auditor.py` → leggi `data/approval_audit_report.json` (`winning_patterns`, `ai_director_instruction`).
3. **Regole di selezione campagne (obbligatorie, in quest'ordine):**
   - **A) Budget (filtro bloccante):** scarta SEMPRE campagne con `budget_remaining < $35`, `budget_progress_percent >= 95%` o `budget_exhausted: true` (`campaign_selector.has_sufficient_budget`). Non scaricare, non tagliare e non pubblicare MAI per una campagna senza soldi. Se l'utente ti dice che una campagna ha finito il budget, imposta `"feasible": false, "recommended_stage": "depleted"` in `data/ai_campaign_decisions.json`.
   - **B) Ancora attiva su Klippify:** `status == Active` e sezione diversa da `Passate / In pausa / Rifiutate`; se sparisce dal catalogo live è terminata.
   - **C) Fattibilità clipping:** esistono video sorgente lunghi (YouTube/Drive/podcast) coerenti col brief, lingua italiana, piattaforma TikTok ammessa dal brief.
   - **D) Potenziale:** `views_per_creator × payout_per_1k`, budget residuo, trazione.
   - **E) Iscrizione utente:** se la campagna scelta per il TEST è ancora in `Nuove` (non attivata dall'utente), puoi preparare le clip ma **DEVI dire all'utente di attivarla su Klippify** (link `https://app.klippify.com/campaigns/<id>`) e NON caricare nulla finché non risulta `Iscritte` o confermata (`/api/campaign/confirm-klippify-activation`).
4. Aggiorna `data/ai_campaign_decisions.json` (fattibilità, `source_urls`, `search_queries`, `video_selection_criteria`) ed esegui:
   ```bash
   python core/campaign_selector.py
   ```
   Leggi `data/campaign_portfolio_plan.json`:
   - **`SCALING`**: campagne con approvazione `>= 50%` e buone views → fino a 2 slot/giorno (`13:00`, `21:00`).
   - **`TESTING`**: campagne promettenti in test (3 clip) → 1 slot/giorno (`17:30`), le altre in coda.
   - **`DROPPED_UNDERPERFORMING` / `depleted`**: fermate (troppi rifiuti, poche views o budget finito).
   - **`campaigns_requiring_user_activation`**: elencale SEMPRE nel tuo report finale all'utente.
   - **Limite ferreo: max 3 video/giorno in totale per account TikTok.**
   - `next_clipping_priorities` indica per quali campagne tagliare nuove clip.

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

### Passo 3b: Scelta Stile Sottotitoli, Hook e CTA Finale (una sola volta per campagna)
Gli stili sono definiti in `core/video_captioner.py` (`STYLES`) e assegnati in **`data/campaign_visual_styles.json`**.
1. **Se la campagna ha già una voce con `"locked": true` → NON cambiarla mai.** Tutti i video futuri useranno lo stesso stile (coerenza di brand e riconoscibilità).
2. **Solo per una campagna nuova senza stile**, scegli in base al brief:
   | Tipo campagna | `style_key` | Palette |
   |---|---|---|
   | Finanza, bilanci, B2B, dati aziendali, podcast business | `executive_fin` | oro finanziario + cyber mint + ciano |
   | E-commerce, corsi, creator lifestyle, testimonianze | `hormozi_gold` | oro caldo + verde smeraldo |
   | Inchieste, polemiche, casi studio "verità/bugie" | `docu_crimson` | ambra + rosso |
   | Trading, mindset, motivazione | `viral_emerald` | verde neon + oro |
   | Tech, AI, entertainment/YouTube | `cyber_cyan` | ciano + oro |
3. Scrivi la voce in `data/campaign_visual_styles.json` con: `style_key`, `hook_kicker` (2 concetti in maiuscolo separati da `•`, es. `CASO STUDIO  •  E-COMMERCE ITALIA`), `outro_kicker` (domanda breve che crea curiosità), `outro_headline` (CTA specifica del brief, max ~50 caratteri, mai "su Klippify"), `outro_action_prefix` (es. `VAI SUL PROFILO  ▸ `), `selected_reason` e **`"locked": true`**.
4. **Regole di copy (anti "AI slop"):** niente emoji nei sottotitoli/overlay, niente frasi generiche ("Guarda fino alla fine!"), numeri e nomi propri reali del video, max 2 righe per hook e CTA.
5. Per ogni clip, in `data/ai_director_cuts.json` scrivi solo `hook_text` (punchline specifica di QUELLA clip, max ~45 caratteri, con il numero/fatto più forte): lo stile grafico resta quello bloccato.
6. Se non scrivi nulla, il captioner sceglie automaticamente lo stile al primo rendering e lo blocca da solo.

---

### Passo 4: Rendering FFmpeg Multi-Segmento & Accodamento Autopilota
Lancia la pipeline passando il tuo file di regia `data/ai_director_cuts.json`:
```bash
python core/clipping_pipeline.py "<CAMPAIGN_ID>" --video "<PERCORSO_VIDEO_MP4>" --cuts data/ai_director_cuts.json
```
Poi riesegui `python core/campaign_selector.py` per assegnare subito le nuove clip agli slot giornalieri (max 3 video/giorno totali: 2 slot `SCALING` + 1 slot `TESTING`).
