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

print("[+] Querying Klippify REST API endpoints directly via Playwright request context...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(login_url)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(2)

    page.locator("input[name='email'], input[type='email']").first.fill(email)
    page.locator("input[name='password'], input[type='password']").first.fill(password)
    page.locator("button[type='submit'], button:has-text('Sign in')").first.click()
    time.sleep(4)

    # Now test REST API endpoints using page.evaluate fetch
    endpoints = [
        "https://app.klippify.com/api/creator/campaign/list?filter=new&limit=100",
        "https://app.klippify.com/api/creator/campaign/list?filter=all&limit=100",
        "https://app.klippify.com/api/creator/campaign/list?filter=active&limit=100",
        "https://app.klippify.com/api/creator/campaign/featured?limit=100",
        "https://app.klippify.com/api/creator/campaign/list"
    ]

    all_api_data = {}

    for ep in endpoints:
        print(f"\n[+] Fetching API: {ep}")
        res = page.evaluate(f"""
            async () => {{
                try {{
                    const r = await fetch('{ep}');
                    return await r.json();
                }} catch(e) {{
                    return {{ error: e.toString() }};
                }}
            }}
        """)
        all_api_data[ep] = res

        if isinstance(res, dict):
            c_list = res.get("data") or res.get("campaigns") or res.get("items") or []
            print(f"  -> Returned Dict with keys: {list(res.keys())}")
            if isinstance(c_list, list):
                print(f"  -> Found {len(c_list)} items in list!")
                for item in c_list[:10]:
                    if isinstance(item, dict):
                        print(f"     * Campaign: '{item.get('title') or item.get('name') or item.get('id')}' | Payout: {item.get('payout') or item.get('payoutRate')}")
        elif isinstance(res, list):
            print(f"  -> Returned List with {len(res)} items!")
            for item in res[:10]:
                if isinstance(item, dict):
                    print(f"     * Campaign: '{item.get('title') or item.get('name') or item.get('id')}'")

    with open(BASE_DIR / "api_direct_response.json", "w", encoding="utf-8") as f:
        json.dump(all_api_data, f, indent=2, ensure_ascii=False)

    print("\n[+] Direct API Response saved to api_direct_response.json")
    browser.close()
