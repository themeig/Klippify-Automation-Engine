# 📋 ISTRUZIONI OPERATIVE PER L'AGENTE AI: AUDIT RIFIUTI, RICERCA & DOWNLOAD FONTI MULTI-CANALE

## 🎯 MISSIONE
1. **Ispezionare i video pubblicati nelle ultime 4 ore** su Klippify: identificare eventuali rifiuti dell'AI, diagnosticare la causa (es. hook debole, CTA mancante, preamboli) e applicare contromisure adattive immediate.
2. **Monitorare periodicamente i canali ufficiali** (YouTube, TikTok, Instagram, Google Drive) associati alle campagne Klippify attive, selezionare con precisione chirurgica i video a più alto potenziale di guadagno e avviare il download verso la catena di montaggio e clipping automatico.

---

## 🔍 1. FONTI DATI E FILE DI RIFERIMENTO
1. **Audit Rifiuti Klippify:** Esegui `rejection_auditor.py` e consulta `rejection_audit_state.json` per monitorare le sottomissioni delle ultime 4 ore.
2. **Campagne Attive:** Consulta `active_campaigns_classified.json` o `campaigns_ranked.json` per conoscere il brief, i requisiti di approvazione, il payout per 1k views e le regole obbligatorie (es. presenza del creator, durata minima, argomento).
3. **Fonti Configurate:** Consulta `campaign_sources.json` per ottenere gli URL dei canali o profili assegnati a ogni campagna.
4. **Archivio Anti-Duplicati:** Consulta `downloaded_sources_history.json` per escludere immediatamente tutti i video già scaricati in passato.

---

## 🛡️ 2. FASE DI AUDIT & ADATTAMENTO A CASCATA (FEEDBACK LOOP 1+6)

A ogni ciclo di 4 ore, **PRIMA di cercare nuovi video**:
1. Esegui il modulo di audit intelligente:
   ```bash
   python rejection_auditor.py
   ```
2. **Algoritmo Adattivo a 2 Fasi (Test Singolo -> Propagazione a Catena):**
   - **Fase 1 (In caso di Rifiuto):** Se un video è stato respinto dall'AI di Klippify (es. Outro CTA mancante, Hook debole), il sistema modifica e ri-renderizza immediatamente **il 1° video cronologicamente successivo** pronto in scaletta per farlo approvare.
   - **Fase 2 (Validazione & Propagazione a 6 video):** Appena il video modificato viene approvato da Klippify, il sistema **propaga ed estende automaticamente le stesse modifiche vincenti ai successivi 6 video in ordine cronologico** presenti nel magazzino clip.

---

## ⚖️ 3. REGOLE DI SELEZIONE E FILTRI DELL'AI

Prima di approvare un nuovo video per il download, applica questa matrice di valutazione:

### ❌ REGOLE DI ESCLUSIONE (Scarta subito se):
- Il video è già presente in `downloaded_sources_history.json`.
- La durata è inferiore a 3 minuti (a meno che non sia un video TikTok/Instagram specifico).
- Il video è una diretta streaming non strutturata superiore a 3 ore.
- Il tema del video è completamente scollegato dalla campagna Klippify.

### ⭐ CRITERI DI PRIORITÀ & PUNTEGGIO VIRALE (Punteggio da 1 a 100):
1. **Attinenza Massima al Brief (40%):** Il titolo e la descrizione contengono le parole chiave del target (es. "negozi online", "guadagni", "risultati", "prima vendita", "caso studio").
2. **Potenziale di Hook Virale (30%):** Titoli che generano forte curiosità, trasformazioni prima/dopo o cifre concrete ("Da 0 a 20.000€ in 2 mesi", "Come ho iniziato da zero").
3. **Metriche e Freschezza (20%):** Video recenti con alto engagement o video sempreverdi con molte visualizzazioni.
4. **Regole Vincolanti del Brand (10%):** Presenza del creator richiesta dal regolamento di Klippify.

---

## 🛠️ 4. PROCEDURA OPERATIVA COMPLETA PASSO-PASSO

A ogni ciclo di controllo (ogni 4 ore):
1. **Passo 1 (Audit Rifiuti):** Esegui `python rejection_auditor.py`. Se ci sono correzioni necessarie, applicale prima di procedere.
2. **Passo 2 (Ispezione Canali):** Esegui:
   ```bash
   python source_downloader.py --inspect "<CANALE_URL>"
   ```
3. **Passo 3 (Valutazione & Selezione):** Confronta i video restituiti con il brief. Assegna il punteggio e seleziona il video #1 non ancora scaricato.
4. **Passo 4 (Download):** Esegui:
   ```bash
   python source_downloader.py --download "<VIDEO_URL>" "<CAMPAIGN_ID>"
   ```
5. **Passo 5 (Verifica & Report):**
   - Riassumi l'esito dell'audit sottomissioni (0 rifiuti o correzioni applicate).
   - Riassumi il nuovo video scaricato e inviato al ritaglio automatico.
