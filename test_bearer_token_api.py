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

print("[+] Extracting Bearer Auth Token from localStorage & querying Klippify REST API...")
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

    # Dump localStorage & sessionStorage keys
    storage_data = page.evaluate("""
        () => {
            const loc = {};
            for (let i = 0; i < localStorage.length; i++) {
                const k = localStorage.key(i);
                loc[k] = localStorage.getItem(k);
            }
            const sess = {};
            for (let i = 0; i < sessionStorage.length; i++) {
                const k = sessionStorage.key(i);
                sess[k] = sessionStorage.getItem(k);
            }
            return { localStorage: loc, sessionStorage: sess };
        }
    """)

    print(f"LocalStorage keys: {list(storage_data['localStorage'].keys())}")
    print(f"SessionStorage keys: {list(storage_data['sessionStorage'].keys())}")

    # Find token
    token = None
    for k, v in storage_data['localStorage'].items():
        if "token" in k.lower() or "auth" in k.lower() or "jwt" in k.lower() or "session" in k.lower():
            print(f"  FOUND STORAGE KEY '{k}': {str(v)[:40]}...")
            if v and len(v) > 20:
                token = v.replace('"', '').replace("'", "").strip()

    # Now make authorized fetch calls
    api_results = {}
    endpoints = [
        "https://app.klippify.com/api/creator/campaign/list?limit=100",
        "https://app.klippify.com/api/creator/campaign/list?filter=all&limit=100",
        "https://app.klippify.com/api/creator/campaign/list?filter=new&limit=100",
        "https://app.klippify.com/api/creator/campaign/list?filter=active&limit=100",
        "https://app.klippify.com/api/creator/campaign/list?filter=paused&limit=100",
        "https://app.klippify.com/api/creator/campaign/list?filter=ended&limit=100",
        "https://app.klippify.com/api/creator/campaign/featured?limit=100"
    ]

    for ep in endpoints:
        print(f"\n[+] Fetching Authorized API: {ep}")
        res = page.evaluate(f"""
            async () => {{
                try {{
                    const token = localStorage.getItem('token') || localStorage.getItem('access_token') || localStorage.getItem('jwt') || Object.values(localStorage).find(v => v && v.length > 50);
                    const cleanToken = token ? token.replace(/"/g, '') : '';
                    const r = await fetch('{ep}', {{
                        headers: {{
                            'Authorization': 'Bearer ' + cleanToken,
                            'Content-Type': 'application/json'
                        }}
                    }});
                    return await r.json();
                }} catch(e) {{
                    return {{ error: e.toString() }};
                }}
            }}
        """)
        api_results[ep] = res

        if isinstance(res, dict):
            c_data = res.get("data")
            if isinstance(c_data, list):
                print(f"  -> SUCCESS! Found {len(c_data)} campaigns in API list!")
                for item in c_data:
                    if isinstance(item, dict):
                        print(f"     * '{item.get('title') or item.get('name')}' | Brand: '{item.get('brandName') or item.get('brand')}' | ID: {item.get('id') or item.get('_id')}")
            elif isinstance(c_data, dict) and "campaigns" in c_data:
                c_list = c_data["campaigns"]
                print(f"  -> SUCCESS! Found {len(c_list)} campaigns in c_data['campaigns']!")
                for item in c_list:
                    if isinstance(item, dict):
                        print(f"     * '{item.get('title') or item.get('name')}' | Brand: '{item.get('brandName') or item.get('brand')}' | ID: {item.get('id') or item.get('_id')}")

    with open(BASE_DIR / "authorized_api_response.json", "w", encoding="utf-8") as f:
        json.dump(api_results, f, indent=2, ensure_ascii=False)

    print("\n[+] Authorized API Response saved to authorized_api_response.json")
    browser.close()
