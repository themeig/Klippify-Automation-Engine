import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\HP\Desktop\contenuti klippify")
CACHE_FILE = BASE_DIR / "klippify_campaigns_cache.json"

if CACHE_FILE.exists():
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(f"=== TOTALE CAMPAGNE STRATTE DA KLIPPIFY: {len(data)} ===\n")
        for i, c in enumerate(data, 1):
            name = c.get("name", "N/A")
            payout = c.get("payout_per_1k_views", 0)
            budget = c.get("budget_remaining", 0)
            score = c.get("convenience_score", 0)
            hashtags = " ".join(c.get("mandatory_hashtags", []))
            mentions = " ".join(c.get("mandatory_mentions", []))
            cta = c.get("call_to_action", "")
            media = "[SI] PRESENTE IN CARTELLA" if c.get("has_local_media") else "[NO] SOLO SU KLIPPIFY"

            print(f"[{i:02d}] {name}")
            print(f"     > Payout Rate: ${payout:.2f} per 1.000 visualizzazioni")
            print(f"     > Score Convenienza: {score} / 100")
            print(f"     > Stato Media Locale: {media}")
            print(f"     > Hashtag: {hashtags}")
            print(f"     > Tag Account: {mentions}")
            print(f"     > CTA (Call To Action): {cta}")
            print("-" * 65)
