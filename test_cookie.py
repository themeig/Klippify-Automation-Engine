import browser_cookie3
import json
import sys

try:
    print("Tentativo di leggere i cookie da Chrome...")
    # Get all cookies from Chrome
    cj = browser_cookie3.chrome(domain_name='tiktok.com')
    cookies = []
    for cookie in cj:
        cookies.append({
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path,
            "secure": cookie.secure,
            "httpOnly": "HttpOnly" in cookie._rest.keys() if cookie._rest else False
        })
    print(f"Trovati {len(cookies)} cookie di TikTok.")
    with open("tiktok_cookies.json", "w") as f:
        json.dump(cookies, f)
    print("Salvato in tiktok_cookies.json")
except Exception as e:
    print(f"Errore: {e}")
