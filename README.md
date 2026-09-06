# 🚀 Klippify Automation Engine

> **Piattaforma autonoma end-to-end per l'automazione completa delle campagne su Klippify: Video Clipping intelligente, Sottotitoli Dinamici, Upload su TikTok, Sottomissione Automatica e Controllo Qualità Anti-Rifiuto 24/7.**

---

## 🎯 Obiettivo del Software

**Klippify Automation Engine** è un'infrastruttura modulare creata per automatizzare al 100% l'intero ciclo operativo dei creator su **Klippify**, massimizzando i guadagni e il payout dalle campagne di video clipping per TikTok, Instagram Reels e YouTube Shorts.

Il software gestisce l'intero flusso senza intervento manuale: dalla scansione delle campagne più remunerative, al download della materia prima, fino al montaggio, trascrizione AI, pubblicazione su TikTok e invio della sottomissione a Klippify con tasso di approvazione garantito.

---

## ⚡ Avvio Rapido in 10 Secondi

### Metodo 1: Doppio Clic (Consigliato su Windows)
Fai doppio clic sul file eseguibile:
* **`Avvia_Server.bat`**

### Metodo 2: Da Terminale
```bash
python server.py
```

🌐 **Dashboard Web attiva su:** [http://localhost:5000](http://localhost:5000)

---

## 🔄 Il Flusso Operativo Completo (Workflow Autonomo)

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. SCRAPING & RANKING: Analisi campagne Klippify e calcolo ROI/Budget  │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 2. SOURCING AUTOMATICO: Download video ad alta viralità (yt-dlp)       │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 3. SMART SLICING 9:16: Riconoscimento scene & ritaglio con blur FFmpeg │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 4. SOTTOTITOLI HORMOZI: Trascrizione Faster-Whisper + Hook + Outro CTA │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 5. AUTOPILOTA TIKTOK: Caricamento programmato con hashtag e menzioni   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 6. SOTTOMISSIONE KLIPPIFY: Invio automatico del link video alle API    │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ 7. AUDIT ANTI-RIFIUTO 24/7: Controllo ogni 4h e auto-adattamento coda  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 💎 Tutte le Funzionalità e Moduli (Feature Breakdown)

### 1. 📊 Scraping Live & Classifica Campagne Klippify
* **Scansione Completa del Catalogo:** Interroga periodicamente le API di Klippify autenticandosi in modo sicuro per tracciare campagne attive, nuove, in pausa o terminate.
* **Calcolo Feasibility & ROI Score:** Algoritmo proprietario che ordina le campagne in base al budget residuo, payout per 1.000 visualizzazioni, lingua e tasso di completamento.
* **Estrazione Regole Tassative:** Rileva in automatico hashtag obbligatori, menzioni richieste (es. `@saradizdari_ecom`) e linee guida specifiche per evitare penalità.

### 2. 📥 Sourcing Video Intelligente & Calcolo Engagement
* **Multi-Piattaforma:** Download automatico da canali YouTube, account TikTok, Instagram o cartelle Drive.
* **Engagement & Viral Score:** Ispeziona i metadati dei video per dare priorità a quelli con il maggior volume di visualizzazioni e commenti.
* **Deduplicazione Storica:** Registro centralizzato `downloaded_sources_history.json` per evitare di riscaricare video già elaborati.

### 3. ✂️ Smart Slicer 9:16 & FFmpeg Engine
* **Formattazione TikTok / Reels (1080x1920):** Conversione automatica da video orizzontali (16:9) a verticali (9:16) con effetto *background blur* dinamico per mantenere il soggetto sempre a fuoco.
* **Analisi Momenti Salienti con AI:** Identificazione dei picchi di coinvolgimento ed estrazione di clip autonome da 25 a 55 secondi.
* **Anti-Preambolo & Frase Compiuta:** Regole rigide per eliminare saluti o convenevoli iniziali e garantire che la frase finale non venga mai troncata.

### 4. 🎙️ Sottotitoli Dinamici Stile Hormozi & Hook Card
* **Trascrizione Parola per Parola:** Utilizza il modello IA `Faster-Whisper` con quantizzazione int8 su CPU per generare sottotitoli precisi al millisecondo.
* **Stile Visivo ad Alta Ritenzione:** Font in grassetto ad alta visibilità con animazione a colori a scorrimento (stile Alex Hormozi), evidenziazione delle parole chiave ed emoji automatiche.
* **Hook Badge nei Primi 2 Secondi:** Applicazione automatica del titolo/gancio visivo nella parte superiore del video per massimizzare la retention iniziale.

### 5. 🎓 Outro CTA Slide & Garanzia Approvazione Klippify
* **Call To Action Integrata:** Negli ultimi 3.5 secondi di ogni video viene visualizzata la schermata di invito all'azione con badge `🎓 VIDEO-LEZIONE` e il rimando al profilo ufficiale del brand.
* **100% Conforme ai Criteri Klippify:** Progettato specificamente per superare i controlli automatici e manuali di approvazione dei moderatori Klippify.

### 6. 🚀 Caricamento Autonomo su TikTok Studio (Playwright)
* **Automazione Browser Ufficiale:** Gestione completa della sessione di upload su TikTok Studio senza trigger di bot detection.
* **Compilazione Completa Metadati:** Inserimento automatico di descrizione persuasiva, tutti gli hashtag obbligatori e le menzioni collegate alla campagna.
* **Recupero Link Pubblicato:** Estrazione istantanea del link univoco del video appena pubblicato (es. `https://www.tiktok.com/@user/video/...`).

### 7. 📤 Invio Automatico alle API Klippify
* **Sottomissione Istantanea:** Appena il video è online su TikTok, il link viene inoltrato all'endpoint `POST /api/creator/content/<campaign_id>` di Klippify associando il profilo social del creator.
* **Aggiornamento Cache:** Lo storico delle sottomissioni viene aggiornato istantaneamente in locale per monitorare approvazioni e ricavi.

### 8. 🛡️ Quality Auditor 24/7 & Auto-Adattamento a Cascata
* **Audit Periodico ogni 4 Ore:** Controlla lo stato delle sottomissioni (Approvate, In Revisione, Rifiutate).
* **Feedback Loop Intelligente:** Se l'AI di Klippify segnala una motivazione di rifiuto (es. hook troppo lento, introduzione parlata), il sistema modifica immediatamente le regole di taglio e rigenera le clip successive nella coda.

### 9. 🌐 Dashboard Web Interattiva (Flask & Modern UI)
* **Pannello di Controllo Completo (`http://localhost:5000`):**
  * Metriche live su visualizzazioni, mi piace, commenti e guadagni TikTok.
  * Tabella campagne attive con stato budget e payout.
  * Gestione slot orari di pubblicazione e modalità pausa programmata (1-7 giorni).
  * Anteprima visiva delle clip, registro log in tempo reale e trigger manuali di clipping/upload.

### 10. 📁 Architettura Modulare `SmartPath` & Sicurezza Dati
* **Separazione Logica / Dati:** Il codice risiede in `core/`, mentre i database e le impostazioni sono archiviati in `data/`.
* **SmartPath Routing:** Risoluzione automatica dei percorsi senza conflitti multipiattaforma.
* **Sicurezza GitHub (`.gitignore`):** Credenziali personali (`klippify_config.json`, token TikTok) e file video pesanti (`.mp4`) sono protetti ed esclusi dal tracking Git.

---

## 📂 Struttura del Progetto

```
Klippify-Automation-Engine/
├── core/                                 # TUTTI i moduli applicativi Python
│   ├── server.py                         # Server Web Flask (Dashboard & API REST)
│   ├── generate_report.py                # Generatore report HTML e interfaccia utente
│   ├── autopilot_engine.py               # Motore orario di pubblicazione automatica 24/7
│   ├── source_downloader.py              # Download video multi-fonte con calcolo virale
│   ├── clipping_pipeline.py              # Pipeline di montaggio e slicing 9:16
│   ├── clipping_queue_manager.py         # Gestore code e background worker
│   ├── clip_processor.py                 # Motore FFmpeg con blur background
│   ├── video_captioner.py                # Sottotitoli Faster-Whisper, Hook ed Outro CTA
│   ├── rejection_auditor.py              # Auditor anti-rifiuto e auto-adattamento
│   ├── tiktok_uploader.py                # Bot Playwright per TikTok Studio
│   ├── tiktok_manager.py                 # Gestione token e metriche API TikTok
│   ├── gemini_analysis_bot.py            # AI Video Analysis per estrazione clip salienti
│   ├── campaign_classifier.py            # Classificazione e ordinamento ROI campagne
│   ├── storage_manager.py                # Pulizia automatica spazio disco e file temporanei
│   └── paths.py                          # SmartPath Virtual Routing Engine
│
├── data/                                 # Database JSON e configurazioni (persistenti)
│   ├── active_campaigns_classified.json  # Dati campagne attive sincronizzate
│   ├── campaign_schedules.json           # Calendario orari e slot di pubblicazione
│   ├── campaign_sources.json             # Fonti video associate alle campagne
│   ├── campaigns_ranked.json             # Classifica globale delle campagne
│   ├── clip_metadata.json                # Metadati delle clip create
│   ├── downloaded_sources_history.json   # Registro anti-duplicazione download
│   ├── klippify_submissions.json         # Storico sottomissioni e payout Klippify
│   └── published_content.json            # Registro video pubblicati su TikTok
│
├── clipping_sources/                     # [Locale] Video grezzi scaricati
├── generated_videos/                     # [Locale] Clip 9:16 pronte con sottotitoli e CTA
│
├── Avvia_Server.bat                      # Launcher rapido Windows a doppio clic
├── server.py                             # Entrypoint radice del server
├── .gitignore                            # Protezione credenziali e file pesanti
└── README.md                             # Documentazione completa del software
```

---

## ⚙️ Configurazione Personalizzata

### ⏰ 1. Orari di Pubblicazione
Puoi impostare gli orari direttamente dalla Dashboard Web o modificando `data/campaign_schedules.json`:
```json
{
  "active": true,
  "daily_limit": 3,
  "preferred_slots": ["11:30", "15:00", "19:30"]
}
```

### 📺 2. Aggiungere Nuovi Canali o Fonti
In `data/campaign_sources.json` puoi associare uno o più canali a una campagna Klippify:
```json
{
  "6a71c6f7245627c68999eae2": {
    "sources": [
      "https://www.youtube.com/@SaraDizdariEcommerce"
    ]
  }
}
```

---

## 🛡️ Privacy & Sicurezza
* **Protezione Credenziali:** Nessun token di accesso o password viene mai inviato ai repository Git.
* **Storage Zero Waste:** Il modulo di pulizia disco rimuove in automatico i file video dopo la pubblicazione confermata su TikTok e Klippify, mantenendo il disco sempre libero.

---

## 📜 Licenza
Progetto sviluppato per l'automazione ad alto rendimento su Klippify e TikTok. Distribuito sotto licenza privata.
