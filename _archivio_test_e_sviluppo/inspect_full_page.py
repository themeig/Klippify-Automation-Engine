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

print("[+] Inspecting complete Klippify campaigns catalog DOM & tabs...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 1000})
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

    # Take screenshot of the page
    screenshot_path = BASE_DIR / "klippify_campaigns_page.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
    print(f"[+] Saved full page screenshot to {screenshot_path}")

    # Inspect all tabs, buttons, links
    print("\n=== BUTTONS & TABS ON PAGE ===")
    buttons = page.locator("button, div[role='button'], a[role='tab'], span[class*='tab'], div[class*='filter']").all()
    for b in buttons:
        txt = b.inner_text().strip().replace("\n", " ")
        if txt and len(txt) < 80:
            print(f"BUTTON/TAB: '{txt}'")

    print("\n=== ALL HREFS ON PAGE ===")
    links = page.locator("a").all()
    for l in links:
        href = l.get_attribute("href")
        txt = l.inner_text().strip().replace("\n", " ")
        if href and len(txt) < 80:
            print(f"LINK: '{txt}' -> {href}")

    # Scroll down 5 times and check if new cards appear
    for s in range(5):
        page.keyboard.press("PageDown")
        time.sleep(1)

    print("\n=== ALL CARDS AFTER PAGE DOWN ===")
    cards = page.locator("article, div[class*='card'], div[class*='campaign']").all()
    print(f"Total card containers: {len(cards)}")
    for i, c in enumerate(cards):
        txt = c.inner_text().strip().replace("\n", " | ")
        if 15 < len(txt) < 300:
            print(f"CARD #{i+1}: {txt[:150]}")

    browser.close()
