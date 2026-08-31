import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\HP\Desktop\contenuti klippify")

with open(BASE_DIR / "authorized_api_response.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for url, resp in data.items():
    print(f"\n==========================================")
    print(f"URL: {url}")
    if isinstance(resp, dict) and "data" in resp:
        d = resp["data"]
        if isinstance(d, dict) and "campaigns" in d:
            camps = d["campaigns"]
            print(f"TOTAL CAMPAIGNS: {len(camps)}")
            if camps:
                print("SAMPLE CAMPAIGN OBJECT KEYS:", list(camps[0].keys()))
                print("SAMPLE CAMPAIGN OBJECT 1:", json.dumps(camps[0], indent=2, ensure_ascii=False))
                if len(camps) > 1:
                    print("SAMPLE CAMPAIGN OBJECT 2:", json.dumps(camps[1], indent=2, ensure_ascii=False))
