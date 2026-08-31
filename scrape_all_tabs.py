import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"C:\Users\HP\Desktop\contenuti klippify")
CONFIG_FILE = BASE_DIR / "klippify_config.json"

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    cfg = json.load(f)

email = cfg["email"]
password = cfg["password"]
login_url = cfg.get("login_url", "https://app.klippify.com/signin")

print("[+] Launching Playwright to scrape ALL campaign tabs on Klippify...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 800})
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

    tabs = ["Nuove", "Iscritte", "In pausa", "Passate", "Lista d'attesa", "Rifiutate"]
    all_campaign_items = []

    for tab_name in tabs:
        print(f"\n[+] Clicking tab: '{tab_name}'...")
        try:
            tab_elem = page.locator(f"button:has-text('{tab_name}'), div:has-text('{tab_name}'), span:has-text('{tab_name}')").first
            if tab_elem.is_visible():
                tab_elem.click()
                time.sleep(2)

                # Scroll down to load cards in this tab
                for _ in range(5):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(0.8)

                links = page.locator("a[href*='/campaigns/']").all()
                print(f"    Found {len(links)} links in tab '{tab_name}'")

                for l in links:
                    href = l.get_attribute("href")
                    if href:
                        full_url = href if href.startswith("http") else f"https://app.klippify.com{href}"
                        token_id = full_url.rstrip("/").split("/")[-1]
                        if token_id not in [item["token"] for item in all_campaign_items]:
                            all_campaign_items.append({"token": token_id, "url": full_url, "tab": tab_name})

        except Exception as e:
            print(f"    Notice clicking tab '{tab_name}': {e}")

    print(f"\n[+] GRAND TOTAL UNIQUE CAMPAIGN TOKENS FOUND ACROSS ALL TABS: {len(all_campaign_items)}")
    for item in all_campaign_items:
        print(f"    -> Token: {item['token']} | Tab: {item['tab']} | URL: {item['url']}")

    browser.close()
