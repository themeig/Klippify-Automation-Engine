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

print("[+] Launching Playwright to inspect Million Hospitality card...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
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

    # Find element containing 'Million'
    million_elems = page.locator("*:has-text('Million Hospitality')").all()
    print(f"[+] Found {len(million_elems)} elements with text Million Hospitality")

    for i, elem in enumerate(million_elems):
        try:
            txt = elem.inner_text()
            if 20 < len(txt) < 1500:
                print(f"\n--- ELEMENT #{i} ---")
                print(txt)
                print("-" * 50)
                html = elem.inner_html()
                print("RAW HTML:")
                print(html[:1000])
        except Exception as e:
            pass

    browser.close()
