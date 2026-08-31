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

print("[+] Inspecting catalog pagination & ALL available campaigns on Klippify...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 900})

    page.goto(login_url)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(2)

    page.locator("input[name='email'], input[type='email']").first.fill(email)
    page.locator("input[name='password'], input[type='password']").first.fill(password)
    page.locator("button[type='submit'], button:has-text('Sign in')").first.click()
    time.sleep(4)

    page.goto("https://app.klippify.com/campaigns")
    time.sleep(3)

    # Click every button on page that might load more or switch tabs
    btns = page.locator("button, div[role='button'], a[role='button']").all()
    print(f"Found {len(btns)} interactive buttons on page:")
    for b in btns:
        try:
            t = b.inner_text().strip().replace("\n", " ")
            if t and len(t) < 50:
                print(f"   BTN: '{t}'")
        except:
            pass

    # Extract all campaign text blocks / titles / brands
    articles = page.locator("article, div[class*='card'], div[class*='border']").all()
    print(f"\nFound {len(articles)} card elements on page")

    browser.close()
