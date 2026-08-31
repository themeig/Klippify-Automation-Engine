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

print("[+] Testing DEEP INFINITE SCROLL with Network Intercept & Keyboard End keys...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1400, "height": 900})
    page = context.new_page()

    # Network listener to capture campaign API responses
    api_campaigns = []
    def handle_response(response):
        if "campaign" in response.url.lower():
            try:
                ct = response.headers.get("content-type", "")
                if "json" in ct:
                    data = response.json()
                    print(f"[NETWORK API DETECTED]: {response.url[:80]}...")
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and "id" in item:
                                api_campaigns.append(item)
                    elif isinstance(data, dict):
                        for k, v in data.items():
                            if isinstance(v, list):
                                for item in v:
                                    if isinstance(item, dict) and ("id" in item or "name" in item):
                                        api_campaigns.append(item)
            except Exception:
                pass

    page.on("response", handle_response)

    page.goto(login_url)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(2)

    page.locator("input[name='email'], input[type='email']").first.fill(email)
    page.locator("input[name='password'], input[type='password']").first.fill(password)
    page.locator("button[type='submit'], button:has-text('Sign in')").first.click()
    time.sleep(4)

    page.goto("https://app.klippify.com/campaigns")
    time.sleep(3)

    print("\n[+] Starting continuous scroll loop with PageDown/End keys and Mouse Wheel...")
    previous_count = 0
    for scroll_idx in range(1, 30):
        # 1. Scroll window and all inner elements
        page.evaluate("""
            () => {
                window.scrollTo(0, document.body.scrollHeight);
                const all = document.querySelectorAll('*');
                all.forEach(el => {
                    if (el.scrollHeight > el.clientHeight && el.clientHeight > 100) {
                        el.scrollTop = el.scrollHeight;
                    }
                });
            }
        """)
        # 2. Press Keyboard END & PageDown
        page.keyboard.press("End")
        page.keyboard.press("PageDown")
        page.mouse.wheel(0, 10000)

        time.sleep(2.0)

        # Count current campaign elements & links
        links = page.locator("a[href*='/campaigns/']").all()
        cards = page.locator("article, div[class*='card'], div[class*='campaign']").all()
        print(f"Scroll step #{scroll_idx}: Found {len(links)} token links | {len(cards)} card containers")

        if len(links) > previous_count:
            previous_count = len(links)
            print(f"  --> 🎉 NEW CAMPAIGNS LOADED! Total now: {len(links)}")

    # Extract all campaign titles visible on page
    titles = page.evaluate("""
        () => {
            const results = [];
            document.querySelectorAll('h1, h2, h3, h4, div, span, p').forEach(el => {
                const text = el.innerText ? el.innerText.strip ? el.innerText.strip() : el.innerText : '';
                if (text && text.length > 3 && text.length < 60) {
                    results.append ? results.append(text) : results.push(text);
                }
            });
            return results;
        }
    """)

    token_items = []
    token_links = page.locator("a[href*='/campaigns/']").all()
    for link in token_links:
        href = link.get_attribute("href")
        if href:
            full_url = href if href.startswith("http") else f"https://app.klippify.com{href}"
            token_id = full_url.rstrip("/").split("/")[-1]
            if token_id not in [t["token"] for t in token_items]:
                token_items.append({"token": token_id, "url": full_url})

    print(f"\n[+] FINAL TOTAL TOKEN CAMPAIGNS FOUND AFTER DEEP SCROLL: {len(token_items)}")
    for i, t in enumerate(token_items, 1):
        print(f"  [{i}] Token: {t['token']} -> {t['url']}")

    with open(BASE_DIR / "deep_scroll_tokens.json", "w", encoding="utf-8") as f:
        json.dump(token_items, f, indent=2, ensure_ascii=False)

    time.sleep(5)
    browser.close()
