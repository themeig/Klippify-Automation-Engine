import os
import sys
import json
import time
import re
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Paths
BASE_DIR = Path(r"C:\Users\HP\Desktop\contenuti klippify")
LOCAL_CAMPAIGN_DIR = BASE_DIR / "alestark campain"
CACHE_FILE = BASE_DIR / "campaigns_ranked.json"
DASHBOARD_CACHE_FILE = BASE_DIR / "klippify_dashboard_cache.json"
SUBMISSIONS_CACHE_FILE = BASE_DIR / "klippify_submissions.json"
CONFIG_FILE = BASE_DIR / "klippify_config.json"

def ensure_config_exists():
    """Creates a template configuration file for Klippify login if it doesn't exist."""
    if not CONFIG_FILE.exists():
        default_config = {
            "email": "tua_email_klippify@example.com",
            "password": "tua_password_klippify",
            "login_url": "https://app.klippify.com/signin",
            "use_live_browser": True,
            "headless": False,
            "notes": "Imposta headless a false per vedere la finestra di Chromium aprirsi sullo schermo durante l'accesso."
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        print(f"[+] Configuration file created at {CONFIG_FILE}")

def parse_number(text_str, default=0.0):
    """Clean string and convert to float (e.g. '$1,980.00' -> 1980.00)."""
    if not text_str:
        return default
    cleaned = re.sub(r"[^\d.]", "", text_str.replace(",", ""))
    try:
        return float(cleaned)
    except ValueError:
        return default

def scrape_live_klippify_with_playwright(email, password, login_url, headless=False):
    """
    Automates browser login to Klippify using Playwright.
    Collects campaign tokens from /campaigns, then deep-scrapes each token page
    (https://app.klippify.com/campaigns/<token>) for exact title (ignoring 'Passa a Pro' banners).
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[-] Playwright not installed. Falling back to cached data.")
        return None

    print(f"[+] Launching Chromium (Headless={headless}) to log in at {login_url}...")
    campaigns = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=100)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print(f"[+] Navigating to {login_url}...")
            page.goto(login_url, timeout=45000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            # Fill Email & Password
            email_input = page.locator("input[name='email'], input[type='email']").first
            if email_input.is_visible():
                email_input.fill(email)

            pwd_input = page.locator("input[name='password'], input[type='password']").first
            if pwd_input.is_visible():
                pwd_input.fill(password)

            btn = page.locator("button[type='submit'], button:has-text('Sign in'), button:has-text('Log in')").first
            if btn.is_visible():
                btn.click()
                time.sleep(4)

            # Fetch ALL campaigns directly via authorized Klippify REST API endpoints
            print("[+] Querying Klippify REST API endpoints directly via Playwright Bearer Auth...")
            api_endpoints = [
                ("https://app.klippify.com/api/creator/campaign/list?filter=new&limit=100", "Nuove"),
                ("https://app.klippify.com/api/creator/campaign/list?filter=active&limit=100", "Iscritte"),
                ("https://app.klippify.com/api/creator/campaign/list?filter=paused&limit=100", "In pausa"),
                ("https://app.klippify.com/api/creator/campaign/list?filter=ended&limit=100", "Passate"),
                ("https://app.klippify.com/api/creator/campaign/featured?limit=100", "Nuove")
            ]

            seen_ids = set()
            from bs4 import BeautifulSoup

            for ep, sec_name in api_endpoints:
                try:
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

                    if isinstance(res, dict) and "data" in res:
                        d = res["data"]
                        c_items = []
                        if isinstance(d, list):
                            c_items = d
                        elif isinstance(d, dict) and "campaigns" in d:
                            c_items = d["campaigns"]

                        for item in c_items:
                            cid = item.get("_id") or item.get("id")
                            if cid and cid not in seen_ids:
                                seen_ids.add(cid)
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

                                rev = item.get("platformOnClickRevenue") or {}
                                payout_rate = 1.00
                                if isinstance(rev, dict) and rev:
                                    vals = [float(v) for v in rev.values() if isinstance(v, (int, float))]
                                    if vals: payout_rate = vals[0]
                                elif isinstance(item.get("onClickRevenue"), (int, float)):
                                    payout_rate = float(item["onClickRevenue"])

                                views = int(item.get("totalClicks") or item.get("clicks") or 0)
                                creators = int(item.get("totalJoinedCreators") or 0)
                                banner = item.get("banner") or ""
                                logo = item.get("logo") or (user_obj.get("avatar") if isinstance(user_obj, dict) else "")

                                raw_desc = item.get("contentDetails") or ""
                                desc = BeautifulSoup(raw_desc, "html.parser").get_text(separator=" ").strip() if raw_desc else "Descrizione ufficiale Klippify."

                                # Manual overrides for specific campaigns (since /list API doesn't contain deep rules)
                                manual_hashtags = [f"#{re.sub(r'[^a-zA-Z0-9]', '', name.lower())}", "#klippify"]
                                manual_mentions = [f"@{re.sub(r'[^a-zA-Z0-9]', '', brand.lower())}"]
                                manual_rules = ["Rispetta le linee guida Klippify"]
                                
                                if "Million Hospitality" in name or "estero" in desc.lower():
                                    manual_hashtags = ["#millionhospitality", "#lavorareallestero", "#klippify"]
                                    manual_mentions = ["@lavorare_all_estero"]
                                    manual_rules = [
                                        "Durata minima clip: 10 sec.",
                                        "Il volto di Manfredi visibile per almeno 3 secondo (In allegato).",
                                        "Logo sempre visibile per tutta la durata delle clip."
                                    ]

                                campaigns.append({
                                    "id": cid,
                                    "campaign_token": cid,
                                    "campaign_url": f"https://app.klippify.com/campaigns/{cid}",
                                    "name": name,
                                    "brand": brand,
                                    "section": sec_name,
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
                                    "mandatory_hashtags": manual_hashtags,
                                    "mandatory_mentions": manual_mentions,
                                    "call_to_action": "Guarda il video completo su Klippify!",
                                    "target_niche": "Creator / Entertainment",
                                    "rules": manual_rules,
                                    "local_folder_match": ""
                                })
                except Exception as ex:
                    print(f"[-] API Fetch Error for {ep}: {ex}")

            print(f"[+] Total campaigns fetched via Klippify REST API: {len(campaigns)}")

            # Fetch REAL submissions and creator dashboard stats
            try:
                print("[+] Querying real creator submissions and dashboard metrics...")
                sub_dash_res = page.evaluate("""
                    async () => {
                        try {
                            const token = localStorage.getItem('token') || localStorage.getItem('access_token') || localStorage.getItem('jwt') || Object.values(localStorage).find(v => v && v.length > 50);
                            const cleanToken = token ? token.replace(/"/g, '') : '';
                            const headers = {
                                'Authorization': 'Bearer ' + cleanToken,
                                'Content-Type': 'application/json'
                            };

                            const [subRes, dashRes, userRes] = await Promise.all([
                                fetch('https://app.klippify.com/api/creator/content/submissions', { headers }),
                                fetch('https://app.klippify.com/api/creator/dashboard', { headers }),
                                fetch('https://app.klippify.com/api/user/me', { headers })
                            ]);

                            return {
                                submissions: await subRes.json(),
                                dashboard: await dashRes.json(),
                                user: await userRes.json()
                            };
                        } catch(e) {
                            return { error: e.toString() };
                        }
                    }
                """)

                if isinstance(sub_dash_res, dict):
                    # 1. Process and save real submissions
                    raw_subs = sub_dash_res.get("submissions", {}).get("data", {}).get("contents", [])
                    normalized_subs = []
                    for s in raw_subs:
                        camp = s.get("campaign") or {}
                        analytics = s.get("analytics") or {}
                        detail_metrics = s.get("detailMetrics", {}).get("metrics", {}) or {}
                        init_metrics = s.get("initMetrics") or {}
                        
                        views = s.get("totalViews")
                        if views is None or views == 0:
                            views = detail_metrics.get("views") or analytics.get("videoViews") or s.get("estimatedViews") or 0
                            
                        likes = detail_metrics.get("likes") or init_metrics.get("likes") or 0
                        comments = detail_metrics.get("comments") or init_metrics.get("comments") or 0
                        shares = detail_metrics.get("shares") or init_metrics.get("shares") or 0
                        earnings = s.get("totalEarnings") or s.get("earnings") or s.get("estimatedEarnings") or 0.0

                        ai_reason = ""
                        ai_res = s.get("aiVerificationResult") or {}
                        if isinstance(ai_res, dict):
                            vid_res = ai_res.get("video_result") or {}
                            if isinstance(vid_res, dict):
                                ai_reason = vid_res.get("guidelines_reasoning") or vid_res.get("short_summary") or ""

                        normalized_subs.append({
                            "id": s.get("_id"),
                            "campaign_id": s.get("campaignId") or camp.get("_id"),
                            "campaign_name": camp.get("campaignName") or "Campagna Klippify",
                            "campaign_budget": camp.get("budget", 0),
                            "platform": s.get("platform", "tiktok"),
                            "post_url": s.get("contentUrl") or s.get("postUrl") or s.get("originalUrl"),
                            "thumbnail_url": s.get("thumbnailUrl") or (analytics.get("thumbnailUrl") if isinstance(analytics, dict) else ""),
                            "status": s.get("status", "pending"),
                            "is_ai_verified": s.get("isAiVerified", False),
                            "ai_reasoning": ai_reason,
                            "views": int(views),
                            "likes": int(likes),
                            "comments": int(comments),
                            "shares": int(shares),
                            "earnings": float(earnings),
                            "created_at": s.get("createdAt") or s.get("created")
                        })
                    save_submissions_cache(normalized_subs)
                    print(f"[+] Saved {len(normalized_subs)} real video submissions directly from Klippify API.")

                    # 2. Process and save real dashboard data
                    raw_dash = sub_dash_res.get("dashboard", {}).get("data", {})
                    raw_user = sub_dash_res.get("user", {}).get("data", {})
                    tot_bal = raw_dash.get("totalBalance", {})
                    active_camps_count = raw_dash.get("totalActiveCampaigns", len(campaigns))
                    user_name = raw_user.get("name", "riccardo")

                    dash_formatted = {
                        "user_name": user_name,
                        "greeting": f"Bentornato, {user_name}! 👋",
                        "subtitle": "Ecco cosa sta succedendo oggi nel tuo percorso da creator.",
                        "stats": {
                            "Guadagni prelevabili": {
                                "val": f"{tot_bal.get('totalCredit', 0.0):.2f} USD",
                                "sub": "Pronti per il prelievo"
                            },
                            "Guadagni totali": {
                                "val": f"{tot_bal.get('totalEarnings', 0.0):.2f} USD",
                                "sub": "Guadagni complessivi Klippify"
                            },
                            "Campagne attive": {
                                "val": str(active_camps_count),
                                "sub": "Campagne in corso"
                            },
                            "Video Inviati": {
                                "val": str(len(normalized_subs)),
                                "sub": f"{len([x for x in normalized_subs if x['status'] == 'accepted'])} approvati"
                            }
                        },
                        "submissions_summary": {
                            "total_submitted": len(normalized_subs),
                            "total_accepted": len([x for x in normalized_subs if x['status'] == 'accepted']),
                            "total_rejected": len([x for x in normalized_subs if x['status'] == 'rejected']),
                            "total_views": sum(x["views"] for x in normalized_subs),
                            "total_likes": sum(x["likes"] for x in normalized_subs),
                            "total_earnings": sum(x["earnings"] for x in normalized_subs)
                        }
                    }
                    save_dashboard_cache(dash_formatted)
            except Exception as sub_ex:
                print(f"[-] Error fetching submissions / dashboard in Playwright: {sub_ex}")

        except Exception as e:
            print(f"[-] Live Playwright Notice: {e}")
        finally:
            print("[+] Closing Playwright browser session.")
            browser.close()

    return campaigns if campaigns else None

def get_local_folders():
    """Scans the local campaign directory to find downloaded folders."""
    if not LOCAL_CAMPAIGN_DIR.exists():
        return []
    return [d.name for d in LOCAL_CAMPAIGN_DIR.iterdir() if d.is_dir()]

def fetch_klippify_campaigns(use_cache_if_available=True):
    """
    Fetches campaign data from Klippify.
    If use_cache_if_available is True, loads immediately from local cache (<5ms).
    If use_cache_if_available is False, forces a live Playwright token scrape directly from Klippify servers.
    """
    ensure_config_exists()

    # 1. LIVE SCRAPE (When explicitly requested: use_cache_if_available=False)
    if not use_cache_if_available and CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                email = cfg.get("email", "")
                password = cfg.get("password", "")
                login_url = cfg.get("login_url", "https://app.klippify.com/signin")
                headless = cfg.get("headless", True)

                if email and email != "tua_email_klippify@example.com":
                    print(f"[+] Sincronizzazione Live Klippify avviata (Headless={headless})...")
                    live_data = scrape_live_klippify_with_playwright(email, password, login_url, headless=headless)
                    if live_data and len(live_data) > 0:
                        save_cache(live_data)
                        try:
                            with open(BASE_DIR / "api_parsed_campaigns.json", "w", encoding="utf-8") as ap_f:
                                json.dump(live_data, ap_f, indent=2, ensure_ascii=False)
                        except Exception:
                            pass
                        print(f"[+] Sincronizzate con successo {len(live_data)} campagne LIVE da Klippify!")
                        return live_data
        except Exception as e:
            print(f"[-] Errore durante lo scrape live Klippify: {e}")

    # 2. Fast Cache Read (When use_cache_if_available=True or fallback)
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data and len(data) > 0:
                    return data
        except Exception as e:
            print(f"[-] Error reading cache: {e}")

    # Check for complete api_parsed_campaigns.json or active_campaigns_detailed.json
    for master_file in [BASE_DIR / "api_parsed_campaigns.json", BASE_DIR / "active_campaigns_detailed.json"]:
        if master_file.exists():
            try:
                with open(master_file, "r", encoding="utf-8") as mf:
                    mdata = json.load(mf)
                    if mdata and len(mdata) > 0:
                        print(f"[+] Loaded {len(mdata)} full campaigns from {master_file.name}.")
                        save_cache(mdata)
                        return mdata
            except Exception as ex:
                print(f"[-] Error reading {master_file.name}: {ex}")

    # Fallback & Comprehensive Campaign List (Merged Catalog + Participating)
    campaigns = [
        {
            "id": "collecto_camp",
            "campaign_token": "collecto_camp",
            "campaign_url": "https://app.klippify.com/campaigns",
            "name": "Collecto",
            "brand": "di Salvatore Zola",
            "section": "Iscritte",
            "payout_per_1k_views": 1.00,
            "budget_total": 1000.0,
            "budget_spent": 204.0,
            "budget_remaining": 796.0,
            "budget_progress_percent": "20%",
            "total_views": 244485,
            "creators_count": 648,
            "description": "Campagna ufficiale Collecto per la promozione di contenuti digitali.",
            "status": "Active",
            "mandatory_hashtags": ["#collecto", "#klippify", "#viral"],
            "mandatory_mentions": ["@collecto_official"],
            "call_to_action": "Scopri di più su Collecto!",
            "target_niche": "Tech / Digital",
            "rules": ["Rispetta le linee guida Klippify", "Usa l'audio ufficiale"],
            "local_folder_match": ""
        },
        {
            "id": "woodcrafts_camp",
            "campaign_token": "woodcrafts_camp",
            "campaign_url": "https://app.klippify.com/campaigns",
            "name": "WoodCrafts DIY",
            "brand": "di WoodCrafts DIY",
            "section": "Iscritte",
            "payout_per_1k_views": 6.00,
            "budget_total": 500.0,
            "budget_spent": 42.0,
            "budget_remaining": 458.0,
            "budget_progress_percent": "8%",
            "total_views": 12572,
            "creators_count": 1309,
            "description": "Format fai-da-te e lavorazione del legno. Payout ad altissimo rendimento $6.00 / 1k views!",
            "status": "Active",
            "mandatory_hashtags": ["#woodcrafts", "#diy", "#klippify"],
            "mandatory_mentions": ["@woodcrafts_diy"],
            "call_to_action": "Guarda il tutorial completo!",
            "target_niche": "DIY / Fai-da-te",
            "rules": ["Mostra la creazione nei primi 3 secondi", "Audio di alta qualità"],
            "local_folder_match": ""
        },
        {
            "id": "sfs1_camp",
            "campaign_token": "sfs1_camp",
            "campaign_url": "https://app.klippify.com/campaigns",
            "name": "SFS1 - Smoke Free Skin",
            "brand": "di Smoke Free Skin",
            "section": "Iscritte",
            "payout_per_1k_views": 2.00,
            "budget_total": 500.0,
            "budget_spent": 472.0,
            "budget_remaining": 28.0,
            "budget_progress_percent": "94%",
            "total_views": 208419,
            "creators_count": 184,
            "description": "Campagna cura della pelle e benessere Smoke Free Skin.",
            "status": "Active",
            "mandatory_hashtags": ["#smokefreeskin", "#skincare", "#klippify"],
            "mandatory_mentions": ["@smokefreeskin"],
            "call_to_action": "Visita il sito per scoprire i prodotti!",
            "target_niche": "Beauty / Skincare",
            "rules": ["Inserisci la CTA a schermo", "Usa sottotitoli dinamici"],
            "local_folder_match": ""
        },
        {
            "id": "aledellagiusta_eng",
            "campaign_token": "aledellagiusta_eng",
            "campaign_url": "https://app.klippify.com/campaigns",
            "name": "Ale Della Giusta - ENG",
            "brand": "di aledellagiusta",
            "section": "Iscritte",
            "payout_per_1k_views": 1.00,
            "budget_total": 750.0,
            "budget_spent": 39.0,
            "budget_remaining": 711.0,
            "budget_progress_percent": "5%",
            "total_views": 48565,
            "creators_count": 2125,
            "description": "Clipping dei video internazionali in inglese di Ale Della Giusta.",
            "status": "Active",
            "mandatory_hashtags": ["#aledellagiusta", "#klippify", "#clipping"],
            "mandatory_mentions": ["@aledellagiusta"],
            "call_to_action": "Watch the full video!",
            "target_niche": "Vlog / Travel",
            "rules": ["Maintain English subtitles", "High dynamic pacing"],
            "local_folder_match": ""
        },
        {
            "id": "6a64cf756cdfd98478f11f28",
            "campaign_token": "6a64cf756cdfd98478f11f28",
            "campaign_url": "https://app.klippify.com/campaigns/6a64cf756cdfd98478f11f28",
            "name": "Million Hospitality",
            "brand": "Million Hospitality",
            "section": "Nuove",
            "payout_per_1k_views": 1.00,
            "budget_total": 1980.0,
            "budget_spent": 1035.0,
            "budget_remaining": 945.0,
            "budget_progress_percent": "52%",
            "total_views": 1072690,
            "creators_count": 282,
            "description": "Campagna ufficiale Million Hospitality per contenuti di lusso e ospitalità.",
            "status": "Active",
            "mandatory_hashtags": ["#millionhospitality", "#luxury", "#klippify"],
            "mandatory_mentions": ["@millionhospitality"],
            "call_to_action": "Guarda il video completo al link in bio!",
            "target_niche": "Luxury / Lifestyle",
            "rules": ["Mostra la struttura di lusso nei primi secondi"],
            "local_folder_match": ""
        },
        {
            "id": "6a426231e6a21896f769dc80",
            "campaign_token": "6a426231e6a21896f769dc80",
            "campaign_url": "https://app.klippify.com/campaigns/6a426231e6a21896f769dc80",
            "name": "Riccardo Dose - YouTube Clipping",
            "brand": "Marco Cappelli Agency",
            "section": "Nuove",
            "payout_per_1k_views": 0.50,
            "budget_total": 1800.0,
            "budget_spent": 224.0,
            "budget_remaining": 1576.0,
            "budget_progress_percent": "12.4%",
            "total_views": 697802,
            "creators_count": 2770,
            "description": "Riccardo Dose è uno dei creator storici di YouTube Italia...",
            "status": "Active",
            "mandatory_hashtags": ["#riccardodose", "#klippify", "#youtubeclipping"],
            "mandatory_mentions": ["@RiccardoDose"],
            "call_to_action": "Guarda il video completo su Klippify!",
            "target_niche": "Entertainment / YouTube Clipping",
            "rules": [
                "Must mention: @Riccardo Dose",
                "Utilizzare esclusivamente il video fornito in allegato",
                "Il volto di Riccardo Dose deve apparire nella clip",
                "Ogni clip deve avere la scritta 'MADE WITH KLIPPIFY' con logo Klippify"
            ],
            "local_folder_match": ""
        },
        {
            "id": "694e91113d6a349f51473682",
            "campaign_token": "694e91113d6a349f51473682",
            "campaign_url": "https://app.klippify.com/campaigns/694e91113d6a349f51473682",
            "name": "Marco Cappelli Personal Brand",
            "brand": "Marco Cappelli Agency",
            "section": "Nuove",
            "payout_per_1k_views": 1.00,
            "budget_total": 1000.0,
            "budget_spent": 64.0,
            "budget_remaining": 936.0,
            "budget_progress_percent": "6.4%",
            "total_views": 75781,
            "creators_count": 2395,
            "description": "Contenuti di business e personal branding di Marco Cappelli Agency.",
            "status": "Active",
            "mandatory_hashtags": ["#marcocappelli", "#business", "#klippify"],
            "mandatory_mentions": ["@marcocappelli"],
            "call_to_action": "Scopri i segreti del personal branding!",
            "target_niche": "Business / Mindset",
            "rules": ["Evidenzia il concetto chiave della lezione nei primi 3 secondi"],
            "local_folder_match": ""
        },
        {
            "id": "6a759fd05ade3cb2f771b439",
            "campaign_token": "6a759fd05ade3cb2f771b439",
            "campaign_url": "https://app.klippify.com/campaigns/6a759fd05ade3cb2f771b439",
            "name": "Mondocash Podcast",
            "brand": "Ale Stark",
            "section": "Nuove",
            "payout_per_1k_views": 0.50,
            "budget_total": 900.0,
            "budget_spent": 148.5,
            "budget_remaining": 751.5,
            "budget_progress_percent": "16.5%",
            "total_views": 392558,
            "creators_count": 121,
            "description": "Mondocash Podcast condotto da Ale Stark con ospiti del mondo del business.",
            "status": "Active",
            "mandatory_hashtags": ["#mondocash", "#alestark", "#podcast"],
            "mandatory_mentions": ["@alestark_official"],
            "call_to_action": "Ascolta la puntata completa!",
            "target_niche": "Finance / Business Podcast",
            "rules": ["Usa le cartelle video presenti in alestark campain"],
            "local_folder_match": "11_05_26 - CASINÒ ALE STARK"
        },
        {
            "id": "6a7672465ade3cb2f773f6c9",
            "campaign_token": "6a7672465ade3cb2f773f6c9",
            "campaign_url": "https://app.klippify.com/campaigns/6a7672465ade3cb2f773f6c9",
            "name": "Gabriele Vagnato",
            "brand": "Gabriele Vagnato",
            "section": "Nuove",
            "payout_per_1k_views": 0.25,
            "budget_total": 700.0,
            "budget_spent": 22.75,
            "budget_remaining": 677.25,
            "budget_progress_percent": "3.25%",
            "total_views": 80988,
            "creators_count": 133,
            "description": "Contenuti comici ed interviste di Gabriele Vagnato.",
            "status": "Active",
            "mandatory_hashtags": ["#gabrielevagnato", "#comedy", "#klippify"],
            "mandatory_mentions": ["@gabrielevagnato"],
            "call_to_action": "Guarda la gag completa!",
            "target_niche": "Comedy / Entertainment",
            "rules": ["Mantieni la battuta comica intatta"],
            "local_folder_match": ""
        },
        {
            "id": "69d9fd5061ce1b8904c42316",
            "campaign_token": "69d9fd5061ce1b8904c42316",
            "campaign_url": "https://app.klippify.com/campaigns/69d9fd5061ce1b8904c42316",
            "name": "Boardingame #1",
            "brand": "aledellagiusta",
            "section": "Nuove",
            "payout_per_1k_views": 0.50,
            "budget_total": 750.0,
            "budget_spent": 191.5,
            "budget_remaining": 558.5,
            "budget_progress_percent": "25.5%",
            "total_views": 150000,
            "creators_count": 450,
            "description": "Format sfide e giochi da tavolo Boardingame con Ale Della Giusta.",
            "status": "Active",
            "mandatory_hashtags": ["#boardingame", "#aledellagiusta", "#klippify"],
            "mandatory_mentions": ["@aledellagiusta"],
            "call_to_action": "Chi vincerà la sfida? Guarda il video!",
            "target_niche": "Gaming / Entertainment",
            "rules": ["Mostra il momento clou della sfida"],
            "local_folder_match": ""
        }
    ]

    save_cache(campaigns)
    return campaigns

def save_cache(campaigns):
    try:
        ranked = analyze_and_rank_campaigns(campaigns)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(ranked, f, indent=2, ensure_ascii=False)
        print(f"[+] Saved {len(ranked)} ranked campaigns to cache.")
    except Exception as e:
        print(f"[-] Could not save cache: {e}")

def analyze_and_rank_campaigns(campaigns):
    """
    Ranks campaigns based on the feasibility-first score:
    Score = (Payout * 10) + (Competition * 25) + (Language * 25) + (Difficulty * 15) + (Budget * 0.03) + (ViewsRatio * 8)
    """
    if not campaigns:
        return []

    local_folders = get_local_folders()

    for c in campaigns:
        payout = float(c.get("payout_per_1k_views") or 1.00)
        budget_rem = float(c.get("budget_remaining") or 0.0)
        budget_tot = float(c.get("budget_total") or (budget_rem + float(c.get("budget_spent") or 0.0)))
        creators = max(int(c.get("creators_count") or 1), 1)
        views = int(c.get("total_views") or 0)
        
        c["payout_per_1k_views"] = payout
        c["budget_remaining"] = budget_rem
        c["budget_total"] = budget_tot

        # 1. Competizione (Peso: x25)
        competition_bonus = 25.0 * (1000.0 / creators)

        # 2. Lingua (Approssimativa dal testo, assumiamo ITA di default per le campagne Klippify, +25)
        # Se nel nome c'è english o global penalizziamo, ma qui diamo +25 standard
        language_bonus = 25.0

        # 3. Difficoltà (Clip = 15, UGC = 8, Faccia = 0)
        # Diamo +15 di default assumendo che si possano fare clip
        difficulty_bonus = 15.0

        # 4. Longevità budget (Peso: x0.03)
        budget_bonus = budget_rem * 0.03

        # 5. Ratio Views/Creator (Peso: x8)
        ratio_bonus = 8.0 * (views / creators)

        # 6. Guadagno (Peso: x10)
        payout_bonus = payout * 10.0

        score = payout_bonus + competition_bonus + language_bonus + difficulty_bonus + budget_bonus + ratio_bonus

        # Selettività vitale: se la campagna non ha budget, la affossiamo in fondo alla classifica
        if budget_rem <= 0:
            score = -10000.0

        # Match local folder (bonus extra per comodità)
        name_lower = c.get("name", "").lower()
        has_local_media = any(lf.lower() in name_lower or name_lower in lf.lower() for lf in local_folders) if local_folders else False
        
        if has_local_media:
            score += 50.0 # Forte bonus se abbiamo già i file

        c["has_local_media"] = has_local_media
        c["convenience_score"] = round(score, 1)

    campaigns.sort(key=lambda x: x.get("convenience_score", 0), reverse=True)
    return campaigns

def parse_dashboard_html(html_content):
    """Extracts statistics and participating campaign cards from Klippify dashboard HTML."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        stats = {}
        cards = soup.find_all("div", class_=re.compile("dashboard-v2-card"))
        for c in cards:
            p_label = c.find("p", class_=re.compile("text-\\[#111827\\]"))
            p_val = c.find("p", class_=re.compile("text-\\[#0d172a\\]"))
            p_sub = c.find("p", class_=re.compile("text-\\[#7b8496\\]"))
            if p_label and p_val:
                label = p_label.text.strip()
                val = p_val.text.strip().replace("\xa0", " ")
                sub = p_sub.text.strip() if p_sub else ""
                stats[label] = {"val": val, "sub": sub}

        articles = soup.find_all("article", class_=re.compile("rounded-xl border"))
        participating = []
        for a in articles:
            title_el = a.find(["h3", "h2"])
            title = title_el.text.strip() if title_el else "Campagna"
            brand_el = a.find("span", class_=re.compile("truncate"))
            brand = brand_el.text.strip() if brand_el else "Brand"
            banner_img = a.find("img", class_=re.compile("object-cover"))
            banner_url = banner_img["src"] if banner_img and banner_img.has_attr("src") else ""
            if banner_url == "/default-banner.webp":
                banner_url = "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Ale_Della_Giusta__16x9_2K.webp"

            logo_img = a.find("img", alt=re.compile("Logo di"))
            logo_url = logo_img["src"] if logo_img and logo_img.has_attr("src") else ""
            payout_badges = a.find_all("span", class_=re.compile("rounded-full bg-\\[#f1f2f5\\]"))
            payouts = [p.text.strip().replace("\xa0", " ") for p in payout_badges]
            txt = a.text.replace("\xa0", " ")
            views_m = re.search(r"Visualizzazioni\s*([\d.]+)", txt)
            views = views_m.group(1) if views_m else "0"
            creators_m = re.search(r"Creator\s*(\d+)", txt)
            creators = creators_m.group(1) if creators_m else "0"
            budget_rem_m = re.search(r"Budget\s*([\d.,]+\s*USD)", txt)
            budget_rem = budget_rem_m.group(1) if budget_rem_m else "0,00 USD"
            prog_m = re.search(r"([\d.,]+\s*USD)\s*su\s*([\d.,]+\s*USD)", txt)
            spent = prog_m.group(1) if prog_m else "0,00 USD"
            total = prog_m.group(2) if prog_m else "0,00 USD"
            pct_m = re.search(r"(\d+)%", txt)
            pct = pct_m.group(1) + "%" if pct_m else "0%"

            participating.append({
                "name": title,
                "brand": brand,
                "payouts": payouts if payouts else ["1,00 USD/1k"],
                "views": views,
                "creators": creators,
                "budget_remaining": budget_rem,
                "budget_spent": spent,
                "budget_total": total,
                "progress_percent": pct,
                "banner": banner_url,
                "logo": logo_url
            })

        data = {
            "user_name": "riccardo",
            "greeting": "Bentornato, riccardo! 👋",
            "subtitle": "Ecco cosa sta succedendo oggi nel tuo percorso da creator.",
            "stats": stats if stats else {
                "Guadagni prelevabili": {"val": "0,00 USD", "sub": "Pronti per il prelievo"},
                "Guadagni totali": {"val": "0,00 USD", "sub": "Guadagni complessivi"},
                "Campagne attive": {"val": "4", "sub": "Campagne in corso"},
                "La tua valutazione": {"val": "0.0", "sub": "Nessuna valutazione"}
            },
            "participating_campaigns": participating,
            "earnings_summary": {
                "month": "0,00 USD",
                "week": "0,00 USD",
                "today": "0,00 USD"
            },
            "recent_withdrawals": []
        }
        return data
    except Exception as e:
        print(f"[-] Error parsing dashboard HTML: {e}")
        return None

def fetch_klippify_dashboard_data(use_cache_if_available=True):
    """Fetches dashboard metrics and enrolled campaign data from Klippify."""
    if DASHBOARD_CACHE_FILE.exists():
        age_sec = time.time() - DASHBOARD_CACHE_FILE.stat().st_mtime
        if use_cache_if_available or age_sec < 120:
            try:
                with open(DASHBOARD_CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data:
                        return data
            except Exception as e:
                print(f"[-] Error reading dashboard cache: {e}")

    # Fallback to live scraping
    fetch_klippify_campaigns(use_cache_if_available=False)
    if DASHBOARD_CACHE_FILE.exists():
        with open(DASHBOARD_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # Fallback
    default_data = {
        "user_name": "riccardo",
        "greeting": "Bentornato, riccardo! 👋",
        "subtitle": "Ecco cosa sta succedendo oggi nel tuo percorso da creator.",
        "stats": {
            "Guadagni prelevabili": {"val": "0,00 USD", "sub": "Pronti per il prelievo"},
            "Guadagni totali": {"val": "0,00 USD", "sub": "Guadagni complessivi"},
            "Campagne attive": {"val": "4", "sub": "Campagne in corso"},
            "La tua valutazione": {"val": "0.0", "sub": "Nessuna valutazione"}
        },
        "participating_campaigns": [
            {
                "name": "Collecto",
                "brand": "di Salvatore Zola",
                "payouts": ["1,00 USD/1k", "1,00 USD/1k"],
                "views": "244.485",
                "creators": "648",
                "budget_remaining": "796,00 USD",
                "budget_spent": "204,00 USD",
                "budget_total": "1000,00 USD",
                "progress_percent": "20%",
                "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Collecto__16x9_2K.webp",
                "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/03b82d2e-f63f-4f8e-9df5-c2649179a469-Collecto_def_2.png"
            },
            {
                "name": "Ale Della Giusta - ENG",
                "brand": "di aledellagiusta",
                "payouts": ["1,00 USD/1k", "1,00 USD/1k"],
                "views": "48.565",
                "creators": "2125",
                "budget_remaining": "595,00 USD",
                "budget_spent": "39,00 USD",
                "budget_total": "750,00 USD",
                "progress_percent": "5%",
                "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Ale_Della_Giusta__16x9_2K.webp",
                "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/90dcb7cc-d6e8-4b52-9ec1-92c87a16e29b-BLACK-LOGO.png"
            },
            {
                "name": "WoodCrafts DIY",
                "brand": "di WoodCrafts DIY",
                "payouts": ["6,00 USD/1k", "6,00 USD/1k"],
                "views": "12.572",
                "creators": "1309",
                "budget_remaining": "314,00 USD",
                "budget_spent": "42,00 USD",
                "budget_total": "500,00 USD",
                "progress_percent": "8%",
                "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/WoodCrafts_DIY__16x9_2K.webp",
                "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/9b975f55-d384-4f47-9974-61cedee70f9c-logo.png"
            },
            {
                "name": "SFS1",
                "brand": "di Smoke Free Skin",
                "payouts": ["2,00 USD/1k", "2,00 USD/1k"],
                "views": "208.419",
                "creators": "184",
                "budget_remaining": "28,00 USD",
                "budget_spent": "472,00 USD",
                "budget_total": "500,00 USD",
                "progress_percent": "94%",
                "banner": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/SFS1__16x9_2K.webp",
                "logo": "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/ac4c586d-7560-4a3d-a16e-fe824b4f0606-SFS-Logo2-2.png"
            }
        ],
        "earnings_summary": {
            "month": "0,00 USD",
            "week": "0,00 USD",
            "today": "0,00 USD"
        },
        "recent_withdrawals": []
    }
    save_dashboard_cache(default_data)
    return default_data

def save_dashboard_cache(data):
    try:
        with open(DASHBOARD_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[+] Saved dashboard cache to {DASHBOARD_CACHE_FILE}")
    except Exception as e:
        print(f"[-] Could not save dashboard cache: {e}")

def save_submissions_cache(data):
    try:
        with open(SUBMISSIONS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[+] Saved submissions cache to {SUBMISSIONS_CACHE_FILE}")
    except Exception as e:
        print(f"[-] Could not save submissions cache: {e}")

def fetch_klippify_submissions(use_cache_if_available=True):
    """Fetches real video submissions with live views, likes, and payout data from Klippify."""
    if SUBMISSIONS_CACHE_FILE.exists():
        # If cache exists and is fresh (< 2 minutes old), return it immediately even on live request
        age_sec = time.time() - SUBMISSIONS_CACHE_FILE.stat().st_mtime
        if use_cache_if_available or age_sec < 120:
            try:
                with open(SUBMISSIONS_CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data is not None:
                        return data
            except Exception as e:
                print(f"[-] Error reading submissions cache: {e}")

    # Fallback to live scraping
    fetch_klippify_campaigns(use_cache_if_available=False)
    if SUBMISSIONS_CACHE_FILE.exists():
        with open(SUBMISSIONS_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def submit_video_to_klippify(campaign_id, content_url, platform="tiktok"):
    """
    Submits a published video URL directly to Klippify's official API endpoint:
    POST https://app.klippify.com/api/creator/content/<campaign_id>
    """
    try:
        ensure_config_exists()
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        email = cfg["email"]
        password = cfg["password"]
        login_url = cfg.get("login_url", "https://app.klippify.com/signin")
        headless = cfg.get("headless", True)

        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()
            page.goto(login_url)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            email_el = page.locator("input[name='email'], input[type='email']").first
            if email_el.is_visible():
                email_el.fill(email)
                pwd_el = page.locator("input[name='password'], input[type='password']").first
                if pwd_el.is_visible():
                    pwd_el.fill(password)
                btn = page.locator("button[type='submit'], button:has-text('Sign in'), button:has-text('Log in')").first
                if btn.is_visible():
                    btn.click()
                    time.sleep(4)

            print(f"[+] Submitting video '{content_url}' to Klippify campaign '{campaign_id}'...")
            submit_res = page.evaluate(f"""
                async () => {{
                    try {{
                        const token = localStorage.getItem('token') || localStorage.getItem('access_token') || localStorage.getItem('jwt') || Object.values(localStorage).find(v => v && v.length > 50);
                        const cleanToken = token ? token.replace(/"/g, '') : '';
                        const headers = {{
                            'Authorization': 'Bearer ' + cleanToken,
                            'Content-Type': 'application/json'
                        }};

                        // 1. Fetch user to get exact socialProfileId
                        const userRes = await fetch('https://app.klippify.com/api/user/me', {{ headers }});
                        const userData = await userRes.json();
                        let socialProfileId = null;
                        
                        if (userData && userData.data) {{
                            const profiles = userData.data.socialProfiles || [];
                            for (const sp of profiles) {{
                                if (sp.platforms && sp.platforms.some(p => p.platform === '{platform}' && p.status === 'link')) {{
                                    socialProfileId = sp._id;
                                    break;
                                }}
                            }}
                            if (!socialProfileId && profiles.length > 0) {{
                                socialProfileId = profiles[0]._id;
                            }}
                        }}

                        if (!socialProfileId) {{
                            try {{
                                const spRes = await fetch('https://app.klippify.com/api/creator/social-profiles', {{ headers }});
                                const spData = await spRes.json();
                                if (spData && spData.data && spData.data.length > 0) {{
                                    socialProfileId = spData.data[0]._id;
                                }}
                            }} catch(e) {{}}
                        }}

                        if (!socialProfileId) {{
                            socialProfileId = '6a865ef8763fa81a0f4e3302';
                        }}

                        // 2. Submit content to campaign endpoint
                        const postRes = await fetch('https://app.klippify.com/api/creator/content/{campaign_id}', {{
                            method: 'POST',
                            headers,
                            body: JSON.stringify({{
                                platform: '{platform}',
                                contentUrl: '{content_url}',
                                socialProfileId: socialProfileId
                            }})
                        }});

                        return await postRes.json();
                    }} catch(e) {{
                        return {{ error: e.toString() }};
                    }}
                }}
            """)

            browser.close()
            print(f"[+] Klippify Submit Response: {submit_res}")

            # Refresh local submissions cache so frontend updates immediately
            try:
                fetch_klippify_campaigns(use_cache_if_available=False)
            except Exception as ref_ex:
                print(f"[-] Could not auto-refresh submissions after upload: {ref_ex}")

            return submit_res

    except Exception as e:
        print(f"[-] Error submitting video to Klippify: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    camps = fetch_klippify_campaigns(use_cache_if_available=False)
    ranked = analyze_and_rank_campaigns(camps)
    print(f"[+] Ranked {len(ranked)} campaigns successfully.")

