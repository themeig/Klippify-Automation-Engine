# ?? Klippify Automation Engine

> **Piattaforma autonoma 24/7 per l''estrazione, clipping video verticale 9:16, sottotitolazione dinamica, controllo qualità e pubblicazione automatizzata su TikTok e Klippify.**

---

## ?? Funzionalità Principali

* ?? **Dashboard Web Interattiva in Tempo Reale (Porta 5000):** Visualizzazione completa delle metriche, ranking campagne, payout, inventario video e controlli manuali.
* ?? **Autopilota 24/7 con Controllo Ciclo di Vita:** Schedulazione intelligente degli slot di pubblicazione, pausa temporanea (1-7 giorni) e ripresa automatica.
* ?? **Downloader Automatico Fonti Virali:** Analisi dei canali sorgente (YouTube, TikTok, Drive) e download prioritario dei video a più alto engagement/visualizzazioni.
* ?? **Pipeline di Ritaglio Verticale 9:16:** Taglio intelligente delle scene salienti con centraggio automatico del soggetto.
* ??? **Sottotitoli Dinamici Parlati (Stile Hormozi):** Trascrizione audio parola per parola con evidenziazione colorata ad alto impatto.
* ??? **Auditor Anti-Rifiuto & Cascata 1+6:** Monitoraggio continuo dello stato di approvazione su Klippify e adattamento istantaneo di Hook Card e Outro CTA (tasso di approvazione al **100%**).
* ?? **Uploader TikTok Automatizzato:** Integrazione diretta con TikTok Studio per il caricamento programmatico con hashtag e menzioni obbligatorie.

---

## ??? Architettura del Sistema

`
?? Klippify-Automation-Engine/
¦
+-- ?? core/                         # TUTTI i moduli e la logica applicativa Python
¦   +-- server.py                    # Server Flask/HTTP per API REST e interfaccia web
¦   +-- generate_report.py           # Generatore del report HTML e widget reattivi
¦   +-- autopilot_engine.py          # Motore di pubblicazione ciclica 24/7
¦   +-- source_downloader.py         # Downloader video con calcolo score virale (yt-dlp)
¦   +-- clipping_pipeline.py         # Segmentazione e montaggio in formato verticale 9:16
¦   +-- clipping_queue_manager.py    # Gestore della coda di elaborazione video
¦   +-- video_captioner.py           # Generatore sottotitoli dinamici e Hook/Outro card
¦   +-- rejection_auditor.py         # Audit automatico delle sottomissioni Klippify
¦   +-- tiktok_uploader.py           # Modulo di caricamento video su TikTok
¦   +-- campaign_classifier.py       # Analisi e ranking di convenienza campagne
¦   +-- paths.py                     # Gestore percorsi intelligente (SmartPath)
¦
+-- ?? data/                         # TUTTI i database JSON e file di stato
¦   +-- campaign_schedules.json      # Orari, slot giornalieri e stato pausa/attivo
¦   +-- campaign_sources.json        # Elenco canali e fonti monitorate
¦   +-- downloaded_sources_history.json # Storico dei video grezzi scaricati
¦   +-- klippify_submissions.json    # Cache locale delle approvazioni
¦   +-- campaigns_ranked.json        # Classifica delle campagne per punteggio virale
¦   +-- autopilot_state.json         # Stato operativo dell''autopilota
¦
+-- ?? _archivio_sviluppo/           # Script di test, debug e screenshot di sviluppo
¦
+-- ?? LAUNCHER RAPIDI
¦   +-- Avvia_Server.bat             # Avvia la dashboard su http://localhost:5000
¦   +-- AVVIA_KLIPPIFY_24H.bat       # Avvia l''intero ciclo in background
¦
+-- ?? server.py                     # Entrypoint rapido per il server
+-- ?? generate_report.py            # Entrypoint rapido per la generazione report
+-- ?? README.md                     # Documentazione del progetto
+-- ?? .gitignore                    # Protezione file pesanti (.mp4, cache, token)
`

---

## ?? Come Avviare e Configurare

### 1. Prerequisiti
* **Python:** 3.11 o 3.12 installato (con pip nel PATH).
* **FFmpeg:** Installato per il rendering e l''elaborazione video.
* **Dipendenze Python:**
`ash
pip install flask yt-dlp playwright requests python-dotenv tabulate
`

### 2. Avvio della Dashboard
Puoi avviare il sistema in due modi:
* **Metodo Rapido:** Doppio clic su Avvia_Server.bat
* **Da Terminale:**
`ash
python server.py
`
Apri il browser su: ?? **http://localhost:5000**

### 3. Configurazione Campagne & Autopilota
Dalla Dashboard web puoi:
1. **Attivare/Disattivare l''Autopilota** per ciascuna campagna con un click.
2. **Impostare gli orari di pubblicazione** e il numero di video giornalieri.
3. **Pausa Temporanea:** Sospendere la pubblicazione per 24h, 48h o 1 settimana con ripresa automatica.
4. **Fonti Canali:** Aggiungere link YouTube/TikTok per il download continuo di nuove clip.

---

## ?? Sicurezza & Backup
Questo repository è configurato con un file .gitignore rigoroso che esclude tutti i file multimediali pesanti (.mp4, .mov), cartelle di download grezze e sessioni browser temporanee, preservando unicamente il codice sorgente leggero e pulito.
