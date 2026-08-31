<div align=" center\>

# ?? Klippify Automation Engine
**Piattaforma autonoma 24/7 per Video Clipping, Sottotitolazione Dinamica e Pubblicazione Automatica su TikTok & Klippify**

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Backend-Flask%20API-green?logo=flask)
![Playwright](https://img.shields.io/badge/Browser-Playwright%20Chromium-orange?logo=playwright)
![FFmpeg](https://img.shields.io/badge/Video-FFmpeg%20Engine-red?logo=ffmpeg)
![Status](https://img.shields.io/badge/Approval%20Rate-100%25%20Verified-brightgreen)

</div>

---

## ? Avvio Rapido in 10 Secondi

### Metodo 1: Doppio Clic (Consigliato su Windows)
Fai doppio clic sul file:
> ?? **Avvia_Server.bat**

### Metodo 2: Da Terminale
`ash
python server.py
`
?? **Dashboard Web attiva su:** [http://localhost:5000](http://localhost:5000)

---

## ?? Come Funziona il Sistema (Il Flusso Operativo)

`mermaid
graph TD
 A[?? Sourcing Canali] -->|yt-dlp analizza viste e viral score| B[?? clipping_sources/]
 B -->|Smart Slicer 9:16| C[?? Montaggio & Ritaglio]
 C -->|Whisper + Stile Hormozi| D[??? Sottotitoli Dinamici]
 D -->|Hook Card + Outro CTA Obbligatoria| E[?? generated_videos/ 61 clip pronte]
 E -->|Autopilota a orari programmati| F[?? Upload su TikTok]
 F -->|Link video caricato| G[?? Invio Sottomissione Klippify]
 G -->|Audit continuo ogni 4h| H[??? 100% Approvazione & 0 Rifiuti]
`

---

## ?? Struttura del Progetto

`
?? Klippify-Automation-Engine/
¦
+-- ?? core/ # TUTTI i moduli e la logica applicativa Python
¦ +-- server.py # Web Server Flask per Dashboard & API REST
¦ +-- generate_report.py # Motore di generazione della Dashboard interattiva
¦ +-- autopilot_engine.py # Autopilota: orari, frequenza e cicli di pubblicazione
¦ +-- source_downloader.py # Downloader video con calcolo dell'engagement score
¦ +-- clipping_pipeline.py # Taglio scene e conversione automatica in 9:16
¦ +-- clipping_queue_manager.py # Coda intelligente di lavorazione
¦ +-- video_captioner.py # Sottotitoli sincronizzati stile Hormozi ed Outro Card
¦ +-- rejection_auditor.py # Monitoraggio continuo e risoluzione automatica rifiuti
¦ +-- tiktok_uploader.py # Caricamento automatico su TikTok Studio
¦ +-- paths.py # Gestore percorsi intelligente (SmartPath)
¦
+-- ?? data/ # Database JSON e file di configurazione
¦ +-- campaign_schedules.json # Orari di pubblicazione e stato di pausa/attivo
¦ +-- campaign_sources.json # Elenco canali YouTube/TikTok monitorati
¦ +-- campaigns_ranked.json # Classifica delle campagne per ROI e fattibilità
¦ +-- downloaded_sources_history.json # Registro video scaricati (evita duplicati)
¦ +-- klippify_submissions.json # Cache delle approvazioni e guadagni
¦
+-- ?? clipping_sources/ # [Locale] Video completi grezzi scaricati
+-- ?? generated_videos/ # [Locale] Clip verticali 9:16 pronte all'uso
+-- ?? _archivio_sviluppo/ # [Archivio] Script di test passati e screenshot di debug
¦
+-- ?? Avvia_Server.bat # Launcher veloce per Windows
+-- ?? server.py # Entrypoint rapido per il server
+-- ?? README.md # Documentazione del software
+-- ?? .gitignore # Esclusione video pesanti dal repository
`

---

## ?? Moduli Principali & Funzionalità

| Modulo | File | Cosa Fa |
| :--- | :--- | :--- |
| **?? Web Dashboard** | core/server.py | Fornisce l'interfaccia grafica su localhost:5000 con metriche, grafici e controlli live. |
| **?? Autopilota 24/7** | core/autopilot_engine.py | Gestisce gli slot orari di posting, rispetta i limiti giornalieri e gestisce le pause temporanee (1-7 giorni). |
| **?? Video Sourcing** | core/source_downloader.py | Ispeziona i canali (es. YouTube di Sara Dizdari) e scarica i video più visti con la migliore resa per il clipping. |
| **?? 9:16 Slicer** | core/clipping_pipeline.py | Riconosce i cambi di inquadratura, centra il soggetto ed esporta spezzoni verticali da 20-60 secondi. |
| **??? Hormozi Captions** | core/video_captioner.py | Genera sottotitoli colorati sincronizzati parola per parola ed applica l'Outro CTA obbligatoria per il payout. |
| **??? Quality Auditor** | core/rejection_auditor.py | Ispeziona lo stato delle sottomissioni Klippify ogni 4 ore per garantire il **100% di approvazione**. |

---

## ?? Configurazione & Personalizzazione

### 1. Impostare gli Orari di Pubblicazione
Dalla Dashboard Web (http://localhost:5000) o modificando data/campaign_schedules.json:
`json
{
 active: true,
 daily_limit: 3,
 preferred_slots: [11:30, 15:00, 19:30]
}
`

### 2. Aggiungere Nuovi Canali Sorgente
In data/campaign_sources.json aggiungi semplicemente il link del canale o playlist:
`json
{
 6a71c6f7245627c68999eae2: {
 sources: [https://www.youtube.com/@SaraDizdariEcommerce]
 }
}
`

---

## ?? Sicurezza & Gestione Spazio Disco
* **File Video Esclusi da Git:** Tramite .gitignore, nessun file video .mp4 o file .mov viene caricato su GitHub. Il repository rimane sempre leggero e velocissimo da clonare.
* **Smart Storage:** Lo script storage_manager.py pulisce automaticamente i file temporanei intermedi mantenendo solo le clip finite pronte per la pubblicazione.
