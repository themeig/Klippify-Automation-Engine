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

target_token_url = "https://app.klippify.com/campaigns/6a426231e6a21896f769dc80"

print(f"[+] Visiting campaign token page: {target_token_url}...")
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

    page.goto(target_token_url)
    time.sleep(4)

    txt = page.locator("body").inner_text()
    print("=== RAW PAGE TEXT ===")
    clean_txt = txt.encode("ascii", "ignore").decode("ascii")
    print(clean_txt[:2500])

    print("\n=== LINKS FOUND ON TOKEN PAGE ===")
    links = page.locator("a").all()
    for l in links:
        href = l.get_attribute("href")
        t = l.inner_text().strip().replace("\n", " ")
        if href:
            print(f"LINK: {t} -> {href}")

    browser.close()
