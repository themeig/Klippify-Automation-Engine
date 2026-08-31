import time
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(r"C:\Users\HP\Desktop\contenuti klippify")
CACHE_FILE = BASE_DIR / "klippify_campaigns_cache.json"

def parse_api_campaign(item, section_name="Nuove"):
    token_id = item.get("_id") or item.get("id", "")
    name = item.get("campaignName") or item.get("title") or "Campagna"
    
    user_obj = item.get("userId") or {}
    brand = "Klippify Partner"
    if isinstance(user_obj, dict):
        brand = user_obj.get("brandName") or user_obj.get("name") or "Klippify Partner"

    budget_tot = float(item.get("budget") or 0.0)
    budget_rem = float(item.get("remainingBudget") or 0.0)
    budget_spent = float(item.get("spentAmount") or item.get("estimatedSpentAmount") or max(budget_tot - budget_rem, 0.0))

    if budget_tot == 0 and (budget_rem > 0 or budget_spent > 0):
        budget_tot = budget_rem + budget_spent

    prog_pct = f"{(budget_spent/budget_tot*100):.1f}%" if budget_tot > 0 else "0%"

    # Payout rate / 1k
    rev = item.get("platformOnClickRevenue") or {}
    payout_rate = 1.00
    if isinstance(rev, dict) and rev:
        vals = [float(v) for v in rev.values() if isinstance(v, (int, float))]
        if vals:
            payout_rate = vals[0]
    elif isinstance(item.get("onClickRevenue"), (int, float)):
        payout_rate = float(item["onClickRevenue"])

    views = int(item.get("totalClicks") or item.get("clicks") or 0)
    creators = int(item.get("totalJoinedCreators") or 0)
    banner = item.get("banner") or ""
    logo = item.get("logo") or (user_obj.get("avatar") if isinstance(user_obj, dict) else "")

    # Clean description HTML
    raw_desc = item.get("contentDetails") or ""
    soup = BeautifulSoup(raw_desc, "html.parser")
    desc = soup.get_text(separator=" ").strip() if raw_desc else "Descrizione ufficiale Klippify."

    return {
        "id": token_id,
        "campaign_token": token_id,
        "campaign_url": f"https://app.klippify.com/campaigns/{token_id}",
        "name": name,
        "brand": brand,
        "section": section_name,
        "payout_per_1k_views": payout_rate,
        "total_views": views,
        "creators_count": creators,
        "budget_remaining": budget_rem,
        "budget_spent": budget_spent,
        "budget_total": budget_tot,
        "budget_progress_percent": prog_pct,
        "banner": banner,
        "logo": logo,
        "description": desc,
        "status": "Active",
        "mandatory_hashtags": [f"#{re.sub(r'[^a-zA-Z0-9]', '', name.lower())}", "#klippify"],
        "mandatory_mentions": [f"@{re.sub(r'[^a-zA-Z0-9]', '', brand.lower())}"],
        "call_to_action": "Guarda il video completo su Klippify!",
        "target_niche": "Creator / Entertainment",
        "rules": ["Rispetta le linee guida Klippify"],
        "local_folder_match": ""
    }

def process_authorized_api():
    with open(BASE_DIR / "authorized_api_response.json", "r", encoding="utf-8") as f:
        api_data = json.load(f)

    all_campaigns = []
    seen_ids = set()

    mapping = [
        ("filter=new", "Nuove"),
        ("filter=active", "Iscritte"),
        ("filter=paused", "In pausa"),
        ("filter=ended", "Passate"),
        ("featured", "Nuove")
    ]

    for url, resp in api_data.items():
        sec = "Nuove"
        for key, s in mapping:
            if key in url:
                sec = s
                break

        if isinstance(resp, dict) and "data" in resp:
            d = resp["data"]
            items = []
            if isinstance(d, list):
                items = d
            elif isinstance(d, dict) and "campaigns" in d:
                items = d["campaigns"]

            for item in items:
                cid = item.get("_id") or item.get("id")
                if cid and cid not in seen_ids:
                    seen_ids.add(cid)
                    all_campaigns.append(parse_api_campaign(item, section_name=sec))

    print(f"[+] Total PARSED CAMPAIGNS FROM REAL REST API: {len(all_campaigns)}")
    return all_campaigns

if __name__ == "__main__":
    camps = process_authorized_api()
    with open(BASE_DIR / "api_parsed_campaigns.json", "w", encoding="utf-8") as f:
        json.dump(camps, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved {len(camps)} campaigns to api_parsed_campaigns.json")
