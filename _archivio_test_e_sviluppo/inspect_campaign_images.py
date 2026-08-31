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

sample_tokens = [
    {"name": "Riccardo Dose", "token": "6a426231e6a21896f769dc80"},
    {"name": "Million Hospitality", "token": "6a64cf756cdfd98478f11f28"},
    {"name": "Marco Cappelli Personal Brand", "token": "694e91113d6a349f51473682"},
    {"name": "Mondocash Podcast", "token": "6a759fd05ade3cb2f771b439"},
    {"name": "Gabriele Vagnato", "token": "6a7672465ade3cb2f773f6c9"},
    {"name": "Boardingame #1", "token": "69d9fd5061ce1b8904c42316"}
]

print("[+] Inspecting real campaign image & banner URLs on token pages...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(login_url)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(2)

    page.locator("input[name='email'], input[type='email']").first.fill(email)
    page.locator("input[name='password'], input[type='password']").first.fill(password)
    page.locator("button[type='submit'], button:has-text('Sign in')").first.click()
    time.sleep(3)

    results = []
    for item in sample_tokens:
        url = f"https://app.klippify.com/campaigns/{item['token']}"
        page.goto(url, timeout=20000)
        time.sleep(2)

        imgs = page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('img')).map(i => ({
                    src: i.src,
                    alt: i.alt,
                    className: i.className,
                    width: i.width,
                    height: i.height
                }));
            }
        """)

        print(f"\n--- {item['name']} ({item['token']}) ---")
        for img in imgs:
            if "avatar" not in img['src'].lower() and "logo" not in img['src'].lower() and img['width'] > 50:
                print(f"  IMAGE: src='{img['src']}' | alt='{img['alt']}' | size={img['width']}x{img['height']}")
            elif "upload" in img['src'].lower() or "klippify" in img['src'].lower():
                print(f"  ASSET: src='{img['src']}' | alt='{img['alt']}'")
        
        results.append({"token": item['token'], "name": item['name'], "images": imgs})

    browser.close()

with open(BASE_DIR / "extracted_campaign_images.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("\n[+] Inspection saved to extracted_campaign_images.json")
