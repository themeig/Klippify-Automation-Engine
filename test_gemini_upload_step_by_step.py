import time
import argparse
import sys
import os
import re
import json
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

ANALYSIS_PROMPT_TEMPLATE = """Analizza con la massima precisione questo video per estrarre le 3 migliori clip virali da 30-60 secondi ideali per TikTok e Instagram Reels.

Per ciascuna delle 3 clip fornisci:
1. Timestamp esatto di inizio e fine (formato MM:SS)
2. Trascrizione fedele delle frasi chiave pronunciate nel segmento
3. Hook visivo accattivante per i primi 2 secondi (testo in sovrimpressione)
4. Titolo/Concept della clip
5. Motivo per cui sarà virale

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
    "viral_reason": "Curiosità e ritmo alto"
  },
  {
    "clip_number": 2,
    "start_time": "01:20",
    "end_time": "01:55",
    "concept": "Consiglio Pratico e Strategia",
    "hook_text": "Non fare questo errore gravissimo!",
    "transcript": "Testo trascritto qui...",
    "viral_reason": "Valore pratico immediato"
  },
  {
    "clip_number": 3,
    "start_time": "02:30",
    "end_time": "03:05",
    "concept": "Conclusione ad Alto Impatto",
    "hook_text": "Guarda cosa succede alla fine...",
    "transcript": "Testo trascritto qui...",
    "viral_reason": "Forte Call to Action"
  }
]
```"""

def run_analysis(video_file_path, prompt_text=None, is_auto=False):
    video_p = Path(video_file_path).resolve()
    if not video_p.exists():
        print(f"[ERROR] File video non trovato: {video_p}")
        return None
        
    print(f"\n=======================================================")
    print(f"[BOT-ANALISI] Avvio analisi per il video: {video_p.name} ({video_p.stat().st_size / (1024*1024):.1f} MB)")
    print(f"=======================================================\n")
    
    with sync_playwright() as p:
        user_data_dir = r"c:\Users\HP\Desktop\contenuti klippify\gemini_profile"
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,
                channel="chrome",
                args=["--start-maximized"]
            )
        except Exception as launch_err:
            print(f"[ERROR] Impossibile avviare Chrome con profilo: {launch_err}")
            return None
            
        try:
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.goto("https://gemini.google.com/", timeout=45000)
        except Exception as nav_err:
            print(f"[ERROR] Errore navigazione Gemini: {nav_err}")
            browser.close()
            return None
            
        time.sleep(5)
        
        # 1. Cerca la chat 'analisi video klippify'
        try:
            print("[BOT-ANALISI] Cerco la chat 'analisi video klippify'...")
            chat_link = page.locator('text=/analisi video klippify/i').first
            if chat_link.is_visible(timeout=8000):
                chat_link.click(force=True)
                print("[BOT-ANALISI] Chat 'analisi video klippify' aperta!")
                time.sleep(3)
            else:
                print("[BOT-ANALISI] Chat specifica non trovata nell'elenco, continuo nella chat corrente.")
        except Exception as e:
            print(f"[INFO] Chat lookup: {e}")
            
        # 2. CONTA I MESSAGGI ESISTENTI NELLA CRONOLOGIA (per ignorarli!)
        initial_responses_count = len(page.locator("message-content, .model-response-text, .response-container-content").all())
        print(f"[BOT-ANALISI] Messaggi storici presenti nella chat: {initial_responses_count} (verranno ignorati)")
        
        # 3. UPLOAD DEL NUOVO FILE VIDEO TRAMITE PULSANTE '+' E MENU 'Carica file'
        print(f"\n[BOT-ANALISI] Carico il NUOVO file video ({video_p.name})...")
        uploaded_successfully = False
        
        plus_btn = page.locator('button[aria-label*="Caricamento e strumenti" i], button[aria-label*="Aggiungi" i], button[aria-label*="Allega" i], .input-area-container button:has(mat-icon), rich-textarea ~ button').first
        if plus_btn.is_visible(timeout=6000):
            try:
                aria = plus_btn.get_attribute("aria-label") or "Plus Button"
                print(f"[BOT-ANALISI] Clicco sul pulsante '+' ({aria})...")
                plus_btn.click(force=True)
                time.sleep(1.5)
                
                # Cerca SPECIFICAMENTE dentro l'overlay del menu
                menu_items = page.locator('.cdk-overlay-container [role="menuitem"], .cdk-overlay-container button, .mat-mdc-menu-content button, [role="menu"] button').all()
                for m in menu_items:
                    txt = m.inner_text().strip().replace('\n', ' ')
                    if any(kw in txt.lower() for kw in ["carica", "dispositivo", "computer", "upload", "file"]):
                        print(f"[BOT-ANALISI] Clicco su '{txt}' con FileChooser...")
                        with page.expect_file_chooser(timeout=6000) as fc_info:
                            m.click(force=True)
                        fc = fc_info.value
                        fc.set_files(str(video_p))
                        uploaded_successfully = True
                        print(f"[BOT-ANALISI] [SUCCESS] Video '{video_p.name}' allegato con successo tramite menu!")
                        break
            except Exception as e:
                print(f"[BOT-ANALISI] Errore menu upload: {e}")
                
        # Fallback se non riuscito dal menu
        if not uploaded_successfully:
            try:
                file_input = page.locator('input[type="file"]').first
                file_input.set_input_files(str(video_p))
                uploaded_successfully = True
                print("[BOT-ANALISI] File impostato tramite input[type=file] fallback.")
            except Exception as e:
                print(f"[WARNING] Fallback input error: {e}")

        # 4. VERIFICA CHE LA CARD DEL VIDEO SIA PRESENTE NELL'INPUT
        print("[BOT-ANALISI] Attendo comparsa della card video nell'area di input...")
        attachment_confirmed = False
        for sec in range(25):
            time.sleep(1)
            att = page.locator('.input-area-container, .chat-input, rich-textarea, form').locator('.attachment-container, .attachment-card, [data-test-id*="attachment"], button[aria-label*="Rimuovi" i], video, .thumbnail, img').all()
            if any(a.is_visible() for a in att):
                attachment_confirmed = True
                print(f"[BOT-ANALISI] [CONFERMATO] Video allegato e visibile nell'area input!")
                break
                
        if not attachment_confirmed:
            print("[BOT-ANALISI] Attesa di sicurezza per upload...")
            time.sleep(5)
        
        # 5. INSERIMENTO DEL PROMPT DI TESTO
        prompt_to_send = prompt_text if prompt_text else ANALYSIS_PROMPT_TEMPLATE
        try:
            text_area = page.locator("rich-textarea div[contenteditable='true'], div[contenteditable='true'][role='textbox'], rich-textarea p, textarea").first
            text_area.wait_for(state="visible", timeout=10000)
            text_area.click(force=True)
            time.sleep(0.5)
            page.keyboard.insert_text(prompt_to_send)
            time.sleep(1.5)
            
            # Clicca pulsante Invia
            send_clicked = False
            try:
                send_btn = page.locator('button[aria-label*="Invia" i], button[aria-label*="Send" i], button.send-button, mat-icon[data-mat-icon-name="send"]').last
                if send_btn.is_visible():
                    send_btn.click(force=True)
                    send_clicked = True
                    print("[BOT-ANALISI] Pulsante Invia premuto!")
            except:
                pass
                
            if not send_clicked:
                page.keyboard.press("Enter")
                print("[BOT-ANALISI] Inviato tramite tasto Enter!")
                
        except Exception as prompt_err:
            print(f"[ERROR] Impossibile inviare il prompt: {prompt_err}")
            browser.close()
            return None
            
        # 6. ATTESA ESCLUSIVA DELLA NUOVA RISPOSTA (Ignora le risposte precedenti!)
        print(f"\n[BOT-ANALISI] In attesa della NUOVA risposta da Gemini (deve essere il messaggio #{initial_responses_count + 1})...")
        print("              Elaborazione del video da parte di Gemini (fino a 180s)...")
        
        time.sleep(15)
        extracted_clips = []
        
        for check_i in range(35): # Loop fino a 3 minuti
            time.sleep(5)
            try:
                all_responses = page.locator("message-content, .model-response-text, .response-container-content").all()
                # Considera SOLO se c'e una NUOVA risposta
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
                                    print(f"\n[SUCCESS] Ricevute {len(extracted_clips)} clip con timestamp dalla NUOVA risposta di Gemini!")
                                    break
                            except:
                                pass
            except:
                pass
                
        # 7. Salva il risultato dell'analisi in un file JSON
        analysis_out = Path(r"c:\Users\HP\Desktop\contenuti klippify\clipping_analysis.json")
        with open(analysis_out, "w", encoding="utf-8") as f:
            json.dump({
                "video_file": str(video_p),
                "analyzed_at": datetime.now().isoformat(),
                "clips": extracted_clips
            }, f, indent=2, ensure_ascii=False)
            
        print(f"[BOT-ANALISI] Risultati salvati in: {analysis_out}")
        
        if not is_auto:
            time.sleep(5)
            
        browser.close()
        return extracted_clips

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bot Analisi Video Gemini per Clipping')
    parser.add_argument('video_path', type=str, help='Percorso del file video da analizzare')
    parser.add_argument('--auto', action='store_true', help='Esecuzione automatica senza pause')
    args = parser.parse_args()
    
    run_analysis(args.video_path, is_auto=args.auto)
