# 🌫 Klippify Automation Engine

> **Piattaforma autonoma 24/7 per Video Clipping, Sottotitolazione Dinamica e Pubblicazione Automatica su TikTok & Klippify**

---

 Avvio Rapido

### 1. Avvio con 1 Clic (Windows)
Fai doppio clic sul file:
* 🚐 **`Avvia_Server.bat`**

### 2. Avvio da Terminale
```bash
python server.py
```

🌐 **Dashboard Web attiva su:** [http://localhost:5000](http://localhost:5000)

---

## 🔛 Come Funziona il Flusso

```
1. 📥 SOURCING: Scarica i video migliori dai canali (YouTube/TikTok) con yt-dlp
        ↓
2. ✄️ CLIPPING: Taglia e centra le scene in formato verticale 9:16
        ↓
3. 🎝 SOTTOTITOLI: Genera trascrizione sincronizzata stile Hormozk + Outro CTA
        ↓
4. �1 UPLOAD: Carica automaticamente le clip pronte su TikTok
        ↓
5. 📤 SUBMISSION: Invia il link a Klippify per il payout
        ↓
6. 🛡Ͻ AUDIT 24/7: Controllo ogni 4h per garantire il 100% di approvazione
```

---

## 👁 Struttura delle Cartelle

* 👁 **`core/`** : Tutti i moduli e gli script Python del motore
  * `server.py` : Server web e API per la dashboard
  * `generate_report.py` : Generatore della dashboard e report
  * `autopilot_engine.py` : Motore di pubblicazione automatica 24/7
  * `source_downloader.py` : Downloader video virali
  * `clipping_pipeline.py` : Montaggio e ritaglio verticale 9:16
  * `clipping_queue_manager.py` : Gestore della coda video
  * `video_captioner.py` : Sottotitoli parlati stile Hormozi ed Outro Card
  * `rejection_auditor.py` : Controllo automatico anti-rifiuto
  * `tiktok_uploader.py` : Caricamento automatico su TikTok
  * `paths.py` : Gestore percorsi intelligente (SmartPath)

* 👁	**`data/`** : Tutti i database JSON e file di configurazione 
  * `campaign_schedules.json` : Orari di pubblicazione e impostazioni pausa
  * `campaign_sources.json` : Elenco canali e fonti monitorate
  * `campaigns_ranked.json` : Classifica campagne per ROI e fattibilità
  * `downloaded_sources_history.json` : Storico dei video scaricati (evita duplicati)
  * `klippify_submissions.json` : Storico delle approvazioni e guadagni

* 👁 **`clipping_sources/`** : Video originali completi scaricati (esclusi da Git)
* 👁 **`generated_videos/`** : Clip verticali 9:16 pronte per la pubblicazione (esclusi da Git)
* 👁 **`_archivio_sviluppo/`** : Vecchi test e screenshot di debug

---

## 📓 Moduli Principali

| Modulo | File | Descrizione |
| :--- | :--- | :--- |
| **Web Dashboard** | `core/server.py` | Interfaccia grafica su `localhost:5000` con metriche e controlli live. |
| **Autopilota 24/7** | `core/autopilot_engine.py` | Gestisce gli slot orari di posting e le pause temporanee (1-7 giorni). |
| **Video Sourcing** | `core/source_downloader.py` | Ispeziona i canali e scarica i video con il miglior engagement. |
| **9:16 Slicer** | `core/clipping_pipeline.py` | Ritaglia ed esporta clip verticali da 20-60 secondi centrate sul soggetto. |
| **Hormozi Captions** | `core/video_captioner.py` | Genera sottotitoli colorati sincronizzati e inserisce la CTA obbligatoria. |
| **Quality Auditor** | `core/rejection_auditor.py` | Ispeziona le sottomissioni Klippify ogni 4 ore per garantire approvazione 100%. |

---

## ☙／ Configurazione

### Impostare gli Orari di Pubblicazione
Dalla Dashboard Web (`http://localhost:5000`) o modificando `data/campaign_schedules.json`:
g``json
{
  "active": true,
  "daily_limit": 3,
  "preferred_slots": ["11:30", "15:00", "19:30"]
}
```

### Aggiungere Nuovi Canali Sorguente
In `data/campaign_sources.json` aggiungi l'URL del canale:
```json
{
  "6a71c6f7245627c68999eae2": {
    "sources": ["https://www.youtube.com/@SaraDizdariEcommerce"]
  }
}
```

---

## 🖐 Sicurezza & Spazio Disco
* **File Video Esclusi da Git:** Tramite `.gitignore`, nessun file video `.mp4` viene caricato su GitHub. Il repository rimane sempre leggero e veloce da sincronizzare.
* **Cleanup Automatico:** I file temporanei vengono puliti in automatico per risparmiare spazio su disco.
