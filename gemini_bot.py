import time
import argparse
import sys
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def run(prompt_to_send=None, is_auto=False):
    print("[BOT] Avvio inizializzazione di Playwright...")
    try:
        with sync_playwright() as p:
            user_data_dir = "./gemini_profile"
            
            try:
                # Avviamo Chrome
                browser = p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=False,
                    channel="chrome" 
                )
            except Exception as launch_err:
                err_str = str(launch_err)
                if "Target page, context or browser has been closed" in err_str or "sessione del browser esistente" in err_str:
                    print("\n[ERROR] BROWSER_LOCKED: C'è un processo di Chrome rimasto aperto in background che blocca l'avvio. Riprova tra poco o chiudi Chrome.")
                else:
                    print(f"\n[ERROR] LAUNCH_FAILED: Impossibile avviare il browser. Dettagli: {err_str}")
                input("\nPremi Invio per chiudere questa finestra...")
                sys.exit(1)
            
            try:
                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto("https://gemini.google.com/", timeout=30000)
            except Exception as nav_err:
                print(f"\n[ERROR] NAV_FAILED: Errore durante il caricamento di Gemini (Connessione internet assente o sito giù?). Dettagli: {nav_err}")
                input("\nPremi Invio per chiudere questa finestra...")
                browser.close()
                sys.exit(1)
            
            if not is_auto:
                print("\n" + "="*60)
                print("Quando vedi la chat di Gemini pronta per essere usata...")
                input("---> PREMI INVIO QUI NEL TERMINALE PER CONTINUARE <---")
                print("="*60 + "\n")
            else:
                print("[BOT] Modalità Automatica: Attendo 10 secondi affinché l'app web si carichi completamente...")
                time.sleep(10)
            
            # Cerca e clicca sulla chat specifica di Klippify
            try:
                print("[BOT] Cerco la chat pinnata 'generazione video klippify' (fino a 30s di attesa)...")
                # Salva l'URL corrente per capire quando la pagina ha cambiato chat
                old_url = page.url
                
                chat_link = page.locator('text=/generazione video klippify/i').first
                chat_link.wait_for(state="visible", timeout=30000)
                chat_link.click(force=True)
                print("[BOT] Chat 'generazione video klippify' trovata e cliccata!")
                
                # Attendi che l'URL cambi (segno che la nuova chat si sta caricando)
                try:
                    page.wait_for_function(f"window.location.href !== '{old_url}'", timeout=8000)
                except:
                    pass
                
                # Attesa abbondante per permettere all'interfaccia di rigenerare la casella di testo
                time.sleep(5) 
            except Exception as e:
                print(f"[WARNING] Non sono riuscito a trovare o cliccare la chat 'generazione video klippify'. Continuo nella chat corrente. Errore: {e}")

            # Usa il prompt dinamico se fornito, altrimenti usa un default
            prompts = [prompt_to_send] if prompt_to_send else [
                "Genera un video di 5 secondi di un paesaggio naturale al tramonto."
            ]
            
            download_selector = 'button:has(mat-icon[data-mat-icon-name="download"]), a:has(mat-icon[data-mat-icon-name="download"]), button[aria-label*="Scarica" i], button[aria-label*="Download" i], mat-icon[data-mat-icon-name="download"]'

            for prompt in prompts:
                # 1. Conta i pulsanti di download già presenti nella chat PRIMA di inviare il nuovo prompt
                initial_download_count = page.locator(download_selector).count()
                print(f"[BOT] Video già presenti nella chat prima dell'invio: {initial_download_count}")

                print(f"[BOT] Sto inviando il prompt ({len(prompt)} caratteri): '{prompt[:80]}...'")
                
                try:
                    selectors_to_try = [
                        "rich-textarea div[contenteditable='true']",
                        "rich-textarea p",
                        "div[contenteditable='true'][role='textbox']",
                        "div[contenteditable='true']",
                        "rich-textarea",
                        "textarea",
                        "[role='textbox']"
                    ]
                    
                    text_area = None
                    for sel in selectors_to_try:
                        try:
                            el = page.locator(sel).first
                            el.wait_for(state="visible", timeout=6000)
                            text_area = el
                            print(f"[BOT] Casella di testo trovata con selettore: {sel}")
                            break
                        except:
                            continue
                            
                    if not text_area:
                        raise Exception("Nessun campo di testo trovato nello schermo. La pagina potrebbe non essersi caricata correttamente o richiede il login.")
                    
                    text_area.click(force=True)
                    time.sleep(0.5)
                    try:
                        text_area.focus()
                    except:
                        pass
                    time.sleep(0.5)
                    
                    # Inserimento del testo
                    page.keyboard.insert_text(prompt)
                    time.sleep(1)
                    
                    # Premi Invio
                    page.keyboard.press("Enter")
                    time.sleep(1)
                    
                    # Prova a cliccare pulsante Invia
                    try:
                        send_btn = page.locator('button[aria-label*="Invia"], button[aria-label*="Send"], button.send-button, button:has(mat-icon[data-mat-icon-name="send"]), mat-icon[data-mat-icon-name="send"]').last
                        if send_btn.is_visible():
                            send_btn.click(force=True)
                            print("[BOT] Cliccato pulsante Invia!")
                    except:
                        pass
                        
                except Exception as ui_err:
                    print(f"\n[ERROR] UI_FAILED: Impossibile inserire il prompt in Gemini. Dettagli: {ui_err}")
                    input("\nPremi Invio per chiudere questa finestra...")
                    browser.close()
                    sys.exit(1)
                
                print(f"[BOT] Prompt inviato con successo! Attendo la generazione del NUOVO video (obiettivo > {initial_download_count} video)...")
                try:
                    # Polling fino a 300s (5 min) per attendere che compaia il NUOVO video
                    start_time = time.time()
                    timeout_seconds = 300
                    new_video_ready = False

                    while time.time() - start_time < timeout_seconds:
                        current_count = page.locator(download_selector).count()
                        if current_count > initial_download_count:
                            print(f"\n[BOT] NUOVO video generato da Gemini! (Conteggio video: {initial_download_count} -> {current_count})")
                            new_video_ready = True
                            time.sleep(3) # Attesa per stabilizzazione del render
                            break
                        
                        elapsed = int(time.time() - start_time)
                        if elapsed > 0 and elapsed % 15 == 0:
                            print(f"[BOT] Gemini sta elaborando il video... ({elapsed}s trascorsi)")
                        
                        time.sleep(3)

                    if not new_video_ready:
                        raise Exception(f"Timeout dopo {timeout_seconds}s: Gemini non ha completato il nuovo video.")

                    print("[BOT] Avvio il download del NUOVO video...")
                    # Selezioniamo l'ULTIMO pulsante di download (il video appena generato)
                    new_download_btn = page.locator(download_selector).last
                    try:
                        new_download_btn.scroll_into_view_if_needed()
                    except:
                        pass
                    time.sleep(1)
                    
                    try:
                        with page.expect_download(timeout=45000) as download_info:
                            try:
                                new_download_btn.click()
                            except:
                                new_download_btn.click(force=True)
                        download = download_info.value
                        
                        videos_dir = Path(__file__).parent / "generated_videos"
                        videos_dir.mkdir(exist_ok=True)
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        ext = download.suggested_filename.split('.')[-1] if '.' in download.suggested_filename else 'mp4'
                        save_path = videos_dir / f"video_gemini_{timestamp}.{ext}"
                        
                        download.save_as(str(save_path))
                        print(f"\n[SUCCESS] NUOVO video scaricato con successo in: {save_path}")
                    except Exception as dl_err:
                        print(f"[WARNING] expect_download ha riscontrato: {dl_err}. Provo click alternativo...")
                        icon = page.locator('mat-icon[data-mat-icon-name="download"]').last
                        with page.expect_download(timeout=30000) as download_info2:
                            icon.click(force=True)
                        download2 = download_info2.value
                        videos_dir = Path(__file__).parent / "generated_videos"
                        videos_dir.mkdir(exist_ok=True)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        ext = download2.suggested_filename.split('.')[-1] if '.' in download2.suggested_filename else 'mp4'
                        save_path = videos_dir / f"video_gemini_{timestamp}.{ext}"
                        download2.save_as(str(save_path))
                        print(f"\n[SUCCESS] NUOVO video scaricato al secondo tentativo in: {save_path}")
                except Exception as e:
                    print(f"\n[WARNING] Errore nel download del nuovo video: {e}")
                
            print("\n" + "="*60)
            print("[BOT] Automazione completata!")
            
            if not is_auto:
                print("Il browser NON si chiuderà. Puoi navigare e scaricare i video manualmente se serve.")
                input("---> PREMI INVIO QUI per terminare lo script e chiudere il browser <---")
            else:
                print("[BOT] Chiusura automatica del browser...")
            
            browser.close()

    except Exception as fatal_err:
        print(f"\n[ERROR] FATAL_ERROR: {str(fatal_err)}")
        input("\nPremi Invio per chiudere questa finestra...")
        sys.exit(1)

from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automazione Gemini per Video')
    parser.add_argument('--prompt', type=str, help='Il prompt dinamico da inviare a Gemini', default=None)
    parser.add_argument('--auto', action='store_true', help='Salta gli input bloccanti per uso tramite API')
    args = parser.parse_args()
    
    prompt = args.prompt
    prompt_file = Path(__file__).parent / "pending_prompt.txt"
    if prompt_file.exists():
        try:
            prompt = prompt_file.read_text(encoding="utf-8").strip()
            prompt_file.unlink()
            print(f"[BOT] Caricato prompt dinamico da file temporaneo.")
        except Exception as e:
            print(f"[BOT] Errore lettura file prompt: {e}")
    
    try:
        run(prompt_to_send=prompt, is_auto=args.auto)
    except SystemExit:
        pass
    except Exception as e:
        print(f"\n[CRASH] Errore imprevisto: {e}")
        input("\nPremi Invio per chiudere questa finestra...")
