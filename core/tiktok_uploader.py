import paths
import sys
import time
import argparse
import os
import re
import json
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.sync_api import sync_playwright

BASE_DIR = paths.PROJECT_ROOT

def dismiss_cookie_and_overlays(page, iframe=None):
    """Automatically dismiss or remove TikTok cookie banner and annoying modal overlays."""
    try:
        cookie_selectors = [
            'button:has-text("Rifiuta tutto")',
            'button:has-text("Accetta tutti")',
            'button:has-text("Accept all")',
            'button:has-text("Decline all")',
            'tiktok-cookie-banner button',
            '.tiktok-cookie-banner button'
        ]
        for sel in cookie_selectors:
            try:
                btn = page.locator(sel)
                if btn.count() > 0 and btn.first.is_visible():
                    btn.first.click(timeout=1500, force=True)
                    print("[BOT] Cookie banner TikTok gestito con successo.")
                    break
            except Exception:
                pass
    except Exception:
        pass

    try:
        page.evaluate("""() => {
            const elements = document.querySelectorAll('tiktok-cookie-banner, .tiktok-cookie-banner, #tiktok-cookie-banner, [user-config-ele-id="tiktok-cookie-banner-config"], .modal-backdrop, .overlay-container');
            elements.forEach(el => {
                try { el.remove(); } catch(e) {}
            });
        }""")
    except Exception:
        pass

    if iframe is not None:
        try:
            iframe.locator('tiktok-cookie-banner button, button:has-text("Rifiuta tutto"), button:has-text("Accetta tutti")').first.click(timeout=1000, force=True)
        except Exception:
            pass

def get_known_old_video_ids():
    """Extract all previously known TikTok video IDs from disk to prevent submitting duplicates."""
    known_ids = set()
    
    # 1. published_content.json
    pub_file = BASE_DIR / "published_content.json"
    if pub_file.exists():
        try:
            with open(pub_file, "r", encoding="utf-8") as pf:
                data = json.load(pf)
                for item in data:
                    for k in ["tiktok_url", "post_url", "video_url"]:
                        url = item.get(k)
                        if url:
                            m = re.search(r'/video/(\d+)', str(url))
                            if m:
                                known_ids.add(m.group(1))
        except Exception:
            pass

    # 2. klippify_submissions.json
    sub_file = BASE_DIR / "klippify_submissions.json"
    if sub_file.exists():
        try:
            with open(sub_file, "r", encoding="utf-8") as sf:
                data = json.load(sf)
                for item in data:
                    url = item.get("post_url")
                    if url:
                        m = re.search(r'/video/(\d+)', str(url))
                        if m:
                            known_ids.add(m.group(1))
        except Exception:
            pass

    # Add static reference IDs
    known_ids.add("7676702767729151254")
    return known_ids

def run_uploader(video_path, title, cover_time_sec=1.0, is_auto=False, campaign_id=None):
    print("[BOT] Avvio inizializzazione di Playwright per TikTok...")
    try:
        # Pre-check file validity
        if not os.path.exists(video_path):
            print(f"[ERROR] Video non trovato sul disco: {video_path}")
            sys.exit(1)

        filesize_mb = os.path.getsize(video_path) / (1024 * 1024)
        if filesize_mb < 0.5:
            print(f"[ERROR] File video corrotto o incompleto ({filesize_mb:.2f} MB < 0.5 MB): {video_path}")
            sys.exit(1)

        print(f"[BOT] File video valido confermato: {os.path.basename(video_path)} ({filesize_mb:.2f} MB)")

        # Carica storico ID esistenti
        known_old_video_ids = get_known_old_video_ids()
        print(f"[BOT] Caricati {len(known_old_video_ids)} ID video storici per escludere duplicati.")

        with sync_playwright() as p:
            user_data_dir = "./tiktok_profile"
            
            try:
                browser = p.chromium.launch_persistent_context(
                    user_data_dir,
                    headless=False,
                    no_viewport=True,
                    executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    args=["--disable-blink-features=AutomationControlled", "--start-maximized", "--no-first-run"]
                )
            except Exception as e:
                print(f"[ERROR] Impossibile avviare il browser. Chiudi eventuali altre finestre di Chrome. Dettagli: {e}")
                sys.exit(1)
            
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            if not is_auto:
                print("\n" + "="*60)
                print("LOGIN MANUALE SU TIKTOK")
                print("1. Sto aprendo la pagina di login di TikTok...")
                page.goto("https://www.tiktok.com/login", timeout=60000)
                print("2. Esegui il login col tuo account.")
                print("="*60 + "\n")
                while True:
                    time.sleep(1)
            
            # AUTOMATION MODE
            print(f"[BOT] Apertura pagina TikTok Studio Upload...")
            page.goto("https://www.tiktok.com/tiktokstudio/upload?from=upload", timeout=60000)
            time.sleep(4)
            dismiss_cookie_and_overlays(page)
            
            if "login" in page.url:
                print("[ERROR] NON SEI LOGGATO! Esegui prima il login su TikTok.")
                browser.close()
                sys.exit(1)

            # 1. Pulisce eventuali bozze non salvate precedenti
            print("[BOT] Controllo e pulizia bozze precedenti...")
            def clear_unsaved_drafts(p_obj):
                try:
                    for _ in range(3):
                        scarta_btns = p_obj.locator('button:has-text("Scarta"), button:has-text("Discard")').all()
                        for btn in scarta_btns:
                            if btn.is_visible():
                                print("[BOT] Trovato avviso bozza non salvata, clicco Scarta...")
                                btn.click(force=True)
                                time.sleep(1)
                        modal_scarta = p_obj.locator('div[role="dialog"] button:has-text("Scarta"), .modal button:has-text("Scarta")').all()
                        for mbtn in modal_scarta:
                            if mbtn.is_visible():
                                print("[BOT] Confermo eliminazione bozza nel popup modale...")
                                mbtn.click(force=True)
                                time.sleep(1)
                except Exception:
                    pass

            clear_unsaved_drafts(page)
            
            # 2. Caricamento video con multi-strategia (frame, pagina principale, file chooser)
            print(f"[BOT] Carico il file video nel browser: {os.path.basename(video_path)}...")
            uploaded = False
            iframe = None

            for attempt in range(40):
                dismiss_cookie_and_overlays(page)
                
                # Strategia A: cerca input file in tutti i frames
                for f in page.frames:
                    try:
                        f_inputs = f.locator('input[type="file"]').all()
                        if f_inputs:
                            f_inputs[0].set_input_files(str(video_path))
                            print("[BOT] File video agganciato con successo tramite frame input!")
                            uploaded = True
                            iframe = f
                            break
                    except Exception:
                        pass
                if uploaded:
                    break

                # Strategia B: cerca input file nella pagina principale
                try:
                    main_inputs = page.locator('input[type="file"]').all()
                    if main_inputs:
                        main_inputs[0].set_input_files(str(video_path))
                        print("[BOT] File video agganciato tramite input file principale!")
                        uploaded = True
                        break
                except Exception:
                    pass
                if uploaded:
                    break

                # Strategia C: FileChooser con clic su "Seleziona video"
                try:
                    sel_btn = page.locator('button:has-text("Seleziona video"), button:has-text("Select video"), button:has-text("Carica"), .upload-btn').first
                    if sel_btn.is_visible():
                        with page.expect_file_chooser(timeout=3000) as fc_info:
                            sel_btn.click(force=True)
                        fc = fc_info.value
                        fc.set_files(str(video_path))
                        print("[BOT] File video caricato con successo tramite FileChooser!")
                        uploaded = True
                        break
                except Exception:
                    pass
                if uploaded:
                    break

                time.sleep(1)

            if not uploaded:
                print(f"[ERROR] Impossibile trovare l'area di caricamento video su TikTok Studio entro 40 secondi.")
                page.screenshot(path=str(BASE_DIR / "debug_tiktok_upload_error.png"))
                browser.close()
                sys.exit(1)
                
            print("[BOT] Video inviato. Attendo transcodifica ed apertura editor TikTok...")
            
            # 3. Attesa e gestione dell'editor (NON scartare bozze durante questa fase!)
            editor_found = False
            print("[BOT] In attesa che TikTok completi la transcodifica del video e apra l'editor (può richiedere 20-40s)...")
            for wait_ed in range(1, 80):
                time.sleep(1)
                dismiss_cookie_and_overlays(page)

                # Cerca l'editor nella pagina principale e in tutti i frame
                all_contexts = [page] + page.frames
                for ctx_target in all_contexts:
                    try:
                        editor = ctx_target.locator('.public-DraftEditor-content, [contenteditable="true"], .DraftEditor-root, div[data-placeholder], textarea')
                        if editor.count() > 0 and editor.first.is_visible():
                            print(f"[BOT] Editor TikTok pronto al secondo {wait_ed}!")
                            editor_found = True
                            try:
                                editor.first.click(force=True)
                                time.sleep(0.5)
                                page.keyboard.press("Control+A")
                                page.keyboard.press("Backspace")
                                time.sleep(0.3)
                                page.keyboard.type(title, delay=15)
                                time.sleep(1)
                                page.keyboard.press("Escape")
                                print("[BOT] Descrizione, hashtag e menzioni inseriti con successo.")
                            except Exception as ed_ex:
                                print(f"[WARNING] Errore digitazione caption: {ed_ex}")
                            break
                    except Exception:
                        pass

                if editor_found:
                    break

                if wait_ed % 10 == 0:
                    print(f"[BOT] Elaborazione video e transcodifica TikTok in corso ({wait_ed}s)...")

            if not editor_found:
                print("[ERROR] Timeout: l'editor video di TikTok non si è aperto entro 80 secondi.")
                try:
                    page.screenshot(path=str(BASE_DIR / "tiktok_error_editor_timeout.png"))
                except:
                    pass
                browser.close()
                sys.exit(1)

            # 4. Attesa che il file raggiunga il 100% del caricamento su TikTok
            print("[BOT] Attendo che il file video completi il caricamento (100%) e i controlli...")
            for wait_upload_sec in range(60):
                time.sleep(1)
                dismiss_cookie_and_overlays(page, iframe)
                
                # Indicatori di upload completato
                indicators = page.locator('div:has-text("100%"), span:has-text("100%"), div:has-text("Caricato"), span:has-text("Caricato"), div:has-text("Uploaded"), span:has-text("Uploaded")')
                if indicators.count() > 0 and indicators.first.is_visible():
                    print(f"[BOT] Caricamento al 100% confermato al secondo {wait_upload_sec + 1}!")
                    break
                
                # Se il pulsante pubblica è visibile e non disabilitato
                ctx = iframe if iframe is not None else page
                pb_test = ctx.locator('button:has-text("Pubblica"), button:has-text("Post"), button[data-e2e="post_video_button"]').first
                if pb_test.is_visible() and not pb_test.is_disabled() and wait_upload_sec > 15:
                    print(f"[BOT] Pulsante Pubblica già attivo e pronto al secondo {wait_upload_sec + 1}!")
                    break

            # 5. Localizzazione ed attivazione del vero pulsante Pubblica in basso a destra
            print("[BOT] Cerco il pulsante 'Pubblica' in basso a destra...")
            post_btn = None
            for find_btn_attempt in range(20):
                ctx = iframe if iframe is not None else page
                candidates = [
                    'button[data-e2e="post_video_button"]',
                    'div.btn-post button',
                    'div[class*="btn-post"] button',
                    'button.btn-post',
                    'button[class*="Button__root--type-primary"]:has-text("Pubblica")',
                    'div[class*="footer"] button:has-text("Pubblica")',
                    'div[class*="form"] button:has-text("Pubblica")',
                    'button:has-text("Pubblica")'
                ]
                for c_sel in candidates:
                    try:
                        locs = ctx.locator(c_sel).all()
                        for loc in locs:
                            if loc.is_visible():
                                txt = loc.inner_text().strip().lower()
                                # Esclude pulsanti di navigazione sidebar o chiusura
                                if "pubblica" in txt or "btn-post" in (loc.get_attribute("class") or "").lower():
                                    post_btn = loc
                                    break
                    except Exception:
                        pass
                    if post_btn:
                        break
                if post_btn:
                    break
                time.sleep(1.5)

            if not post_btn:
                print("[ERROR] Impossibile trovare il pulsante 'Pubblica' sulla pagina di TikTok Studio.")
                page.screenshot(path=str(BASE_DIR / "tiktok_error_post_btn.png"))
                browser.close()
                sys.exit(1)

            try:
                post_btn.scroll_into_view_if_needed(timeout=3000)
            except Exception:
                pass

            # Attendi che il pulsante sia abilitato
            print("[BOT] Verifico che il pulsante Pubblica sia attivo...")
            for wait_enable in range(25):
                try:
                    if not post_btn.is_disabled():
                        print("[BOT] Pulsante Pubblica abilitato!")
                        break
                except Exception:
                    pass
                time.sleep(1)

            # Click su Pubblica
            print("[BOT] Clicco su 'Pubblica'...")
            try:
                post_btn.click(force=True)
                print("[BOT] Cliccato su Pubblica. Attendo conferma di TikTok...")
            except Exception as click_err:
                print(f"[ERROR] Errore nel click su Pubblica: {click_err}")
                browser.close()
                sys.exit(1)

            # Gestione eventuali popup di conferma post-pubblicazione (es: "Pubblica ora", "Pubblica comunque", "Gestisci i tuoi post")
            print("[BOT] Attendo e gestisco eventuale modale di conferma pubblicazione...")
            for sec in range(1, 15):
                time.sleep(1)
                try:
                    confirm_btns = page.locator('div[role="dialog"] button:has-text("Pubblica ora"), div[role="dialog"] button:has-text("Post now"), div[role="dialog"] button:has-text("Pubblica comunque"), div[role="dialog"] button:has-text("Post anyway"), div[role="dialog"] button:has-text("Continua"), div[role="dialog"] button:has-text("Continue"), div[role="dialog"] button.Button__root--type-primary, div[role="dialog"] button:has-text("Gestisci"), div[role="dialog"] button:has-text("Visualizza")')
                    if confirm_btns.count() > 0 and confirm_btns.first.is_visible():
                        btn_txt = confirm_btns.first.text_content().strip()
                        print(f"[BOT] Trovato popup di conferma ('{btn_txt}'), clicco conferma...")
                        confirm_btns.first.click(force=True)
                        time.sleep(3)
                        break
                except Exception:
                    pass

            # 6. Estrazione RIGOROSA del link del NUOVO video pubblicato
            post_url = None
            new_video_id = None
            try:
                print("[BOT] Verifica e recupero del NUOVO link video...")
                # Prova dai link presenti nella schermata di successo
                links = page.locator('a[href*="/video/"]').all()
                for l in links:
                    href = l.get_attribute("href")
                    if href and "/video/" in href:
                        m = re.search(r'/video/(\d+)', href)
                        if m and m.group(1) not in known_old_video_ids:
                            new_video_id = m.group(1)
                            post_url = href.split("?")[0]
                            break
                
                # Se non presente sulla schermata, navighiamo su TikTok Studio Content
                if not post_url:
                    print("[BOT] Navigo su TikTok Studio Content per estrarre l'ID del nuovo video...")
                    page.goto("https://www.tiktok.com/tiktokstudio/content", timeout=30000, wait_until="domcontentloaded")
                    time.sleep(4)
                    
                    # Polling con refresh progressivo fino a 40 secondi
                    for attempt in range(1, 10):
                        if attempt > 1:
                            try:
                                page.reload(wait_until="domcontentloaded", timeout=15000)
                                time.sleep(3)
                            except Exception:
                                pass
                                
                        content_links = page.locator('a[href*="/video/"]').all()
                        for l in content_links:
                            href = l.get_attribute("href")
                            if href and "/video/" in href:
                                m = re.search(r'/video/(\d+)', href)
                                if m and m.group(1) not in known_old_video_ids:
                                    new_video_id = m.group(1)
                                    post_url = href.split("?")[0]
                                    print(f"[BOT] Nuovo video ID individuato con successo: {new_video_id} -> {post_url}")
                                    break
                        if post_url:
                            break
                        print(f"[BOT] Attesa elaborazione nuovo video su TikTok Studio (tentativo {attempt}/9)...")
                        time.sleep(4)
            except Exception as find_ex:
                print(f"[BOT] Nota recupero URL: {find_ex}")

            # Salvataggio screenshot di stato finale
            try:
                debug_shot = BASE_DIR / "tiktok_last_upload_state.png"
                page.screenshot(path=str(debug_shot), full_page=True)
                print(f"[BOT] Screenshot stato salvato in: {debug_shot}")
            except Exception:
                pass

            if post_url and new_video_id:
                if not post_url.startswith("http"):
                    post_url = "https://www.tiktok.com" + ("/" if not post_url.startswith("/") else "") + post_url
                print("\n" + "="*60)
                print(f"🎬 LINK DEL NUOVO VIDEO TIKTOK CONFERMATO: {post_url}")
                print("="*60 + "\n")

                # Registra in published_content.json
                try:
                    pub_file = BASE_DIR / "published_content.json"
                    records = []
                    if pub_file.exists():
                        with open(pub_file, "r", encoding="utf-8") as pf:
                            records = json.load(pf)
                    records.append({
                        "filename": os.path.basename(video_path),
                        "tiktok_url": post_url,
                        "post_url": post_url,
                        "video_id": new_video_id,
                        "campaign_id": campaign_id,
                        "title": title,
                        "published_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    with open(pub_file, "w", encoding="utf-8") as pf:
                        json.dump(records, pf, indent=2, ensure_ascii=False)
                    print("[BOT] Salvato nuovo video nel registro published_content.json.")
                except Exception as save_err:
                    print(f"[WARNING] Impossibile salvare in published_content.json: {save_err}")
            else:
                print("\n⚠️ [ATTENZIONE] Il nuovo video non è stato rilevato tra i post appena pubblicati.")
                print("⚠️ [BLOCCO SICUREZZA] Nessun vecchio video verrà inviato a Klippify per prevenire duplicati.")

            print("\n[SUCCESS] Sessione browser TikTok completata.")
            browser.close()

        # SOTTOMISSIONE AUTOMATICA SU KLIPPIFY SOLO CON LINK NUOVO CONFERMATO
        if campaign_id and campaign_id != "unknown" and post_url and new_video_id:
            print(f"\n[KLIPPIFY] Avvio invio automatico del nuovo video a Klippify per la campagna ID: {campaign_id}...")
            try:
                from klippify_scraper import submit_video_to_klippify
                k_res = submit_video_to_klippify(campaign_id, post_url, platform="tiktok")
                print(f"[KLIPPIFY] Risposta API Klippify: {k_res}")
                if isinstance(k_res, dict) and (k_res.get("statusCode") == 200 or k_res.get("success") or "Submited" in str(k_res)):
                    print("✅ VIDEO INVIATO E REGISTRATO SU KLIPPIFY CON SUCCESSO!")
                else:
                    print(f"⚠️ Nota invio Klippify: {k_res}")

                # Pulizia automatica file .mp4 della clip pubblicata SOLO ADESSO che tutto è completato
                try:
                    import storage_manager
                    storage_manager.delete_published_clip(os.path.basename(video_path), campaign_id=campaign_id)
                except Exception as cl_err:
                    print(f"[STORAGE WARNING] Impossibile eliminare clip post-upload: {cl_err}")

            except Exception as k_ex:
                print(f"[KLIPPIFY ERROR] Errore invio automatico a Klippify: {k_ex}")
        elif not post_url:
            print("[KLIPPIFY] Invio a Klippify annullato: nessun nuovo post TikTok rilevato.")
            sys.exit(1)

    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, help="Percorso del video da caricare")
    parser.add_argument("--title", type=str, help="Titolo/Caption del video")
    parser.add_argument("--cover", type=float, default=1.0, help="Secondo esatto da usare come copertina")
    parser.add_argument("--auto", action="store_true", help="Esegui in modalità automatica senza attendere input")
    parser.add_argument("--campaign_id", type=str, default="unknown", help="ID della campagna Klippify")
    parser.add_argument("--payload", type=str, help="File JSON contenente i parametri di upload")

    args = parser.parse_args()

    v_path = args.video
    v_title = args.title
    v_cover = args.cover
    v_auto = args.auto
    v_camp = args.campaign_id

    if args.payload and os.path.exists(args.payload):
        with open(args.payload, "r", encoding="utf-8") as pf:
            p_data = json.load(pf)
            v_path = p_data.get("video") or p_data.get("video_path") or v_path
            v_title = p_data.get("title") or v_title
            v_cover = p_data.get("cover") or p_data.get("cover_time_sec") or v_cover
            v_camp = p_data.get("campaign_id") or v_camp
            v_auto = True

    if not v_path:
        print("Uso: python tiktok_uploader.py --video <file.mp4> --title <titolo> [--auto] [--campaign_id <id>]")
        print("Oppure: python tiktok_uploader.py (per aprire il browser ed eseguire il login)")
        run_uploader(None, None, is_auto=False)
    else:
        run_uploader(v_path, v_title, cover_time_sec=v_cover, is_auto=v_auto, campaign_id=v_camp)