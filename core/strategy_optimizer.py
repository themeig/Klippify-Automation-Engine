import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# UTF-8 encoding support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "core"))

DATA_DIR = ROOT / "data"
PERF_FILE = DATA_DIR / "strategy_performance.json"
STATE_FILE = DATA_DIR / "autopilot_state.json"
TIKTOK_PROFILE = ROOT / "tiktok_profile"

def load_performance_data():
    if PERF_FILE.exists():
        try:
            with open(PERF_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "last_updated": None,
        "active_combinations": [
            "combo_1_shock_loop",
            "combo_2_controversy_comment_bait",
            "combo_3_breaking_news_loop",
            "combo_4_loss_aversion_story"
        ],
        "winning_combination": None,
        "highest_views_recorded": 264,
        "milestone_1000_achieved": False,
        "switch_campaign_recommended": False,
        "stats_by_strategy": {},
        "video_logs": []
    }

def save_performance_data(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PERF_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def monitor_tiktok_performance(headless=False):
    """
    Estrae le statistiche aggiornate dei video pubblicati da TikTok Studio,
    associa a ciascun video la strategia applicata e calcola la classifica di efficacia.
    """
    from playwright.sync_api import sync_playwright

    print("\n=======================================================", flush=True)
    print("📊 [OPTIMIZER] AVVIO MONITORAGGIO STRATEGIE TIKTOK STUDIO", flush=True)
    print(f"   Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("=======================================================\n", flush=True)

    perf_data = load_performance_data()
    scraped_videos = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                str(TIKTOK_PROFILE),
                headless=headless,
                no_viewport=True,
                executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                args=["--disable-blink-features=AutomationControlled", "--start-maximized", "--no-first-run"]
            )
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            print("[+] Navigazione su TikTok Studio Content...", flush=True)
            page.goto("https://www.tiktok.com/tiktokstudio/content", timeout=45000)
            time.sleep(5)

            # Estrai dati tabella contenuti
            raw_text = page.evaluate("() => document.body.innerText")
            lines = [l.strip() for l in raw_text.split("\n") if l.strip()]

            # Parsing video recenti
            # Struttura tipica: "00:38", Titolo, Data (es. "2 ott 20:01"), Privacy ("Tutti"), Views (es. "122"), Likes (es. "1"), Comments (es. "0")
            i = 0
            while i < len(lines):
                if lines[i].startswith("00:") and i + 5 < len(lines):
                    duration = lines[i]
                    title = lines[i+1]
                    date_str = lines[i+2]
                    privacy = lines[i+3]
                    
                    try:
                        views = int(lines[i+4].replace("K", "000").replace(".", "").replace(",", ""))
                        likes = int(lines[i+5]) if lines[i+5].isdigit() else 0
                        comments = int(lines[i+6]) if i + 6 < len(lines) and lines[i+6].isdigit() else 0
                        
                        scraped_videos.append({
                            "title": title,
                            "date": date_str,
                            "duration": duration,
                            "views": views,
                            "likes": likes,
                            "comments": comments
                        })
                        i += 6
                    except Exception:
                        i += 1
                else:
                    i += 1

            browser.close()
    except Exception as e:
        print(f"[!] Errore durante l'ispezione browser: {e}", flush=True)

    print(f"[+] Estratti {len(scraped_videos)} post recenti da TikTok Studio.", flush=True)

    # Associazione strategie ai titoli
    # Se il titolo contiene certe parole chiave, viene classificato nella rispettiva combo
    for vid in scraped_videos:
        t_upper = vid["title"].upper()
        if "ATTENZIONE" in t_upper or "BRUCIANDO" in t_upper or "NON COMPRARE" in t_upper:
            vid["strategy"] = "combo_1_shock_loop"
        elif "VERITÀ" in t_upper or "SEGRETO" in t_upper or "SBAGLIA" in t_upper or "DANNI" in t_upper:
            vid["strategy"] = "combo_2_controversy_comment_bait"
        elif "ULTIM'ORA" in t_upper or "NOTIZIA" in t_upper or "REGOLA" in t_upper:
            vid["strategy"] = "combo_3_breaking_news_loop"
        elif "PERSO" in t_upper or "ERRORE" in t_upper or "RISCHIO" in t_upper:
            vid["strategy"] = "combo_4_loss_aversion_story"
        else:
            vid["strategy"] = "baseline_standard"

    # Aggiorna statistiche per strategia
    strategy_stats = {}
    highest_views = perf_data.get("highest_views_recorded", 0)

    for vid in scraped_videos:
        strat = vid["strategy"]
        if strat not in strategy_stats:
            strategy_stats[strat] = {"count": 0, "total_views": 0, "total_likes": 0, "total_comments": 0}
        strategy_stats[strat]["count"] += 1
        strategy_stats[strat]["total_views"] += vid["views"]
        strategy_stats[strat]["total_likes"] += vid["likes"]
        strategy_stats[strat]["total_comments"] += vid["comments"]

        if vid["views"] > highest_views:
            highest_views = vid["views"]

    # Calcola metriche medie e virality score
    leaderboard = []
    for strat, st in strategy_stats.items():
        avg_views = round(st["total_views"] / max(1, st["count"]), 1)
        avg_likes = round(st["total_likes"] / max(1, st["count"]), 1)
        avg_comments = round(st["total_comments"] / max(1, st["count"]), 1)
        virality_score = round(avg_views * 0.5 + avg_likes * 2.0 + avg_comments * 10.0, 1)

        leaderboard.append({
            "strategy": strat,
            "sample_size": st["count"],
            "avg_views": avg_views,
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
            "virality_score": virality_score
        })

    leaderboard.sort(key=lambda x: x["virality_score"], reverse=True)
    best_strategy = leaderboard[0]["strategy"] if leaderboard else "combo_1_shock_loop"

    perf_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    perf_data["highest_views_recorded"] = highest_views
    perf_data["winning_combination"] = best_strategy
    perf_data["stats_by_strategy"] = strategy_stats
    perf_data["leaderboard"] = leaderboard
    perf_data["milestone_1000_achieved"] = (highest_views >= 1000)

    # Se dopo 3 cicli completi di test nessuna combinazione supera i 500-1000 views, raccomanda rotazione campagna
    if len(scraped_videos) >= 15 and highest_views < 500:
        perf_data["switch_campaign_recommended"] = True
    else:
        perf_data["switch_campaign_recommended"] = False

    save_performance_data(perf_data)

    print("\n🏆 CLASSIFICA STRATEGIE A/B:")
    for rank, entry in enumerate(leaderboard, 1):
        print(f"   {rank}. {entry['strategy']}: Avg Views = {entry['avg_views']} | Score = {entry['virality_score']} (Campioni: {entry['sample_size']})")

    print(f"\n🎯 STRATEGIA VINCENTE DA SPINGERE: {best_strategy}")
    print(f"📈 Picco visualizzazioni registrato: {highest_views} views")
    if perf_data["milestone_1000_achieved"]:
        print("🎉 TRAGUARDO 1.000+ VISUALIZZAZIONI RAGGIUNTO! Strategia confermata a regime.")
    else:
        print("⏳ Milestone 1.000 visualizzazioni in corso: test A/B attivo.")

    return perf_data

if __name__ == "__main__":
    monitor_tiktok_performance()
