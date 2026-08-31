import json
import re
from pathlib import Path

def classify_active_campaigns():
    root = Path(r"c:\Users\HP\Desktop\contenuti klippify")
    
    # 1. Carica le campagne classificate/salvate
    campaigns_file = root / "campaigns_ranked.json"
    dashboard_file = root / "klippify_dashboard_cache.json"
    cache_file = root / "klippify_campaigns_cache.json"
    
    all_campaigns = []
    detailed_file = root / "active_campaigns_detailed.json"
    if detailed_file.exists():
        try:
            with open(detailed_file, "r", encoding="utf-8") as f:
                detailed_camps = json.load(f)
                if detailed_camps:
                    out_path = root / "active_campaigns_classified.json"
                    with open(out_path, "w", encoding="utf-8") as out_f:
                        json.dump(detailed_camps, out_f, indent=2, ensure_ascii=False)
                    print(f"[+] Classificazione sincronizzata da active_campaigns_detailed ({len(detailed_camps)} campagne attive): {out_path}")
                    return detailed_camps
        except Exception as e:
            print(f"[!] Errore lettura active_campaigns_detailed: {e}")
            
    # Filtra solo le campagne a cui l'utente è iscritto (o sezione Iscritte/Active)
    active_campaigns = []
    for c in all_campaigns:
        c_name = c.get("name", "").strip().lower()
        c_sec = c.get("section", "").strip().lower()
        
        # Considera attiva se presente nella dashboard participating o marcata come Iscritte
        if c_name in participating_names or "iscritte" in c_sec or "active" in c_sec:
            active_campaigns.append(c)
            
    # Se per qualche motivo il filtro è vuoto, prendi quelle della dashboard
    if not active_campaigns and participating_names:
        for c in all_campaigns:
            if any(pn in c.get("name", "").lower() for pn in participating_names):
                active_campaigns.append(c)

    print(f"[+] Trovate {len(active_campaigns)} campagne ATTIVE/ISCRITTE.")
    
    classified_results = []
    
    clipping_keywords = [
        "drive.google.com", "dropbox.com", "we.tl", "wetransfer", "youtube.com", "youtu.be",
        "podcast", "spezzon", "tagliare", "clip", "materiale fornito", "video forniti",
        "cartella drive", "risorse allegate", "in allegato", "audio originale"
    ]
    
    url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
    
    for c in active_campaigns:
        cid = c.get("id") or c.get("campaign_token")
        name = c.get("name", "Senza Nome")
        desc = c.get("description", "")
        rules = " ".join(c.get("rules", []))
        full_text = f"{name} {desc} {rules}".lower()
        
        # Trova tutti i link presenti nella descrizione o regole
        found_urls = url_pattern.findall(f"{desc} {rules}")
        drive_links = [u for u in found_urls if "drive.google.com" in u or "dropbox" in u or "wetransfer" in u]
        video_links = [u for u in found_urls if "youtube" in u or "youtu.be" in u or u.endswith((".mp4", ".mov", ".mkv"))]
        
        is_clipping = False
        reasons = []
        
        if drive_links:
            is_clipping = True
            reasons.append(f"Link a risorse esterne trovato: {drive_links[0]}")
        if video_links:
            is_clipping = True
            reasons.append(f"Link video sorgente trovato: {video_links[0]}")
            
        matched_kws = [kw for kw in clipping_keywords if kw in full_text]
        if matched_kws:
            is_clipping = True
            reasons.append(f"Parole chiave clipping rilevate: {', '.join(matched_kws)}")
            
        category = "CLIPPING" if is_clipping else "AI_GENERATION"
        
        classified_item = {
            "campaign_id": cid,
            "campaign_name": name,
            "category": category,
            "reasons": reasons,
            "drive_links": drive_links,
            "video_links": video_links,
            "all_extracted_links": found_urls,
            "logo_url": c.get("logo") or "",
            "banner_url": c.get("banner") or "",
            "mandatory_hashtags": c.get("mandatory_hashtags") or [],
            "mandatory_mentions": c.get("mandatory_mentions") or [],
            "rules": c.get("rules") or [],
            "payout_per_1k": c.get("payout_per_1k_views") or 0.0,
            "budget_remaining": c.get("budget_remaining") or 0.0
        }
        classified_results.append(classified_item)
        
    out_path = root / "active_campaigns_classified.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(classified_results, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Classificazione completata e salvata in: {out_path}")
    return classified_results

if __name__ == "__main__":
    results = classify_active_campaigns()
    for r in results:
        cat_badge = "[CLIPPING]" if r.get("category") == "CLIPPING" else "[AI_GENERATION]"
        cname = r.get("name") or r.get("campaign_name")
        cid = r.get("id") or r.get("campaign_id")
        print(f"- {cat_badge} {cname} (ID: {cid})")
