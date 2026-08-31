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

print("[+] Testing infinite scroll on Klippify campaigns catalog...")
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

    # Initial links
    init_links = page.locator("a[href*='/campaigns/']").all()
    print(f"[+] Initial campaign links before scrolling: {len(init_links)}")

    # Scroll down 8 times
    for i in range(1, 9):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1.5)
        current_links = page.locator("a[href*='/campaigns/']").all()
        print(f"    Scroll #{i}: {len(current_links)} campaign links found.")

    # Unique tokens
    unique_urls = []
    for l in page.locator("a[href*='/campaigns/']").all():
        href = l.get_attribute("href")
        if href and href not in unique_urls:
            unique_urls.append(href)

    print(f"\n[+] TOTAL UNIQUE CAMPAIGNS DISCOVERED AFTER SCROLLING: {len(unique_urls)}")
    for u in unique_urls:
        print(f"    -> {u}")

    browser.close()
