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

print("[+] Testing inner container scrolling on Klippify campaigns catalog...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
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

    # 1. Inspect all elements with overflow
    print("=== SCROLLABLE ELEMENTS ===")
    scrollables = page.evaluate("""
        () => {
            const elems = Array.from(document.querySelectorAll('*'));
            return elems.filter(el => {
                const style = window.getComputedStyle(el);
                return (style.overflowY === 'auto' || style.overflowY === 'scroll') && el.scrollHeight > el.clientHeight;
            }).map(el => ({
                tag: el.tagName,
                className: el.className,
                id: el.id,
                scrollHeight: el.scrollHeight,
                clientHeight: el.clientHeight
            }));
        }
    """)
    print(f"Found {len(scrollables)} scrollable inner elements:")
    for s in scrollables:
        print(f"   -> <{s['tag']}> class='{s['className']}' id='{s['id']}' | scrollHeight={s['scrollHeight']} clientHeight={s['clientHeight']}")

    # 2. Scroll ALL scrollable elements and window
    print("\n[+] Triggering deep scroll across all elements & mouse wheel...")
    for step in range(10):
        page.evaluate("""
            () => {
                window.scrollTo(0, document.body.scrollHeight);
                document.querySelectorAll('*').forEach(el => {
                    if (el.scrollHeight > el.clientHeight) {
                        el.scrollTop = el.scrollHeight;
                    }
                });
            }
        """)
        # Mouse wheel down
        page.mouse.wheel(0, 3000)
        time.sleep(1.5)

    # Count campaign links after scroll
    links = page.locator("a[href*='/campaigns/']").all()
    print(f"\n[+] Total campaign links after inner scrolling: {len(links)}")

    cards = page.locator("article, div[class*='campaign-card'], div[class*='card']").all()
    print(f"[+] Total campaign cards found: {len(cards)}")

    # Check search input / filters / tabs
    print("\n=== INPUTS & FILTERS ON PAGE ===")
    inputs = page.locator("input, select, button").all()
    for inp in inputs:
        val = inp.get_attribute("placeholder") or inp.inner_text().strip().replace("\n", " ")
        if val and len(val) < 60:
            print(f"INPUT/BTN: '{val}'")

    browser.close()
