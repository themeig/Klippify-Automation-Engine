import time
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"C:\Users\HP\Desktop\contenuti klippify")
CONFIG_FILE = BASE_DIR / "klippify_config.json"

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    cfg = json.load(f)

email = cfg["email"]
password = cfg["password"]
login_url = cfg.get("login_url", "https://app.klippify.com/signin")

print("[+] Starting FULL DEEP MULTI-TAB SCRAPE across ALL sections...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()

    page.goto(login_url)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(2)

    page.locator("input[name='email'], input[type='email']").first.fill(email)
    page.locator("input[name='password'], input[type='password']").first.fill(password)
    page.locator("button[type='submit'], button:has-text('Sign in')").first.click()
    time.sleep(4)

    page.goto("https://app.klippify.com/campaigns")
    time.sleep(3)

    tabs_to_scan = ["Nuove", "Iscritte", "In pausa", "Passate", "Lista d'attesa", "Rifiutate"]
    all_campaign_items = []

    for tab_name in tabs_to_scan:
        print(f"\n[+] === SCANNING TAB: '{tab_name}' ===")
        try:
            tab_locator = page.get_by_text(tab_name, exact=False).first
            if tab_locator.is_visible():
                print(f"[+] Clicking tab '{tab_name}'...")
                tab_locator.click()
                time.sleep(2.5)
            else:
                print(f"[-] Tab '{tab_name}' not visible")
        except Exception as e:
            print(f"[-] Could not click tab '{tab_name}': {e}")

        # Infinite Scroll on main container
        for step in range(8):
            page.evaluate("""
                () => {
                    const main = document.querySelector('main.app-main-content, main, div.overflow-auto');
                    if (main) { main.scrollTop = main.scrollHeight; }
                    window.scrollTo(0, document.body.scrollHeight);
                    document.querySelectorAll('div').forEach(d => {
                        if (d.scrollHeight > d.clientHeight && d.clientHeight > 200) {
                            d.scrollTop = d.scrollHeight;
                        }
                    });
                }
            """)
            page.mouse.wheel(0, 5000)
            time.sleep(1.0)

        # Extract links
        links = page.locator("a[href*='/campaigns/']").all()
        print(f"[+] Found {len(links)} links on tab '{tab_name}'")

        for l in links:
            try:
                href = l.get_attribute("href")
                if href:
                    full_url = href if href.startswith("http") else f"https://app.klippify.com{href}"
                    token_id = full_url.rstrip("/").split("/")[-1]
                    if token_id and token_id not in [item["token"] for item in all_campaign_items]:
                        all_campaign_items.append({"token": token_id, "url": full_url, "section": tab_name})
            except Exception as e:
                pass

    print(f"\n[+] Total UNIQUE campaign tokens found across ALL tabs: {len(all_campaign_items)}")
    for idx, item in enumerate(all_campaign_items, 1):
        print(f"  [{idx}] Section: {item['section']} | Token: {item['token']} | URL: {item['url']}")

    # Save to file
    with open(BASE_DIR / "all_discovered_tokens.json", "w", encoding="utf-8") as f:
        json.dump(all_campaign_items, f, indent=2, ensure_ascii=False)

    browser.close()
