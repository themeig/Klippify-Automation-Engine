import paths
import time
import argparse
import sys
import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Force UTF-8 on Windows stdout/stderr
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

from playwright.sync_api import sync_playwright

ANALYSIS_PROMPT_TEMPLATE = """Analizza con la massima cura questo video ed estrai TUTTI i momenti salienti ad altissimo potenziale virale ideali per TikTok, Instagram Reels e YouTube Shorts (durata 30-60 secondi ciascuno).

REGOLE DI SELEZIONE:
1. Estrai un MINIMO ASSOLUTO DI 3 CLIP (anche se il video è breve).
2. Se il video è lungo o ricco di argomenti, estrai liberamente tutte le clip di valore che ritieni opportune (fino a 6-8 clip).
3. Ciascun segmento deve avere un forte gancio nei primi 2 secondi, ritmo incalzante e un senso logico compiuto.

Per CIASCUNA clip estratta fornisci:
1. Timestamp esatto di inizio e fine (formato MM:SS)
2. Hook visivo accattivante per i primi 2 secondi (testo in sovrimpressione)
3. Titolo / Concept del momento saliente
4. Trascrizione fedele delle frasi chiave
5. Una TikTok Caption specifica, accattivante ed emozionante creata appositamente per questo spezzone
6. Motivo per cui sarà virale

Rispondi formattando la risposta ESCLUSIVAMENTE in un blocco JSON valido:
```json
[
  {
    "clip_number": 1,
    "start_time": "00:15",
    "end_time": "00:50",
    "concept": "Momento Saliente e Rivelazione",
    "hook_text": "POV: Quello che non ti dicono mai...",
    "transcript": "Testo trascritto qui...",
    "tiktok_caption": "Non crederai a cosa è successo! 😱 Guarda fino alla fine e dimmi la tua nei commenti 👇",
    "viral_reason": "Curiosità e ritmo alto"
  },
  {
    "clip_number": 2,
    "start_time": "01:20",
    "end_time": "01:55",
    "concept": "Consiglio Pratico e Strategia",
    "hook_text": "Non fare questo errore gravissimo!",
    "transcript": "Testo trascritto qui...",
    "tiktok_caption": "Ecco il segreto che cambia tutto 💡 Salva il video per non dimenticarlo! ✨",
    "viral_reason": "Valore pratico immediato"
  },
  {
    "clip_number": 3,
    "start_time": "02:30",
    "end_time": "03:05",
    "concept": "Conclusione ad Alto Impatto",
    "hook_text": "Guarda cosa succede alla fine...",
    "transcript": "Testo trascritto qui...",
    "tiktok_caption": "La parte più importante che tutti ignorano 🔥 Scopri di più al link!",
    "viral_reason": "Forte Call to Action"
  }
]
```"""

def _cleanup_stale_gemini_profile_locks():
    """Chiude eventuali processi orfani di Chrome agganciati al profilo gemini_profile."""
    if sys.platform == "win32":
        try:
            ps_cmd = 'Get-CimInstance Win32_Process -Filter "name = \'chrome.exe\'" | Where-Object { $_.CommandLine -like "*gemini_profile*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }'
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, timeout=5)
        except Exception:
            pass

def run_analysis(video_file_path, prompt_text=None, is_auto=False, task_logger=None):
    video_p = Path(video_file_path).resolve()
    if not video_p.exists():
        msg = f"[ERROR] File video non trovato: {video_p}"
        print(msg, flush=True)
        if task_logger: task_logger(msg)
        return None
        
    header_msg = f"[BOT-ANALISI] Avvio analisi per il video: {video_p.name} ({video_p.stat().st_size / (1024*1024):.1f} MB)"
    print(header_msg, flush=True)
    if task_logger: task_logger(header_msg)

    # Pulisce eventuali lock pendenti
    _cleanup_stale_gemini_profile_locks()
    time.sleep(1)
    
    with sync_playwright() as p:
        user_data_dir = str(paths.PROJECT_ROOT / "gemini_profile")
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,
                channel="chrome",
                args=["--start-maximized"]
            )
        except Exception as launch_err:
            msg = f"[ERROR] Impossibile avviare Chrome con profilo: {launch_err}"
            print(msg, flush=True)
            if task_logger: task_logger(msg)
            return None
            
        GEMINI_ANALISI_CHAT_URL = "https://gemini.google.com/app/c4300b74b47b860e"
        
        try:
            page = browser.pages[0] if browser.pages else browser.new_page()
            print(f"[BOT-ANALISI] Navigazione diretta alla chat 'analisi video klippify' ({GEMINI_ANALISI_CHAT_URL})...", flush=True)
            try:
                page.goto(GEMINI_ANALISI_CHAT_URL, timeout=45000, wait_until="domcontentloaded")
            except Exception as goto_err:
                print(f"[BOT-ANALISI] Goto warning (continuo): {goto_err}", flush=True)
        except Exception as nav_err:
            msg = f"[ERROR] Errore navigazione Gemini: {nav_err}"
            print(msg, flush=True)
            if task_logger: task_logger(msg)
            browser.close()
            return None
            
        time.sleep(4)
        
        # 1. Verifica di essere nella chat 'analisi video klippify'
        try:
            curr_url = page.url
            if "c4300b74b47b860e" not in curr_url:
                print(f"[BOT-ANALISI] Non ancora nella chat target (URL: {curr_url}), ricerco nella barra laterale...", flush=True)
                
                # Apri menu laterale se collassato
                menu_btn = page.locator('button[aria-label*="menu" i], button[aria-label*="Pannello" i], button[aria-label*="Navigazione" i], button[data-test-id*="menu"]').first
                if menu_btn.is_visible(timeout=3000):
                    menu_btn.click(force=True)
                    time.sleep(1.5)
                
                chat_link = page.locator('a[href*="c4300b74b47b860e"], text=/analisi video klippify/i, [aria-label*="analisi video klippify" i]').first
                if chat_link.is_visible(timeout=6000):
                    chat_link.click(force=True)
                    time.sleep(3)
                else:
                    # Naviga di nuovo forzando l'URL diretto
                    try:
                        page.goto(GEMINI_ANALISI_CHAT_URL, timeout=30000, wait_until="domcontentloaded")
                    except Exception:
                        pass
                    time.sleep(3)

            print("[BOT-ANALISI] Chat 'analisi video klippify' confermata ed attiva!", flush=True)
            if task_logger: task_logger("[BOT] Chat 'analisi video klippify' aperta con successo.")
        except Exception as e:
            print(f"[INFO] Chat lookup: {e}", flush=True)
            
        # 2. CONTA I MESSAGGI ESISTENTI NELLA CRONOLOGIA (per ignorarli!)
        initial_responses_count = len(page.locator("message-content, .model-response-text, .response-container-content").all())
        print(f"[BOT-ANALISI] Messaggi storici nella chat: {initial_responses_count} (verranno ignorati)", flush=True)
        
        # 3. UPLOAD DEL NUOVO FILE VIDEO TRAMITE PULSANTE '+' E MENU 'Carica file'
        print(f"[BOT-ANALISI] Carico il file video ({video_p.name})...", flush=True)
        if task_logger: task_logger(f"[BOT] Caricamento video '{video_p.name}' in corso su Gemini...")
        uploaded_successfully = False
        
        plus_btn = page.locator('button[aria-label*="Caricamento e strumenti" i], button[aria-label*="Aggiungi" i], button[aria-label*="Allega" i], .input-area-container button:has(mat-icon), rich-textarea ~ button').first
        if plus_btn.is_visible(timeout=8000):
            try:
                plus_btn.click(force=True)
                time.sleep(1.5)
                
                # Click sul pulsante 'Carica file'
                upload_btn = page.locator('.cdk-overlay-container button:has-text("Carica file"), .cdk-overlay-container [role="menuitem"]:has-text("Carica file")').first
                if upload_btn.is_visible(timeout=4000):
                    with page.expect_file_chooser(timeout=8000) as fc_info:
                        upload_btn.click(force=True)
                    fc = fc_info.value
                    fc.set_files(str(video_p))
                    uploaded_successfully = True
                    print(f"[BOT-ANALISI] [SUCCESS] Video '{video_p.name}' allegato tramite menu!", flush=True)
                    if task_logger: task_logger(f"[BOT] Video '{video_p.name}' inserito nell'input Gemini.")
            except Exception as e:
                print(f"[BOT-ANALISI] Errore menu upload: {e}", flush=True)
                
        # Fallback se non riuscito dal menu
        if not uploaded_successfully:
            try:
                file_input = page.locator('input[type="file"]').first
                file_input.set_input_files(str(video_p))
                uploaded_successfully = True
                print("[BOT-ANALISI] File impostato tramite input[type=file] fallback.", flush=True)
            except Exception as e:
                print(f"[WARNING] Fallback input error: {e}", flush=True)

        # 4. ATTESA CARICAMENTO E PREPARAZIONE
        print("[BOT-ANALISI] Attendo caricamento video nell'area di input...", flush=True)
        time.sleep(8)
        
        # 5. INSERIMENTO DEL PROMPT DI TESTO
        prompt_to_send = prompt_text if prompt_text else ANALYSIS_PROMPT_TEMPLATE
        try:
            text_area = page.locator("rich-textarea div[contenteditable='true'], div[contenteditable='true'][role='textbox'], rich-textarea p, textarea").first
            text_area.wait_for(state="visible", timeout=10000)
            text_area.click(force=True)
            time.sleep(0.5)
            page.keyboard.insert_text(prompt_to_send)
            time.sleep(1.5)
            
            # Clicca pulsante Invia quando abilitato
            send_btn = page.locator('button[aria-label*="Invia" i], button[aria-label*="Send" i], button.send-button, mat-icon[data-mat-icon-name="send"]').last
            send_clicked = False
            
            for check_send in range(25):
                is_disabled = send_btn.get_attribute("aria-disabled") == "true" or send_btn.get_attribute("disabled") is not None
                if not is_disabled and send_btn.is_visible():
                    send_btn.click(force=True)
                    send_clicked = True
                    print("[BOT-ANALISI] Pulsante Invia premuto con successo!", flush=True)
                    if task_logger: task_logger("[BOT] Prompt inviato a Gemini. In attesa di elaborazione AI...")
                    break
                time.sleep(1.5)
                
            if not send_clicked:
                page.keyboard.press("Enter")
                print("[BOT-ANALISI] Inviato tramite tasto Enter!", flush=True)
                if task_logger: task_logger("[BOT] Prompt inviato (Enter). In attesa di elaborazione AI...")
                
        except Exception as prompt_err:
            msg = f"[ERROR] Impossibile inviare il prompt: {prompt_err}"
            print(msg, flush=True)
            if task_logger: task_logger(msg)
            browser.close()
            return None
            
        # 6. ATTESA ESCLUSIVA DELLA NUOVA RISPOSTA (Ignora le risposte precedenti!)
        print(f"\n[BOT-ANALISI] In attesa della NUOVA risposta da Gemini (messaggio #{initial_responses_count + 1})...", flush=True)
        time.sleep(10)
        extracted_clips = []
        
        for check_i in range(40): # Loop fino a 3.5 minuti
            time.sleep(5)
            try:
                all_responses = page.locator("message-content, .model-response-text, .response-container-content").all()
                if len(all_responses) > initial_responses_count:
                    new_resp_elem = all_responses[-1]
                    new_resp_text = new_resp_elem.inner_text()
                    
                    if "clip_number" in new_resp_text or "start_time" in new_resp_text or "[" in new_resp_text:
                        json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', new_resp_text, re.DOTALL)
                        if json_match:
                            try:
                                parsed = json.loads(json_match.group(1))
                                if isinstance(parsed, list) and len(parsed) > 0:
                                    extracted_clips = parsed
                                    print(f"\n[SUCCESS] Ricevute {len(extracted_clips)} clip con timestamp da Gemini!", flush=True)
                                    if task_logger: task_logger(f"[BOT] Ricevuti timestamp e hook per {len(extracted_clips)} clip virali da Gemini!")
                                    break
                            except:
                                pass
            except:
                pass
                
        # 7. Salva il risultato dell'analisi in un file JSON
        analysis_out = paths.PROJECT_ROOT / "clipping_analysis.json"
        with open(analysis_out, "w", encoding="utf-8") as f:
            json.dump({
                "video_file": str(video_p),
                "analyzed_at": datetime.now().isoformat(),
                "clips": extracted_clips
            }, f, indent=2, ensure_ascii=False)
            
        print(f"[BOT-ANALISI] Risultati salvati in: {analysis_out}", flush=True)
        
        if not is_auto:
            time.sleep(3)
            
        browser.close()
        return extracted_clips

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bot Analisi Video Gemini per Clipping')
    parser.add_argument('video_path', type=str, help='Percorso del file video da analizzare')
    parser.add_argument('--auto', action='store_true', help='Esecuzione automatica senza pause')
    args = parser.parse_args()
    
    run_analysis(args.video_path, is_auto=args.auto)