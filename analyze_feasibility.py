import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

BASE_DIR = Path(r"C:\Users\HP\Desktop\contenuti klippify")

camps = json.load(open(BASE_DIR / "api_parsed_campaigns.json", encoding="utf-8"))

# Calculate feasibility score
for c in camps:
    payout = float(c.get("payout_per_1k_views") or 1.00)
    budget_rem = float(c.get("budget_remaining") or 0.0)
    budget_tot = float(c.get("budget_total") or (budget_rem + float(c.get("budget_spent") or 0.0)))
    creators = max(int(c.get("creators_count") or 1), 1)
    views = int(c.get("total_views") or 0)
    
    c["payout_per_1k_views"] = payout
    c["budget_remaining"] = budget_rem
    c["budget_total"] = budget_tot

    competition_bonus = 25.0 * (1000.0 / creators)
    language_bonus = 25.0
    difficulty_bonus = 15.0
    budget_bonus = budget_rem * 0.03
    ratio_bonus = 8.0 * (views / creators)
    payout_bonus = payout * 10.0

    score = payout_bonus + competition_bonus + language_bonus + difficulty_bonus + budget_bonus + ratio_bonus
    c["feasibility_score"] = round(score, 1)

camps.sort(key=lambda x: x["feasibility_score"], reverse=True)

print("TOP 15 CAMPAIGNS BY FEASIBILITY SCORE:")
print("=" * 80)
for i, c in enumerate(camps[:15], 1):
    sec = c.get("section", "?")
    name = c.get("name", "?")
    payout = c.get("payout_per_1k_views", 0)
    brem = c.get("budget_remaining", 0)
    cr = c.get("creators_count", 0)
    sc = c.get("feasibility_score", 0)
    desc = c.get("description", "")[:150].encode("ascii", "replace").decode("ascii")
    print(f"{i}. [{sec}] {name}")
    print(f"   Payout: ${payout}/1k | Budget Left: ${brem} | Creators: {cr} | SCORE: {sc}")
    print(f"   Brief: {desc}...")
    print()

# Save ranked data
with open(BASE_DIR / "campaigns_ranked.json", "w", encoding="utf-8") as f:
    json.dump(camps, f, indent=2, ensure_ascii=False)

print(f"Saved {len(camps)} ranked campaigns to campaigns_ranked.json")
