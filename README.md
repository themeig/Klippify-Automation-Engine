# Klippify Automation Engine

> **Piattaforma autonoma 24/7 per Video Clipping, Sottotitolazione Dinamica, controllo audit e Pubblicazione Automatica su TikTok & Klippify**

---

## Avvio Rapido in 10 Secondi

### Metodo 1: Doppio Clic (Consigliato su Windows)
Fai doppio clic sul file:
* **Avvia_Server.bat**

### Metodo 2: Da Terminale
```bash
python server.py
```

Dashboard Web attiva su: http://localhost:5000

---

## Come Funziona il Flusso Operativo

```
1. SOURCING: Scarica i video migliori dai canali (YouTube/TikTok) con yt-dlp
       |
2. CLIPPING: Taglia e centra le scene in formato verticale 9:16
       |
3. SOTTOTITOLI: Genera trascrizione sincronizzata stile Hormozi + Outro CTA
       |
4. UPLOAD: Carica automaticamente le clip pronte su TikTok
       |
5. SUBMISSION: Invia il link a Klippify per il payout
       |
6. AUDIT 24/7: Controllo ogni 4h per garantire il 100% di approvazione
```

---

## Struttura del Progetto

```
Klippify-Automation-Engine/
e|
e|-- core/                             # TUTTI i moduli e la logica applicativa Python
e|   |-- server.py                    # Server Flask per Dashboard & API REST
e|   |-- generate_report.py           # Generatore della dashboard e report
e|   |-- autopilot_engine.py          # Motore di pubblicazione automatica 24/7
e|   |-- source_downloader.py         # Downloader video con engagement score
e|   |-- clipping_pipeline.py         # Montaggio e ritaglio verticale 9:16
e|   |-- clipping_queue_manager.py    # Gestore della coda video
e|   |-- video_captioner.py           # Sottotitoli parlati stile Hormozi ed Outro Card
e|   |-- rejection_auditor.py         # Controllo automatico anti-rifiuto
e|   |-- tiktok_uploader.py           # Caricamento automatico su TikTok Studio
e|   +-- paths.py                     # Gestore percorsi intelligente (SmartPath)
e|
e|-- data/                             # Database JSON e file di configurazione
e|   |-- campaign_schedules.json      # Orark di pubblicazione e impostazioni pausa
e|   |-- campaign_sources.json        # Elenco canali e fonti monitorate
e|   |-- campaigns_ranked.json        # Classifica campagne per ROI e fattibilita
e|   |-- downloaded_sources_history.json # Registro video scaricati (evita duplicati)
e|   +-- klippify_submissions.json    # Storico delle approvazioni e guadagni
e|
e|-- clipping_sources/                # [Locale] Video completi grezzi scaricati
e|-- generated_videos/                # [Locale] Clip verticali 9:16 pronte all'uso
+-- _archivio_sviluppo/              # [Archivio] Script di test passati e screenshot di debug
e|
e|-- Avvia_Server.bat                 # Launcher rapido per Windows
e|-- server.py                        # Entrypoint rapido per il server
e|-- README.md                         # Documentazione del software
+-- .gitignore                       # Esclusione video pesanti dal repository
```

---

## Moduli Principali & Funzionalita

| Modulo | File | Descrizione |
| :--- | :--- | :--- |
| **Web Dashboard** | `core/server.py` | Interfaccia grafica su `localhost:5000` con metriche, grafici e controlli live. |
| **Autopilota 24/7** | `core/autopilot_engine.py` | Gestisce gli slot orari di posting e le pause temporanee (1-7 giorni). |
| **Video Sourcing** | `core/source_downloader.py` | Ispeziona i canali (es. YouTube di Sara Dizdari) e scarica i video con il miglior engagement. |
| **9:16 Slicer** | `core/clipping_pipeline.py` | Riconosce i cambi di inquadratura e ritaglia clip verticali da 20-60 secondi. |
| **Hormozi Captions** | `core/video_captioner.py` | Genera sottotitoli colorati sincronizzati parola per parola ed applica l'Outro CTA. |
| **Quality Auditor** | `core/rejection_auditor.py` | Ispeziona le sottomissioni Klippify ogni 4 ore per garantire il 100% di approvazione. |

---

## Configurazione & Personalizzazione

### 1. Impostare gli Orari di Pubblicazione
Dalla Dashboard Web (`http://localhost:5000`) o modificando `data/campaign_schedules.json`:
g``json
{
  "active": true,
  "daily_limit": 3,
  "preferred_slots": ["11:30", "15:00", "19:30"]
}
```

### 2. Aggiungere Nuovi Canali Sorguente
In `data/campaign_sources.json` aggiungi l'URL del canale:
g``json
{
  "6a71c6f7245627c68999eae2": {
    "sources": ["https://www.youtube.com/@SaraDizdariEcommerce"]
  }
}
```

---

## Sicurezza & Spazio Disco
* **File Video Esclusi da Git:** Tramite `.gitignore`, nessun file video `.mp4` viene caricato su GitHub. Il repository rimane sempre leggero e veloce da sincronizzare.
* **Cleanup Automatico:** I file intermedi vengono puliti in automatico per risparmiare spazio su disco.
