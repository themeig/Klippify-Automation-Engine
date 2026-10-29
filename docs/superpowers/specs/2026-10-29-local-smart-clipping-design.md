# Design: Motore di Montaggio Video Intelligente 100% Locale (Ottimizzato per Portatile Vecchio)

**Data:** 2026-10-29  
**Progetto:** `Klippify-Automation-Engine` (`C:\Users\Leo\Desktop\automazione-klippify`)  
**Dimensione:** Progetto (Riprogettazione della pipeline di analisi, selezione, ritaglio 9:16 e sottotitolazione)

---

## 1. Intento e Motivazione (Il "Perché")

Il sistema attuale ha generato circa 200 video su TikTok per le campagne Klippify, ma nessuno ha superato la soglia delle **1.000 visualizzazioni** necessaria per sbloccare i pagamenti.

L'analisi del codice e dei log storici in `data/` ha rivelato tre cause tecniche:
1. **100% di tagli ciechi (`data/clip_metadata.json` e `_archivio_sviluppo/clipping_analysis.json`):** `core/gemini_analysis_bot.py` provava a caricare interi file `.mp4` pesanti nella chat web di Gemini tramite Playwright, andando in timeout (`"clips": []`). Di conseguenza, `core/clipping_pipeline.py` cadeva sempre sul fallback cablato (`00:10-00:45`, `01:00-01:35`, `02:00-02:35`) usando per tutte le 68 clip le stesse 3 frasi hook e caption identiche, tagliando discorsi a metà frase.
2. **Estetica da "spot pubblicitario" e formato francobollo:** `core/clip_processor.py` rimpiccioliva il video 16:9 al centro su sfondo sfocato (`boxblur`), mentre `core/video_captioner.py` mostrava il banner fisso `🎓 LEZIONE GRATUITA / SUL PROFILO DI SARA` per tutta la durata del video (`persistent=True`) e ignorava il parametro `cta_text` delle altre campagne.
3. **Vincolo Hardware:** il sistema deve girare **100% in locale** su un **portatile vecchiotto** (CPU datata, RAM limitata, nessuna GPU dedicata moderna e nessuna dipendenza da API cloud a pagamento o chiavi esterne).

L'obiettivo di questa riprogettazione è sostituire il fragile upload browser di file `.mp4` e il taglio cieco con un **motore 100% locale, leggero per la CPU**, capace di selezionare momenti davvero virali su frasi compiute, anticipare un *Cold-Open Teaser* nei primi 2-3 secondi, inquadrare il parlante a tutto schermo in 9:16, tagliare i tempi morti e applicare sottotitoli dinamici puliti conformi alle regole Klippify.

---

## 2. Obiettivi, Non-Obiettivi e Anti-Obiettivi

### Obiettivi (Goals)
- **Zero tagli alla cieca:** ogni clip deve iniziare esattamente sull'attacco di una frase ad alto impatto (senza saluti/preamboli) e terminare alla fine naturale di una frase compiuta (durata totale 25–55s).
- **100% Locale e Leggero per CPU vecchie:** nessuna chiave API esterna richiesta e nessuna apertura di Chrome/Playwright per caricare gigabyte di video; l'elaborazione di un video sorgente da 15–30 minuti deve richiedere pochi minuti anche su una CPU datata.
- **Cold-Open Teaser automatico (Primi 2–3s):** estrarre la frase breve (1.8s–3.5s) più forte/scioccante contenuta all'interno della clip e anteporla a `00:00` come gancio iniziale prima che parta il discorso principale.
- **Jump-Cut automatico dei silenzi:** rimuovere pause morte e respiri lunghi (> `0.45s`) all'interno della clip per mantenere un ritmo serrato in stile TikTok.
- **Smart Crop 9:16 centrato sul volto:** convertire i video 16:9 in 9:16 (`1080x1920`) a tutto schermo centrando automaticamente il volto del parlante tramite campionamento leggero dei frame (fallback automatico a split-screen se ci sono 2 volti distanti o a `blur_background` migliorato se non ci sono volti/schermo condiviso).
- **Grafica Nativa (Anti-Spot) e Multi-Campagna:**
  - Hook testuale mostrato **solo nei primi 3 secondi** (durante il Teaser), mai fisso per tutto il video.
  - Sottotitoli dinamici parola-per-parola (`Faster-Whisper`) puliti e sincronizzati con il montaggio finale (incluso Teaser + Jump-Cut).
  - Slide Outro CTA mostrata **solo negli ultimi 3 secondi**, popolata dinamicamente con la CTA e la menzione obbligatoria della campagna attiva (rimuovendo l'hardcoding su `@saradizdari_ecom`).

### Non-Obiettivi (Non-Goals in questa fase)
- Riprogettazione della strategia multi-account TikTok o della rotazione campagne (verrà affrontata in una fase successiva dedicata).
- Generazione di video AI da zero tramite testo (focus esclusivo sulla pipeline di *Video Clipping*).

### Anti-Obiettivi (Cosa renderebbe il progetto un fallimento)
- Qualsiasi soluzione che saturi la CPU/RAM del portatile vecchio per 30+ minuti a video (es. far girare LLM pesanti da 8B su CPU o trascrivere 60 minuti di audio con modelli Whisper `large` su CPU).
- Qualsiasi fallback silenzioso che torni a tagliare `00:10-00:45` con hook generici scollegati dal parlato.
- Qualsiasi dipendenza obbligatoria da browser Chrome/Playwright durante la fase di analisi e montaggio video.

---

## 3. Vincoli Tecnici

- **OS & Ambiente:** Windows, Python 3.x, FFmpeg + FFprobe installati nel `PATH`.
- **Hardware Target:** Portatile datato (solo CPU, 4–8 GB RAM disponibili, disco SSD/HDD con spazio limitato gestito da `core/storage_manager.py`).
- **Retrocompatibilità:** `core/clipping_pipeline.py` deve mantenere la firma pubblica `run_clipping_workflow(campaign_id, video_source_path=None, is_auto=True, task_logger=None)` e il formato di ritorno JSON così da non rompere `core/autopilot_engine.py`, `core/clipping_queue_manager.py` e `core/server.py`.
- **Portabilità Percorsi:** i file `.bat` di avvio (`AVVIA_KLIPPIFY_24H.bat`, `Avvia_Server.bat`, ecc.) devono usare `cd /d "%~dp0"` invece di percorsi cablati come `c:\Users\HP\Desktop\contenuti klippify`.

---

## 4. Approcci Considerati e Scelta Effettuata

1. **Approccio 1 — Trascrizione GPU + API Cloud/Web:** scartato perché la macchina di produzione finale è un portatile vecchio senza GPU RTX e l'utente richiede funzionamento interamente locale.
2. **Approccio 2 — Cloud-Light tramite API Gratuita (Groq/Gemini API):** scartato perché l'utente vuole un sistema **100% locale** senza dipendere da chiavi API esterne.
3. **Approccio 3 (SCELTO) — "AI Director Cronjob su Antigravity" + Motore FFmpeg Locale "CPU-Smart":**
   - **Cervello Primario (Cronjob Antigravity):** un'automazione pianificata nativa di Antigravity (`sidecar.json` con `"builtin": "schedule"`) sveglia periodicamente l'agente AI di Antigravity. L'agente legge la trascrizione coi timestamp del video sorgente, ispeziona i frame estratti dal video tramite il suo strumento multimodale `read_file`, analizza le performance storiche (`views` in `klippify_submissions.json`), sceglie i tagli migliori, il *Cold-Open Teaser*, gli Hook e le Caption TikTok e li salva in `data/ai_director_cuts.json` avviano il rendering FFmpeg. Zero carico AI sulla CPU del portatile vecchio e zero browser Chrome per Gemini Web!
   - **Motore Locale & Salvagente Offline (`core/local_viral_analyzer.py`):** se `clipping_pipeline.py` viene lanciato manualmente dalla dashboard quando il cronjob non ha ancora pre-analizzato il video, usa l'analizzatore locale deterministico sui sottotitoli/audio (mai più tagli ciechi a `00:10-00:45`).
   - **Smart Crop 9:16 + Teaser + Jump-Cut:** ritaglio verticale centrato sul volto del parlante, rimozione silenzi `> 0.45s` e sottotitoli puliti senza banner fisso.

---

## 5. Architettura Dettagliata della Soluzione

### 5.1 Modulo 1: Download Sottotitoli Nativi & Pre-Filtro Audio (`core/source_downloader.py` + `core/local_viral_analyzer.py`)
Per evitare di trascrivere su CPU video lunghi 20–45 minuti:
1. **Estrazione Sottotitoli Nativi (`yt-dlp`):**
   - Durante `download_source_video()`, `yt-dlp` viene configurato con `writesubtitles=True`, `writeautomaticsub=True`, `subtitleslangs=['it', 'en']`, `subtitlesformat='json3/vtt'`.
   - Se il file `.json3` o `.vtt` viene scaricato insieme al `.mp4`, il parser locale estrae istantaneamente (in `< 0.2s`) la lista completa delle parole con i timestamp `start` ed `end` sull'intero video.
2. **Fallback Locale "Audio Energy Hotspots" (se il video non ha sottotitoli, es. Google Drive):**
   - Esegue un'analisi ultraleggera della traccia audio con FFmpeg (`ffmpeg -i input.mp4 -af astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level -f null -`), che legge 30 minuti di audio in ~2 secondi sulla CPU.
   - Individua le 4–6 finestre da 75 secondi con la maggiore energia vocale e densità di parlato (escludendo i primi 15 secondi di sigle/saluti e la coda finale) e trascrive **solo quelle finestre** con `Faster-Whisper` (`model_size="base"`, `compute_type="int8"`, `vad_filter=True`).

### 5.2 Modulo 2: Selezione Virale, Confini di Frase, Teaser e Hook (`core/local_viral_analyzer.py`)
Sostituisce `core/gemini_analysis_bot.py` come motore primario nella pipeline:
1. **Segmentazione in Frasi Compiute:**
   - Raggruppa le parole trascritte in frasi basandosi su punteggiatura (`.`, `?`, `!`) e pause vocali (`gap >= 0.35s`).
   - Scarta automaticamente qualsiasi frase iniziale contenente pattern di saluto/preambolo (`"ciao a tutti"`, `"bentornati"`, `"in questo video"`, `"mi chiamo"`, `"oggi parliamo"`, `"prima di iniziare"`).
2. **Algoritmo di Viral Scoring (0–100 punti per finestra di 28–50 secondi):**
   - **Numeri, Cifre e Valori (`+25 pt`):** presenza di importi (`€`, `euro`, `mila`, `%`, cifre numeriche), tempi rapidi (`giorni`, `settimane`, `mesi`, `da zero`, `primo mese`).
   - **Trigger Emotivi / Curiosità / Conflitto (`+25 pt`):** parole chiave ad alta ritenzione (`errore`, `segreto`, `nessuno`, `verità`, `problema`, `sbagliato`, `incredibile`, `paura`, `rischio`, `libertà`, `cambiato`, `stipendio`, `fatturato`, `clienti`, domande dirette con `?`).
   - **Ritmo del Parlato — Words Per Second (`+25 pt`):** premia i passaggi con ritmo incalzante (`2.4 – 3.8 parole/secondo`) e penalizza i passaggi lenti o esitanti.
   - **Energia Vocale / Enfasi (`+25 pt`):** calcolata dal volume RMS medio e dai picchi d'enfasi della voce nel segmento.
3. **Selezione Top Clip Distinte (3–5 clip per video):**
   - Seleziona le migliori finestre non sovrapposte (distanza minima 20s tra una clip e l'altra), garantendo che `start_time` coincida con la prima parola di una frase forte e `end_time` coincida con l'ultima parola di una frase conclusa (con `0.25s` di margine audio per non troncare la consonante finale).
4. **Estrazione del Cold-Open Teaser (2.0s – 3.5s):**
   - All'interno di ciascuna clip selezionata (escludendo i primi 4 secondi), individua la singola micro-frase (2.0s – 3.5s) con il punteggio d'impatto più alto (`teaser_start`, `teaser_end`).
   - Questa micro-frase verrà montata a `00:00` (prima dell'inizio della clip) per catturare l'attenzione nei primi 2 secondi.
5. **Generatore Locale di Hook e Caption Contestuali (Zero frasi fisse):**
   - Costruisce l'`hook_text` (max 7–9 parole, tutto maiuscolo) direttamente dalla frase più forte/teaser della clip stessa (es. se la frase dice *"in due mesi sono arrivata a 12.400 euro partendo da zero"*, l'hook estratto diventa `"DA ZERO A 12.400€ IN 2 MESI"` oppure la frase punchline pulita dai riempitivi).
   - Costruisce una `tiktok_caption` unica combinando la frase chiave della clip, una domanda di engagement coerente col tema, la CTA della campagna e gli hashtag/menzioni obbligatorie.

### 5.3 Modulo 3: Smart Crop 9:16 "Lightweight", Jump-Cut e Rendering (`core/clip_processor.py`)
1. **Rilevamento Volto Ultra-Leggero (`detect_smart_crop_coordinates`):**
   - Estrae tramite FFmpeg solo **10 frame** distribuiti nel segmento della clip (`-vf fps=1/3`, risoluzione ridotta `480p`, in memoria/temp, tempo `< 0.2s`).
   - Usa `cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')` di OpenCV per rilevare i volti in ciascun frame:
     - **Caso 1 — Singolo parlante predominante (o inquadratura fissa/podcast 1 persona):** calcola la mediana della coordinata orizzontale `center_x` del volto e applica un **Crop 9:16 a tutto schermo** centrato sul parlante (`crop=ih*9/16:ih:x_offset:0,scale=1080:1920`).
     - **Caso 2 — Due volti distanti contemporaneamente (es. intervista doppia in 16:9):** applica un layout **Split-Screen 9:16** (volto sinistro nella metà superiore `1080x960`, volto destro nella metà inferiore `1080x960`) oppure, se i volti si muovono troppo o c'è condivisione schermo (0 volti), usa un **Zoomed Blur 9:16** dove il video centrale è ingrandito al **135% della larghezza** (tagliando i bordi laterali inutili) così il soggetto è grande e leggibile, non un francobollo.
2. **Jump-Cut dei Silenzi + Montaggio Teaser:**
   - Usando i timestamp delle parole (o `silencedetect`), individua i vuoti interni `> 0.45s` e costruisce la lista di sotto-segmenti attivi:
     - `[Teaser (2.5s)]` + (breve effetto flash/stacco di `0.1s`) + `[Segmento 1 parlato]` + `[Segmento 2 parlato]` ...
   - Concatena i segmenti e applica il filtro di crop 9:16 in un singolo comando FFmpeg con `-preset veryfast -crf 20`.

### 5.4 Modulo 4: Sottotitoli Dinamici Puliti e CTA Dinamica (`core/video_captioner.py`)
1. **Eliminazione del Banner Promozionale Permanente:**
   - `format_hook_card()` viene modificato con `persistent=False` di default: il badge + titolo Hook appare a `0:00:00.00` e scompare con fade-out a `0:00:03.20` (esattamente alla fine del Cold-Open Teaser).
2. **Rimozione Hardcoding "Sara Dizdari":**
   - `clip_processor.process_clip_ffmpeg()` passa esplicitamente `brand_cta=cta_text` e `brand_mention=mention_text` a `video_captioner.burn_captions_to_video()`.
   - La slide Outro finale (ultimi `3.0s`) mostra la CTA specifica della campagna attiva e il relativo `@mention` (non più `@saradizdari_ecom` fisso).
3. **Sottotitoli Stile Hormozi Ottimizzati:**
   - Posizionati nella *safe zone* di TikTok (`pos_y = 1320`, sopra la descrizione TikTok e sotto il volto del parlante), 2–3 parole per schermata con evidenziazione della parola attiva e iniezione emoji contestuale allargata a tutte le nicchie (business, intrattenimento, podcast, lifestyle, DIY).

### 5.5 Modulo 5: Cronjob Nativo Antigravity ("AI Director") + Aggiornamento `watcher_instructions.md`
1. **Come funziona il Cronjob su Antigravity:**
   - Antigravity supporta nativamente le **Scheduled Automations** (`~/.gemini/config/sidecars/klippify-ai-director/sidecar.json` con `"builtin": "schedule"`).
   - A intervalli regolari (es. ogni 4 ore), Antigravity avvia in background una sessione dell'agente AI nella cartella `C:\Users\Leo\Desktop\automazione-klippify`.
2. **Compiti del "Regista AI" (Agente Antigravity) ad ogni esecuzione del Cronjob:**
   - **Passo 1 — Audit Rifiuti & Analisi Views:** esegue `rejection_auditor.py` e legge `data/klippify_submissions.json` per verificare sia eventuali rifiuti sia quali clip hanno generato più visualizzazioni (es. 720 views vs 0-2 views), adattando lo stile degli hook ai pattern più performanti.
   - **Passo 2 — Scelta Campagna & Download Video + Trascrizione:** ispeziona i canali in `data/campaign_sources.json`, sceglie il video migliore non ancora scaricato e lancia `source_downloader.py` che scarica il `.mp4` e genera subito il file di trascrizione timestampata (`<video_stem>_transcript.json`) + 6 frame JPG campione del video.
   - **Passo 3 — Regia AI Multimodale (Lettura Copione + Visione Frame):** l'agente Antigravity legge il file `<video_stem>_transcript.json` e **guarda i frame JPG** tramite `read_file`. Sceglie da 3 a 5 clip virali reali e scrive direttamente il piano di taglio in `data/ai_director_cuts.json` (con `teaser_start`, `teaser_end`, `start_time`, `end_time`, `crop_mode` / coordinate volto, `hook_text` persuasivo e `tiktok_caption` completa).
   - **Passo 4 — Rendering FFmpeg & Accodamento Autopilota:** l'agente lancia `python core/clipping_pipeline.py <campaign_id> --video <file> --cuts data/ai_director_cuts.json`, che esegue il taglio FFmpeg 9:16 con Teaser, Jump-Cut e sottotitoli puliti e mette le clip pronte nella coda di `autopilot_engine.py`.

---

## 6. Scelte Tecniche delegate al Builder ("My Calls")

- **Dipendenze Python (`requirements.txt` + `Installa_Dipendenze.bat`):** usare `opencv-python-headless` (più leggero di `opencv-python` completo e senza conflitti GUI su Windows), `faster-whisper`, `yt-dlp`, `numpy`, `flask`, `playwright`.
- **Caching delle Trascrizioni:** salvare la trascrizione completa di ogni video sorgente in `clipping_sources/<campaign_id>/<video_stem>_transcript.json` così se si vogliono rigenerare clip dallo stesso video non serve mai ritrascriverlo.
- **Pulizia Automatica Clip Vecchie "Cieche":** fornire uno script/opzione per archiviare o rigenerare le vecchie clip nel magazzino che avevano `"transcript": "Estratto dal video originale"`, evitando che l'autopilota continui a pubblicare vecchie clip tagliate a `00:10-00:45`.
