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

print("[+] Launching Playwright to test deep campaign URL extraction...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()

    print(f"[+] Logging in at {login_url}...")
    page.goto(login_url)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(2)

    page.locator("input[name='email'], input[type='email']").first.fill(email)
    page.locator("input[name='password'], input[type='password']").first.fill(password)
    page.locator("button[type='submit'], button:has-text('Sign in')").first.click()
    time.sleep(4)

    print("[+] Navigating to https://app.klippify.com/campaigns...")
    page.goto("https://app.klippify.com/campaigns")
    time.sleep(3)

    # Find all campaign links matching /campaigns/<id>
    links = page.locator("a[href*='/campaigns/']").all()
    print(f"[+] Found {len(links)} links matching /campaigns/<id>")

    campaign_urls = []
    for link in links:
        href = link.get_attribute("href")
        if href and href not in campaign_urls:
            if not href.startswith("http"):
                href = f"https://app.klippify.com{href}"
            campaign_urls.append(href)

    print(f"[+] Unique Campaign URLs Extracted ({len(campaign_urls)}):")
    for u in campaign_urls[:10]:
        print(f"    -> {u}")

    # Inspect the first campaign detail page
    if campaign_urls:
        target_url = campaign_urls[0]
        print(f"\n[+] Deep inspecting campaign detail page: {target_url}")
        page.goto(target_url)
        time.sleep(3)

        txt = page.locator("body").inner_text()
        print("\n--- DEEP PAGE TEXT SNIPPET ---")
        print(txt[:1500])

    browser.close()
