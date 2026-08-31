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

target_url = "https://app.klippify.com/campaigns/6a426231e6a21896f769dc80"

print(f"[+] Inspecting token page: {target_url}")
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

    page.goto(target_url)
    time.sleep(3)

    print("=== HEADINGS ON TOKEN PAGE ===")
    headings = page.locator("h1, h2, h3, h4, h5").all()
    for h in headings:
        tag = h.evaluate("el => el.tagName")
        txt = h.inner_text().strip()
        print(f"<{tag}> {txt}")

    print("\n=== TEXT SURROUNDING 'Dettagli campagna' ===")
    detail_elem = page.locator("*:has-text('Dettagli campagna')").all()
    for el in detail_elem:
        txt = el.inner_text()
        if 20 < len(txt) < 500:
            print("FOUND:", txt.replace("\n", " | "))

    browser.close()
