import os
import json
import webbrowser
from datetime import datetime
from pathlib import Path
from klippify_scraper import fetch_klippify_campaigns, analyze_and_rank_campaigns, fetch_klippify_dashboard_data, fetch_klippify_submissions

BASE_DIR = Path(r"C:\Users\HP\Desktop\contenuti klippify")
HTML_REPORT_PATH = BASE_DIR / "klippify_report.html"
MD_REPORT_PATH = BASE_DIR / "klippify_report.md"

def generate_html_report(campaigns, dashboard_data=None, submissions_data=None):
    if dashboard_data is None:
        dashboard_data = fetch_klippify_dashboard_data(use_cache_if_available=True)
    if submissions_data is None:
        submissions_data = fetch_klippify_submissions(use_cache_if_available=True)

    top_camp = campaigns[0] if campaigns else None
    now_str = datetime.now().strftime("%d/%m/%Y alle %H:%M")
    campaigns_json = json.dumps(campaigns, ensure_ascii=False)
    dashboard_json = json.dumps(dashboard_data, ensure_ascii=False)
    submissions_json = json.dumps(submissions_data, ensure_ascii=False)

    # Load generated content if available
    gen_content_path = BASE_DIR / "generated_content.json"
    generated_content = []
    if gen_content_path.exists():
        with open(gen_content_path, "r", encoding="utf-8") as gcf:
            generated_content = json.load(gcf)
    generated_json = json.dumps(generated_content, ensure_ascii=False)
    gen_count = len(generated_content)

    # Load published content
    pub_content_path = BASE_DIR / "published_content.json"
    published_content = []
    if pub_content_path.exists():
        with open(pub_content_path, "r", encoding="utf-8") as pcf:
            published_content = json.load(pcf)
    published_json = json.dumps(published_content, ensure_ascii=False)

    # Load selected campaigns
    sel_camps_path = BASE_DIR / "campagne_selezionate.json"
    selected_campaigns = []
    if sel_camps_path.exists():
        with open(sel_camps_path, "r", encoding="utf-8") as scf:
            selected_campaigns = json.load(scf)
    selected_json = json.dumps(selected_campaigns, ensure_ascii=False)

    # Load campaign schedules
    sched_path = BASE_DIR / "campaign_schedules.json"
    campaign_schedules = {}
    if sched_path.exists():
        try:
            with open(sched_path, "r", encoding="utf-8") as scf:
                campaign_schedules = json.load(scf)
        except Exception:
            pass
    schedules_json = json.dumps(campaign_schedules, ensure_ascii=False)

    # Count campaigns by section
    counts = {
        "all": len(campaigns),
        "Nuove": sum(1 for c in campaigns if c.get("section") == "Nuove"),
        "Iscritte": sum(1 for c in campaigns if c.get("section") == "Iscritte"),
        "In pausa": sum(1 for c in campaigns if c.get("section") == "In pausa"),
        "Passate": sum(1 for c in campaigns if c.get("section") == "Passate"),
        "Lista d'attesa": sum(1 for c in campaigns if c.get("section") == "Lista d'attesa"),
        "Rifiutate": sum(1 for c in campaigns if c.get("section") == "Rifiutate")
    }
    cnt_all = counts.get("all", 0)

    # Extract dashboard parameters
    user_greeting = dashboard_data.get("greeting", "Bentornato, riccardo! 👋")
    user_subtitle = dashboard_data.get("subtitle", "Ecco cosa sta succedendo oggi nel tuo percorso da creator.")
    stats = dashboard_data.get("stats", {})
    participating = dashboard_data.get("participating_campaigns", [])

    # Stat Card Values
    val_prelevabili = stats.get("Guadagni prelevabili", {}).get("val", "0,00 USD")
    sub_prelevabili = stats.get("Guadagni prelevabili", {}).get("sub", "Pronti per il prelievo")
    val_totali = stats.get("Guadagni totali", {}).get("val", "0,00 USD")
    sub_totali = stats.get("Guadagni totali", {}).get("sub", "Guadagni complessivi")
    val_attive = stats.get("Campagne attive", {}).get("val", str(len(participating)))
    sub_attive = stats.get("Campagne attive", {}).get("sub", "Campagne in corso")
    val_valutazione = stats.get("La tua valutazione", {}).get("val", "0.0")
    sub_valutazione = stats.get("La tua valutazione", {}).get("sub", "Nessuna valutazione")

    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Klippify Intelligence & Creator Control Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-gradient: linear-gradient(135deg, #090d16 0%, #111827 50%, #0f172a 100%);
            --card-bg: rgba(30, 41, 59, 0.65);
            --card-border: rgba(255, 255, 255, 0.08);
            --accent-purple: #8b5cf6;
            --accent-cyan: #38bdf8;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Outfit', sans-serif; }}

        body {{
            background: var(--bg-gradient);
            color: var(--text-main);
            height: 100vh;
            overflow: hidden;
            margin: 0;
        }}

        .app-container {{
            display: flex;
            height: 100vh;
        }}

        .sidebar {{
            width: 70px;
            height: 100vh;
            background: rgba(15, 23, 42, 0.98);
            border-right: 1px solid var(--card-border);
            padding: 2rem 0.8rem;
            display: flex;
            flex-direction: column;
            z-index: 50;
            overflow-x: hidden;
            overflow-y: auto;
            flex-shrink: 0;
            box-shadow: 4px 0 24px rgba(0,0,0,0.3);
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), padding 0.3s ease;
        }}

        .sidebar:hover {{
            width: 250px;
            padding: 2rem 1.2rem;
        }}

        .sidebar .sidebar-text {{
            opacity: 0;
            visibility: hidden;
            width: 0;
            display: inline-block;
            white-space: nowrap;
            overflow: hidden;
            transition: opacity 0.2s ease, width 0.2s ease;
        }}

        .sidebar:hover .sidebar-text {{
            opacity: 1;
            visibility: visible;
            width: auto;
            display: inline;
        }}

        .sidebar .sidebar-footer {{
            opacity: 0;
            visibility: hidden;
            height: 0;
            overflow: hidden;
            transition: opacity 0.2s ease, height 0.2s ease;
        }}

        .sidebar:hover .sidebar-footer {{
            opacity: 1;
            visibility: visible;
            height: auto;
        }}

        .sidebar-logo {{
            font-size: 1.4rem;
            font-weight: 800;
            background: linear-gradient(90deg, #c084fc, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 2rem;
            white-space: nowrap;
        }}

        .sidebar-nav {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .main-content {{
            flex: 1;
            height: 100vh;
            overflow-y: auto;
            padding: 2rem 3rem;
            scroll-behavior: smooth;
        }}

        header {{
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--card-border);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 1.4rem;
            font-weight: 800;
            background: linear-gradient(90deg, #c084fc, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}

        .container {{
            max-width: 1280px;
            margin: 1.5rem auto;
            padding: 0 1.5rem;
        }}

        /* SIDEBAR NAV */
        .sidebar-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 0.85rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            text-align: left;
            width: 100%;
            white-space: nowrap;
        }}

        .sidebar-btn:hover {{
            color: #fff;
            background: rgba(255, 255, 255, 0.05);
        }}

        .sidebar-btn.active {{
            background: rgba(139, 92, 246, 0.15);
            color: #fff;
            border-left: 4px solid var(--accent-purple);
            border-radius: 0 0.5rem 0.5rem 0;
        }}

        /* KLIPPIFY DASHBOARD V2 STYLES */
        .creator-dashboard-v2 {{
            display: flex;
            flex-direction: column;
            gap: 1.8rem;
        }}

        .dashboard-welcome-header h1 {{
            font-size: 1.8rem;
            font-weight: 800;
            color: #fff;
        }}

        .dashboard-welcome-header p {{
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 0.3rem;
        }}

        .k-stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.2rem;
        }}

        .k-stat-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 1.25rem;
            padding: 1.3rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1.2rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .k-stat-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(167, 139, 250, 0.4);
        }}

        .k-stat-icon-wrapper {{
            width: 54px;
            height: 54px;
            border-radius: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .k-stat-icon-wrapper svg {{
            width: 26px;
            height: 26px;
        }}

        .k-stat-info {{
            min-width: 0;
            flex: 1;
        }}

        .k-stat-title {{
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 0.3rem;
        }}

        .k-stat-val {{
            font-size: 1.6rem;
            font-weight: 800;
            color: #fff;
            line-height: 1.1;
        }}

        .k-stat-sub {{
            font-size: 0.75rem;
            color: #7b8496;
            margin-top: 0.38rem;
        }}

        /* DASHBOARD LAYOUT GRID (LEFT: CAMPAIGNS, RIGHT: SIDEBAR) */
        .k-dashboard-main-grid {{
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 1.8rem;
        }}

        @media (max-width: 1024px) {{
            .k-dashboard-main-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .k-panel-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 1.25rem;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
        }}

        .k-panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1.2rem;
        }}

        .k-panel-title {{
            font-size: 1.2rem;
            font-weight: 700;
            color: #fff;
        }}

        .k-panel-subtitle {{
            font-size: 0.82rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }}

        .k-tabs-sub {{
            display: flex;
            gap: 1.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 1.2rem;
            padding-bottom: 0.6rem;
        }}

        .k-subtab {{
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            position: relative;
            padding-bottom: 0.4rem;
            transition: color 0.2s;
        }}

        .k-subtab.active {{
            color: var(--accent-cyan);
        }}

        .k-subtab.active::after {{
            content: '';
            position: absolute;
            bottom: -0.6rem;
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--accent-cyan);
            border-radius: 2px;
        }}

        /* PARTICIPATING CAMPAIGNS GRID */
        .k-campaigns-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.4rem;
        }}

        .k-part-card {{
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--card-border);
            border-radius: 1rem;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.25s ease, border-color 0.25s ease;
            position: relative;
        }}

        .k-part-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 12px 30px rgba(56, 189, 248, 0.15);
        }}

        .k-banner-box {{
            width: 100%;
            height: 160px;
            position: relative;
            overflow: hidden;
            background: #0f172a;
        }}

        .k-banner-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
        }}

        .k-part-body {{
            padding: 1.2rem;
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
            flex-grow: 1;
        }}

        .k-part-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .k-brand-row {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.82rem;
            color: var(--text-muted);
        }}

        .k-brand-avatar {{
            width: 20px;
            height: 20px;
            border-radius: 0.35rem;
            object-fit: cover;
            border: 1px solid rgba(255,255,255,0.1);
        }}

        .k-payout-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .k-payout-pill {{
            background: rgba(255, 255, 255, 0.08);
            color: #f1f5f9;
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            font-size: 0.72rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .k-metrics-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            background: rgba(0, 0, 0, 0.3);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding: 0.65rem 0;
            text-align: center;
        }}

        .k-metric-col {{
            display: flex;
            flex-direction: column;
            align-items: center;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .k-metric-col:last-child {{ border-right: none; }}

        .k-metric-lbl {{
            font-size: 0.68rem;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .k-metric-val {{
            font-size: 0.85rem;
            font-weight: 700;
            color: #fff;
            margin-top: 0.2rem;
        }}

        .k-budget-row {{
            display: flex;
            justify-content: space-between;
            font-size: 0.78rem;
            margin-top: 0.2rem;
        }}

        /* SIDEBAR WIDGETS */
        .k-sidebar-widgets {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}

        .k-widget-box {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 1.25rem;
            padding: 1.3rem;
            backdrop-filter: blur(10px);
        }}

        .k-widget-title {{
            font-size: 1rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.8rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .k-empty-state {{
            background: rgba(15, 23, 42, 0.5);
            border: 1px dashed var(--card-border);
            border-radius: 0.85rem;
            padding: 1.5rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        .k-action-tip-card {{
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(139, 92, 246, 0.1));
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 0.85rem;
            padding: 1rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 0.8rem;
        }}

        .k-action-tip-card:last-child {{ margin-bottom: 0; }}

        .k-action-icon {{
            font-size: 1.4rem;
        }}

        .k-action-title {{
            font-size: 0.88rem;
            font-weight: 700;
            color: #fff;
        }}

        .k-action-sub {{
            font-size: 0.75rem;
            color: var(--text-muted);
        }}

        /* EXISTING INTELLIGENCE VISTA STYLES */
        .winner-card {{
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(56, 189, 248, 0.1));
            border: 2px solid rgba(167, 139, 250, 0.4);
            border-radius: 1.25rem;
            padding: 2rem;
            margin-bottom: 2.5rem;
            backdrop-filter: blur(10px);
            position: relative;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            cursor: pointer;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .winner-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(167, 139, 250, 0.8);
        }}

        .badge-hero {{
            background: linear-gradient(90deg, var(--accent-amber), #ef4444);
            color: #fff;
            padding: 0.3rem 1rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 0.8rem;
        }}

        .stats-row {{
            display: flex;
            gap: 1rem;
            margin: 1.5rem 0;
            flex-wrap: wrap;
        }}

        .mini-stat {{
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--card-border);
            padding: 0.8rem 1.2rem;
            border-radius: 0.75rem;
            flex: 1;
            min-width: 140px;
        }}

        .stat-label {{ font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; }}
        .stat-val {{ font-size: 1.3rem; font-weight: 700; color: #fff; margin-top: 0.2rem; }}

        .copy-box {{
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid var(--card-border);
            border-radius: 0.85rem;
            padding: 1.2rem;
            margin-top: 1rem;
        }}

        .copy-item {{ margin-bottom: 0.8rem; }}
        .copy-item:last-child {{ margin-bottom: 0; }}

        .copy-header {{ font-size: 0.8rem; font-weight: 600; color: var(--accent-cyan); margin-bottom: 0.3rem; }}
        .copy-flex {{ display: flex; gap: 0.5rem; }}

        .copy-val {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 0.5rem 0.8rem;
            border-radius: 0.5rem;
            font-family: monospace;
            font-size: 0.85rem;
            flex-grow: 1;
            color: #e2e8f0;
            white-space: nowrap;
            overflow-x: auto;
        }}

        .btn-cp {{
            background: rgba(139, 92, 246, 0.3);
            border: 1px solid rgba(139, 92, 246, 0.5);
            color: #d8b4fe;
            padding: 0.5rem 0.8rem;
            border-radius: 0.5rem;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }}

        .btn-cp:hover {{ background: var(--accent-purple); color: #fff; }}

        .nav-btn {{
            background: linear-gradient(135deg, var(--accent-purple), #6d28d9);
            border: none;
            color: #fff;
            padding: 0.6rem 1.2rem;
            border-radius: 0.6rem;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(139, 92, 246, 0.35);
        }}

        .section-title {{
            font-size: 1.4rem;
            font-weight: 700;
            margin: 2rem 0 1.2rem 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 1rem;
            padding: 1.5rem;
            backdrop-filter: blur(8px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        }}

        .card:hover {{
            transform: translateY(-5px);
            border-color: rgba(167, 139, 250, 0.5);
            box-shadow: 0 12px 30px rgba(139, 92, 246, 0.25);
        }}

        .progress-bar-bg {{
            background: rgba(255, 255, 255, 0.1);
            height: 6px;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 0.4rem;
        }}

        .progress-bar-fill {{
            background: linear-gradient(90deg, #38bdf8, #8b5cf6);
            height: 100%;
        }}

        /* MODAL STYLING */
        .modal-overlay {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(9, 13, 22, 0.85);
            backdrop-filter: blur(12px);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
            padding: 1.5rem;
        }}

        .modal-overlay.active {{
            opacity: 1;
            pointer-events: auto;
        }}

        .modal-container {{
            background: #111827;
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 1.25rem;
            max-width: 780px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            padding: 2rem;
            position: relative;
            box-shadow: 0 25px 50px rgba(0,0,0,0.6);
            transform: translateY(20px);
            transition: transform 0.3s ease;
        }}

        .modal-overlay.active .modal-container {{
            transform: translateY(0);
        }}

        .modal-close {{
            position: absolute;
            top: 1.2rem;
            right: 1.5rem;
            background: rgba(255,255,255,0.1);
            border: none;
            color: #fff;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }}

        .modal-close:hover {{ background: rgba(239, 68, 68, 0.8); }}

        .click-hint {{
            font-size: 0.75rem;
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 700;
            margin-top: 0.5rem;
        }}

        .tab-filters {{
            display: flex;
            gap: 0.6rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }}

        .tab-filter-btn {{
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 0.5rem 1rem;
            border-radius: 0.6rem;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .tab-filter-btn:hover, .tab-filter-btn.active {{
            background: rgba(139, 92, 246, 0.25);
            border-color: rgba(139, 92, 246, 0.5);
            color: #fff;
        }}

        /* TIKTOK VIDEO CARDS */
        .tiktok-video-card {{
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid var(--card-border);
            border-radius: 1rem;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            position: relative;
        }}
        .tiktok-video-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(56, 189, 248, 0.5);
            box-shadow: 0 12px 28px rgba(56, 189, 248, 0.2);
        }}
        .tiktok-cover-wrap {{
            position: relative;
            width: 100%;
            padding-top: 125%;
            background: #0f172a;
            overflow: hidden;
        }}
        .tiktok-cover-img {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        .tiktok-video-card:hover .tiktok-cover-img {{
            transform: scale(1.03);
        }}
        .tiktok-duration-badge {{
            position: absolute;
            bottom: 8px;
            right: 8px;
            background: rgba(0,0,0,0.8);
            color: #fff;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 4px;
            backdrop-filter: blur(4px);
        }}
        .tiktok-card-body {{
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.7rem;
            flex-grow: 1;
            justify-content: space-between;
        }}
        .tiktok-card-title {{
            font-size: 0.88rem;
            font-weight: 600;
            color: #f8fafc;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            min-height: 2.5em;
        }}
        .tiktok-metrics-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.5rem;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 0.6rem;
            padding: 0.6rem;
        }}
        .tiktok-metric-pill {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.76rem;
            color: #cbd5e1;
        }}
        .tiktok-metric-pill strong {{
            color: #fff;
            font-weight: 700;
        }}
        .tiktok-link-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(139, 92, 246, 0.15));
            border: 1px solid rgba(56, 189, 248, 0.3);
            color: #38bdf8;
            padding: 0.5rem;
            border-radius: 0.5rem;
            font-size: 0.8rem;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.2s ease;
        }}
        /* =================================================== */
        /* NUOVO LAYOUT DASHBOARD CAMPAGNA: CASCATA ROVESCIATA */
        /* =================================================== */

        .camp-layout-grid {{
            display: grid;
            grid-template-columns: 260px 1fr;
            gap: 1.5rem;
            align-items: start;
            perspective: 1200px;
        }}

        @media (max-width: 1024px) {{
            .camp-layout-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .camp-subnav-panel {{
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-top: 1.5px solid rgba(255, 255, 255, 0.25);
            border-bottom: 4px solid #090d16;
            border-radius: 1.25rem;
            padding: 1.2rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
            box-shadow: 0 15px 35px -5px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.2), inset 0 -2px 0 rgba(0,0,0,0.6);
            position: sticky;
            top: 1.5rem;
            z-index: 10;
            transform: translateZ(5px);
        }}

        .camp-subnav-btn {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-top: 1px solid rgba(255, 255, 255, 0.12);
            border-bottom: 2px solid rgba(0, 0, 0, 0.5);
            color: #94a3b8;
            padding: 0.85rem 1rem;
            border-radius: 0.75rem;
            font-weight: 700;
            font-size: 0.88rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-align: left;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            width: 100%;
            box-shadow: 0 3px 8px rgba(0,0,0,0.3);
        }}

        .camp-subnav-btn:hover {{
            background: rgba(255, 255, 255, 0.08);
            color: #f8fafc;
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(0,0,0,0.4);
        }}

        .camp-subnav-btn.active {{
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.35), rgba(56, 189, 248, 0.25));
            border: 1px solid rgba(139, 92, 246, 0.6);
            border-top: 1.5px solid rgba(192, 132, 252, 0.8);
            border-bottom: 3px solid #4c1d95;
            color: #fff;
            box-shadow: 0 6px 18px rgba(139, 92, 246, 0.35), inset 0 1px 0 rgba(255,255,255,0.3);
            transform: translateY(-1px);
        }}

        /* TOP 4 WIDGETS */
        .camp-top-widgets-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}

        @media (max-width: 1300px) {{
            .camp-top-widgets-grid {{
                grid-template-columns: 1fr 1fr;
            }}
        }}

        @media (max-width: 768px) {{
            .camp-top-widgets-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .camp-widget-card {{
            background: linear-gradient(175deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-top: 1.5px solid rgba(255, 255, 255, 0.25);
            border-bottom: 3.5px solid #090d16;
            border-radius: 1.1rem;
            padding: 1.1rem 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 0.6rem;
            box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255,255,255,0.15), inset 0 -2px 0 rgba(0,0,0,0.5);
            backdrop-filter: blur(10px);
            transition: all 0.25s ease;
        }}

        .camp-widget-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 18px 36px -6px rgba(0, 0, 0, 0.75), inset 0 1px 0 rgba(255,255,255,0.25);
        }}

        /* ANIMATED CASCADE WATERFALL */
        .cascade-waterfall-stream {{
            display: flex;
            flex-direction: column;
            gap: 1.3rem;
            position: relative;
        }}

        /* ========================================================= */
        /* 3D RELIEF HERO TOP CARD (1° IN CODA / PROSSIMO AD USCIRE) */
        /* ========================================================= */
        .cascade-hero-card {{
            background: linear-gradient(175deg, #1e293b 0%, #0f172a 60%, #090d16 100%);
            border: 1.5px solid rgba(16, 185, 129, 0.5);
            border-top: 2.5px solid rgba(52, 211, 153, 0.95); /* Luce superiore in rilievo */
            border-left: 2px solid rgba(16, 185, 129, 0.7);
            border-right: 2px solid rgba(5, 150, 105, 0.4);
            border-bottom: 5px solid #047857; /* Spessore 3D inferiore */
            border-radius: 1.4rem;
            padding: 1.6rem;
            box-shadow: 0 20px 45px -10px rgba(0,0,0,0.8), 0 8px 16px -4px rgba(0,0,0,0.6), inset 0 2px 1px 0 rgba(255, 255, 255, 0.35), inset 0 -3px 0 0 rgba(0, 0, 0, 0.7), 0 0 30px rgba(16, 185, 129, 0.3);
            animation: heroGlowPulse 3s infinite ease-in-out, cascadeSlideIn 0.5s ease-out;
            position: relative;
            transform: translateZ(15px);
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        .cascade-hero-card:hover {{
            transform: translateY(-5px) scale(1.008) translateZ(20px);
            border-bottom-color: #059669;
            box-shadow: 0 28px 55px -8px rgba(0, 0, 0, 0.9), inset 0 2px 2px 0 rgba(255, 255, 255, 0.45), inset 0 -3px 0 0 rgba(0, 0, 0, 0.7), 0 0 45px rgba(16, 185, 129, 0.5);
        }}

        @keyframes heroGlowPulse {{
            0% {{ box-shadow: 0 20px 45px -10px rgba(0,0,0,0.8), inset 0 2px 1px 0 rgba(255, 255, 255, 0.35), 0 0 25px rgba(16, 185, 129, 0.25); }}
            50% {{ box-shadow: 0 24px 50px -8px rgba(0,0,0,0.85), inset 0 2px 2px 0 rgba(255, 255, 255, 0.45), 0 0 40px rgba(16, 185, 129, 0.5), 0 0 20px rgba(56, 189, 248, 0.35); }}
            100% {{ box-shadow: 0 20px 45px -10px rgba(0,0,0,0.8), inset 0 2px 1px 0 rgba(255, 255, 255, 0.35), 0 0 25px rgba(16, 185, 129, 0.25); }}
        }}

        @keyframes cascadeSlideIn {{
            from {{
                opacity: 0;
                transform: translateY(30px) scale(0.98);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) scale(1);
            }}
        }}

        /* ========================================================= */
        /* 3D RELIEF MEDIUM CASCADE SLOT CARDS (SLOT DI OGGI)        */
        /* ========================================================= */
        .cascade-slot-card {{
            background: linear-gradient(175deg, #1e293b 0%, #0f172a 70%, #0b1120 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 1.8px solid rgba(192, 132, 252, 0.75); /* Luce superiore in rilievo */
            border-left: 6px solid #8b5cf6; /* Nervatura viola in rilievo */
            border-right: 1px solid rgba(255, 255, 255, 0.06);
            border-bottom: 4px solid #4c1d95; /* Spessore 3D inferiore */
            border-radius: 1.15rem;
            padding: 1.3rem 1.5rem;
            box-shadow: 0 14px 32px -8px rgba(0, 0, 0, 0.7), 0 4px 10px rgba(0,0,0,0.5), inset 0 1.5px 0 0 rgba(255, 255, 255, 0.22), inset 0 -2px 0 0 rgba(0, 0, 0, 0.6);
            transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
            animation: cascadeSlideIn 0.5s ease-out both;
            transform: translateZ(8px);
        }}

        .cascade-slot-card:hover {{
            transform: translateY(-4px) scale(1.008) translateZ(12px);
            border-bottom-color: #6d28d9;
            box-shadow: 0 20px 42px -6px rgba(0, 0, 0, 0.8), 0 0 25px rgba(139, 92, 246, 0.35), inset 0 2px 0 rgba(255, 255, 255, 0.35);
        }}

        /* ========================================================= */
        /* 3D RELIEF COMPACT RESERVE ROW (MAGAZZINO CLIP A SCALARE)  */
        /* ========================================================= */
        .cascade-reserve-row {{
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 1.2px solid rgba(56, 189, 248, 0.6);
            border-left: 5px solid #38bdf8;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 3px solid #0369a1;
            border-radius: 0.9rem;
            padding: 0.95rem 1.25rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.8rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            animation: cascadeSlideIn 0.4s ease-out both;
            box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15), inset 0 -2px 0 rgba(0, 0, 0, 0.5);
        }}

        .cascade-reserve-row:hover {{
            background: linear-gradient(180deg, #334155 0%, #1e293b 100%);
            border-bottom-color: #0284c7;
            transform: translateY(-3px) translateX(3px);
            box-shadow: 0 14px 28px -4px rgba(56, 189, 248, 0.35), inset 0 1.5px 0 rgba(255, 255, 255, 0.25);
        }}

        /* ========================================================= */
        /* MENU A TENDINA ACCORDION PER VIDEO GIÀ PUBBLICATI         */
        /* ========================================================= */
        .published-accordion-dropdown {{
            margin-top: 1.2rem;
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(9, 13, 22, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-top: 1.5px solid rgba(255, 255, 255, 0.2);
            border-bottom: 3px solid #000;
            border-radius: 1rem;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
            transition: all 0.25s ease;
        }}

        .published-accordion-dropdown summary {{
            padding: 1rem 1.3rem;
            font-weight: 800;
            font-size: 0.88rem;
            color: #cbd5e1;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
            list-style: none;
            transition: background 0.2s;
        }}

        .published-accordion-dropdown summary::-webkit-details-marker {{
            display: none;
        }}

        .published-accordion-dropdown summary:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
        }}

        .published-accordion-dropdown[open] summary {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(0, 0, 0, 0.3);
        }}

        .published-accordion-content {{
            padding: 1.2rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
            background: rgba(0, 0, 0, 0.35);
        }}
        /* ========================================================= */
        /* RETTANGOLO ATTIVO "STO PROCESSANDO" (3D PULSING ACTIVE)   */
        /* ========================================================= */
        .processing-active-card {{
            background: linear-gradient(175deg, #2a1b06 0%, #171103 60%, #0d0800 100%);
            border: 2px solid rgba(245, 158, 11, 0.7);
            border-top: 3px solid rgba(253, 224, 71, 0.95);
            border-left: 3px solid rgba(245, 158, 11, 0.85);
            border-right: 2px solid rgba(217, 119, 6, 0.6);
            border-bottom: 5px solid #78350f;
            border-radius: 1.4rem;
            padding: 1.5rem 1.6rem;
            box-shadow: 0 20px 45px -10px rgba(0,0,0,0.85), 0 0 35px rgba(245, 158, 11, 0.35), inset 0 2px 1px 0 rgba(255, 255, 255, 0.4), inset 0 -3px 0 0 rgba(0, 0, 0, 0.8);
            animation: processingGlowPulse 2s infinite ease-in-out, cascadeSlideIn 0.4s ease-out;
            margin-bottom: 1.2rem;
            position: relative;
            transform: translateZ(20px);
        }}

        @keyframes processingGlowPulse {{
            0% {{ box-shadow: 0 20px 45px -10px rgba(0,0,0,0.85), 0 0 25px rgba(245, 158, 11, 0.3), inset 0 2px 1px 0 rgba(255, 255, 255, 0.4); border-color: rgba(245, 158, 11, 0.7); }}
            50% {{ box-shadow: 0 25px 55px -8px rgba(0,0,0,0.9), 0 0 45px rgba(245, 158, 11, 0.6), inset 0 2px 2px 0 rgba(255, 255, 255, 0.6); border-color: rgba(253, 224, 71, 1); }}
            100% {{ box-shadow: 0 20px 45px -10px rgba(0,0,0,0.85), 0 0 25px rgba(245, 158, 11, 0.3), inset 0 2px 1px 0 rgba(255, 255, 255, 0.4); border-color: rgba(245, 158, 11, 0.7); }}
        }}

        .processing-pulse-badge {{
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #000;
            font-weight: 900;
            font-size: 0.82rem;
            padding: 0.35rem 0.85rem;
            border-radius: 0.5rem;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.6);
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            letter-spacing: 0.5px;
        }}

        .pulse-dot {{
            display: inline-block;
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: #000;
            animation: pulse 1s infinite;
        }}

        .processing-animated-bar {{
            width: 100%;
            height: 8px;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}

        .processing-bar-fill {{
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, #f59e0b, #fbbf24, #f59e0b, #fbbf24);
            background-size: 200% 100%;
            animation: moveStripes 1.5s linear infinite;
        }}

        @keyframes moveStripes {{
            0% {{ background-position: 0% 0%; }}
            100% {{ background-position: 200% 0%; }}
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <div class="sidebar" id="sidebar">
            <div class="sidebar-logo">
                <span style="width:20px; text-align:center;">⚡</span>
                <span class="sidebar-text" style="margin-left: 0.6rem;">Klippify OS</span>
            </div>
            
            <nav class="sidebar-nav">
                <button id="main-tab-dashboard" class="sidebar-btn active" onclick="switchMainView('dashboard')">
                    <span style="width:20px; text-align:center;">📊</span> <span class="sidebar-text">Creator Dashboard</span>
                </button>
                <button id="main-tab-my-campaigns" class="sidebar-btn" onclick="switchMainView('my-campaigns')">
                    <span style="width:20px; text-align:center;">🔥</span> <span class="sidebar-text">Campagne Attive</span>
                </button>
                <button id="main-tab-intelligence" class="sidebar-btn" onclick="switchMainView('intelligence')">
                    <span style="width:20px; text-align:center;">🎯</span> <span class="sidebar-text">Intelligence ({cnt_all})</span>
                </button>
                <button id="main-tab-studio" class="sidebar-btn" onclick="switchMainView('studio')">
                    <span style="width:20px; text-align:center;">🎬</span> <span class="sidebar-text">Content Studio ({gen_count})</span>
                </button>
                <button id="main-tab-tiktok" class="sidebar-btn" onclick="switchMainView('tiktok')">
                    <span style="width:20px; text-align:center;">📱</span> <span class="sidebar-text">TikTok Manager</span>
                </button>
                <button id="main-tab-debug" class="sidebar-btn" onclick="switchMainView('debug')">
                    <span style="width:20px; text-align:center;">🛠️</span> <span class="sidebar-text">Debug & Processi</span>
                    <span id="debug-active-badge" style="display:none; background:#10b981; color:#000; font-size:0.68rem; font-weight:800; padding:0.1rem 0.45rem; border-radius:1rem; margin-left:auto;">0</span>
                </button>
            </nav>
            
            <div class="sidebar-footer" style="margin-top: auto; font-size: 0.75rem; color: var(--text-muted); display:flex; flex-direction:column; gap:0.8rem;">
                <div>Ultimo Sync: {now_str}</div>
                <button class="nav-btn" style="width:100%; border-radius: 0.5rem; background:linear-gradient(135deg, #0284c7, #0369a1); font-weight:800; color:#fff; cursor:pointer;" onclick="triggerRefresh(this)">🔄 Sincronizza Dati Klippify</button>
            </div>
        </div>
        
        <div class="main-content">
            <div class="container" style="margin: 0; max-width: 1400px; padding: 0;">

        <!-- ========================================== -->
        <!-- VIEW 1: KLIPPIFY CREATOR DASHBOARD VIEW    -->
        <!-- ========================================== -->
        <div id="view-dashboard-section" class="creator-dashboard-v2">
            <div class="dashboard-welcome-header">
                <h1>{user_greeting}</h1>
                <p>{user_subtitle}</p>
            </div>

            <!-- 4 STAT CARDS -->
            <div class="k-stats-grid">
                <div class="k-stat-card">
                    <div class="k-stat-icon-wrapper" style="background: rgba(255, 90, 31, 0.15); color: #ff5a1f;">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"></rect><path d="M3 9a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2"></path><path d="M3 11h3c.8 0 1.6.3 2.1.9l1.1.9c1.6 1.6 4.1 1.6 5.7 0l1.1-.9c.5-.5 1.3-.9 2.1-.9H21"></path></svg>
                    </div>
                    <div class="k-stat-info">
                        <div class="k-stat-title">Guadagni prelevabili</div>
                        <div class="k-stat-val">{val_prelevabili}</div>
                        <div class="k-stat-sub">{sub_prelevabili}</div>
                    </div>
                </div>

                <div class="k-stat-card">
                    <div class="k-stat-icon-wrapper" style="background: rgba(142, 66, 238, 0.15); color: #8e42ee;">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 16v5"></path><path d="M16 14v7"></path><path d="M20 10v11"></path><path d="m22 3-8.646 8.646a.5.5 0 0 1-.708 0L9.354 8.354a.5.5 0 0 0-.707 0L2 15"></path><path d="M4 18v3"></path><path d="M8 14v7"></path></svg>
                    </div>
                    <div class="k-stat-info">
                        <div class="k-stat-title">Guadagni totali</div>
                        <div class="k-stat-val">{val_totali}</div>
                        <div class="k-stat-sub">{sub_totali}</div>
                    </div>
                </div>

                <div class="k-stat-card">
                    <div class="k-stat-icon-wrapper" style="background: rgba(8, 125, 244, 0.15); color: #087df4;">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path></svg>
                    </div>
                    <div class="k-stat-info">
                        <div class="k-stat-title">Campagne attive</div>
                        <div class="k-stat-val">{val_attive}</div>
                        <div class="k-stat-sub">{sub_attive}</div>
                    </div>
                </div>

                <div class="k-stat-card">
                    <div class="k-stat-icon-wrapper" style="background: rgba(245, 173, 0, 0.15); color: #f5ad00;">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path></svg>
                    </div>
                    <div class="k-stat-info">
                        <div class="k-stat-title">La tua valutazione</div>
                        <div class="k-stat-val">{val_valutazione}</div>
                        <div class="k-stat-sub">{sub_valutazione}</div>
                    </div>
                </div>
            </div>

            <!-- DASHBOARD MAIN GRID -->
            <div class="k-dashboard-main-grid">
                <!-- LEFT COLUMN: PARTICIPATING CAMPAIGNS -->
                <div class="k-panel-card">
                    <div class="k-panel-header">
                        <div>
                            <div class="k-panel-title">Campagne</div>
                            <div class="k-panel-subtitle">Monitora le campagne partecipate, concluse e in lista d'attesa.</div>
                        </div>
                    </div>

                    <div class="k-tabs-sub">
                        <button class="k-subtab active">Partecipate ({len(participating)})</button>
                        <button class="k-subtab">Concluse (0)</button>
                        <button class="k-subtab">Lista d'attesa (0)</button>
                    </div>

                    <div class="k-campaigns-grid">
    """

    for pc in participating:
        p_name = pc.get("name", "Campagna")
        p_brand = pc.get("brand", "Klippify Partner")
        p_banner = pc.get("banner") or "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Collecto__16x9_2K.webp"
        p_logo = pc.get("logo") or ""
        p_views = pc.get("views", "0")
        p_creators = pc.get("creators", "0")
        p_spent = pc.get("budget_spent", "0,00 USD")
        p_total = pc.get("budget_total", "0,00 USD")
        p_pct = pc.get("progress_percent", "0%")
        p_payouts = pc.get("payouts", ["1,00 USD/1k"])

        pills_html = "".join([f'<span class="k-payout-pill"><span>🎵</span> {pay}</span>' for pay in p_payouts])
        logo_html = f'<img src="{p_logo}" class="k-brand-avatar" alt="Brand Logo">' if p_logo else ''

        html_content += f"""
                        <div class="k-part-card">
                            <div class="k-banner-box">
                                <img src="{p_banner}" class="k-banner-img" alt="{p_name}" onerror="this.src='https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Collecto__16x9_2K.webp'">
                            </div>
                            <div class="k-part-body">
                                <div class="k-part-title">{p_name}</div>
                                <div class="k-brand-row">
                                    {logo_html}
                                    <span>{p_brand}</span>
                                </div>

                                <div class="k-payout-pills">
                                    {pills_html}
                                </div>

                                <div class="k-metrics-grid">
                                    <div class="k-metric-col">
                                        <span class="k-metric-lbl">👁️ Views</span>
                                        <span class="k-metric-val">{p_views}</span>
                                    </div>
                                    <div class="k-metric-col">
                                        <span class="k-metric-lbl">👥 Creator</span>
                                        <span class="k-metric-val">{p_creators}</span>
                                    </div>
                                    <div class="k-metric-col">
                                        <span class="k-metric-lbl">💰 Budget</span>
                                        <span class="k-metric-val">{p_total}</span>
                                    </div>
                                </div>

                                <div>
                                    <div class="k-budget-row">
                                        <span><strong>{p_spent}</strong> <span style="color:var(--text-muted)">su {p_total}</span></span>
                                        <span style="color:var(--accent-cyan); font-weight:700">{p_pct}</span>
                                    </div>
                                    <div class="progress-bar-bg" style="margin-top:0.4rem;">
                                        <div class="progress-bar-fill" style="width: {p_pct}"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
        """

    html_content += f"""
                    </div>
                </div>

                <!-- RIGHT COLUMN: SIDEBAR WIDGETS -->
                <div class="k-sidebar-widgets">
                    <!-- RIEPILOGO GUADAGNI -->
                    <div class="k-widget-box">
                        <div class="k-widget-title">
                            <span>Riepilogo guadagni</span>
                            <span style="font-size:0.75rem; color:var(--accent-cyan); font-weight:normal;">Questo mese</span>
                        </div>
                        <div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin: 0.5rem 0;">0,00 USD</div>
                        <div class="k-empty-state">Nessun dato sui guadagni registrato per il periodo selezionato.</div>
                    </div>

                    <!-- PRELIEVI RECENTI -->
                    <div class="k-widget-box">
                        <div class="k-widget-title">
                            <span>Prelievi recenti</span>
                            <span style="font-size:0.75rem; color:var(--text-muted); cursor:pointer">Vedi tutti</span>
                        </div>
                        <div class="k-empty-state">
                            <div style="font-size:1.2rem; margin-bottom:0.3rem">💳</div>
                            <strong>Nessun prelievo</strong><br>
                            I tuoi prelievi appariranno qui dopo una richiesta di pagamento.
                        </div>
                    </div>

                    <!-- TIPS & ACTIONS -->
                    <div class="k-widget-box">
                        <div class="k-widget-title">Suggerimenti Creator</div>
                        <div class="k-action-tip-card">
                            <div class="k-action-icon">🚀</div>
                            <div>
                                <div class="k-action-title">Continua a creare</div>
                                <div class="k-action-sub">La costanza aumenta i guadagni complessivi</div>
                            </div>
                        </div>
                        <div class="k-action-tip-card">
                            <div class="k-action-icon">🎯</div>
                            <div>
                                <div class="k-action-title">Partecipa a nuove campagne</div>
                                <div class="k-action-sub">Più campagne attive = più entrate</div>
                            </div>
                        </div>
                        <div class="k-action-tip-card">
                            <div class="k-action-icon">📈</div>
                            <div>
                                <div class="k-action-title">Condividi e cresci</div>
                                <div class="k-action-sub">Fai crescere il tuo pubblico sui social</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- VIEW 2: INTELLIGENCE CONTROL CENTER VIEW  -->
        <!-- ========================================== -->
        <div id="view-intelligence-section" style="margin-top: 3rem;">
    """

    if top_camp:
        payout = top_camp.get("payout_per_1k_views", 1.0)
        pool_rem = top_camp.get("budget_remaining", 0.0)
        budget_tot = top_camp.get("budget_total", 0.0)
        budget_spent = top_camp.get("budget_spent", max(budget_tot - pool_rem, 0.0))
        prog_pct = top_camp.get("budget_progress_percent", f"{(budget_spent/budget_tot*100):.0f}%" if budget_tot > 0 else "0%")
        score = top_camp.get("convenience_score", 50)
        token = top_camp.get("campaign_token", top_camp.get("id", ""))

        html_content += f"""
            <!-- WINNER HERO CARD -->
            <div class="winner-card" onclick="openModal(0)">
                <span class="badge-hero">🏆 1° Scelta Consiglio del Giorno</span>
                <h1 style="font-size:2rem; font-weight:800; color:#fff;">{top_camp['name']}</h1>
                <p style="color: var(--text-muted); font-size:0.95rem; margin-top:0.3rem;">
                    Brand: <strong>{top_camp.get('brand', 'Klippify Partner')}</strong> | Token ID: <code style="color:#a78bfa;">{token}</code>
                </p>

                <div class="stats-row">
                    <div class="mini-stat">
                        <div class="stat-label">Punteggio Convenienza</div>
                        <div class="stat-val" style="color:#c084fc">{score} <span style="font-size:0.8rem; font-weight:normal;">/ 100</span></div>
                    </div>
                    <div class="mini-stat">
                        <div class="stat-label">Tariffa Payout / 1k Views</div>
                        <div class="stat-val" style="color:#34d399">${payout:.2f} /1k</div>
                    </div>
                    <div class="mini-stat">
                        <div class="stat-label">Pool Rimanente</div>
                        <div class="stat-val" style="color:#38bdf8">${pool_rem:,.2f}</div>
                    </div>
                    <div class="mini-stat">
                        <div class="stat-label">Budget Totale Campagna</div>
                        <div class="stat-val" style="color:#f59e0b">${budget_tot:,.2f}</div>
                    </div>
                </div>

                <div style="background:rgba(15,23,42,0.6); padding:0.8rem 1.2rem; border-radius:0.75rem; border:1px solid var(--card-border); margin-bottom:1rem;">
                    <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:var(--text-muted);">
                        <span>Avanzamento Speso: <strong>${budget_spent:,.2f}</strong> di <strong>${budget_tot:,.2f}</strong></span>
                        <span>Progresso: <strong style="color:#38bdf8">{prog_pct}</strong></span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: {prog_pct}"></div>
                    </div>
                </div>

                <div class="click-hint">👉 Clicca per aprire la scheda con Token URL e requisiti trascritti</div>
            </div>
    """

    cnt_all = counts.get("all", 0)
    cnt_nuove = counts.get("Nuove", 0)
    cnt_iscritte = counts.get("Iscritte", 0)
    cnt_in_pausa = counts.get("In pausa", 0)
    cnt_passate = counts.get("Passate", 0)
    cnt_attesa = counts.get("Lista d'attesa", 0)

    html_content += f"""
            <div class="tab-filters">
                <button class="tab-filter-btn active" onclick="filterBySection('all', this)">Tutte ({cnt_all})</button>
                <button class="tab-filter-btn" onclick="filterBySection('Nuove', this)">🔥 Nuove ({cnt_nuove})</button>
                <button class="tab-filter-btn" onclick="filterBySection('Iscritte', this)">✅ Iscritte ({cnt_iscritte})</button>
                <button class="tab-filter-btn" onclick="filterBySection('In pausa', this)">⏸️ In Pausa ({cnt_in_pausa})</button>
                <button class="tab-filter-btn" onclick="filterBySection('Passate', this)">📜 Concluse ({cnt_passate})</button>
                <button class="tab-filter-btn" onclick="filterBySection('Lista d\'attesa', this)">⏳ In Attesa ({cnt_attesa})</button>
            </div>

            <div class="section-title" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                <div>
                    <span>📊 Tutte le Campagne Scansionate ({len(campaigns)})</span>
                    <div style="font-size:0.85rem; font-weight:normal; color:var(--text-muted); margin-top:0.3rem;">Usa le spunte per selezionare le campagne da generare, poi clicca "Salva Selezionate". Clicca sulla scheda per aprire i dettagli.</div>
                </div>
                <div style="display:flex; gap:0.6rem; align-items:center; flex-wrap:wrap;">
                    <button onclick="triggerRefresh(this)" style="background:linear-gradient(135deg, #0284c7, #0369a1); color:white; border:none; padding:0.6rem 1.2rem; border-radius:0.6rem; font-weight:800; cursor:pointer; font-size:0.88rem; display:flex; align-items:center; gap:0.4rem; box-shadow:0 4px 12px rgba(2,132,199,0.3); transition:transform 0.15s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
                        🔄 Sincronizza Dati Klippify
                    </button>
                    <button onclick="saveSelectedCampaigns()" id="btn-save-selected" style="background:linear-gradient(135deg, #10b981, #059669); color:white; border:none; padding:0.6rem 1.2rem; border-radius:0.6rem; font-weight:700; cursor:pointer; font-size:0.9rem; display:flex; align-items:center; gap:0.5rem; transition:transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
                        💾 Salva Selezionate
                    </button>
                </div>
            </div>

            <div class="cards-grid" id="main-cards-grid">
    """

    for idx, c in enumerate(campaigns):
        payout = c.get("payout_per_1k_views", 1.0)
        pool_rem = c.get("budget_remaining", 0.0)
        budget_tot = c.get("budget_total", 0.0)
        prog_pct = c.get("budget_progress_percent", "0%")
        score = c.get("convenience_score", 50)
        has_media = c.get("has_local_media", False)
        token = c.get("campaign_token", c.get("id", ""))
        sec = c.get("section", "Nuove")
        banner_url = c.get("banner") or "https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Collecto__16x9_2K.webp"
        logo_url = c.get("logo") or ""

        logo_img_html = f'<img src="{logo_url}" style="width:20px; height:20px; border-radius:4px; object-fit:cover;">' if logo_url else '⚡'

        html_content += f"""
                <div class="card" data-section="{sec}" onclick="openModal({idx})" style="padding:0; overflow:hidden;">
                    <div style="width:100%; height:140px; position:relative; overflow:hidden; background:#0f172a;">
                        <img src="{banner_url}" style="width:100%; height:100%; object-fit:cover; object-position:center; transition:transform 0.3s ease;" alt="{c['name']}" onerror="this.src='https://klippify-prod.s3.us-east-1.amazonaws.com/uploads/banners-ai/Collecto__16x9_2K.webp'">
                        <div style="position:absolute; top:0.8rem; left:0.8rem; background:rgba(15,23,42,0.85); backdrop-filter:blur(8px); border:1px solid rgba(255,255,255,0.15); padding:0.2rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700; color:#38bdf8; display:flex; align-items:center; gap:0.4rem;" onclick="event.stopPropagation();">
                            <input type="checkbox" class="campaign-checkbox" data-campaign-id="{token}" style="width:1.2rem; height:1.2rem; cursor:pointer; accent-color:#10b981;">
                            🏷️ {sec}
                        </div>
                        <div style="position:absolute; top:0.8rem; right:0.8rem; background:rgba(139,92,246,0.9); color:#fff; font-size:0.75rem; font-weight:800; padding:0.2rem 0.6rem; border-radius:0.4rem;">
                            {score} pts
                        </div>
                    </div>

                    <div style="padding:1.2rem;">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.8rem;">
                            <div>
                                <div style="font-size:1.1rem; font-weight:700; color:#fff;">#{idx+1} {c['name']}</div>
                                <div style="font-size:0.83rem; color:var(--text-muted); display:flex; align-items:center; gap:0.4rem; margin-top:0.2rem;">
                                    {logo_img_html} <span>{c.get('brand', 'Klippify Partner')}</span>
                                </div>
                                <div style="font-size:0.72rem; font-family:monospace; color:#a78bfa; margin-top:0.25rem;">Token: {token[:12]}...</div>
                            </div>
                        </div>

                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.8rem; background:rgba(15,23,42,0.6); padding:0.8rem; border-radius:0.6rem; border:1px solid var(--card-border); margin:1rem 0;">
                            <div>
                                <div style="font-size:0.72rem; color:var(--text-muted);">PAYOUT / 1K</div>
                                <div style="font-size:1.1rem; font-weight:700; color:#34d399;">${payout:.2f}</div>
                            </div>
                            <div>
                                <div style="font-size:0.72rem; color:var(--text-muted);">POOL RIMANENTE</div>
                                <div style="font-size:1.1rem; font-weight:700; color:#38bdf8;">${pool_rem:,.2f}</div>
                            </div>
                            <div style="grid-column: span 2; border-top:1px solid rgba(255,255,255,0.05); padding-top:0.5rem; display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-size:0.72rem; color:var(--text-muted);">Budget Totale:</span>
                                <span style="font-size:0.78rem; font-weight:600; color:#f59e0b;">${budget_tot:,.2f}</span>
                            </div>
                        </div>

                        <div style="font-size:0.78rem; color:var(--text-muted);">
                            Avanzamento Pool: <strong style="color:#fff">{prog_pct}</strong>
                            <div class="progress-bar-bg" style="height:6px; margin-top:0.3rem;">
                                <div class="progress-bar-fill" style="width: {prog_pct}"></div>
                            </div>
                        </div>

                        <div style="margin-top:1rem; display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.05); padding-top:0.7rem;">
                            <span style="font-size:0.75rem; color:{'#34d399' if has_media else '#94a3b8'};">
                                {'✅ File locali trovati' if has_media else '📁 Media su Klippify'}
                            </span>
                            <span style="font-size:0.78rem; font-weight:700; color:var(--accent-purple);">Dettagli Token →</span>
                        </div>
                    </div>
                </div>
        """

    html_content += f"""
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- VIEW MY CAMPAIGNS                         -->
    <!-- ========================================== -->
    <div id="view-my-campaigns-section" class="creator-dashboard-v2" style="display: none;">
        <div class="dashboard-welcome-header">
            <h1>⚡ Campagne Attive</h1>
            <p>Tutte le campagne a cui sei iscritto su Klippify con strumenti per Generazione AI e Clipping Video.</p>
        </div>
        
        <div id="my-campaigns-grid" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:1.5rem;">
            <!-- Rendered by JS renderMyCampaigns() -->
        </div>
        
        <div id="my-campaign-detail-view" style="display: none;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1.5rem; flex-wrap:wrap; gap:1rem;">
                <button onclick="closeCampaignDetail()" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 0.5rem; color: #fff; cursor: pointer; font-weight: bold; display: flex; align-items: center; gap: 0.5rem; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                    ⬅ Torna alla griglia
                </button>
                <button onclick="if(currentDetailCampToken) deleteCampaign(currentDetailCampToken)" style="background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.35); padding: 0.5rem 1.2rem; border-radius: 0.5rem; color: #ef4444; cursor: pointer; font-weight: bold; display: flex; align-items: center; gap: 0.5rem; transition: all 0.2s;" onmouseover="this.style.background='rgba(239,68,68,0.3)'" onmouseout="this.style.background='rgba(239,68,68,0.15)'">
                    🗑️ Elimina questa Campagna
                </button>
            </div>
            <div id="my-campaign-detail-content"></div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- VIEW 3: CONTENT STUDIO                    -->
    <!-- ========================================== -->
    <div id="view-studio-section" style="margin-top: 3rem; display: none;">
        <div style="text-align:center; margin-bottom: 2rem;">
            <h2 style="font-size:2rem; font-weight:800; background: linear-gradient(90deg, #f59e0b, #ef4444); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">🎬 Content Studio</h2>
            <p style="color: var(--text-muted); margin-top:0.5rem;">Genera i tuoi video per le campagne attive</p>
        </div>
        
        <!-- CUSTOM DYNAMIC PROMPT BOX -->
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(139, 92, 246, 0.5); border-radius: 1rem; padding: 1.5rem; margin-bottom: 2rem;">
            <h3 style="color:#fff; margin-bottom: 0.5rem;">🤖 Generazione Video Automatica</h3>
            <p style="color:var(--text-muted); font-size:0.85rem; margin-bottom: 1rem;">Scrivi un prompt personalizzato e clicca il pulsante per far generare il video direttamente al tuo bot Playwright in background.</p>
            <textarea id="dynamic-prompt-input" style="width: 100%; height: 80px; background: rgba(0,0,0,0.3); border: 1px solid var(--card-border); border-radius: 0.5rem; color: #fff; padding: 0.8rem; font-family: inherit; margin-bottom: 1rem;" placeholder="Esempio: Genera un video realistico di un tramonto sul mare..."></textarea>
            
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div id="dynamic-prompt-status" style="font-size: 0.85rem; font-weight: bold; color: var(--accent-cyan);">Pronto.</div>
                <button onclick="generateDynamicVideo()" id="dynamic-prompt-btn" style="background:linear-gradient(135deg, #8b5cf6, #3b82f6); color:white; border:none; padding:0.6rem 1.2rem; border-radius:0.6rem; font-weight:700; cursor:pointer; font-size:0.9rem; transition:transform 0.2s;">
                    Genera Video con Gemini 🎬
                </button>
            </div>
        </div>
        
        <!-- VIDEO GALLERY -->
        <div style="margin-bottom: 2rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <h3 style="color:#fff; font-size:1.5rem;">🎞️ I Tuoi Video Generati</h3>
                <button onclick="fetchAndRenderVideos()" style="background:rgba(255,255,255,0.1); color:white; border:1px solid rgba(255,255,255,0.2); padding:0.4rem 0.8rem; border-radius:0.4rem; cursor:pointer;">
                    🔄 Aggiorna Lista
                </button>
            </div>
            <div id="video-gallery-grid" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap:1rem;">
                <!-- Video verranno iniettati qui via JS -->
            </div>
        </div>

    </div> <!-- End Studio View -->
        <!-- ========================================== -->
        <!-- VIEW 4: TIKTOK MANAGER                     -->
        <!-- ========================================== -->
        <div id="view-tiktok-section" class="creator-dashboard-v2" style="display: none;">
            <div class="dashboard-welcome-header">
                <h1>TikTok Manager 📱</h1>
                <p>Gestisci il tuo account TikTok e pubblica i video generati con un clic.</p>
            </div>

            <div class="k-stats-grid" id="tiktok-stats-container">
                <div class="k-stat-card" style="justify-content:center; color:var(--text-muted);">
                    ⏳ Caricamento statistiche TikTok in corso...
                </div>
            </div>

            <div class="k-dashboard-main-grid" style="grid-template-columns: 1fr; margin-top:2rem;">
                <div class="k-panel-card">
                    <div class="k-panel-header">
                        <div>
                            <div class="k-panel-title">Pubblica su TikTok</div>
                            <div class="k-panel-subtitle">Seleziona un video generato per caricarlo direttamente sul tuo profilo.</div>
                        </div>
                    </div>
                    
                    <div style="display:flex; gap:1.5rem; flex-wrap:wrap; margin-top:1rem;">
                        <div style="flex:1; min-width:300px;">
                            <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem; display:block;">1. Seleziona Campagna (opzionale)</label>
                            <select id="tiktok-campaign-select" style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.8rem; border-radius:0.5rem; font-size:0.95rem; margin-bottom:1rem;">
                                <option value="unknown">Nessuna campagna specifica</option>
                            </select>

                            <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem; display:block;">2. Seleziona Video</label>
                            <select id="tiktok-video-select" style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.8rem; border-radius:0.5rem; font-size:0.95rem;">
                                <option value="">⏳ Caricamento video...</option>
                            </select>
                        </div>
                        
                        <div style="flex:2; min-width:300px;">
                            <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem; display:block;">3. Titolo del Video</label>
                            <input type="text" id="tiktok-video-title" placeholder="Es. Il segreto del successo" style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.8rem; border-radius:0.5rem; font-size:0.95rem; margin-bottom:1rem;">
                            
                            <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700; margin-bottom:0.4rem; display:block;">3. Descrizione / Caption</label>
                            <textarea id="tiktok-video-caption" rows="3" placeholder="Scrivi una descrizione lunga, inserisci gli hashtag... #klippify #trend" style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.8rem; border-radius:0.5rem; font-size:0.95rem; font-family:inherit; resize:vertical;"></textarea>
                            
                            <div style="margin-top:1rem; display:flex; align-items:center; gap:1rem;">
                                <label style="font-size:0.85rem; color:var(--text-muted); font-weight:700;">4. Copertina (secondi):</label>
                                <input type="number" id="tiktok-video-cover" value="1.0" step="0.5" min="0" style="width:80px; background:rgba(0,0,0,0.4); border:1px solid var(--card-border); color:#fff; padding:0.5rem; border-radius:0.5rem; font-size:0.95rem; text-align:center;">
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-top:1.5rem;">
                        <button onclick="publishToTikTok()" id="tiktok-publish-btn" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; padding:0.8rem 1.5rem; border:none; border-radius:0.5rem; font-size:1rem; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 15px rgba(16, 185, 129, 0.3);">
                            Pubblica su TikTok 🚀
                        </button>
                        <div id="tiktok-publish-status" style="margin-top:0.8rem; font-size:0.9rem; font-weight:600;"></div>
                    </div>
                </div>
            </div>

            <!-- ALL PUBLISHED TIKTOK VIDEOS GALLERY -->
            <div class="k-dashboard-main-grid" style="grid-template-columns: 1fr; margin-top:2rem;">
                <div class="k-panel-card">
                    <div class="k-panel-header" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                        <div>
                            <div class="k-panel-title">🎬 Tutti i Tuoi Video su TikTok</div>
                            <div class="k-panel-subtitle">Visualizzazioni, Mi Piace, commenti e condivisioni in tempo reale dai tuoi video TikTok.</div>
                        </div>
                        <button onclick="loadTikTokPublishedVideos(true)" id="btn-refresh-tiktok-vids" style="background:rgba(56, 189, 248, 0.15); color:#38bdf8; border:1px solid rgba(56, 189, 248, 0.3); padding:0.6rem 1.2rem; border-radius:0.5rem; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:0.5rem; transition:transform 0.2s;">
                            🔄 Aggiorna Metriche
                        </button>
                    </div>

                    <div id="tiktok-published-videos-grid" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap:1.5rem; margin-top:1.5rem;">
                        <div style="color:var(--text-muted); padding:1rem; grid-column: 1 / -1; text-align:center;">⏳ Caricamento video pubblicati da TikTok...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- VIEW 6: DEBUG & PROCESS MONITOR VIEW       -->
        <!-- ========================================== -->
        <div id="view-debug-section" style="display:none; padding:1.5rem 0;">
            <div class="k-panel-card" style="margin-bottom:1.5rem; background:linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border:1px solid rgba(56, 189, 248, 0.25); box-shadow:0 8px 32px rgba(0,0,0,0.4);">
                <div class="k-panel-header" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                    <div>
                        <div class="k-panel-title" style="display:flex; align-items:center; gap:0.6rem;">
                            <span>🛠️ Monitor Processi &amp; Debug</span>
                            <span id="debug-live-indicator" style="font-size:0.75rem; background:rgba(16,185,129,0.2); color:#10b981; border:1px solid rgba(16,185,129,0.4); padding:0.2rem 0.6rem; border-radius:1rem; font-weight:700;">🟢 LIVE</span>
                        </div>
                        <div class="k-panel-subtitle">Monitora in tempo reale l&#39;esecuzione di Gemini, TikTok Uploader, FFmpeg e API Klippify. Controlla la velocità, leggi i log e termina i processi lenti o bloccati.</div>
                    </div>
                    <div style="display:flex; gap:0.8rem; align-items:center; flex-wrap:wrap;">
                        <button onclick="loadDebugTasks(true)" style="background:rgba(56, 189, 248, 0.15); color:#38bdf8; border:1px solid rgba(56, 189, 248, 0.3); padding:0.6rem 1rem; border-radius:0.5rem; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:transform 0.2s;">
                            🔄 Aggiorna Log
                        </button>
                        <button onclick="clearFinishedTasks()" style="background:rgba(255,255,255,0.08); color:#cbd5e1; border:1px solid rgba(255,255,255,0.15); padding:0.6rem 1rem; border-radius:0.5rem; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:0.4rem;">
                            🧹 Pulisci Conclusi
                        </button>
                        <button onclick="killAllTasks()" style="background:linear-gradient(135deg, #ef4444, #dc2626); color:#fff; border:none; padding:0.6rem 1.2rem; border-radius:0.5rem; font-weight:800; cursor:pointer; display:flex; align-items:center; gap:0.4rem; box-shadow:0 4px 12px rgba(239, 68, 68, 0.3); transition:transform 0.2s;">
                            🛑 Termina Tutti i Processi
                        </button>
                    </div>
                </div>

                <!-- METRICS STRIP -->
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:1rem; margin-top:1.5rem; border-top:1px solid rgba(255,255,255,0.06); padding-top:1.2rem;">
                    <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.9rem 1.2rem; border-left:4px solid #10b981;">
                        <div style="font-size:0.75rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Processi Attivi</div>
                        <div id="debug-stat-running" style="font-size:1.6rem; font-weight:800; color:#10b981; margin-top:0.2rem;">0</div>
                    </div>
                    <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.9rem 1.2rem; border-left:4px solid #f59e0b;">
                        <div style="font-size:0.75rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Lenti / In Attesa (&gt;3 min)</div>
                        <div id="debug-stat-stuck" style="font-size:1.6rem; font-weight:800; color:#f59e0b; margin-top:0.2rem;">0</div>
                    </div>
                    <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.9rem 1.2rem; border-left:4px solid #38bdf8;">
                        <div style="font-size:0.75rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Completati</div>
                        <div id="debug-stat-completed" style="font-size:1.6rem; font-weight:800; color:#38bdf8; margin-top:0.2rem;">0</div>
                    </div>
                    <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.9rem 1.2rem; border-left:4px solid #ef4444;">
                        <div style="font-size:0.75rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Interrotti / Errori</div>
                        <div id="debug-stat-failed" style="font-size:1.6rem; font-weight:800; color:#ef4444; margin-top:0.2rem;">0</div>
                    </div>
                </div>
            </div>

            <!-- TASK LIST CONTAINER -->
            <div id="debug-tasks-container" style="display:flex; flex-direction:column; gap:1.2rem;">
                <div id="debug-tasks-empty-placeholder" style="text-align:center; padding:3.5rem; color:var(--text-muted); background:rgba(0,0,0,0.2); border:1px dashed rgba(255,255,255,0.1); border-radius:1rem;">
                    <div style="font-size:2.5rem; margin-bottom:0.6rem;">⚙️</div>
                    <div style="font-size:1.1rem; font-weight:700; color:#cbd5e1;">Caricamento processi in corso...</div>
                    <div style="font-size:0.85rem; margin-top:0.3rem;">I processi in corso e lo storico delle esecuzioni verranno visualizzati qui in tempo reale.</div>
                </div>
            </div>
        </div>

    </div> <!-- closes container -->
    </div> <!-- closes main-content -->
    </div> <!-- closes app-container -->

    <!-- MODAL OVERLAY -->
    <div class="modal-overlay" id="modal-overlay" onclick="closeModalOnOverlay(event)">
        <div class="modal-container">
            <button class="modal-close" onclick="closeModal()">✕</button>
            <div id="modal-body"></div>
        </div>
    </div>
    <script>
        const allCampaignsData = {campaigns_json};
        const dashboardData = {dashboard_json};
        let klippifySubmissions = {submissions_json};
        let generatedContent = {generated_json};
        let selectedCampaigns = {selected_json};
        const publishedContent = {published_json};
        let campaignSchedules = {schedules_json};
        let cachedTikTokVideos = [];
        let currentDetailCampToken = null;

        function formatDuration(sec) {{
            if (!sec) return "";
            const m = Math.floor(sec / 60);
            const s = Math.floor(sec % 60);
            return `${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
        }}

        function formatTikTokDate(timestamp) {{
            if (!timestamp) return "";
            const d = new Date(timestamp * 1000);
            return d.toLocaleDateString('it-IT', {{ day: '2-digit', month: '2-digit', year: 'numeric' }});
        }}

        function renderTikTokVideoCard(v, isCompact=false) {{
            const durBadge = v.duration ? `<span class="tiktok-duration-badge">⏱ ${{formatDuration(v.duration)}}</span>` : '';
            const coverImg = v.cover_image_url || 'https://via.placeholder.com/300x400/0f172a/94a3b8?text=TikTok+Video';
            const titleText = (v.title || v.description || 'Senza descrizione').replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const dateStr = formatTikTokDate(v.create_time);

            return `
                <div class="tiktok-video-card" style="${{isCompact ? 'max-width:320px;' : ''}}">
                    <div class="tiktok-cover-wrap" style="${{isCompact ? 'padding-top:100%;' : ''}}">
                        <img src="${{coverImg}}" class="tiktok-cover-img" alt="Cover" loading="lazy" onerror="this.src='https://via.placeholder.com/300x400/0f172a/94a3b8?text=TikTok+Video'">
                        ${{durBadge}}
                    </div>
                    <div class="tiktok-card-body">
                        <div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
                                <span style="font-size:0.75rem; color:#a78bfa; font-weight:700;">TikTok Live</span>
                                <span style="font-size:0.72rem; color:var(--text-muted);">${{dateStr}}</span>
                            </div>
                            <div class="tiktok-card-title" title="${{titleText}}">${{titleText}}</div>
                        </div>

                        <div class="tiktok-metrics-grid">
                            <div class="tiktok-metric-pill" title="Visualizzazioni">
                                <span style="color:#38bdf8;">👁️</span>
                                <span><strong>${{(v.view_count || 0).toLocaleString()}}</strong> views</span>
                            </div>
                            <div class="tiktok-metric-pill" title="Mi Piace">
                                <span style="color:#f43f5e;">❤️</span>
                                <span><strong>${{(v.like_count || 0).toLocaleString()}}</strong> like</span>
                            </div>
                            <div class="tiktok-metric-pill" title="Commenti">
                                <span style="color:#34d399;">💬</span>
                                <span><strong>${{(v.comment_count || 0).toLocaleString()}}</strong> comm.</span>
                            </div>
                            <div class="tiktok-metric-pill" title="Condivisioni">
                                <span style="color:#f59e0b;">🔄</span>
                                <span><strong>${{(v.share_count || 0).toLocaleString()}}</strong> share</span>
                            </div>
                        </div>

                        <a href="${{v.share_url || '#'}}" target="_blank" class="tiktok-link-btn">
                            <span>Guarda su TikTok</span>
                            <span>↗</span>
                        </a>
                    </div>
                </div>
            `;
        }}

        async function loadTikTokPublishedVideos(force=false) {{
            const grid = document.getElementById('tiktok-published-videos-grid');
            const refreshBtn = document.getElementById('btn-refresh-tiktok-vids');

            if (!force && cachedTikTokVideos && cachedTikTokVideos.length > 0) {{
                if (grid) renderTikTokVideosGrid(cachedTikTokVideos);
                return;
            }}

            if (refreshBtn) refreshBtn.innerHTML = '⏳ Caricamento...';
            if (grid) grid.innerHTML = '<div style="color:var(--text-muted); padding:2rem; grid-column: 1 / -1; text-align:center;">⏳ Connessione all&apos;API TikTok per estrarre tutti i tuoi video...</div>';

            try {{
                const res = await fetch('/api/tiktok/videos');
                const data = await res.json();
                if (data.error) throw new Error(data.error);

                cachedTikTokVideos = data.videos || [];
                if (grid) renderTikTokVideosGrid(cachedTikTokVideos);

                // Update any open campaign view stats
                updateCampaignDetailTikTokStats();
            }} catch(err) {{
                console.error("Errore caricamento video TikTok", err);
                if (grid) grid.innerHTML = `<div style="color:#ef4444; padding:2rem; grid-column: 1 / -1; text-align:center;">❌ Errore nel caricare i video: ${{err.message}}</div>`;
            }} finally {{
                if (refreshBtn) refreshBtn.innerHTML = '🔄 Aggiorna Metriche';
            }}
        }}

        function renderTikTokVideosGrid(videos) {{
            const grid = document.getElementById('tiktok-published-videos-grid');
            if (!grid) return;

            if (!videos || videos.length === 0) {{
                grid.innerHTML = '<div style="color:var(--text-muted); padding:2rem; grid-column: 1 / -1; text-align:center;">Nessun video trovato sul profilo TikTok.</div>';
                return;
            }}

            grid.innerHTML = videos.map(v => renderTikTokVideoCard(v)).join('');
        }}

        function findMatchingTikTokVideo(campToken, campName, pubItem) {{
            if (!cachedTikTokVideos || cachedTikTokVideos.length === 0) return null;
            
            // 1. Direct match by pubItem filename / title
            if (pubItem) {{
                if (pubItem.filename) {{
                    const match = cachedTikTokVideos.find(v => (v.title || '').includes(pubItem.filename) || (v.description || '').includes(pubItem.filename));
                    if (match) return match;
                }}
                if (pubItem.title) {{
                    const cleanT = pubItem.title.split('\\n')[0].trim().toLowerCase();
                    if (cleanT.length > 3) {{
                        const match = cachedTikTokVideos.find(v => (v.title || '').toLowerCase().includes(cleanT) || (v.description || '').toLowerCase().includes(cleanT));
                        if (match) return match;
                    }}
                }}
            }}

            // 2. Match by campaign name or token
            if (campName) {{
                const cleanName = campName.toLowerCase().replace(/[^a-z0-9]/g, '');
                if (cleanName.length > 3) {{
                    const match = cachedTikTokVideos.find(v => {{
                        const desc = (v.description || '').toLowerCase().replace(/[^a-z0-9]/g, '');
                        return desc.includes(cleanName);
                    }});
                    if (match) return match;
                }}
            }}

            return null;
        }}

        function updateCampaignDetailTikTokStats() {{
            const kanbanCards = document.querySelectorAll('.kanban-card[data-video-file]');
            kanbanCards.forEach(card => {{
                const filename = card.getAttribute('data-video-file');
                const campToken = card.getAttribute('data-camp-token') || '';
                const match = findMatchingTikTokVideo(campToken, null, {{ filename }});
                if (match) {{
                    const vEl = card.querySelector('.stat-views');
                    const lEl = card.querySelector('.stat-likes');
                    if (vEl) vEl.innerText = (match.view_count || 0).toLocaleString();
                    if (lEl) lEl.innerText = (match.like_count || 0).toLocaleString();
                    
                    const coverEl = card.querySelector('.kanban-video-cover');
                    if (coverEl && match.cover_image_url) {{
                        coverEl.src = match.cover_image_url;
                        coverEl.style.display = 'block';
                    }}
                }}
            }});
        }}

        // --- DRAG AND DROP KANBAN LOGIC ---
        function allowDrop(ev) {{
            ev.preventDefault();
        }}

        function drag(ev) {{
            ev.dataTransfer.setData("scriptId", ev.target.id);
            ev.dataTransfer.setData("campToken", ev.target.getAttribute("data-camp-token"));
            ev.dataTransfer.setData("scriptIndex", ev.target.getAttribute("data-script-index"));
        }}

        async function drop(ev, newStatus) {{
            ev.preventDefault();
            const scriptId = ev.dataTransfer.getData("scriptId");
            const campToken = ev.dataTransfer.getData("campToken");
            const scriptIndex = parseInt(ev.dataTransfer.getData("scriptIndex"));
            
            // Find the closest drop zone (the column body)
            let dropZone = ev.target;
            while(dropZone && !dropZone.classList.contains('kanban-column-body')) {{
                dropZone = dropZone.parentElement;
            }}
            if(!dropZone) return;

            const draggedElement = document.getElementById(scriptId);
            if (draggedElement) {{
                dropZone.appendChild(draggedElement);
            }}

            // Update Backend
            try {{
                await fetch('/api/update-script-status', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        campaign_id: campToken,
                        script_index: scriptIndex,
                        status: newStatus
                    }})
                }});
                
                // Aggiorniamo anche la variabile locale in memoria per evitare glitch se l'utente non ricarica
                const item = generatedContent.find(gc => gc.campaign_id === campToken);
                if (item && item.scripts) {{
                    item.scripts[scriptIndex].status = newStatus;
                }}
                
            }} catch(e) {{
                console.error("Errore salvataggio status", e);
            }}
        }}

        async function fetchAndRenderVideos() {{
            const grid = document.getElementById('video-gallery-grid');
            grid.innerHTML = '<div style="color:var(--text-muted)">Caricamento video in corso...</div>';
            try {{
                const res = await fetch('/api/videos');
                const videos = await res.json();
                
                if (videos.length === 0) {{
                    grid.innerHTML = '<div style="color:var(--text-muted); font-style:italic;">Nessun video generato ancora. Usa il box qui sopra!</div>';
                    return;
                }}
                
                grid.innerHTML = '';
                videos.forEach(v => {{
                    const sizeMB = (v.size / (1024 * 1024)).toFixed(2);
                    const card = document.createElement('div');
                    card.style.background = 'rgba(15, 23, 42, 0.6)';
                    card.style.border = '1px solid var(--card-border)';
                    card.style.borderRadius = '0.5rem';
                    card.style.padding = '0.5rem';
                    card.style.display = 'flex';
                    card.style.flexDirection = 'column';
                    
                    const videoEl = document.createElement('video');
                    videoEl.src = '/generated_videos/' + encodeURIComponent(v.filename);
                    videoEl.controls = true;
                    videoEl.preload = 'metadata';
                    videoEl.playsInline = true;
                    videoEl.style.width = '100%';
                    videoEl.style.borderRadius = '0.4rem';
                    videoEl.style.background = '#000';
                    videoEl.style.maxHeight = '320px';
                    
                    const title = document.createElement('div');
                    title.style.color = '#fff';
                    title.style.fontSize = '0.8rem';
                    title.style.marginTop = '0.5rem';
                    title.style.wordBreak = 'break-all';
                    title.innerText = v.filename;
                    
                    const meta = document.createElement('div');
                    meta.style.color = 'var(--text-muted)';
                    meta.style.fontSize = '0.7rem';
                    meta.innerText = sizeMB + ' MB';
                    
                    const downloadBtn = document.createElement('a');
                    downloadBtn.href = videoEl.src;
                    downloadBtn.download = v.filename;
                    downloadBtn.innerText = '💾 Salva File';
                    downloadBtn.style.marginTop = '0.5rem';
                    downloadBtn.style.display = 'block';
                    downloadBtn.style.textAlign = 'center';
                    downloadBtn.style.background = 'rgba(255,255,255,0.1)';
                    downloadBtn.style.color = '#fff';
                    downloadBtn.style.padding = '0.3rem';
                    downloadBtn.style.borderRadius = '0.3rem';
                    downloadBtn.style.textDecoration = 'none';
                    downloadBtn.style.fontSize = '0.8rem';
                    
                    card.appendChild(videoEl);
                    card.appendChild(title);
                    card.appendChild(meta);
                    card.appendChild(downloadBtn);
                    grid.appendChild(card);
                }});
            }} catch (err) {{
                grid.innerHTML = '<div style="color:#ef4444;">Errore durante il caricamento dei video.</div>';
                console.error(err);
            }}
        }}

        async function generateDynamicVideo() {{
            const inputEl = document.getElementById('dynamic-prompt-input');
            const btnEl = document.getElementById('dynamic-prompt-btn');
            const statusEl = document.getElementById('dynamic-prompt-status');
            
            const prompt = inputEl.value.trim();
            if (!prompt) {{
                alert("Per favore, inserisci un prompt prima di generare!");
                return;
            }}
            
            btnEl.disabled = true;
            btnEl.innerText = "⏳ Avvio in corso...";
            btnEl.style.opacity = "0.5";
            
            const spinnerSvg = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 5px;"><path d="M21 12a9 9 0 1 1-6.219-8.56"><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite" /></path></svg>`;
            statusEl.innerHTML = spinnerSvg + "Avvio bot...";
            statusEl.style.color = "#f59e0b"; // amber
            
            // Conta video iniziali
            let initialVideoCount = 0;
            try {{
                const resCount = await fetch('/api/videos');
                const vids = await resCount.json();
                initialVideoCount = vids.length;
            }} catch (e) {{}}

            try {{
                const res = await fetch('/api/generate-video', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{ prompt: prompt }})
                }});
                
                const data = await res.json();
                if (res.ok) {{
                    btnEl.innerText = "⏳ Generazione (~1 min)...";
                    statusEl.innerHTML = spinnerSvg + "Generazione video in corso...";
                    
                    // Polling per controllare quando spunta un nuovo video
                    const pollInterval = setInterval(async () => {{
                        try {{
                            const pollRes = await fetch('/api/videos');
                            const currentVideos = await pollRes.json();
                            if (currentVideos.length > initialVideoCount) {{
                                clearInterval(pollInterval);
                                statusEl.innerText = "✅ Video pronto!";
                                statusEl.style.color = "#10b981"; // green
                                btnEl.disabled = false;
                                btnEl.innerText = "Genera Video con Gemini 🎬";
                                btnEl.style.opacity = "1";
                                fetchAndRenderVideos();
                            }}
                        }} catch(e) {{}}
                    }}, 3000);
                    
                }} else {{
                    statusEl.innerText = "❌ " + (data.error || "Errore sconosciuto");
                    statusEl.style.color = "#ef4444"; // red
                    btnEl.disabled = false;
                    btnEl.innerText = "Genera Video con Gemini 🎬";
                    btnEl.style.opacity = "1";
                }}
            }} catch (err) {{
                statusEl.innerText = "❌ Errore di rete: " + err.message;
                statusEl.style.color = "#ef4444"; // red
                btnEl.disabled = false;
                btnEl.innerText = "Genera Video con Gemini 🎬";
                btnEl.style.opacity = "1";
            }}
        }}

        async function triggerRefresh(btnElem) {{
            const el = btnElem || document.querySelector('.sidebar-footer button');
            const origHtml = el ? el.innerHTML : "";
            if (el) {{
                el.innerHTML = "⏳ Sincronizzazione Klippify...";
                el.disabled = true;
            }}
            try {{
                const res = await fetch('/api/sync/klippify', {{ method: 'POST' }});
                const data = await res.json();
                if (el) el.innerHTML = "✅ Sincronizzato!";
                setTimeout(() => {{
                    window.location.reload();
                }}, 1200);
            }} catch(e) {{
                alert("Errore sincronizzazione: " + e.message);
                if (el) {{
                    el.innerHTML = origHtml;
                    el.disabled = false;
                }}
            }}
        }}

        let currentActiveView = 'dashboard';

        function switchMainView(viewName) {{
            currentActiveView = viewName;
            const dashView = document.getElementById('view-dashboard-section');
            const intelView = document.getElementById('view-intelligence-section');
            const studioView = document.getElementById('view-studio-section');
            const tiktokView = document.getElementById('view-tiktok-section');
            const myCampsView = document.getElementById('view-my-campaigns-section');
            const debugView = document.getElementById('view-debug-section');
            
            const dashBtn = document.getElementById('main-tab-dashboard');
            const intelBtn = document.getElementById('main-tab-intelligence');
            const studioBtn = document.getElementById('main-tab-studio');
            const tiktokBtn = document.getElementById('main-tab-tiktok');
            const myCampsBtn = document.getElementById('main-tab-my-campaigns');
            const debugBtn = document.getElementById('main-tab-debug');

            if (dashView) dashView.style.display = 'none';
            if (intelView) intelView.style.display = 'none';
            if (studioView) studioView.style.display = 'none';
            if (tiktokView) tiktokView.style.display = 'none';
            if (myCampsView) myCampsView.style.display = 'none';
            if (debugView) debugView.style.display = 'none';
            
            if (dashBtn) dashBtn.classList.remove('active');
            if (intelBtn) intelBtn.classList.remove('active');
            if (studioBtn) studioBtn.classList.remove('active');
            if (tiktokBtn) tiktokBtn.classList.remove('active');
            if (myCampsBtn) myCampsBtn.classList.remove('active');
            if (debugBtn) debugBtn.classList.remove('active');
            
            if (viewName === 'dashboard') {{
                if (dashView) dashView.style.display = 'flex';
                if (dashBtn) dashBtn.classList.add('active');
                if (dashView) dashView.scrollIntoView({{ behavior: 'smooth' }});
            }} else if (viewName === 'my-campaigns') {{
                if (myCampsView) myCampsView.style.display = 'block';
                if (myCampsBtn) myCampsBtn.classList.add('active');
                if (myCampsView) myCampsView.scrollIntoView({{ behavior: 'smooth' }});
                renderMyCampaigns();
            }} else if (viewName === 'intelligence') {{
                if (intelView) intelView.style.display = 'block';
                if (intelBtn) intelBtn.classList.add('active');
                if (intelView) intelView.scrollIntoView({{ behavior: 'smooth' }});
            }} else if (viewName === 'studio') {{
                if (studioView) studioView.style.display = 'block';
                if (studioBtn) studioBtn.classList.add('active');
                if (studioView) studioView.scrollIntoView({{ behavior: 'smooth' }});
                fetchAndRenderVideos();
            }} else if (viewName === 'tiktok') {{
                if (tiktokView) tiktokView.style.display = 'block';
                if (tiktokBtn) tiktokBtn.classList.add('active');
                if (tiktokView) tiktokView.scrollIntoView({{ behavior: 'smooth' }});
                loadTikTokPublishedVideos();
            }} else if (viewName === 'debug') {{
                if (debugView) debugView.style.display = 'block';
                if (debugBtn) debugBtn.classList.add('active');
                if (debugView) debugView.scrollIntoView({{ behavior: 'smooth' }});
                loadDebugTasks(true);
            }}
        }}

        // ==========================================
        // AUTOPILOT ENGINE LOGIC & UI FUNCTIONS
        // ==========================================
        // CAMPAIGN-SPECIFIC AUTOPILOT FUNCTIONS
        // ==========================================
        let currentCampaignAutopilotState = {{}};

        async function loadCampaignAutopilotState(campToken) {{
            if (!campToken) return null;
            try {{
                const res = await fetch(`/api/autopilot/campaign-status?campaign_id=${{encodeURIComponent(campToken)}}`);
                const data = await res.json();
                currentCampaignAutopilotState[campToken] = data;

                const toggleBtn = document.getElementById(`btn-camp-autopilot-toggle-${{campToken}}`);
                const statusBadge = document.getElementById(`camp-autopilot-status-badge-${{campToken}}`);
                const nextRunEl = document.getElementById(`camp-ap-stat-next-run-${{campToken}}`);
                const readyEl = document.getElementById(`camp-ap-stat-ready-${{campToken}}`);

                const isEnabled = data.is_enabled;

                if (toggleBtn) {{
                    if (isEnabled) {{
                        toggleBtn.innerHTML = '⏸ METTI IN PAUSA';
                        toggleBtn.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
                        toggleBtn.style.boxShadow = '0 4px 15px rgba(245,158,11,0.35)';
                    }} else {{
                        toggleBtn.innerHTML = '🟢 ATTIVA PILOTA AUTOMATICO';
                        toggleBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                        toggleBtn.style.boxShadow = '0 4px 15px rgba(16,185,129,0.35)';
                    }}
                }}

                if (statusBadge) {{
                    if (isEnabled) {{
                        statusBadge.innerHTML = '🟢 ATTIVO (CLIPPING &amp; POSTING AUTOMATICI)';
                        statusBadge.style.background = 'rgba(16,185,129,0.2)';
                        statusBadge.style.color = '#10b981';
                        statusBadge.style.borderColor = 'rgba(16,185,129,0.4)';
                    }} else {{
                        statusBadge.innerHTML = '⏸ IN PAUSA';
                        statusBadge.style.background = 'rgba(239,68,68,0.2)';
                        statusBadge.style.color = '#ef4444';
                        statusBadge.style.borderColor = 'rgba(239,68,68,0.4)';
                    }}
                }}

                if (nextRunEl) {{
                    if (!isEnabled) {{
                        nextRunEl.innerText = 'In pausa';
                        nextRunEl.style.color = '#94a3b8';
                    }} else if (data.next_clip) {{
                        const clipName = data.next_clip.generated_clip || data.next_clip.source_video || 'Video';
                        const timeStr = data.next_clip.concept_name || 'Prossimo slot';
                        nextRunEl.innerText = `${{timeStr}} (${{clipName}})`;
                        nextRunEl.style.color = '#38bdf8';
                    }} else {{
                        nextRunEl.innerText = 'Tutti gli slot completati!';
                        nextRunEl.style.color = '#34d399';
                    }}
                }}

                if (readyEl) readyEl.innerText = `${{data.ready_count || 0}} / ${{data.target_count || 3}}`;

                return data;
            }} catch(e) {{
                console.error("Errore fetch stato autopilot campagna:", e);
                return null;
            }}
        }}

        async function toggleCampaignAutopilot(campToken) {{
            const current = currentCampaignAutopilotState[campToken] || {{}};
            const newState = !current.is_enabled;
            try {{
                const res = await fetch('/api/autopilot/campaign-toggle', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken, enable: newState }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    await loadCampaignAutopilotState(campToken);
                    if (newState) {{
                        alert("🤖 Pilota Automatico ATTIVATO per questa campagna!\\n\\nIl bot elaborerà in background il ritaglio (clipping) dei video sorgente mancanti e pubblicherà le clip su TikTok agli orari programmati inviando subito la conferma a Klippify!");
                    }} else {{
                        alert("⏸ Pilota Automatico MESSO IN PAUSA per questa campagna.");
                    }}
                }}
            }} catch(e) {{
                alert("Errore cambio stato pilota automatico: " + e.message);
            }}
        }}

        async function queueAllCampaignSlots(campToken, btnEl) {{
            if (btnEl) {{
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Inserimento in coda...";
            }}
            try {{
                const res = await fetch('/api/autopilot/campaign-queue-slots', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    alert(`✅ Inseriti con successo ${{data.added_count}} slot di questa campagna nella coda del Pilota Automatico!`);
                    await loadCampaignAutopilotState(campToken);
                }}
            }} catch(e) {{
                alert("Errore accodamento: " + e.message);
            }} finally {{
                if (btnEl) {{
                    btnEl.disabled = false;
                    btnEl.innerText = "📋 Accoda Tutti gli Slot all'Autopilota";
                }}
            }}
        }}

        async function runCampaignAutopilotNow(campToken, btnEl) {{
            if (btnEl) {{
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Avvio immediato...";
            }}
            try {{
                const res = await fetch('/api/autopilot/campaign-run-now', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    alert("🚀 Esecuzione avviata! Il bot sta elaborando/pubblicando il prossimo slot di questa campagna.");
                    await loadCampaignAutopilotState(campToken);
                }} else {{
                    alert("Nota: " + (data.message || data.error));
                }}
            }} catch(e) {{
                alert("Errore esecuzione immediata: " + e.message);
            }} finally {{
                if (btnEl) {{
                    btnEl.disabled = false;
                    btnEl.innerText = "⚡ Pubblica Subito Prossimo Slot";
                }}
            }}
        }}

        async function pauseCampaignLifecycle(campToken) {{
            const sel = document.getElementById(`pause-days-select-${{campToken}}`);
            const days = sel ? parseFloat(sel.value) : 1;
            const daysTxt = days === 1 ? "1 giorno (24 ore)" : `${{days}} giorni`;
            if (!confirm(`Sei sicuro di voler mettere in PAUSA questa campagna per ${{daysTxt}}?\\n\\nI video NON verranno pubblicati per tutto l'intervallo specificato. Dal giorno successivo le pubblicazioni riprenderanno in automatico!`)) {{
                return;
            }}
            try {{
                const res = await fetch('/api/autopilot/campaign-pause', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken, days: days }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    alert(`⏸️ Campagna messa in pausa fino al: ${{data.pause_until}}\\n\\nLe pubblicazioni sono sospese e riprenderanno automaticamente al termine.`);
                    window.location.reload();
                }} else {{
                    alert("Errore: " + (data.error || "Impossibile mettere in pausa"));
                }}
            }} catch(e) {{
                alert("Errore di connessione: " + e.message);
            }}
        }}

        async function endCampaignLifecycle(campToken) {{
            if (!confirm("🛑 ATTENZIONE: Sei sicuro di voler TERMINARE DEFINITIVAMENTE questa campagna?\\n\\nLa pubblicazione automatica verrà conclusa e interrotta per sempre.")) {{
                return;
            }}
            try {{
                const res = await fetch('/api/autopilot/campaign-end', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    alert("🛑 Campagna terminata per sempre con successo.");
                    window.location.reload();
                }} else {{
                    alert("Errore: " + (data.error || "Impossibile terminare la campagna"));
                }}
            }} catch(e) {{
                alert("Errore di connessione: " + e.message);
            }}
        }}

        async function resumeCampaignLifecycle(campToken) {{
            try {{
                const res = await fetch('/api/autopilot/campaign-resume', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    alert("▶️ Campagna riattivata con successo! La pubblicazione e il pilota automatico sono di nuovo attivi.");
                    window.location.reload();
                }} else {{
                    alert("Errore: " + (data.error || "Impossibile riattivare la campagna"));
                }}
            }} catch(e) {{
                alert("Errore di connessione: " + e.message);
            }}
        }}

        async function loadDebugTasks(showLoading = false) {{
            const container = document.getElementById('debug-tasks-container');
            if (!container) return;

            try {{
                const res = await fetch('/api/debug/tasks');
                let tasks = await res.json();
                if (!Array.isArray(tasks)) tasks = [];

                // ⚡ RIGOROSO ORDINAMENTO: PRIMA i processi 'running' (in corso), poi per data/orario decrescente
                tasks.sort((a, b) => {{
                    const aRunning = a.status === 'running' ? 1 : 0;
                    const bRunning = b.status === 'running' ? 1 : 0;
                    if (bRunning !== aRunning) return bRunning - aRunning;
                    return (b.start_timestamp || 0) - (a.start_timestamp || 0);
                }});

                let runningCount = 0;
                let stuckCount = 0;
                let completedCount = 0;
                let failedCount = 0;

                tasks.forEach(t => {{
                    if (t.status === 'running') {{
                        runningCount++;
                        if (t.is_stuck_warning) stuckCount++;
                    }} else if (t.status === 'completed') {{
                        completedCount++;
                    }} else {{
                        failedCount++;
                    }}
                }});

                const badge = document.getElementById('debug-active-badge');
                if (badge) {{
                    if (runningCount > 0) {{
                        badge.style.display = 'inline-block';
                        badge.innerText = runningCount;
                        badge.style.background = stuckCount > 0 ? '#f59e0b' : '#10b981';
                    }} else {{
                        badge.style.display = 'none';
                    }}
                }}

                const statRunning = document.getElementById('debug-stat-running');
                const statStuck = document.getElementById('debug-stat-stuck');
                const statComp = document.getElementById('debug-stat-completed');
                const statFail = document.getElementById('debug-stat-failed');

                if (statRunning) statRunning.innerText = runningCount;
                if (statStuck) statStuck.innerText = stuckCount;
                if (statComp) statComp.innerText = completedCount;
                if (statFail) statFail.innerText = failedCount;

                // Aggiorna dinamicamente i rettangoli "⚡ STO PROCESSANDO" nelle campagne aperte
                updateActiveProcessingBoxes(tasks);

                if (tasks.length === 0) {{
                    container.innerHTML = `
                        <div id="debug-tasks-empty-placeholder" style="text-align:center; padding:3.5rem; color:var(--text-muted); background:rgba(0,0,0,0.2); border:1px dashed rgba(255,255,255,0.1); border-radius:1rem;">
                            <div style="font-size:2.5rem; margin-bottom:0.6rem;">⚙️</div>
                            <div style="font-size:1.1rem; font-weight:700; color:#cbd5e1;">Nessun processo registrato</div>
                            <div style="font-size:0.85rem; margin-top:0.4rem; color:var(--text-muted);">Tutti i processi completati sono stati archiviati o puliti.</div>
                        </div>
                    `;
                    return;
                }}

                // Rimuovi l'empty placeholder se presente
                const emptyPlaceholder = document.getElementById('debug-tasks-empty-placeholder');
                if (emptyPlaceholder) {{
                    emptyPlaceholder.remove();
                }}

                // Rimuovi card che non esistono più
                const currentIds = new Set(tasks.map(t => 'debug-card-' + t.id));
                Array.from(container.children).forEach(child => {{
                    if (child.id && child.id.startsWith('debug-card-') && !currentIds.has(child.id)) {{
                        child.remove();
                    }}
                }});

                tasks.forEach((t, index) => {{
                    const isRunning = t.status === 'running';
                    const isStuck = t.is_stuck_warning;
                    
                    let statusBadge = '';
                    let cardBorder = 'rgba(255,255,255,0.08)';
                    let cardBg = 'rgba(15,23,42,0.85)';

                    if (isRunning) {{
                        if (isStuck) {{
                            statusBadge = `<span style="background:rgba(245,158,11,0.2); color:#f59e0b; border:1px solid rgba(245,158,11,0.4); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:800; display:inline-flex; align-items:center; gap:0.4rem;"><span style="width:8px; height:8px; border-radius:50%; background:#f59e0b; display:inline-block; animation:pulse 1s infinite;"></span> ⚠️ LENTO / IN ATTESA (${{t.duration_seconds}}s)</span>`;
                            cardBorder = 'rgba(245,158,11,0.5)';
                        }} else {{
                            statusBadge = `<span style="background:rgba(16,185,129,0.2); color:#10b981; border:1px solid rgba(16,185,129,0.4); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:800; display:inline-flex; align-items:center; gap:0.4rem; box-shadow:0 0 10px rgba(16,185,129,0.3);"><span style="width:8px; height:8px; border-radius:50%; background:#10b981; display:inline-block; animation:pulse 1s infinite;"></span> 🟢 IN ESECUZIONE (${{t.duration_seconds}}s)</span>`;
                            cardBorder = 'rgba(16,185,129,0.4)';
                        }}
                    }} else if (t.status === 'completed') {{
                        statusBadge = `<span style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:700;">✅ COMPLETATO (${{t.duration_seconds}}s)</span>`;
                    }} else if (t.status === 'terminated') {{
                        statusBadge = `<span style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:700;">🛑 TERMINATO DALL'UTENTE</span>`;
                    }} else {{
                        statusBadge = `<span style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); padding:0.3rem 0.7rem; border-radius:1rem; font-size:0.8rem; font-weight:700;">❌ ERRORE (${{t.duration_seconds}}s)</span>`;
                    }}

                    const logsJoined = (t.logs || []).join('\\n') || 'Nessun log registrato.';
                    const pidInfo = t.pid ? `PID: ${{t.pid}}` : 'Thread Interno';

                    let cardEl = document.getElementById('debug-card-' + t.id);
                    if (!cardEl) {{
                        cardEl = document.createElement('div');
                        cardEl.id = 'debug-card-' + t.id;
                        cardEl.className = 'k-panel-card';
                        cardEl.style.background = cardBg;
                        cardEl.style.border = '1px solid ' + cardBorder;
                        cardEl.style.padding = '1.2rem';
                        cardEl.style.borderRadius = '0.8rem';
                        cardEl.style.boxShadow = isRunning ? '0 8px 25px rgba(0,0,0,0.5), 0 0 15px rgba(16,185,129,0.2)' : '0 4px 20px rgba(0,0,0,0.3)';

                        cardEl.innerHTML = `
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.8rem; margin-bottom:0.8rem;">
                                <div>
                                    <div style="font-size:1.05rem; font-weight:800; color:#fff; display:flex; align-items:center; gap:0.5rem;">
                                        <span>${{t.name}}</span>
                                    </div>
                                    <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.3rem; display:flex; gap:1rem; flex-wrap:wrap;">
                                        <span>🕒 Avviato: ${{t.start_time}}</span>
                                        <span id="debug-pid-${{t.id}}">⚡ ${{pidInfo}}</span>
                                        <span>ID: <code style="color:#a78bfa;">${{t.id}}</code></span>
                                    </div>
                                </div>
                                <div style="display:flex; align-items:center; gap:0.8rem;">
                                    <div id="debug-badge-${{t.id}}">${{statusBadge}}</div>
                                    <div id="debug-action-${{t.id}}">
                                        ${{isRunning ? `
                                            <button onclick="killTask('${{t.id}}', this)" style="background:#ef4444; color:#fff; border:none; padding:0.4rem 0.9rem; border-radius:0.4rem; font-size:0.8rem; font-weight:800; cursor:pointer; display:inline-flex; align-items:center; gap:0.3rem; box-shadow:0 2px 8px rgba(239,68,68,0.4); transition:all 0.2s;">
                                                🛑 Termina
                                            </button>
                                        ` : ''}}
                                    </div>
                                </div>
                            </div>

                            <!-- TERMINAL LOG BOX -->
                            <div id="debug-log-${{t.id}}" style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:0.5rem; padding:0.8rem; font-family:'Courier New', Courier, monospace; font-size:0.78rem; color:#a5f3fc; max-height:180px; overflow-y:auto; white-space:pre-wrap; line-height:1.4; box-shadow:inset 0 2px 8px rgba(0,0,0,0.6); scroll-behavior:smooth;"></div>
                        `;
                    }} else {{
                        cardEl.style.border = '1px solid ' + cardBorder;
                        cardEl.style.boxShadow = isRunning ? '0 8px 25px rgba(0,0,0,0.5), 0 0 15px rgba(16,185,129,0.2)' : '0 4px 20px rgba(0,0,0,0.3)';
                        const badgeEl = document.getElementById('debug-badge-' + t.id);
                        if (badgeEl) badgeEl.innerHTML = statusBadge;

                        const actionEl = document.getElementById('debug-action-' + t.id);
                        if (actionEl) {{
                            actionEl.innerHTML = isRunning ? `
                                <button onclick="killTask('${{t.id}}', this)" style="background:#ef4444; color:#fff; border:none; padding:0.4rem 0.9rem; border-radius:0.4rem; font-size:0.8rem; font-weight:800; cursor:pointer; display:inline-flex; align-items:center; gap:0.3rem; box-shadow:0 2px 8px rgba(239,68,68,0.4); transition:all 0.2s;">
                                    🛑 Termina
                                </button>
                            ` : '';
                        }}

                        const pidEl = document.getElementById('debug-pid-' + t.id);
                        if (pidEl) pidEl.innerText = `⚡ ${{pidInfo}}`;
                    }}

                    // Riordinamento dinamico: posiziona l'elemento all'indice esatto per mostrare i running in cima
                    const targetChild = container.children[index];
                    if (targetChild !== cardEl) {{
                        container.insertBefore(cardEl, targetChild || null);
                    }}

                    const logBox = document.getElementById('debug-log-' + t.id);
                    if (logBox) {{
                        const wasScrolledToBottom = (logBox.scrollHeight - logBox.clientHeight <= logBox.scrollTop + 35);
                        if (logBox.innerText !== logsJoined) {{
                            logBox.innerText = logsJoined;
                            if (isRunning || wasScrolledToBottom) {{
                                logBox.scrollTop = logBox.scrollHeight;
                            }}
                        }}
                    }}
                }});

            }} catch (err) {{
                console.error("Errore fetch debug tasks:", err);
            }}
        }}

        async function killTask(taskId, btnEl) {{
            if (!confirm("Vuoi davvero interrompere e terminare forzatamente questo processo?")) return;
            if (btnEl) {{
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Arresto...";
            }}
            try {{
                const res = await fetch('/api/debug/kill', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ task_id: taskId }})
                }});
                const data = await res.json();
                loadDebugTasks();
            }} catch (e) {{
                alert("Errore durante l'interruzione: " + e.message);
                loadDebugTasks();
            }}
        }}

        async function killAllTasks() {{
            if (!confirm("Sei sicuro di voler terminare TUTTI i processi in corso (Gemini bot, upload, ffmpeg)?")) return;
            try {{
                const res = await fetch('/api/debug/kill', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ kill_all: true }})
                }});
                const data = await res.json();
                alert(data.message || "Tutti i processi attivi sono stati interrotti.");
                loadDebugTasks();
            }} catch (e) {{
                alert("Errore durante la terminazione: " + e.message);
            }}
        }}

        async function clearFinishedTasks() {{
            try {{
                await fetch('/api/debug/clear', {{ method: 'POST' }});
                loadDebugTasks();
            }} catch (e) {{
                console.error("Errore pulizia task:", e);
            }}
        }}

        function updateActiveProcessingBoxes(tasks) {{
            document.querySelectorAll('[id^="assembly-active-processing-box-"]').forEach(box => {{
                const cToken = box.id.replace('assembly-active-processing-box-', '');
                const activeUpload = (Array.isArray(tasks) ? tasks : []).find(t => t.status === 'running' && (
                    (t.meta && (t.meta.campaign_id === cToken || t.meta.campaignId === cToken)) ||
                    (t.name && (t.name.includes(cToken) || t.name.toLowerCase().includes('upload tiktok')))
                ));
                if (activeUpload) {{
                    box.style.display = 'block';
                    const titleEl = document.getElementById('processing-clip-title-' + cToken);
                    const fileEl = document.getElementById('processing-clip-filename-' + cToken);
                    const timerEl = document.getElementById('processing-elapsed-timer-' + cToken);
                    if (titleEl) titleEl.innerText = activeUpload.name || "Upload TikTok & Invio Klippify";
                    if (fileEl && activeUpload.meta && activeUpload.meta.filename) fileEl.innerText = activeUpload.meta.filename;
                    if (timerEl) timerEl.innerText = `⏳ In corso (${{activeUpload.duration_seconds || 0}}s)`;
                }} else {{
                    box.style.display = 'none';
                }}
            }});
        }}

        // Periodic background poll for task status, dynamic processing boxes, and badges
        let _lastRunningTasksCount = 0;
        setInterval(() => {{
            fetch('/api/debug/tasks')
                .then(r => r.json())
                .then(tasks => {{
                    if (!Array.isArray(tasks)) tasks = [];
                    const runningCount = tasks.filter(t => t.status === 'running').length;
                    
                    // Aggiorna sempre il rettangolo "⚡ STO PROCESSANDO" in qualunque scheda/campagna
                    updateActiveProcessingBoxes(tasks);
                    
                    // Se un task è appena terminato, ricarica automaticamente la lista video e gli slot
                    if (_lastRunningTasksCount > 0 && runningCount === 0) {{
                        if (typeof fetchAvailableVideosList === 'function') {{
                            fetchAvailableVideosList();
                        }}
                    }}
                    _lastRunningTasksCount = runningCount;

                    const badge = document.getElementById('debug-active-badge');
                    if (badge) {{
                        if (runningCount > 0) {{
                            badge.style.display = 'inline-block';
                            badge.innerText = runningCount;
                        }} else {{
                            badge.style.display = 'none';
                        }}
                    }}

                    if (currentActiveView === 'debug') {{
                        loadDebugTasks(false);
                    }}
                }})
                .catch(() => {{}});

            if (currentActiveView === 'autopilot') {{
                loadAutopilotState(false);
            }} else {{
                fetch('/api/autopilot/status')
                    .then(r => r.json())
                    .then(st => {{
                        const badge = document.getElementById('autopilot-active-badge');
                        if (badge) {{
                            if (st.is_enabled) {{
                                badge.style.display = 'inline-block';
                                badge.innerText = 'ON';
                            }} else {{
                                badge.style.display = 'none';
                            }}
                        }}
                    }})
                    .catch(() => {{}});
            }}
        }}, 3000);

        function getRatingColor(rating) {{
            if (rating === 'ALTA') return '#10b981';
            if (rating === 'MEDIA') return '#f59e0b';
            return '#ef4444';
        }}

        function copyToClipboard(text, btnEl) {{
            navigator.clipboard.writeText(text).then(() => {{
                const orig = btnEl.innerText;
                btnEl.innerText = '✅ Copiato!';
                btnEl.style.background = '#10b981';
                setTimeout(() => {{ btnEl.innerText = orig; btnEl.style.background = ''; }}, 1500);
            }});
        }}

        function toggleAccordion(idx) {{
            const body = document.getElementById('accordion-body-' + idx);
            const icon = document.getElementById('accordion-icon-' + idx);
            if (body.style.display === 'none') {{
                body.style.display = 'block';
                icon.style.transform = 'rotate(180deg)';
            }} else {{
                body.style.display = 'none';
                icon.style.transform = 'rotate(0deg)';
            }}
        }}

        let activeCampaignsClassified = [];

        async function fetchActiveClassifiedCampaigns() {{
            try {{
                const res = await fetch('/api/clipping/classified-active');
                activeCampaignsClassified = await res.json();
                return activeCampaignsClassified;
            }} catch(e) {{
                activeCampaignsClassified = [];
                return [];
            }}
        }}

        async function renderMyCampaigns() {{
            const grid = document.getElementById('my-campaigns-grid');
            grid.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:2rem; grid-column: 1 / -1;">⏳ Caricamento Campagne Attive da Klippify...</div>';

            try {{
                const subRes = await fetch('/api/klippify/submissions');
                if (subRes.ok) {{
                    const freshSubs = await subRes.json();
                    if (Array.isArray(freshSubs) && freshSubs.length > 0) klippifySubmissions = freshSubs;
                }}
            }} catch(e) {{}}

            await fetchActiveClassifiedCampaigns();

            // Raccogli tutti i token delle campagne attive (da iscrizioni Klippify + selezione manuale + submissions)
            const activeTokensSet = new Set();
            
            // 1. Campagne classificate come attive da Klippify
            (activeCampaignsClassified || []).forEach(ac => {{
                const token = ac.id || ac.campaign_token || ac.campaign_id;
                if (token) activeTokensSet.add(token);
            }});

            // 2. Campagne con submission video inviate
            (typeof klippifySubmissions !== 'undefined' ? klippifySubmissions : []).forEach(s => {{
                if (s.campaign_id) activeTokensSet.add(s.campaign_id);
            }});

            // 3. Campagne con contenuti/script generati
            (typeof generatedContent !== 'undefined' ? generatedContent : []).forEach(gc => {{
                if (gc.campaign_id) activeTokensSet.add(gc.campaign_id);
            }});

            // 4. Campagne dalla dashboard participating
            if (typeof dashboardData !== 'undefined' && dashboardData.participating_campaigns) {{
                dashboardData.participating_campaigns.forEach(p => {{
                    const match = allCampaignsData.find(c => (c.name && p.name && c.name.toLowerCase() === p.name.toLowerCase()) || (c.id === p.id));
                    if (match && match.id) activeTokensSet.add(match.id);
                }});
            }}

            // 5. Campagne salvate dall'utente
            (selectedCampaigns || []).forEach(st => activeTokensSet.add(st));

            const activeTokensList = Array.from(activeTokensSet);

            if (activeTokensList.length === 0) {{
                grid.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding:2rem; grid-column: 1 / -1;">Nessuna campagna attiva rilevata su Klippify. Iscriviti a una campagna su Klippify o selezionala dalla Dashboard!</div>';
                return;
            }}

            grid.innerHTML = '';

            // Iterate over active campaigns to build WIDGETS
            activeTokensList.forEach((campToken) => {{
                const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {{}};
                if (!originalCamp.id) return;

                const classifiedInfo = activeCampaignsClassified.find(ac => 
                    ac.id === campToken || 
                    ac.campaign_token === campToken || 
                    ac.campaign_id === campToken ||
                    (originalCamp.name && ac.name && ac.name.toLowerCase() === originalCamp.name.toLowerCase())
                ) || {{}};
                const isClipping = classifiedInfo.category === 'CLIPPING' || 
                                   (classifiedInfo.drive_links && classifiedInfo.drive_links.length > 0) ||
                                   (classifiedInfo.all_links && classifiedInfo.all_links.some(l => l.type === 'drive' || l.type === 'wetransfer' || l.type === 'youtube' || l.type === 'reel')) ||
                                   (originalCamp.description && (
                                       originalCamp.description.toLowerCase().includes('podcast') || 
                                       originalCamp.description.toLowerCase().includes('clip') ||
                                       originalCamp.description.toLowerCase().includes('taglia') ||
                                       originalCamp.description.toLowerCase().includes('youtube') ||
                                       originalCamp.description.toLowerCase().includes('drive')
                                   ));

                const item = generatedContent.find(gc => gc.campaign_id === campToken) || {{}};
                const campSubmissions = (typeof klippifySubmissions !== 'undefined' ? klippifySubmissions : []).filter(s => {{
                    if (s.campaign_id && (s.campaign_id === campToken || s.campaign_id === originalCamp.id || s.campaign_id === originalCamp.campaign_token)) return true;
                    if (originalCamp.name && s.campaign_name && originalCamp.name.trim().toLowerCase() === s.campaign_name.trim().toLowerCase()) return true;
                    return false;
                }});
                
                const widget = document.createElement('div');
                widget.className = 'campaign-widget';
                widget.style.cssText = 'background:rgba(30,41,59,0.9); border:1px solid rgba(255,255,255,0.1); border-radius:1rem; padding:1.5rem; cursor:pointer; transition: transform 0.2s, box-shadow 0.2s; position:relative;';
                
                widget.onmouseover = () => {{
                    widget.style.transform = 'translateY(-5px)';
                    widget.style.boxShadow = '0 10px 25px rgba(0,0,0,0.5)';
                    widget.style.borderColor = isClipping ? 'rgba(245,158,11,0.6)' : 'rgba(139,92,246,0.6)';
                }};
                widget.onmouseout = () => {{
                    widget.style.transform = 'none';
                    widget.style.boxShadow = 'none';
                    widget.style.borderColor = 'rgba(255,255,255,0.1)';
                }};
                
                widget.onclick = () => openCampaignDetail(campToken);

                const typeBadge = isClipping 
                    ? '<span style="background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid rgba(245,158,11,0.4); padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800;">✂️ CLIPPING</span>'
                    : '<span style="background:rgba(139,92,246,0.2); color:#c084fc; border:1px solid rgba(139,92,246,0.4); padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800;">🤖 AI VEO</span>';

                widget.innerHTML = `
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.8rem; gap:0.5rem;">
                        <div style="flex:1;">
                            <div style="font-size:1.15rem; font-weight:800; color:#fff; line-height:1.3; margin-bottom:0.4rem;">${{originalCamp.name}}</div>
                            <div style="display:flex; gap:0.4rem; align-items:center; flex-wrap:wrap;">
                                ${{typeBadge}}
                                <span style="background:rgba(16,185,129,0.15); color:#34d399; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-weight:bold;">$${{originalCamp.payout_per_1k_views || '?'}}/1k</span>
                            </div>
                        </div>
                        <button onclick="deleteCampaign('${{campToken}}', event)" title="Rimuovi da Campagne Attive" style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); border-radius:0.5rem; padding:0.35rem 0.55rem; font-size:0.85rem; cursor:pointer; transition:all 0.2s;" onmouseover="this.style.background='rgba(239,68,68,0.35)'" onmouseout="this.style.background='rgba(239,68,68,0.15)'">
                            🗑️
                        </button>
                    </div>
                    <div style="font-size:0.82rem; color:var(--text-muted); margin-bottom:1rem; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                        ${{originalCamp.description || 'Nessun brief fornito'}}
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.08); padding-top:0.8rem;">
                        <span style="font-size:0.78rem; color:#a78bfa;">⏳ ${{item.scripts ? item.scripts.length : (item.video_prompt_gemini ? 1 : 0)}} Slot/Clip</span>
                        <div style="display:flex; gap:0.35rem; align-items:center;">
                            ${{campSubmissions.filter(s => s.status === 'accepted').length > 0 ? `<span style="font-size:0.72rem; background:rgba(16,185,129,0.2); color:#34d399; padding:0.15rem 0.45rem; border-radius:0.35rem; font-weight:700;">✅ ${{campSubmissions.filter(s => s.status === 'accepted').length}}</span>` : ''}}
                            ${{campSubmissions.filter(s => s.status === 'rejected').length > 0 ? `<span style="font-size:0.72rem; background:rgba(239,68,68,0.25); color:#ef4444; border:1px solid rgba(239,68,68,0.4); padding:0.15rem 0.45rem; border-radius:0.35rem; font-weight:800;">❌ ${{campSubmissions.filter(s => s.status === 'rejected').length}} Rifiutati</span>` : ''}}
                            ${{campSubmissions.length === 0 ? `<span style="font-size:0.72rem; color:var(--text-muted);">0 Inviati</span>` : ''}}
                        </div>
                    </div>
                `;
                grid.appendChild(widget);
            }});
        }}

        // campaignSchedules is declared globally at top
        let localAvailableVideos = [];

        async function openLocalFolder(campToken) {{
            try {{
                const res = await fetch('/api/open-local-folder', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    console.log("Cartella aperta:", data.folder);
                }} else {{
                    alert("Errore apertura cartella: " + (data.error || "Errore sconosciuto"));
                }}
            }} catch(e) {{
                alert("Errore di connessione: " + e.message);
            }}
        }}

        // ============================================================
        // 📡 MULTICHANNEL SOURCE DOWNLOADER (YOUTUBE / TIKTOK / IG / DRIVE)
        // ============================================================
        async function inspectSourceUrl(campToken) {{
            const input = document.getElementById(`source-url-input-${{campToken}}`);
            const resultBox = document.getElementById(`source-inspect-results-${{campToken}}`);
            const btn = document.getElementById(`btn-inspect-source-${{campToken}}`);
            if (!input || !input.value.trim()) {{
                alert("Inserisci un link valido (YouTube, TikTok, Instagram o Drive)!");
                return;
            }}
            const url = input.value.trim();
            if (btn) {{ btn.innerHTML = "⏳ Ispezione..."; btn.disabled = true; }}
            if (resultBox) {{ 
                resultBox.innerHTML = '<div style="text-align:center; padding:1.2rem; color:#38bdf8; font-size:0.85rem;">⏳ Analisi dei metadati video da <code>' + url.substring(0,40) + '...</code> in corso...</div>'; 
                resultBox.style.display = 'block'; 
            }}

            try {{
                const res = await fetch('/api/sources/inspect', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ url: url, limit: 6 }})
                }});
                const data = await res.json();
                if (data.error) {{
                    if (resultBox) resultBox.innerHTML = `<div style="color:#ef4444; padding:0.8rem; background:rgba(239,68,68,0.1); border-radius:0.6rem; font-size:0.82rem;">❌ ${{data.error}}</div>`;
                }} else {{
                    renderInspectedVideos(campToken, data);
                }}
            }} catch(e) {{
                if (resultBox) resultBox.innerHTML = `<div style="color:#ef4444; padding:0.8rem; background:rgba(239,68,68,0.1); border-radius:0.6rem; font-size:0.82rem;">❌ Errore di rete: ${{e.message}}</div>`;
            }} finally {{
                if (btn) {{ btn.innerHTML = "🔍 Ispeziona Video"; btn.disabled = false; }}
            }}
        }}

        function renderInspectedVideos(campToken, data) {{
            const resultBox = document.getElementById(`source-inspect-results-${{campToken}}`);
            if (!resultBox) return;
            const entries = data.entries || [];
            if (!entries.length) {{
                resultBox.innerHTML = '<div style="color:#94a3b8; padding:0.8rem; font-size:0.82rem;">Nessun video trovato in questa fonte.</div>';
                return;
            }}

            const platformBadges = {{
                youtube: '<span style="background:#ef4444; color:#fff; padding:0.15rem 0.45rem; border-radius:0.3rem; font-size:0.65rem; font-weight:800;">YOUTUBE</span>',
                tiktok: '<span style="background:#00f2fe; color:#000; padding:0.15rem 0.45rem; border-radius:0.3rem; font-size:0.65rem; font-weight:800;">TIKTOK</span>',
                instagram: '<span style="background:linear-gradient(45deg,#f09433,#bc1888); color:#fff; padding:0.15rem 0.45rem; border-radius:0.3rem; font-size:0.65rem; font-weight:800;">INSTAGRAM</span>',
                gdrive: '<span style="background:#10b981; color:#fff; padding:0.15rem 0.45rem; border-radius:0.3rem; font-size:0.65rem; font-weight:800;">DRIVE</span>'
            }};

            let cardsHtml = entries.map(item => {{
                const badge = platformBadges[item.platform] || `<span style="background:#64748b; color:#fff; padding:0.15rem 0.45rem; border-radius:0.3rem; font-size:0.65rem; font-weight:800;">${{(item.platform || 'WEB').toUpperCase()}}</span>`;
                const thumb = item.thumbnail ? `<img src="${{item.thumbnail}}" style="width:90px; height:55px; object-fit:cover; border-radius:0.4rem; border:1px solid rgba(255,255,255,0.1);">` : '<div style="width:90px; height:55px; background:#1e293b; border-radius:0.4rem; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">🎬</div>';
                const dlBtn = item.already_downloaded 
                    ? '<span style="background:rgba(16,185,129,0.2); color:#10b981; padding:0.35rem 0.7rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700; display:inline-block;">✅ Già Scaricato</span>'
                    : `<button onclick="downloadSourceVideoFromUI('${{campToken}}', '${{encodeURIComponent(item.url)}}', '${{encodeURIComponent(item.title)}}')" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; font-weight:800; border:none; padding:0.45rem 0.85rem; border-radius:0.5rem; font-size:0.78rem; cursor:pointer; display:flex; align-items:center; gap:0.3rem; box-shadow:0 2px 8px rgba(16,185,129,0.3); transition:transform 0.15s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='none'">📥 Scarica &amp; Clippa</button>`;

                return `
                    <div style="display:flex; align-items:center; justify-content:space-between; background:rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.08); border-radius:0.6rem; padding:0.7rem; gap:0.8rem; flex-wrap:wrap;">
                        <div style="display:flex; align-items:center; gap:0.8rem; min-width:0; flex:1;">
                            ${{thumb}}
                            <div style="min-width:0; flex:1;">
                                <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.2rem; flex-wrap:wrap;">
                                    ${{badge}}
                                    <span style="color:#94a3b8; font-size:0.72rem;">⏱️ ${{item.duration_str}} &bull; 👁️ ${{(item.view_count || 0).toLocaleString()}} views</span>
                                </div>
                                <div style="font-size:0.82rem; font-weight:700; color:#f8fafc; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${{item.title}}">${{item.title}}</div>
                            </div>
                        </div>
                        <div>
                            ${{dlBtn}}
                        </div>
                    </div>
                `;
            }}).join('');

            resultBox.innerHTML = `
                <div style="margin-top:0.8rem; display:flex; flex-direction:column; gap:0.5rem;">
                    <div style="font-size:0.82rem; color:#38bdf8; font-weight:800; margin-bottom:0.2rem;">✨ Risultati trovati per: <em>${{data.channel_title || 'Fonte'}}</em> (${{entries.length}} video)</div>
                    ${{cardsHtml}}
                </div>
            `;
        }}

        async function downloadSourceVideoFromUI(campToken, encodedUrl, encodedTitle) {{
            const url = decodeURIComponent(encodedUrl);
            const title = decodeURIComponent(encodedTitle);
            try {{
                const res = await fetch('/api/sources/download', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ url: url, campaign_id: campToken, title: title }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    showToast(`📥 Download avviato per "${{title.substring(0,25)}}..."! Verrà clippato in automatico con Gemini.`);
                    setTimeout(() => {{
                        loadClippingQueue(campToken);
                        fetchAvailableVideosList(campToken);
                    }}, 2000);
                }} else {{
                    alert("Errore download: " + data.error);
                }}
            }} catch(e) {{
                alert("Errore di rete: " + e.message);
            }}
        }}

        async function saveCampaignSourceFromUI(campToken) {{
            const input = document.getElementById(`source-url-input-${{campToken}}`);
            if (!input || !input.value.trim()) {{
                alert("Inserisci un link prima di salvare!");
                return;
            }}
            const url = input.value.trim();
            try {{
                const res = await fetch('/api/sources/save-campaign-source', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken, url: url, auto_download: true }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    showToast("✅ Fonte salvata con successo per il monitoraggio 24/7!");
                    loadCampaignSourcesFromUI(campToken);
                }} else {{
                    alert("Errore salvataggio fonte: " + (data.message || data.error));
                }}
            }} catch(e) {{
                alert("Errore di rete: " + e.message);
            }}
        }}

        async function loadCampaignSourcesFromUI(campToken) {{
            const container = document.getElementById(`saved-campaign-sources-${{campToken}}`);
            if (!container) return;
            try {{
                const res = await fetch('/api/sources/get-campaign-sources');
                const allSources = await res.json();
                const campSources = allSources[campToken] || {{ sources: [] }};
                const list = campSources.sources || [];
                if (!list.length) {{
                    container.innerHTML = '<span style="color:#64748b; font-size:0.75rem;">Nessun canale o link salvato per il monitoraggio continuo.</span>';
                    return;
                }}
                container.innerHTML = list.map(sUrl => `
                    <span style="display:inline-flex; align-items:center; gap:0.4rem; background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); padding:0.25rem 0.6rem; border-radius:0.5rem; font-size:0.75rem;">
                        <span>🔗 ${{sUrl.length > 35 ? sUrl.substring(0, 35) + '...' : sUrl}}</span>
                        <button onclick="removeCampaignSourceFromUI('${{campToken}}', '${{encodeURIComponent(sUrl)}}')" style="background:none; border:none; color:#ef4444; cursor:pointer; font-weight:800; padding:0 0.2rem;" title="Rimuovi">&times;</button>
                    </span>
                `).join(' ');
            }} catch(e) {{
                console.log("Errore caricamento fonti:", e);
            }}
        }}

        async function removeCampaignSourceFromUI(campToken, encUrl) {{
            const url = decodeURIComponent(encUrl);
            try {{
                await fetch('/api/sources/remove-campaign-source', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken, url: url }})
                }});
                showToast("🗑️ Fonte rimossa.");
                loadCampaignSourcesFromUI(campToken);
            }} catch(e) {{
                alert("Errore rimozione: " + e.message);
            }}
        }}

        // ============================================================
        // ✂️ MULTI-VIDEO SOURCE UPLOAD & CLIPPING QUEUE ENGINE
        // ============================================================
        let clippingQueuePollTimers = {{}};
        let clippingQueueWasProcessing = {{}};

        async function uploadSourceVideoFiles(inputElem, campToken) {{
            const files = Array.from(inputElem.files || []);
            if (!files.length) return;

            const btnElem = document.getElementById(`btn-upload-file-assembly-${{campToken}}`) || document.getElementById(`btn-upload-file-${{campToken}}`);
            let origHtml = "";
            if (btnElem) {{
                origHtml = btnElem.innerHTML;
                btnElem.disabled = true;
            }}

            let successCount = 0;
            let totalFiles = files.length;

            for (let i = 0; i < totalFiles; i++) {{
                const file = files[i];
                if (btnElem) {{
                    btnElem.innerHTML = `⏳ Caricamento ${{i+1}}/${{totalFiles}} (${{file.name.substring(0, 18)}}...)...`;
                }}

                try {{
                    const res = await fetch('/api/clipping/upload-source', {{
                        method: 'POST',
                        headers: {{
                            'X-Filename': encodeURIComponent(file.name),
                            'X-Campaign-Id': campToken
                        }},
                        body: file
                    }});
                    const data = await res.json();
                    if (data.status === 'ok') {{
                        successCount++;
                    }} else {{
                        console.error("Errore upload file:", file.name, data.error);
                    }}
                }} catch(e) {{
                    console.error("Errore rete upload:", file.name, e);
                }}
            }}

            if (btnElem) {{
                btnElem.innerHTML = origHtml;
                btnElem.disabled = false;
            }}
            inputElem.value = "";

            if (successCount > 0) {{
                await fetchAvailableVideosList(campToken);
                await loadClippingQueue(campToken);
                renderCampaignDetailContent(campToken);
            }} else {{
                alert("Errore durante il caricamento dei video. Riprova.");
            }}
        }}

        async function loadClippingQueue(campToken) {{
            if (!campToken) return;
            loadCampaignSourcesFromUI(campToken);
            const container = document.getElementById(`clipping-queue-list-${{campToken}}`);
            const assemblyContainer = document.getElementById(`assembly-clipping-queue-list-${{campToken}}`);
            const countBadge = document.getElementById(`clipping-queue-count-${{campToken}}`);
            const assemblyCountBadge = document.getElementById(`assembly-clipping-queue-count-${{campToken}}`);
            const statusSummary = document.getElementById(`clipping-queue-summary-${{campToken}}`);
            const assemblyStatusSummary = document.getElementById(`assembly-clipping-queue-summary-${{campToken}}`);
            const liveBanner = document.getElementById(`assembly-clipping-live-banner-${{campToken}}`);
            const tabRawBtn = document.getElementById(`camp-subnav-btn-raw-${{campToken}}`);
            
            try {{
                const res = await fetch(`/api/clipping/queue?campaign_id=${{encodeURIComponent(campToken)}}`);
                const queue = await res.json();
                
                if (countBadge) countBadge.innerText = `${{queue.length}} Video`;
                if (assemblyCountBadge) assemblyCountBadge.innerText = `${{queue.length}} Video`;

                if (statusSummary || assemblyStatusSummary) {{
                    const queuedCount = queue.filter(q => q.status === 'queued').length;
                    const processingCount = queue.filter(q => q.status === 'processing').length;
                    const completedCount = queue.filter(q => q.status === 'completed').length;
                    const summaryHtml = `
                        <span style="color:#fbbf24; font-weight:700;">⏳ ${{queuedCount}} in attesa</span> &bull; 
                        <span style="color:#38bdf8; font-weight:700;">⚙️ ${{processingCount}} in elaborazione</span> &bull; 
                        <span style="color:#34d399; font-weight:700;">✅ ${{completedCount}} completati</span>
                    `;
                    if (statusSummary) statusSummary.innerHTML = summaryHtml;
                    if (assemblyStatusSummary) assemblyStatusSummary.innerHTML = summaryHtml;
                }}

                const emptyHtml = `
                    <div style="text-align:center; padding:2rem 1rem; color:var(--text-muted); background:rgba(0,0,0,0.25); border-radius:0.8rem; border:1px dashed rgba(255,255,255,0.15);">
                        <div style="font-size:1.8rem; margin-bottom:0.4rem;">🎬</div>
                        <div style="font-weight:700; color:#cbd5e1; font-size:0.95rem;">Nessun video presente nella coda di clipping</div>
                        <div style="font-size:0.8rem; margin-top:0.3rem;">Clicca sul pulsante <strong>📁 Carica Video Lunghi</strong> sopra per aggiungere i file completi del brand.</div>
                    </div>
                `;

                if (!queue || queue.length === 0) {{
                    if (container) container.innerHTML = emptyHtml;
                    if (assemblyContainer) assemblyContainer.innerHTML = emptyHtml;
                    if (liveBanner) liveBanner.style.display = 'none';
                    if (tabRawBtn) tabRawBtn.innerHTML = '<span>📁</span> <span>Materia Prima &amp; Taglio</span>';
                    return;
                }}

                const processingItems = queue.filter(q => q.status === 'processing');
                const pendingItems = queue.filter(q => q.status !== 'completed' && q.status !== 'processing');
                const completedItems = queue.filter(q => q.status === 'completed');

                let hasProcessing = processingItems.length > 0;
                let processingFilename = hasProcessing ? processingItems[0].filename : '';

                let htmlOutput = '';

                // 1. BOX DINAMICO: STO KLIPPANDO CON GEMINI (Solo se un video è in elaborazione)
                if (hasProcessing) {{
                    const procItem = processingItems[0];
                    htmlOutput += `
                        <div style="background: linear-gradient(135deg, rgba(8,145,178,0.25), rgba(15,23,42,0.95)); border:2px solid #38bdf8; border-radius:1.1rem; padding:1.2rem 1.4rem; margin-bottom:1.1rem; box-shadow:0 0 25px rgba(56,189,248,0.35);">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; margin-bottom:0.8rem;">
                                <div style="display:flex; align-items:center; gap:0.6rem;">
                                    <span class="live-dot" style="background:#38bdf8; width:10px; height:10px; border-radius:50%; display:inline-block; animation:pulse 1s infinite;"></span>
                                    <span style="font-weight:900; color:#38bdf8; font-size:0.85rem; letter-spacing:0.05em; text-transform:uppercase;">⚡ STO KLIPPANDO CON GEMINI AI</span>
                                </div>
                                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; border:1px solid rgba(56,189,248,0.4); padding:0.2rem 0.65rem; border-radius:1rem; font-size:0.75rem; font-weight:800;">
                                    Analisi &amp; Ritaglio Continuo...
                                </span>
                            </div>
                            <div style="display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
                                <div style="font-size:1.8rem; background:rgba(56,189,248,0.15); width:48px; height:48px; border-radius:0.7rem; display:flex; align-items:center; justify-content:center; flex-shrink:0;">🎬</div>
                                <div style="flex:1; min-width:220px;">
                                    <div style="font-weight:900; font-size:1.05rem; color:#fff; word-break:break-all;">${{procItem.filename}}</div>
                                    <div style="font-size:0.78rem; color:#cbd5e1; margin-top:0.2rem;">
                                        Dimensione: <strong>${{(procItem.file_size_mb || 0).toFixed(1)}} MB</strong> &bull; Caricato: ${{procItem.uploaded_at || 'oggi'}}
                                    </div>
                                </div>
                            </div>
                            <div style="margin-top:0.9rem;">
                                <div style="font-size:0.78rem; color:#94a3b8; margin-bottom:0.4rem; display:flex; justify-content:space-between;">
                                    <span>🤖 Gemini sta estraendo le clip virali 9:16 con didascalie dedicate...</span>
                                    <span style="color:#38bdf8; font-weight:700;">Appena completato scorrerà in archivio e passerà al prossimo!</span>
                                </div>
                                <div class="processing-animated-bar" style="height:7px; background:rgba(255,255,255,0.1); border-radius:4px; overflow:hidden;">
                                    <div class="processing-bar-fill" style="height:100%; width:100%; background:linear-gradient(90deg, #38bdf8, #818cf8, #38bdf8); animation:shimmer 2s infinite linear;"></div>
                                </div>
                            </div>
                        </div>
                    `;
                }}

                // 2. HERO CARD: 1° VIDEO IN CODA (Prossimo al Taglio)
                if (pendingItems.length > 0) {{
                    const heroItem = pendingItems[0];
                    const isErr = heroItem.status === 'error';
                    htmlOutput += `
                        <div style="background: linear-gradient(135deg, rgba(245,158,11,0.14), rgba(15,23,42,0.92)); border:2px solid rgba(245,158,11,0.6); border-radius:1.1rem; padding:1.2rem 1.4rem; margin-bottom:1rem; box-shadow:0 4px 20px rgba(245,158,11,0.15);">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; margin-bottom:0.8rem;">
                                <span style="background:rgba(245,158,11,0.25); color:#fbbf24; border:1px solid rgba(245,158,11,0.5); padding:0.25rem 0.75rem; border-radius:1rem; font-size:0.8rem; font-weight:900; display:flex; align-items:center; gap:0.35rem;">
                                    <span>🌟 1° IN CODA</span> <span>(Prossimo al Taglio)</span>
                                </span>
                                <span style="color:#94a3b8; font-size:0.75rem;">Caricato: ${{heroItem.uploaded_at || 'oggi'}}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                                <div style="display:flex; align-items:center; gap:0.9rem; flex:1; min-width:240px;">
                                    <div style="width:44px; height:44px; border-radius:0.6rem; background:rgba(245,158,11,0.2); display:flex; align-items:center; justify-content:center; font-size:1.5rem; flex-shrink:0;">
                                        🎬
                                    </div>
                                    <div>
                                        <div style="font-weight:900; font-size:1rem; color:#fff; word-break:break-all;">
                                            ${{heroItem.filename}}
                                        </div>
                                        <div style="font-size:0.78rem; color:#94a3b8; margin-top:0.2rem;">
                                            Dimensione: <strong style="color:#fbbf24;">${{(heroItem.file_size_mb || 0).toFixed(1)}} MB</strong>
                                            ${{isErr ? `<span style="color:#ef4444; margin-left:0.5rem; font-weight:700;">⚠️ ${{heroItem.error_message || 'Errore precedente'}}</span>` : ''}}
                                        </div>
                                    </div>
                                </div>
                                <div style="display:flex; align-items:center; gap:0.4rem; flex-wrap:wrap;">
                                    <button onclick="clipSingleVideoFromQueue('${{campToken}}', '${{encodeURIComponent(heroItem.filename)}}', this)" style="background:linear-gradient(135deg, #f59e0b, #d97706); color:#000; font-weight:800; border:none; padding:0.35rem 0.8rem; border-radius:0.5rem; font-size:0.75rem; cursor:pointer; display:inline-flex; align-items:center; gap:0.35rem; box-shadow:0 2px 8px rgba(245,158,11,0.3); transition:all 0.15s;" onmouseover="this.style.transform='translateY(-1px)'" onmouseout="this.style.transform='none'">
                                        <span>⚡ Klippa Subito</span>
                                    </button>
                                    <button onclick="removeVideoFromClippingQueue('${{campToken}}', '${{encodeURIComponent(heroItem.filename)}}', this)" style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); padding:0.35rem 0.6rem; border-radius:0.5rem; font-size:0.75rem; cursor:pointer;" title="Rimuovi dalla coda">
                                        🗑️
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                }}

                // 3. STRISCE COMPATTE IN RISERVA (#2, #3, #4...)
                if (pendingItems.length > 1) {{
                    const reserveItems = pendingItems.slice(1);
                    htmlOutput += `
                        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.08); border-radius:1rem; padding:1.1rem; margin-bottom:1rem;">
                            <div style="font-size:0.88rem; font-weight:800; color:#38bdf8; margin-bottom:0.7rem; display:flex; justify-content:space-between; align-items:center;">
                                <span>📦 Video Lunghi Successivi in Coda (${{reserveItems.length}} in attesa)</span>
                                <span style="font-size:0.74rem; color:#94a3b8; font-weight:500;">Scorreranno automaticamente verso l'alto finché non sono finiti</span>
                            </div>
                            <div style="display:flex; flex-direction:column; gap:0.5rem;">
                                ${{reserveItems.map((qItem, rIdx) => `
                                    <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.06); border-radius:0.6rem; padding:0.65rem 0.9rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; transition:all 0.2s;" onmouseover="this.style.borderColor='rgba(56,189,248,0.3)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.06)'">
                                        <div style="display:flex; align-items:center; gap:0.7rem;">
                                            <span style="font-weight:900; color:#94a3b8; font-size:0.82rem; font-family:monospace; min-width:24px;">#${{rIdx + 2}}</span>
                                            <span style="font-weight:700; color:#e2e8f0; font-size:0.85rem; word-break:break-all;">${{qItem.filename}}</span>
                                            <span style="font-size:0.72rem; color:#64748b;">(${{(qItem.file_size_mb || 0).toFixed(1)}} MB)</span>
                                        </div>
                                        <div style="display:flex; align-items:center; gap:0.4rem;">
                                            <button onclick="clipSingleVideoFromQueue('${{campToken}}', '${{encodeURIComponent(qItem.filename)}}', this)" style="background:rgba(245,158,11,0.15); color:#fbbf24; border:1px solid rgba(245,158,11,0.3); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.74rem; font-weight:800; cursor:pointer;">
                                                ⚡ Klippa
                                            </button>
                                            <button onclick="removeVideoFromClippingQueue('${{campToken}}', '${{encodeURIComponent(qItem.filename)}}', this)" style="background:transparent; color:#ef4444; border:none; padding:0.25rem 0.4rem; cursor:pointer;" title="Rimuovi">
                                                🗑️
                                            </button>
                                        </div>
                                    </div>
                                `).join('')}}
                            </div>
                        </div>
                    `;
                }}

                // Se non c'è nulla in attesa o in elaborazione
                if (!hasProcessing && pendingItems.length === 0 && completedItems.length === 0) {{
                    htmlOutput = emptyHtml;
                }}

                // 4. ARCHIVIO A TENDINA: VIDEO LUNGHI GIÀ ELABORATI
                if (completedItems.length > 0) {{
                    htmlOutput += `
                        <details style="margin-top:1.2rem; background:rgba(15,23,42,0.5); border:1px solid rgba(16,185,129,0.25); border-radius:0.9rem; overflow:hidden;">
                            <summary style="padding:0.9rem 1.2rem; cursor:pointer; font-weight:800; color:#34d399; font-size:0.9rem; display:flex; align-items:center; justify-content:space-between; user-select:none;">
                                <span style="display:flex; align-items:center; gap:0.5rem;">
                                    <span>✅ Video Lunghi Già Elaborati (${{completedItems.length}})</span>
                                    <span style="font-size:0.74rem; color:#94a3b8; font-weight:500;">(Clicca per espandere e vedere le clip generate)</span>
                                </span>
                                <span style="font-size:0.75rem; background:rgba(16,185,129,0.15); color:#34d399; padding:0.2rem 0.6rem; border-radius:1rem; border:1px solid rgba(16,185,129,0.3);">
                                    Archiviati
                                </span>
                            </summary>
                            <div style="padding:0.8rem 1.2rem 1.2rem; display:flex; flex-direction:column; gap:0.6rem; border-top:1px solid rgba(255,255,255,0.06);">
                                ${{completedItems.map(cItem => `
                                    <div style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.06); border-radius:0.7rem; padding:0.8rem 1rem;">
                                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
                                            <div style="font-weight:700; color:#e2e8f0; font-size:0.85rem;">
                                                🎬 ${{cItem.filename}} <span style="font-size:0.72rem; color:#64748b;">(${{(cItem.file_size_mb || 0).toFixed(1)}} MB)</span>
                                            </div>
                                            <div style="display:flex; gap:0.4rem; align-items:center;">
                                                <span style="font-size:0.72rem; color:#34d399; font-weight:700;">✅ ${{(cItem.generated_clips || []).length}} clip estratte</span>
                                                <button onclick="clipSingleVideoFromQueue('${{campToken}}', '${{encodeURIComponent(cItem.filename)}}', this)" style="background:rgba(245,158,11,0.15); color:#fbbf24; border:1px solid rgba(245,158,11,0.3); padding:0.2rem 0.5rem; border-radius:0.3rem; font-size:0.7rem; font-weight:700; cursor:pointer;">
                                                    Ri-Klippa
                                                </button>
                                                <button onclick="removeVideoFromClippingQueue('${{campToken}}', '${{encodeURIComponent(cItem.filename)}}', this)" style="background:transparent; color:#ef4444; border:none; padding:0.2rem 0.3rem; cursor:pointer;" title="Elimina">
                                                    🗑️
                                                </button>
                                            </div>
                                        </div>
                                        ${{cItem.generated_clips && cItem.generated_clips.length > 0 ? `
                                            <div style="margin-top:0.5rem; display:flex; flex-wrap:wrap; gap:0.4rem;">
                                                ${{cItem.generated_clips.map(clipF => `
                                                    <span style="background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.25); color:#34d399; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-family:monospace; display:inline-flex; align-items:center; gap:0.3rem;">
                                                        <span>✂️</span> <span>${{clipF}}</span>
                                                    </span>
                                                `).join('')}}
                                            </div>
                                        ` : ''}}
                                    </div>
                                `).join('')}}
                            </div>
                        </details>
                    `;
                }}

                if (container) container.innerHTML = htmlOutput;
                if (assemblyContainer) assemblyContainer.innerHTML = htmlOutput;

                // Gestione Badge Live e Polling dinamico
                if (hasProcessing) {{
                    clippingQueueWasProcessing[campToken] = true;
                    if (liveBanner) {{
                        liveBanner.style.display = 'flex';
                        liveBanner.innerHTML = `<span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#38bdf8; animation:pulse 1s infinite;"></span> <span>⚙️ <strong>Analisi &amp; Taglio in corso con Gemini...</strong> Ritaglio delle migliori clip 9:16 per <em>${{processingFilename}}</em> in corso. Entreranno in automatico nella cascata!</span>`;
                    }}
                    if (tabRawBtn) {{
                        tabRawBtn.innerHTML = '<span>📁</span> <span>Materia Prima &amp; Taglio</span> <span style="background:rgba(56,189,248,0.25); color:#38bdf8; border:1px solid rgba(56,189,248,0.5); font-size:0.68rem; padding:0.1rem 0.45rem; border-radius:1rem; font-weight:900; animation:pulse 1.2s infinite;">⚙️ IN CORSO</span>';
                    }}

                    if (clippingQueuePollTimers[campToken]) clearTimeout(clippingQueuePollTimers[campToken]);
                    clippingQueuePollTimers[campToken] = setTimeout(() => {{
                        loadClippingQueue(campToken);
                    }}, 3000);
                }} else {{
                    if (liveBanner) liveBanner.style.display = 'none';
                    if (tabRawBtn) tabRawBtn.innerHTML = '<span>📁</span> <span>Materia Prima &amp; Taglio</span>';

                    // Se ci sono video in attesa e nessuno in elaborazione, avvia subito il clipping automatico
                    if (pendingItems.length > 0) {{
                        fetch('/api/clipping/queue/process-all', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ campaign_id: campToken }})
                        }}).catch(() => {{}});
                    }}

                    // Se il task è appena terminato (da processing a done), aggiorniamo la cascata
                    if (clippingQueueWasProcessing[campToken]) {{
                        clippingQueueWasProcessing[campToken] = false;
                        fetchAvailableVideosList(campToken).then(() => {{
                            renderCampaignDetailContent(campToken);
                        }});
                    }}
                }}

            }} catch(e) {{
                console.error("Errore caricamento coda clipping:", e);
            }}
        }}

        async function processEntireClippingQueue(campToken, btnElem) {{
            const origHtml = btnElem ? btnElem.innerHTML : "";
            if (btnElem) {{
                btnElem.innerHTML = '⏳ Avvio Coda...';
                btnElem.disabled = true;
            }}

            try {{
                const res = await fetch('/api/clipping/queue/process-all', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    alert(`🚀 Elaborazione Coda Avviata!\n\nIl Bot Gemini e FFmpeg analizzeranno e ritaglieranno in sequenza tutti i video presenti nella coda per questa campagna.\n\nLe clip generate verranno assegnate automaticamente agli slot e rese pronte per la pubblicazione!`);
                    await loadClippingQueue(campToken);
                }} else {{
                    alert("Errore avvio coda: " + (data.error || "Errore sconosciuto"));
                }}
            }} catch(e) {{
                alert("Errore di connessione: " + e.message);
            }} finally {{
                if (btnElem) {{
                    btnElem.innerHTML = origHtml;
                    btnElem.disabled = false;
                }}
            }}
        }}

        async function clipSingleVideoFromQueue(campToken, encFilename, btnElem) {{
            const filename = decodeURIComponent(encFilename);
            const origHtml = btnElem ? btnElem.innerHTML : "";
            if (btnElem) {{
                btnElem.innerHTML = '⏳ In avvio...';
                btnElem.disabled = true;
            }}

            try {{
                const res = await fetch('/api/clipping/run-pipeline', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        campaign_id: campToken,
                        video_name: filename
                    }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    await loadClippingQueue(campToken);
                }} else {{
                    alert("Errore avvio clipping: " + (data.error || "Errore sconosciuto"));
                    if (btnElem) {{
                        btnElem.innerHTML = origHtml;
                        btnElem.disabled = false;
                    }}
                }}
            }} catch(e) {{
                alert("Errore di connessione: " + e.message);
                if (btnElem) {{
                    btnElem.innerHTML = origHtml;
                    btnElem.disabled = false;
                }}
            }}
        }}

        async function removeVideoFromClippingQueue(campToken, encFilename, btnElem) {{
            const filename = decodeURIComponent(encFilename);
            if (!confirm(`Sei sicuro di voler rimuovere "${{filename}}" dalla coda di clipping?`)) return;

            try {{
                const res = await fetch('/api/clipping/queue/remove', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        campaign_id: campToken,
                        filename: filename
                    }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    await loadClippingQueue(campToken);
                }} else {{
                    alert("Errore rimozione video: " + (data.error || "Errore sconosciuto"));
                }}
            }} catch(e) {{
                alert("Errore di rete: " + e.message);
            }}
        }}

        async function startClippingPipelineForCampaign(campToken, btnElem) {{
            const selector = document.getElementById(`source-video-selector-assembly-${{campToken}}`) || document.getElementById(`source-video-selector-${{campToken}}`);
            const selectedVideo = selector ? selector.value : "";
            if (!selectedVideo) {{
                alert("Seleziona prima un file video sorgente da klippare!");
                return;
            }}
            return clipSingleVideoFromQueue(campToken, encodeURIComponent(selectedVideo), btnElem);
        }}

        function getCampaignIsolatedVideos(campToken) {{
            const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {{}};
            const campNameLower = (originalCamp.name || '').toLowerCase();
            const campShortName = campNameLower.replace(/[^a-zA-Z0-9]/g, '').substring(0, 8);

            return (localAvailableVideos || []).filter(v => {{
                if (!v || !v.filename) return false;
                const fn = v.filename.toLowerCase();
                
                // 1. Se il video ha campaign_id esplicito dal server
                if (v.campaign_id && v.campaign_id !== 'general') {{
                    return v.campaign_id === campToken;
                }}
                
                // 2. Se l'URL relativo contiene il token
                if (v.rel_url && v.rel_url.includes(campToken)) return true;
                
                // 3. Regole di esclusione incrociata tra brand noti
                const isSaraCamp = (campToken === '6a71c6f7245627c68999eae2' || campNameLower.includes('dizdari') || campNameLower.includes('sara'));
                const isDoseCamp = (campToken === '6a426231e6a21896f769dc80' || campNameLower.includes('dose') || campNameLower.includes('riccardo'));
                const isStarkCamp = (campToken === '6a759fd05ade3cb2f771b439' || campNameLower.includes('stark') || campNameLower.includes('ale'));

                const isSaraFile = (fn.includes('saradizdari') || fn.includes('sara') || fn.includes('zaharia') || fn.includes('amoroso') || fn.includes('fedra'));
                const isDoseFile = (fn.includes('dose') || fn.includes('riccardo'));
                const isStarkFile = (fn.includes('stark') || fn.includes('alestark'));

                if (isSaraFile) return isSaraCamp;
                if (isDoseFile) return isDoseCamp;
                if (isStarkFile) return isStarkCamp;

                // 4. Se il nome del file include il token o il nome compatto della campagna
                if (campShortName && fn.includes(campShortName)) return true;
                if (campToken && fn.includes(campToken.toLowerCase())) return true;

                // Se non c'è match, escludi per sicurezza
                return false;
            }});
        }}

        async function fetchAvailableVideosList(campToken = null) {{
            try {{
                const url = campToken ? `/api/videos?campaign_id=${{encodeURIComponent(campToken)}}` : '/api/videos';
                const res = await fetch(url);
                const vids = await res.json();
                localAvailableVideos = vids || [];
                return localAvailableVideos;
            }} catch(e) {{
                return [];
            }}
        }}

        async function openCampaignDetail(campToken) {{
            currentDetailCampToken = campToken;
            document.getElementById('my-campaigns-grid').style.display = 'none';
            document.getElementById('my-campaign-detail-view').style.display = 'block';
            
            const detailContainer = document.getElementById('my-campaign-detail-content');
            detailContainer.innerHTML = '<div style="text-align:center; padding:3rem; color:var(--text-muted);">⏳ Caricamento Piano Editoriale...</div>';

            try {{
                const subRes = await fetch('/api/klippify/submissions');
                if (subRes.ok) {{
                    const freshSubs = await subRes.json();
                    if (Array.isArray(freshSubs) && freshSubs.length > 0) klippifySubmissions = freshSubs;
                }}
            }} catch(e) {{}}

            await fetchAvailableVideosList(campToken);

            try {{
                const schedRes = await fetch('/api/campaign/schedules');
                campaignSchedules = await schedRes.json();
            }} catch(e) {{
                campaignSchedules = {{}};
            }}

            renderCampaignDetailContent(campToken);
        }}

        async function refreshCampaignSubmissions(campToken, btnEl) {{
            if (btnEl) {{
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Controllo...";
            }}
            try {{
                const subRes = await fetch('/api/klippify/submissions');
                if (subRes.ok) {{
                    const freshSubs = await subRes.json();
                    if (Array.isArray(freshSubs) && freshSubs.length > 0) klippifySubmissions = freshSubs;
                }}
                renderCampaignDetailContent(campToken);
            }} catch(e) {{
                console.error("Errore aggiornamento submissions:", e);
            }} finally {{
                if (btnEl) {{
                    btnEl.disabled = false;
                    btnEl.innerText = "🔄 Aggiorna Stato Klippify";
                }}
            }}
        }}

        async function changeDailyTargetCount(campToken, delta) {{
            if (!campaignSchedules[campToken]) {{
                campaignSchedules[campToken] = {{ target_count: 3, slots: [] }};
            }}
            let current = campaignSchedules[campToken].target_count || 3;
            let next = Math.max(1, Math.min(10, current + delta));
            campaignSchedules[campToken].target_count = next;
            
            await saveCurrentCampaignSchedule(campToken);
            renderCampaignDetailContent(campToken);
        }}

        function showToast(message, type = 'success') {{
            let toast = document.getElementById('global-toast-notification');
            if (!toast) {{
                toast = document.createElement('div');
                toast.id = 'global-toast-notification';
                toast.style.cssText = 'position:fixed; bottom:25px; right:25px; z-index:99999; background:linear-gradient(135deg, #065f46 0%, #047857 100%); color:#fff; padding:0.85rem 1.4rem; border-radius:0.85rem; font-weight:800; font-size:0.9rem; box-shadow:0 10px 25px rgba(0,0,0,0.6), 0 0 20px rgba(16,185,129,0.4); border:1.5px solid #34d399; transition:opacity 0.3s, transform 0.3s; opacity:0; pointer-events:none;';
                document.body.appendChild(toast);
            }}
            toast.innerText = message;
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
            clearTimeout(toast._timeout);
            toast._timeout = setTimeout(() => {{
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(10px)';
            }}, 3000);
        }}

        async function saveCampaignSlotTime(campToken, slotIdx, timeVal, inputElem) {{
            if (!campaignSchedules[campToken]) {{
                campaignSchedules[campToken] = {{ target_count: 3, slots: [] }};
            }}
            if (!campaignSchedules[campToken].slots) {{
                campaignSchedules[campToken].slots = [];
            }}
            while (campaignSchedules[campToken].slots.length <= slotIdx) {{
                campaignSchedules[campToken].slots.push({{ time: "12:00", video: "" }});
            }}
            campaignSchedules[campToken].slots[slotIdx].time = timeVal;
            
            const savedData = await saveCurrentCampaignSchedule(campToken);
            if (savedData && savedData.slots) {{
                campaignSchedules[campToken].slots = savedData.slots;
            }}
            showToast(`💾 Orario Slot ${{slotIdx + 1}} salvato alle ${{timeVal}}!`);
            
            if (inputElem) {{
                inputElem.style.color = '#34d399';
                inputElem.style.borderColor = '#10b981';
            }}
        }}

        async function saveCampaignSlotVideo(campToken, slotIdx, videoFilename) {{
            if (!campaignSchedules[campToken]) {{
                campaignSchedules[campToken] = {{ target_count: 3, slots: [] }};
            }}
            if (!campaignSchedules[campToken].slots) {{
                campaignSchedules[campToken].slots = [];
            }}
            while (campaignSchedules[campToken].slots.length <= slotIdx) {{
                campaignSchedules[campToken].slots.push({{ time: "12:00", video: "" }});
            }}
            campaignSchedules[campToken].slots[slotIdx].video = videoFilename;
            const savedData = await saveCurrentCampaignSchedule(campToken);
            if (savedData && savedData.slots) {{
                campaignSchedules[campToken].slots = savedData.slots;
            }}
            showToast(`📹 Video aggiornato per lo Slot ${{slotIdx + 1}}!`);
        }}

        async function saveCurrentCampaignSchedule(campToken) {{
            const data = campaignSchedules[campToken] || {{ target_count: 3, slots: [] }};
            try {{
                const res = await fetch('/api/campaign/save-schedule', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        campaign_id: campToken,
                        target_count: data.target_count || 3,
                        slots: data.slots || []
                    }})
                }});
                if (res.ok) {{
                    const resJson = await res.json();
                    return resJson;
                }}
            }} catch(e) {{
                console.error("Errore salvataggio schedule", e);
            }}
            return null;
        }}

        window.resetCampaignPublishedClips = async function(campToken, btnEl) {{
            if (!confirm("Vuoi ripristinare tutte le clip pubblicate di questa campagna come vergini/nuove? Rientreranno immediatamente nella cascata.")) return;
            if (btnEl) {{
                btnEl.disabled = true;
                btnEl.innerText = "⏳ Ripristino...";
            }}
            try {{
                const res = await fetch('/api/campaign/reset-published-clips', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken }})
                }});
                if (res.ok) {{
                    await openCampaignDetail(campToken);
                }}
            }} catch(e) {{
                console.error("Errore reset published clips", e);
            }} finally {{
                if (btnEl) {{
                    btnEl.disabled = false;
                    btnEl.innerText = "🧹 Ripristina Clip come Nuove";
                }}
            }}
        }};

        function switchCampaignSubTab(campToken, tabName) {{
            const tabs = ['cascade', 'raw', 'analytics', 'prompts', 'brief'];
            tabs.forEach(t => {{
                const pane = document.getElementById('camp-subtab-' + t + '-' + campToken);
                const btn = document.getElementById('camp-navbtn-' + t + '-' + campToken);
                if (pane) pane.style.display = (t === tabName) ? 'block' : 'none';
                if (btn) {{
                    if (t === tabName) btn.classList.add('active');
                    else btn.classList.remove('active');
                }}
            }});
            if (tabName === 'raw' && typeof loadClippingQueueForCampaign === 'function') {{
                loadClippingQueueForCampaign(campToken);
            }}
        }}
        window.switchCampaignSubTab = switchCampaignSubTab;
        window.switchCampSubTab = switchCampaignSubTab;

        function switchCampaignViewMode(campToken, mode) {{
            const assemblyView = document.getElementById('camp-assembly-view-' + campToken);
            const classicView = document.getElementById('camp-classic-view-' + campToken);
            const tabAssembly = document.getElementById('tab-btn-assembly-' + campToken);
            const tabClassic = document.getElementById('tab-btn-classic-' + campToken);

            if (mode === 'classic') {{
                if (assemblyView) assemblyView.style.display = 'none';
                if (classicView) classicView.style.display = 'block';
                if (tabAssembly) {{
                    tabAssembly.style.background = 'transparent';
                    tabAssembly.style.color = '#94a3b8';
                    tabAssembly.style.boxShadow = 'none';
                    tabAssembly.style.borderColor = 'rgba(255,255,255,0.1)';
                }}
                if (tabClassic) {{
                    tabClassic.style.background = 'linear-gradient(135deg, #8b5cf6, #6366f1)';
                    tabClassic.style.color = '#ffffff';
                    tabClassic.style.boxShadow = '0 4px 15px rgba(139,92,246,0.35)';
                    tabClassic.style.borderColor = 'transparent';
                }}
                try {{ localStorage.setItem('camp_view_mode_' + campToken, 'classic'); }} catch(e) {{}}
            }} else {{
                if (assemblyView) assemblyView.style.display = 'grid';
                if (classicView) classicView.style.display = 'none';
                if (tabAssembly) {{
                    tabAssembly.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                    tabAssembly.style.color = '#ffffff';
                    tabAssembly.style.boxShadow = '0 4px 15px rgba(16,185,129,0.35)';
                    tabAssembly.style.borderColor = 'transparent';
                }}
                if (tabClassic) {{
                    tabClassic.style.background = 'transparent';
                    tabClassic.style.color = '#94a3b8';
                    tabClassic.style.boxShadow = 'none';
                    tabClassic.style.borderColor = 'rgba(255,255,255,0.1)';
                }}
                try {{ localStorage.setItem('camp_view_mode_' + campToken, 'assembly'); }} catch(e) {{}}
            }}
        }}

        async function autoConfigureAssemblyPipeline(campToken, btnEl) {{
            const origHtml = btnEl ? btnEl.innerHTML : '';
            if (btnEl) {{
                btnEl.disabled = true;
                btnEl.innerHTML = '⚙️ Configurazione & Avvio...';
            }}

            try {{
                // 1. Prendi tutte le clip già pubblicate per non riutilizzarle mai
                const schedInfo = campaignSchedules[campToken] || {{}};
                const publishedClipsList = Array.isArray(schedInfo.published_clips) ? schedInfo.published_clips : [];
                const publishedFromGlobal = (typeof publishedContent !== 'undefined' ? publishedContent : []).map(p => p.filename).filter(Boolean);
                const allPublishedFilenames = Array.from(new Set([...publishedClipsList, ...publishedFromGlobal]));

                // 2. Prendi solo le clip 9:16 vergini (non pubblicate) appartenenti SOLO a questa campagna
                const campIsolatedVids = getCampaignIsolatedVideos(campToken);
                const availableClips = campIsolatedVids.filter(v => v.filename && (v.filename.startsWith('clip_') || v.filename.includes('clip')) && !allPublishedFilenames.includes(v.filename));
                
                // 3. Prendi gli slot attuali o default
                const curSched = campaignSchedules[campToken] || {{ target_count: 3, slots: [] }};
                const defaultTimes = ["15:00", "17:00", "20:00", "22:00"];
                const targetCount = 3;
                
                const newSlots = [];
                for (let i = 0; i < targetCount; i++) {{
                    const timeVal = (curSched.slots && curSched.slots[i] && curSched.slots[i].time) ? curSched.slots[i].time : defaultTimes[i];
                    let videoVal = availableClips.length > i ? availableClips[i].filename : '';
                    newSlots.push({{ time: timeVal, video: videoVal }});
                }}

                // Salva schedule aggiornata
                campaignSchedules[campToken] = {{
                    target_count: targetCount,
                    slots: newSlots,
                    published_clips: publishedClipsList,
                    autopilot_enabled: true
                }};

                await fetch('/api/campaign/save-schedule', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        campaign_id: campToken,
                        target_count: targetCount,
                        slots: newSlots
                    }})
                }});

                // 4. Accoda gli slot all'autopilota
                await fetch('/api/autopilot/campaign-queue-slots', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken }})
                }});

                // 5. Abilita il pilota automatico per la campagna
                await fetch('/api/autopilot/campaign-toggle', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken, enable: true }})
                }});

                if (btnEl) {{
                    btnEl.innerHTML = '✅ Catena Avviata!';
                    setTimeout(() => {{
                        renderCampaignDetailContent(campToken);
                    }}, 600);
                }}
            }} catch(err) {{
                console.error("Errore auto-configurazione catena", err);
                alert("Errore nell'avvio automatico: " + err.message);
                if (btnEl) {{
                    btnEl.disabled = false;
                    btnEl.innerHTML = origHtml;
                }}
            }}
        }}

        async function addNewCampaignSlot(campToken) {{
            const timeVal = prompt("Inserisci l'orario per il nuovo slot di pubblicazione (formato HH:MM):", "18:00");
            if (!timeVal || !timeVal.trim()) return;
            
            try {{
                const res = await fetch('/api/campaign/add-slot', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        campaign_id: campToken,
                        time: timeVal.trim(),
                        video: ''
                    }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    if (!campaignSchedules[campToken]) campaignSchedules[campToken] = {{ slots: [] }};
                    campaignSchedules[campToken].slots = data.slots;
                    campaignSchedules[campToken].target_count = data.target_count;
                    renderCampaignDetailContent(campToken);
                }} else {{
                    alert("Errore aggiunta slot: " + (data.error || "Errore sconosciuto"));
                }}
            }} catch(e) {{
                alert("Errore di rete: " + e.message);
            }}
        }}

        async function removeCampaignSlot(campToken, originalIdx) {{
            if (!confirm("Sei sicuro di voler rimuovere questo slot dalla programmazione giornaliera?")) return;
            try {{
                const res = await fetch('/api/campaign/remove-slot', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        campaign_id: campToken,
                        slot_index: originalIdx
                    }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    if (campaignSchedules[campToken]) {{
                        campaignSchedules[campToken].slots = data.slots;
                        campaignSchedules[campToken].target_count = data.target_count;
                    }}
                    renderCampaignDetailContent(campToken);
                }} else {{
                    alert("Errore rimozione slot: " + (data.error || "Errore sconosciuto"));
                }}
            }} catch(e) {{
                alert("Errore di rete: " + e.message);
            }}
        }}

        async function generateVideoFromSlot(campToken, promptText, btnElem) {{
            if (!promptText || !promptText.trim()) {{
                alert("Il prompt è vuoto!");
                return;
            }}
            const origHtml = btnElem.innerHTML;
            btnElem.innerHTML = '⏳ Avvio Bot...';
            btnElem.disabled = true;

            try {{
                const res = await fetch('/api/generate-video', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ prompt: promptText }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    alert("🚀 Bot Gemini avviato con successo in background! Il video apparirà nella cartella e nel selettore non appena pronto.");
                }} else {{
                    alert("Errore avvio bot: " + (data.error || "Errore sconosciuto"));
                }}
            }} catch(e) {{
                alert("Errore di connessione al server: " + e.message);
            }} finally {{
                btnElem.innerHTML = origHtml;
                btnElem.disabled = false;
            }}
        }}

        async function publishSlotToTikTok(campToken, slotIdx, btnElem) {{
            // 1. Identifica il video assegnato allo slot o la prima clip vergine
            const schedInfo = campaignSchedules[campToken] || {{ slots: [] }};
            const slotData = (schedInfo.slots && schedInfo.slots[slotIdx]) ? schedInfo.slots[slotIdx] : {{}};
            let filename = slotData.video || "";

            if (!filename) {{
                const publishedClipsList = Array.isArray(schedInfo.published_clips) ? schedInfo.published_clips : [];
                const publishedFromGlobal = (typeof publishedContent !== 'undefined' ? publishedContent : []).map(p => p.filename).filter(Boolean);
                const allPublished = Array.from(new Set([...publishedClipsList, ...publishedFromGlobal]));
                const campIsolatedVids = getCampaignIsolatedVideos(campToken);
                const availableClips = campIsolatedVids.filter(v => v.filename && !allPublished.includes(v.filename));
                if (availableClips.length > 0) {{
                    filename = availableClips[0].filename;
                }}
            }}
            
            if (!filename) {{
                alert("Nessun video pronto disponibile per questo slot. Genera o seleziona una clip 9:16!");
                return;
            }}

            // 2. Recupera la didascalia specifica o i tag della campagna
            const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {{}};
            const item = (typeof generatedContent !== 'undefined' ? generatedContent : []).find(gc => gc.campaign_id === campToken) || {{}};
            const scripts = item.scripts || [];
            let captionText = "";
            
            if (scripts[slotIdx] && scripts[slotIdx].tiktok_caption) {{
                captionText = scripts[slotIdx].tiktok_caption;
            }} else if (scripts[0] && scripts[0].tiktok_caption) {{
                captionText = scripts[0].tiktok_caption;
            }} else {{
                const tags = (originalCamp.mandatory_hashtags || []).join(' ');
                const mentions = (originalCamp.mandatory_mentions || []).join(' ');
                captionText = `${{tags}} ${{mentions}} ${{originalCamp.call_to_action || ''}}`.trim();
            }}

            const origHtml = btnElem ? btnElem.innerHTML : "";
            if (btnElem) {{
                btnElem.innerHTML = '⏳ Pubblicazione in corso...';
                btnElem.disabled = true;
            }}

            // 3. MOSTRA IL RETTANGOLO DINAMICO "STO PROCESSANDO"
            const procBox = document.getElementById(`assembly-active-processing-box-${{campToken}}`);
            const procTitle = document.getElementById(`processing-clip-title-${{campToken}}`);
            const procStatus = document.getElementById(`processing-status-label-${{campToken}}`);
            const procFilename = document.getElementById(`processing-clip-filename-${{campToken}}`);
            const procTimer = document.getElementById(`processing-elapsed-timer-${{campToken}}`);

            if (procBox) {{
                procBox.style.display = 'block';
                procBox.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            }}
            if (procTitle) procTitle.innerText = `Pubblicazione Slot #${{slotIdx + 1}} (In corso...)`;
            if (procStatus) procStatus.innerText = 'Caricamento video su TikTok Studio, verifica copyright e invio automatico a Klippify...';
            if (procFilename) procFilename.innerText = `📹 ${{filename}}`;

            let secElapsed = 0;
            const timerInterval = setInterval(() => {{
                secElapsed++;
                if (procTimer) procTimer.innerText = `⏳ In corso (${{secElapsed}}s)...`;
            }}, 1000);

            try {{
                const res = await fetch('/api/tiktok/upload', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        filename: filename,
                        title: captionText || filename,
                        cover_time_ms: 1000,
                        campaign_id: campToken
                    }})
                }});
                const data = await res.json();

                if (data.status === 'success' && data.task_id) {{
                    const activeTaskId = data.task_id;
                    
                    // Polling in tempo reale del bot Playwright per TikTok Studio
                    const pollInterval = setInterval(async () => {{
                        try {{
                            const taskRes = await fetch('/api/debug/tasks');
                            const allTasks = await taskRes.json();
                            const curTask = allTasks.find(t => t.id === activeTaskId);

                            if (curTask) {{
                                if (curTask.logs && curTask.logs.length > 0) {{
                                    const latestLog = curTask.logs[curTask.logs.length - 1];
                                    if (procStatus) procStatus.innerText = latestLog;
                                }}

                                if (curTask.status === 'completed') {{
                                    clearInterval(pollInterval);
                                    clearInterval(timerInterval);

                                    if (procStatus) procStatus.innerHTML = '✅ <strong>Video pubblicato su TikTok Studio e inviato a Klippify!</strong> Scalamento slot in corso...';

                                    // Registra la clip come pubblicata nella schedule della campagna
                                    if (!campaignSchedules[campToken]) campaignSchedules[campToken] = {{ slots: [], published_clips: [] }};
                                    if (!Array.isArray(campaignSchedules[campToken].published_clips)) campaignSchedules[campToken].published_clips = [];
                                    if (!campaignSchedules[campToken].published_clips.includes(filename)) {{
                                        campaignSchedules[campToken].published_clips.push(filename);
                                    }}
                                    await saveCurrentCampaignSchedule(campToken);

                                    // Aggiorna lo storico locale
                                    if (typeof publishedContent !== 'undefined') {{
                                        publishedContent.push({{
                                            campaign_id: campToken,
                                            filename: filename,
                                            timestamp: new Date().toISOString().replace('T', ' ').substr(0, 19),
                                            title: captionText
                                        }});
                                    }}

                                    // Ricarica le submissions da Klippify
                                    try {{
                                        const subRes = await fetch('/api/klippify/submissions');
                                        if (subRes.ok) {{
                                            const freshSubs = await subRes.json();
                                            if (Array.isArray(freshSubs) && freshSubs.length > 0) klippifySubmissions = freshSubs;
                                        }}
                                    }} catch(e) {{}}

                                    setTimeout(() => {{
                                        if (procBox) procBox.style.display = 'none';
                                        renderCampaignDetailContent(campToken);
                                    }}, 2200);

                                }} else if (curTask.status === 'error') {{
                                    clearInterval(pollInterval);
                                    clearInterval(timerInterval);
                                    const errMsg = curTask.error || "Errore durante l'upload TikTok";
                                    if (procStatus) procStatus.innerHTML = `❌ <span style="color:#ef4444;">Errore: ${{errMsg}}</span>`;
                                    alert("Errore upload TikTok: " + errMsg);
                                    if (btnElem) {{
                                        btnElem.innerHTML = origHtml;
                                        btnElem.disabled = false;
                                    }}
                                }}
                            }}
                        }} catch(pollErr) {{
                            console.error("Errore polling task upload:", pollErr);
                        }}
                    }}, 1500);

                }} else if (data.status === 'success' || data.id) {{
                    clearInterval(timerInterval);
                    if (procStatus) procStatus.innerHTML = '✅ <strong>Video inviato con successo!</strong> Scalamento slot in corso...';
                    setTimeout(() => {{
                        if (procBox) procBox.style.display = 'none';
                        renderCampaignDetailContent(campToken);
                    }}, 1800);
                }} else {{
                    clearInterval(timerInterval);
                    const errMsg = data.error || data.message || "Errore sconosciuto";
                    if (procStatus) procStatus.innerHTML = `❌ <span style="color:#ef4444;">Errore: ${{errMsg}}</span>`;
                    alert("Errore upload TikTok: " + errMsg);
                    if (btnElem) {{
                        btnElem.innerHTML = origHtml;
                        btnElem.disabled = false;
                    }}
                }}
            }} catch(e) {{
                clearInterval(timerInterval);
                if (procStatus) procStatus.innerHTML = `❌ <span style="color:#ef4444;">Errore di rete: ${{e.message}}</span>`;
                alert("Errore comunicazione server: " + e.message);
                if (btnElem) {{
                    btnElem.innerHTML = origHtml;
                    btnElem.disabled = false;
                }}
            }}
        }}
        const publishVideoFromSlot = publishSlotToTikTok;

        async function submitManualVideoToKlippify(campToken, btnElem) {{
            const inputEl = document.getElementById(`manual-tiktok-url-${{campToken}}`);
            const url = inputEl ? inputEl.value.trim() : "";
            if (!url || !url.includes("http")) {{
                alert("Inserisci un link video valido di TikTok o Instagram!");
                return;
            }}
            const origHtml = btnElem.innerHTML;
            btnElem.innerHTML = "⏳ Invio a Klippify...";
            btnElem.disabled = true;
            try {{
                const res = await fetch("/api/klippify/submit-content", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{
                        campaign_id: campToken,
                        content_url: url,
                        platform: url.includes("instagram") ? "instagram" : "tiktok"
                    }})
                }});
                const data = await res.json();
                if (res.ok && !data.error) {{
                    alert("✅ Video inviato con successo a Klippify! Ora il sistema lo analizzerà e lo mostrerà nello storico.");
                    if (inputEl) inputEl.value = "";
                    renderCampaignDetailContent(campToken);
                }} else {{
                    alert("Errore invio Klippify: " + (data.error || JSON.stringify(data)));
                }}
            }} catch(e) {{
                alert("Errore di rete: " + e.message);
            }} finally {{
                btnElem.innerHTML = origHtml;
                btnElem.disabled = false;
            }}
        }}

        function onSlotVideoChange(selectElem, slotIdx, campToken) {{
            const filename = selectElem.value;
            const videoElem = document.getElementById(`slot-video-player-${{slotIdx}}`);
            const badgeElem = document.getElementById(`slot-status-badge-${{slotIdx}}`);

            if (filename) {{
                if (videoElem) {{
                    videoElem.src = `/generated_videos/${{encodeURIComponent(filename)}}`;
                    videoElem.style.display = 'block';
                }}
                if (badgeElem) {{
                    badgeElem.innerHTML = '🔵 Video Pronto';
                    badgeElem.style.background = 'rgba(56,189,248,0.2)';
                    badgeElem.style.color = '#38bdf8';
                }}
            }} else {{
                if (videoElem) {{
                    videoElem.style.display = 'none';
                }}
                if (badgeElem) {{
                    badgeElem.innerHTML = '🟡 Da Generare';
                    badgeElem.style.background = 'rgba(245,158,11,0.2)';
                    badgeElem.style.color = '#fbbf24';
                }}
            }}
            saveCampaignSlotVideo(campToken, slotIdx, filename);
        }}

        async function syncCampaignLiveStats(campToken, btnElem) {{
            const origHtml = btnElem ? btnElem.innerHTML : "";
            if (btnElem) {{
                btnElem.innerHTML = "⏳ Sincronizzazione TikTok API &amp; Klippify...";
                btnElem.disabled = true;
            }}
            try {{
                const res = await fetch(`/api/campaign/total-performance?campaign_id=${{encodeURIComponent(campToken)}}&sync_live=true`);
                const data = await res.json();
                if (data.status === "success") {{
                    if (typeof klippifySubmissions !== 'undefined' && data.submissions) {{
                        klippifySubmissions = data.submissions;
                    }}
                    renderCampaignDetailContent(campToken);
                }} else {{
                    alert("Errore sincronizzazione: " + (data.message || "Errore sconosciuto"));
                }}
            }} catch(e) {{
                console.error("Sync error:", e);
                alert("Errore di connessione con TikTok API: " + e.message);
            }} finally {{
                if (btnElem) {{
                    btnElem.innerHTML = origHtml;
                    btnElem.disabled = false;
                }}
            }}
        }}

        async function triggerStorageCleanup(btnElem) {{
            const origHtml = btnElem ? btnElem.innerHTML : "";
            if (btnElem) {{
                btnElem.innerHTML = "⏳ Pulizia disco in corso...";
                btnElem.disabled = true;
            }}
            try {{
                const res = await fetch("/api/storage/cleanup");
                const data = await res.json();
                if (data.status === "success") {{
                    alert(`✅ Pulizia completata!\\nLiberati: ${{data.freed_mb}} MB\\nFile temporanei/vecchi eliminati: ${{data.deleted_count}}`);
                    window.location.reload();
                }} else {{
                    alert("Errore durante la pulizia: " + (data.message || "Errore sconosciuto"));
                }}
            }} catch(e) {{
                alert("Errore di rete durante la pulizia: " + e.message);
            }} finally {{
                if (btnElem) {{
                    btnElem.innerHTML = origHtml;
                    btnElem.disabled = false;
                }}
            }}
        }}

        function buildCampaignDailyStatsHtml(campToken, originalCamp, campSubmissions, targetCount) {{
            const subs = campSubmissions || [];
            
            let totalViews = 0;
            let totalLikes = 0;
            let totalComments = 0;
            let totalShares = 0;
            let totalEarnings = 0;
            let acceptedCount = 0;
            let rejectedCount = 0;
            let pendingCount = 0;

            const dailyMap = {{}};

            subs.forEach(s => {{
                const views = s.views || s.view_count || 0;
                const likes = s.likes || s.like_count || 0;
                const comments = s.comments || s.comment_count || 0;
                const shares = s.shares || s.share_count || 0;
                const earnings = s.earnings || 0;

                totalViews += views;
                totalLikes += likes;
                totalComments += comments;
                totalShares += shares;
                totalEarnings += earnings;

                if (s.status === 'accepted') {{
                    acceptedCount++;
                }} else if (s.status === 'rejected') {{
                    rejectedCount++;
                }} else {{
                    pendingCount++;
                }}

                let dateKey = 'Oggi';
                let timeStr = '';
                if (s.created_at) {{
                    try {{
                        const d = new Date(s.created_at);
                        dateKey = d.toISOString().split('T')[0];
                        timeStr = d.toLocaleTimeString('it-IT', {{ hour: '2-digit', minute: '2-digit' }});
                    }} catch(e) {{
                        dateKey = 'Oggi';
                    }}
                }}

                if (!dailyMap[dateKey]) {{
                    dailyMap[dateKey] = {{
                        dateKey: dateKey,
                        videos: [],
                        views: 0,
                        likes: 0,
                        earnings: 0,
                        accepted: 0,
                        rejected: 0,
                        pending: 0
                    }};
                }}
                dailyMap[dateKey].views += views;
                dailyMap[dateKey].likes += likes;
                dailyMap[dateKey].earnings += earnings;
                if (s.status === 'accepted') dailyMap[dateKey].accepted++;
                else if (s.status === 'rejected') dailyMap[dateKey].rejected++;
                else dailyMap[dateKey].pending++;

                dailyMap[dateKey].videos.push({{
                    id: s.id,
                    post_url: s.post_url,
                    status: s.status,
                    views: views,
                    likes: likes,
                    time: timeStr
                }});
            }});

            const totalVideos = subs.length;
            const avgViews = totalVideos > 0 ? Math.round(totalViews / totalVideos) : 0;
            const approvalRate = totalVideos > 0 ? Math.round((acceptedCount / totalVideos) * 100) : 0;

            // Griglia Performance Totale di ciascun video pubblicato
            let videoPerformanceGridHtml = '';
            if (subs.length === 0) {{
                videoPerformanceGridHtml = `
                    <div style="text-align:center; padding:2.5rem 1.5rem; background:rgba(0,0,0,0.25); border:1px dashed rgba(255,255,255,0.1); border-radius:1rem; color:var(--text-muted);">
                        <div style="font-size:2.2rem; margin-bottom:0.5rem;">📊</div>
                        <div style="font-size:1.05rem; font-weight:800; color:#e2e8f0; margin-bottom:0.3rem;">Nessuna metrica ancora registrata</div>
                        <div style="font-size:0.82rem; max-width:480px; margin:0 auto; line-height:1.4;">Quando le clip verranno caricate su TikTok e inviate a Klippify, qui vedrai in tempo reale le visualizzazioni totali, i mi piace, i commenti e il guadagno accumulato.</div>
                    </div>
                `;
            }} else {{
                videoPerformanceGridHtml = `
                    <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:1.2rem;">
                        ${{subs.map((s, idx) => {{
                            const isAcc = s.status === 'accepted';
                            const isRej = s.status === 'rejected';
                            const vViews = s.views || s.view_count || 0;
                            const vLikes = s.likes || s.like_count || 0;
                            const vComments = s.comments || s.comment_count || 0;
                            const vEarnings = s.earnings || 0;
                            const dFormatted = s.created_at ? new Date(s.created_at).toLocaleDateString('it-IT', {{ day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit' }}) : 'N/D';

                            const badgeStatus = isAcc 
                                ? '<span style="background:rgba(16,185,129,0.2); color:#34d399; border:1px solid rgba(16,185,129,0.4); padding:0.2rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800;">✅ Approvato AI</span>'
                                : isRej 
                                    ? '<span style="background:rgba(239,68,68,0.25); color:#ef4444; border:1px solid rgba(239,68,68,0.5); padding:0.2rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:900;">❌ Rifiutato</span>'
                                    : '<span style="background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid rgba(245,158,11,0.35); padding:0.2rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800;">⏳ In Verifica</span>';

                            return `
                                <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.08); border-radius:1rem; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; gap:1rem; box-shadow:0 8px 20px rgba(0,0,0,0.35);">
                                    <div>
                                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
                                            <div style="display:flex; align-items:center; gap:0.4rem;">
                                                <span style="background:rgba(56,189,248,0.15); color:#38bdf8; font-weight:900; font-size:0.78rem; padding:0.2rem 0.5rem; border-radius:0.4rem;">Video #${{idx+1}}</span>
                                                <span style="font-size:0.72rem; color:#64748b;">${{dFormatted}}</span>
                                            </div>
                                            ${{badgeStatus}}
                                        </div>

                                        <div style="margin-bottom:0.8rem;">
                                            <a href="${{s.post_url}}" target="_blank" style="display:flex; align-items:center; justify-content:space-between; background:rgba(0,0,0,0.4); border:1px solid rgba(56,189,248,0.25); color:#38bdf8; text-decoration:none; padding:0.5rem 0.8rem; border-radius:0.6rem; font-size:0.8rem; font-weight:700; transition:all 0.2s;" onmouseover="this.style.background='rgba(56,189,248,0.15)'" onmouseout="this.style.background='rgba(0,0,0,0.4)'">
                                                <span style="display:flex; align-items:center; gap:0.4rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                                                    <span>🎵</span> <span>${{s.post_url}}</span>
                                                </span>
                                                <span style="font-size:0.75rem; flex-shrink:0; margin-left:0.4rem;">↗</span>
                                            </a>
                                        </div>

                                        <!-- REAL STATS GRID FROM TIKTOK API -->
                                        <div style="background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:0.8rem; display:grid; grid-template-columns:repeat(3, 1fr); gap:0.6rem; text-align:center;">
                                            <div>
                                                <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Views Reali</div>
                                                <div style="font-size:1.2rem; font-weight:900; color:#38bdf8;">${{vViews.toLocaleString()}}</div>
                                            </div>
                                            <div>
                                                <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Mi Piace</div>
                                                <div style="font-size:1.2rem; font-weight:900; color:#f43f5e;">${{vLikes.toLocaleString()}}</div>
                                            </div>
                                            <div>
                                                <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Guadagno</div>
                                                <div style="font-size:1.2rem; font-weight:900; color:#34d399;">$${{vEarnings.toFixed(2)}}</div>
                                            </div>
                                        </div>
                                    </div>

                                    <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.05); padding-top:0.6rem; font-size:0.72rem; color:#64748b;">
                                        <span>💬 ${{vComments}} commenti • 🔄 ${{s.shares || 0}} condivisioni</span>
                                        <span style="color:#38bdf8; font-weight:700;">📡 TikTok API Live</span>
                                    </div>
                                </div>
                            `;
                        }}).join('')}}
                    </div>
                `;
            }}

            const daysKeys = Object.keys(dailyMap).sort().reverse();
            let dailyBreakdownHtml = '';
            daysKeys.forEach(dk => {{
                const dayData = dailyMap[dk];
                dailyBreakdownHtml += `
                    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.05); padding:0.65rem 0.9rem; border-radius:0.6rem; font-size:0.8rem;">
                        <span style="font-weight:700; color:#e2e8f0;">📅 ${{dk}}</span>
                        <div style="display:flex; gap:1.2rem; align-items:center;">
                            <span style="color:#38bdf8; font-weight:700;">👁️ ${{dayData.views.toLocaleString()}} views</span>
                            <span style="color:#34d399; font-weight:700;">💰 $${{dayData.earnings.toFixed(2)}}</span>
                            <span style="color:#94a3b8;">${{dayData.videos.length}} video</span>
                        </div>
                    </div>
                `;
            }});

            return `
                <!-- STATISTICHE TOTALI DELLA CAMPAGNA (ALL-TIME) -->
                <div style="background:linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border:1px solid rgba(56,189,248,0.35); border-radius:1.25rem; padding:1.8rem; margin-bottom:2rem; box-shadow:0 12px 35px rgba(0,0,0,0.4);">
                    
                    <!-- HERO HEADER WITH LIVE SYNC BUTTON -->
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1.5rem; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:1.2rem;">
                        <div>
                            <div style="font-size:1.35rem; font-weight:900; color:#fff; display:flex; align-items:center; gap:0.6rem;">
                                <span>📊 Dati &amp; Performance Totali della Campagna</span>
                                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; font-size:0.78rem; padding:0.25rem 0.7rem; border-radius:1rem; font-weight:900;">
                                    TUTTI I VIDEO PUBBLICATI
                                </span>
                            </div>
                            <div style="font-size:0.85rem; color:#94a3b8; margin-top:0.25rem;">
                                Visualizzazioni complessive accumulate, metriche TikTok ufficiali e rendimento totale dall'inizio.
                            </div>
                        </div>

                        <div style="display:flex; gap:0.6rem; align-items:center; flex-wrap:wrap;">
                            <button onclick="syncCampaignLiveStats('${{campToken}}', this)" style="background:linear-gradient(135deg, #0284c7, #0369a1); color:#fff; font-weight:800; border:none; padding:0.65rem 1.2rem; border-radius:0.6rem; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 14px rgba(2,132,199,0.35); transition:transform 0.15s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='none'">
                                🔄 Sincronizza Views da TikTok API in Tempo Reale
                            </button>
                        </div>
                    </div>

                    <!-- 5 MEGA TOTAL KPI CARDS -->
                    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(190px, 1fr)); gap:1.1rem; margin-bottom:1.8rem;">
                        
                        <!-- 1. TOTAL VIEWS -->
                        <div style="background:rgba(0,0,0,0.4); border:1px solid rgba(56,189,248,0.3); border-radius:0.9rem; padding:1.1rem 1.3rem; border-left:5px solid #38bdf8; box-shadow:0 4px 15px rgba(0,0,0,0.2);">
                            <div style="font-size:0.75rem; color:#94a3b8; font-weight:800; text-transform:uppercase;">Visualizzazioni Totali</div>
                            <div id="perf-total-views-${{campToken}}" style="font-size:1.85rem; font-weight:900; color:#38bdf8; margin-top:0.25rem; line-height:1.1;">
                                ${{totalViews.toLocaleString()}}
                            </div>
                            <div style="font-size:0.75rem; color:#cbd5e1; margin-top:0.4rem;">${{totalLikes.toLocaleString()}} mi piace • ${{totalComments}} commenti</div>
                        </div>

                        <!-- 2. TOTAL EARNINGS -->
                        <div style="background:rgba(0,0,0,0.4); border:1px solid rgba(16,185,129,0.3); border-radius:0.9rem; padding:1.1rem 1.3rem; border-left:5px solid #10b981; box-shadow:0 4px 15px rgba(0,0,0,0.2);">
                            <div style="font-size:0.75rem; color:#94a3b8; font-weight:800; text-transform:uppercase;">Guadagno Totale Maturato</div>
                            <div id="perf-total-earnings-${{campToken}}" style="font-size:1.85rem; font-weight:900; color:#34d399; margin-top:0.25rem; line-height:1.1;">
                                $${{totalEarnings.toFixed(2)}}
                            </div>
                            <div style="font-size:0.75rem; color:#cbd5e1; margin-top:0.4rem;">su $${{originalCamp.payout_per_1k_views || '1.00'}}/1k views</div>
                        </div>

                        <!-- 3. TOTAL VIDEOS PUBLISHED -->
                        <div style="background:rgba(0,0,0,0.4); border:1px solid rgba(139,92,246,0.3); border-radius:0.9rem; padding:1.1rem 1.3rem; border-left:5px solid #8b5cf6; box-shadow:0 4px 15px rgba(0,0,0,0.2);">
                            <div style="font-size:0.75rem; color:#94a3b8; font-weight:800; text-transform:uppercase;">Video Pubblicati Totali</div>
                            <div id="perf-total-videos-${{campToken}}" style="font-size:1.85rem; font-weight:900; color:#c084fc; margin-top:0.25rem; line-height:1.1;">
                                ${{totalVideos}} <span style="font-size:0.9rem; font-weight:700; color:#94a3b8;">video</span>
                            </div>
                            <div style="font-size:0.75rem; color:#cbd5e1; margin-top:0.4rem;">${{acceptedCount}} approvati • ${{pendingCount}} in verifica</div>
                        </div>

                        <!-- 4. AVG VIEWS / VIDEO -->
                        <div style="background:rgba(0,0,0,0.4); border:1px solid rgba(245,158,11,0.3); border-radius:0.9rem; padding:1.1rem 1.3rem; border-left:5px solid #f59e0b; box-shadow:0 4px 15px rgba(0,0,0,0.2);">
                            <div style="font-size:0.75rem; color:#94a3b8; font-weight:800; text-transform:uppercase;">Media Views / Video</div>
                            <div id="perf-avg-views-${{campToken}}" style="font-size:1.85rem; font-weight:900; color:#fbbf24; margin-top:0.25rem; line-height:1.1;">
                                ${{avgViews.toLocaleString()}}
                            </div>
                            <div style="font-size:0.75rem; color:#cbd5e1; margin-top:0.4rem;">Indice di viralità medio</div>
                        </div>

                        <!-- 5. AI APPROVAL RATE -->
                        <div style="background:rgba(0,0,0,0.4); border:1px solid rgba(59,130,246,0.3); border-radius:0.9rem; padding:1.1rem 1.3rem; border-left:5px solid #3b82f6; box-shadow:0 4px 15px rgba(0,0,0,0.2);">
                            <div style="font-size:0.75rem; color:#94a3b8; font-weight:800; text-transform:uppercase;">Tasso Approvazione AI</div>
                            <div id="perf-approval-rate-${{campToken}}" style="font-size:1.85rem; font-weight:900; color:#60a5fa; margin-top:0.25rem; line-height:1.1;">
                                ${{approvalRate}}%
                            </div>
                            <div style="font-size:0.75rem; color:#cbd5e1; margin-top:0.4rem;">Conformità brief e regole</div>
                        </div>

                    </div>

                    <!-- DETTAGLIO VIDEO PER VIDEO (TOTALS VIEW) -->
                    <div style="margin-bottom:1.5rem;">
                        <div style="font-size:1.05rem; font-weight:800; color:#fff; margin-bottom:1rem; display:flex; align-items:center; gap:0.5rem;">
                            <span>🎬 Performance Dettagliata per Ciascun Video:</span>
                        </div>
                        ${{videoPerformanceGridHtml}}
                    </div>

                    <!-- STORICO GIORNALIERO (ACCORDION OPZIONALE) -->
                    ${{daysKeys.length > 0 ? `
                        <details style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:1rem;">
                            <summary style="font-size:0.85rem; font-weight:800; color:#94a3b8; cursor:pointer; display:flex; justify-content:space-between; align-items:center;">
                                <span>📅 Ripartizione Giorno per Giorno (Cronologia Storica)</span>
                                <span style="font-size:0.75rem; color:#64748b;">Clicca per espandere (${{daysKeys.length}} giorni)</span>
                            </summary>
                            <div style="display:flex; flex-direction:column; gap:0.6rem; margin-top:0.8rem;">
                                ${{dailyBreakdownHtml}}
                            </div>
                        </details>
                    ` : ''}}

                </div>
            `;
        }}

        function buildCampaignAssemblyPipelineHtml(campToken, originalCamp, item, isClipping, localAvailableVideos, savedSlots, targetCount, campSubmissions, scripts, defaultTimes, budgetRemaining, isDepleted, validLinks, allLinksHtml, dailyStatsHtml) {{
            const schedInfo = campaignSchedules[campToken] || {{}};
            const isAutopilotOn = schedInfo.autopilot_enabled !== undefined ? !!schedInfo.autopilot_enabled : true;
            const pauseUntilStr = schedInfo.pause_until || null;
            let isPaused = false;
            let pauseUntilFormatted = '';
            if (pauseUntilStr) {{
                try {{
                    const pDate = new Date(pauseUntilStr.replace(' ', 'T'));
                    if (pDate > new Date()) {{
                        isPaused = true;
                        pauseUntilFormatted = pDate.toLocaleDateString('it-IT', {{ day:'2-digit', month:'2-digit' }}) + ' alle ' + pDate.toLocaleTimeString('it-IT', {{ hour:'2-digit', minute:'2-digit' }});
                    }}
                }} catch(e) {{}}
            }}
            const isEnded = !!schedInfo.is_ended;
            const publishedClipsList = Array.isArray(schedInfo.published_clips) ? schedInfo.published_clips : [];
            const publishedFromGlobal = (typeof publishedContent !== 'undefined' ? publishedContent : [])
                .filter(p => p && p.campaign_id === campToken && (p.tiktok_url || p.content_url || p.status === 'published' || p.status === 'accepted'))
                .map(p => p.filename).filter(Boolean);
            const allPublishedFilenames = Array.from(new Set([...publishedClipsList, ...publishedFromGlobal]));

            const campIsolatedVids = getCampaignIsolatedVideos(campToken);
            const allClips = campIsolatedVids.filter(v => v.filename && (v.filename.startsWith('clip_') || v.filename.includes('clip')));
            const rawVideos = campIsolatedVids.filter(v => v.filename && !v.filename.startsWith('clip_'));
            
            // ⚡ ORDINAMENTO CRONOLOGICO ASSOLUTO & NUMERAZIONE UNICA PROGRESSIVA E IMMUTABILE
            const sortedAllClips = [...allClips].sort((a, b) => (a.mtime || 0) - (b.mtime || 0) || a.filename.localeCompare(b.filename));
            const clipNumberMap = {{}};
            sortedAllClips.forEach((c, idx) => {{
                clipNumberMap[c.filename] = idx + 1;
            }});

            // Separa le clip vergini disponibili da quelle già pubblicate
            const virginClips = sortedAllClips.filter(c => !allPublishedFilenames.includes(c.filename));
            const publishedClips = sortedAllClips.filter(c => allPublishedFilenames.includes(c.filename));

            const originalBrief = originalCamp.description || 'Nessun brief fornito.';
            const originalHashtags = (originalCamp.mandatory_hashtags || []).join(', ') || '#klippify';
            const originalMentions = (originalCamp.mandatory_mentions || []).join(', ') || 'Nessuna';
            const originalCTA = originalCamp.call_to_action || 'Guarda il video completo su Klippify!';

            // ⚡ SLIDING SLOTS LOGIC: separa gli slot già pubblicati oggi da quelli ancora pendenti
            const pendingSlots = [];
            const completedSlots = [];

            savedSlots.forEach((slot, originalIdx) => {{
                const vid = slot.video;
                const isPub = vid && allPublishedFilenames.includes(vid);
                if (isPub) {{
                    completedSlots.push({{ ...slot, originalIdx, isPublished: true }});
                }} else {{
                    pendingSlots.push({{ ...slot, originalIdx, isPublished: false }});
                }}
            }});

            // Assegna automaticamente le clip vergini disponibili in modo univoco agli slot pendenti
            const assignedFilenames = new Set(pendingSlots.map(s => s.video).filter(Boolean));
            let virginIdx = 0;
            pendingSlots.forEach((pSlot) => {{
                if (!pSlot.video) {{
                    while (virginIdx < virginClips.length && assignedFilenames.has(virginClips[virginIdx].filename)) {{
                        virginIdx++;
                    }}
                    if (virginIdx < virginClips.length) {{
                        pSlot.video = virginClips[virginIdx].filename;
                        assignedFilenames.add(pSlot.video);
                        virginIdx++;
                    }}
                }}
            }});

            const currentSlotVideos = pendingSlots.map(s => s.video).filter(Boolean);
            // ⚡ CLIP VERAMENTE IN RISERVA: SOLO quelle vergini NON ancora assegnate a nessuno slot
            const trulyReserveClips = virginClips.filter(c => !currentSlotVideos.includes(c.filename));

            let slotsMainViewHtml = '';

            if (pendingSlots.length === 0) {{
                // TUTTI GLI SLOT DI OGGI SONO STATI COMPLETATI!
                slotsMainViewHtml = `
                    <div style="background:linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.25)); border:2px solid rgba(16,185,129,0.4); border-radius:1.4rem; padding:2.2rem; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.5);">
                        <div style="font-size:3.2rem; margin-bottom:0.6rem; filter:drop-shadow(0 4px 10px rgba(0,0,0,0.5));">🎉</div>
                        <div style="font-size:1.45rem; font-weight:900; color:#34d399; margin-bottom:0.5rem;">Tutti i Video di Oggi sono stati Pubblicati!</div>
                        <div style="font-size:0.92rem; color:#cbd5e1; max-width:620px; margin:0 auto 1.4rem auto; line-height:1.5;">
                            Tutti gli slot previsti per questa campagna sono stati caricati con successo su TikTok e registrati su Klippify.<br>
                            <strong>Alle ore 00:00 il ciclo si resetterà in automatico</strong> ripristinando tutti gli slot con le nuove clip vergini pronte in magazzino.
                        </div>
                        <div style="display:flex; gap:0.8rem; justify-content:center; align-items:center; flex-wrap:wrap;">
                            <button onclick="addNewCampaignSlot('${{campToken}}')" style="background:linear-gradient(135deg, #38bdf8, #0284c7); color:#fff; border:none; padding:0.7rem 1.3rem; border-radius:0.6rem; font-weight:800; font-size:0.88rem; cursor:pointer; box-shadow:0 4px 15px rgba(56,189,248,0.3); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                                ➕ Aggiungi un altro Slot per Oggi
                            </button>
                            <button onclick="resetCampaignPublishedClips('${{campToken}}', this)" style="background:rgba(255,255,255,0.08); color:#cbd5e1; border:1px solid rgba(255,255,255,0.2); padding:0.7rem 1.3rem; border-radius:0.6rem; font-weight:800; font-size:0.88rem; cursor:pointer;" title="Ripristina clip pubblicate come vergini">
                                🧹 Ripristina Clip per Rivederle
                            </button>
                        </div>
                    </div>
                `;
            }} else {{
                // 1. HERO TOP RECTANGLE: IL PROSSIMO SLOT PENDENTE (1° IN CODA)
                const heroSlot = pendingSlots[0];
                const heroSlotTime = heroSlot.time || defaultTimes[0] || "15:00";
                const heroSavedVideo = heroSlot.video || (virginClips.length > 0 ? virginClips[0].filename : "");
                const hasHeroVideo = !!heroSavedVideo && !allPublishedFilenames.includes(heroSavedVideo);
                const heroScript = scripts[0] || {{}};
                const heroCaption = heroScript.tiktok_caption || `${{originalCamp.mandatory_hashtags ? originalCamp.mandatory_hashtags.join(' ') : '#klippify'}} ${{originalCamp.mandatory_mentions ? originalCamp.mandatory_mentions.join(' ') : ''}}`;
                const heroClipNum = heroSavedVideo ? (clipNumberMap[heroSavedVideo] || (heroSlot.originalIdx + 1)) : null;
                const heroTitleDisplay = heroSavedVideo ? `Clip #${{heroClipNum}} (${{heroSavedVideo}})` : `In attesa di Clip (${{originalCamp.name}})`;

                let heroVideoOptions = '<option value="">-- Seleziona Clip 9:16 --</option>';
                virginClips.forEach(v => {{
                    const isSel = (v.filename === heroSavedVideo) ? 'selected' : '';
                    const num = clipNumberMap[v.filename] || '?';
                    const isUsedElsewhere = currentSlotVideos.includes(v.filename) && v.filename !== heroSavedVideo;
                    const disabledAttr = isUsedElsewhere ? 'disabled style="color:#64748b;"' : '';
                    const label = isUsedElsewhere ? `🔒 Clip #${{num}}: ${{v.filename}} (Assegnata ad un altro slot)` : `🟢 Clip #${{num}}: ${{v.filename}} (${{(v.size_mb || 0).toFixed(1)}} MB)`;
                    heroVideoOptions += `<option value="${{v.filename}}" ${{isSel}} ${{disabledAttr}}>${{label}}</option>`;
                }});
                publishedClips.forEach(v => {{
                    const isSel = (v.filename === heroSavedVideo) ? 'selected' : '';
                    const num = clipNumberMap[v.filename] || '?';
                    heroVideoOptions += `<option value="${{v.filename}}" ${{isSel}} disabled style="color:#64748b;">🔒 Clip #${{num}}: ${{v.filename}} (✅ Già Pubblicata)</option>`;
                }});

                const heroCardHtml = `
                    <div class="cascade-hero-card">
                        <!-- BADGE HERO IN TESTA -->
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; margin-bottom:1.2rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:1rem;">
                            <div style="display:flex; align-items:center; gap:0.6rem;">
                                <span style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; font-weight:900; font-size:0.82rem; padding:0.35rem 0.8rem; border-radius:0.5rem; box-shadow:0 0 15px rgba(16,185,129,0.5); display:flex; align-items:center; gap:0.4rem;">
                                    <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#fff; animation:pulse 1.5s infinite;"></span>
                                    🌟 1° IN CODA: PROSSIMA PUBBLICAZIONE
                                </span>
                                <span style="font-size:0.85rem; color:#34d399; font-weight:800;">Slot ${{heroSlot.originalIdx + 1}} (In Uscita)</span>
                            </div>

                            <div style="display:flex; align-items:center; gap:0.8rem;">
                                <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(0,0,0,0.5); padding:0.35rem 0.8rem; border-radius:0.6rem; border:1px solid rgba(16,185,129,0.3);">
                                    <span style="font-size:0.78rem; color:#94a3b8; font-weight:700;">⏰ Orario:</span>
                                    <input type="time" value="${{heroSlotTime}}" onchange="saveCampaignSlotTime('${{campToken}}', ${{heroSlot.originalIdx}}, this.value, this)" style="background:transparent; border:none; color:#34d399; font-weight:900; font-size:0.95rem; outline:none; cursor:pointer;">
                                </div>
                                <button onclick="addNewCampaignSlot('${{campToken}}')" style="background:linear-gradient(135deg, #38bdf8, #0284c7); color:#fff; font-weight:800; border:none; padding:0.45rem 0.85rem; border-radius:0.6rem; font-size:0.8rem; cursor:pointer; display:flex; align-items:center; gap:0.35rem; box-shadow:0 4px 12px rgba(56,189,248,0.3); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                                    <span>➕ Aggiungi Slot</span>
                                </button>
                            </div>
                        </div>

                        <!-- CORPO HERO: ANTEPRIMA 3D A SINISTRA + AZIONI IN RILIEVO A DESTRA -->
                        <div style="display:grid; grid-template-columns:230px 1fr; gap:1.5rem; align-items:stretch;">
                            <div style="background:linear-gradient(180deg, #0f172a 0%, #020617 100%); border:2px solid rgba(255,255,255,0.12); border-top:2px solid rgba(255,255,255,0.3); border-bottom:4px solid #000; border-radius:1.2rem; padding:0.85rem; display:flex; flex-direction:column; justify-content:space-between; align-items:center; text-align:center; box-shadow:inset 0 2px 8px rgba(0,0,0,0.8), 0 10px 25px rgba(0,0,0,0.6);">
                                ${{heroSavedVideo ? `
                                    <div style="position:relative; width:100%; height:240px; border-radius:0.85rem; overflow:hidden; background:#000; border:1.5px solid rgba(56,189,248,0.35); box-shadow:0 6px 16px rgba(0,0,0,0.8); margin-bottom:0.5rem;">
                                        <video src="/video/${{encodeURIComponent(heroSavedVideo)}}" controls playsinline preload="metadata" style="width:100%; height:100%; object-fit:contain; background:#000; border-radius:0.75rem;"></video>
                                    </div>
                                    <div style="width:100%; margin-bottom:0.4rem;">
                                        <div style="font-size:0.75rem; font-weight:800; color:#38bdf8; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${{heroSavedVideo}}">📹 Clip #${{heroClipNum}}: ${{heroSavedVideo}}</div>
                                        <div style="font-size:0.68rem; color:#94a3b8;">Formato 9:16 TikTok HD</div>
                                    </div>
                                    <a href="/video/${{encodeURIComponent(heroSavedVideo)}}" target="_blank" style="width:100%; background:linear-gradient(180deg, #0284c7, #0369a1); color:#fff; border:1px solid rgba(255,255,255,0.2); border-top:1.5px solid rgba(255,255,255,0.4); border-bottom:3px solid #075985; padding:0.45rem; border-radius:0.6rem; font-size:0.75rem; font-weight:800; text-decoration:none; display:flex; align-items:center; justify-content:center; gap:0.4rem; box-shadow:0 4px 12px rgba(0,0,0,0.4); transition:all 0.15s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
                                        🔍 Apri a Schermo Intero
                                    </a>
                                ` : `
                                    <div style="font-size:2.8rem; margin-top:1rem; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.5));">📱</div>
                                    <div>
                                        <div style="font-size:0.82rem; font-weight:800; color:#fff; margin-bottom:0.2rem;">Formato 9:16 TikTok</div>
                                        <div style="font-size:0.72rem; color:#94a3b8;">In attesa di clip...</div>
                                    </div>
                                    <span style="font-size:0.72rem; color:#fbbf24; margin-bottom:1rem;">⚠️ Seleziona una clip</span>
                                `}}
                            </div>

                            <div style="display:flex; flex-direction:column; justify-content:space-between; gap:1rem;">
                                <div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                                        <h3 style="margin:0; font-size:1.35rem; font-weight:900; color:#fff; text-shadow:0 2px 8px rgba(0,0,0,0.5);">🎬 ${{heroTitleDisplay}}</h3>
                                        <span style="background:linear-gradient(135deg, rgba(16,185,129,0.3), rgba(5,150,105,0.2)); border:1px solid rgba(16,185,129,0.5); border-top:1.5px solid rgba(52,211,153,0.8); border-bottom:2px solid #047857; color:#34d399; font-size:0.75rem; font-weight:800; padding:0.25rem 0.7rem; border-radius:0.5rem; box-shadow:0 3px 8px rgba(0,0,0,0.3);">
                                            ${{hasHeroVideo ? '🟢 PRONTA PER INVIO' : '⚠️ SELEZIONA CLIP'}}
                                        </span>
                                    </div>

                                    <div style="margin-bottom:0.8rem;">
                                        <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase; display:block; margin-bottom:0.25rem;">Cambia Clip Assegnata:</label>
                                        <select onchange="saveCampaignSlotVideo('${{campToken}}', ${{heroSlot.originalIdx}}, this.value)" style="width:100%; background:linear-gradient(180deg, #090d16 0%, #0f172a 100%); border:1px solid rgba(16,185,129,0.4); border-top:1px solid rgba(52,211,153,0.6); border-bottom:2px solid #047857; color:#f8fafc; padding:0.65rem; border-radius:0.6rem; font-size:0.82rem; font-weight:800; box-shadow:inset 0 2px 5px rgba(0,0,0,0.7);">
                                            ${{heroVideoOptions}}
                                        </select>
                                    </div>

                                    <div style="background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.08); border-bottom:2px solid rgba(0,0,0,0.8); border-radius:0.75rem; padding:0.85rem; box-shadow:inset 0 2px 6px rgba(0,0,0,0.6);">
                                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
                                            <span style="font-size:0.72rem; color:#34d399; font-weight:800; text-transform:uppercase;">📱 Caption &amp; Tag Obbligatori:</span>
                                            <button onclick="copyToClipboard(decodeURIComponent('${{encodeURIComponent(heroCaption)}}'), this)" style="background:rgba(255,255,255,0.1); color:#fff; border:1px solid rgba(255,255,255,0.15); border-bottom:2px solid rgba(0,0,0,0.5); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:bold; cursor:pointer;">📋 Copia</button>
                                        </div>
                                        <div style="font-size:0.8rem; color:#cbd5e1; line-height:1.4; max-height:48px; overflow-y:auto;">${{heroCaption}}</div>
                                    </div>
                                </div>

                                <button onclick="publishSlotToTikTok('${{campToken}}', ${{heroSlot.originalIdx}}, this)" ${{hasHeroVideo ? '' : 'disabled'}} style="background:${{hasHeroVideo ? 'linear-gradient(180deg, #10b981 0%, #059669 100%)' : 'rgba(255,255,255,0.08)'}}; color:${{hasHeroVideo ? '#ffffff' : '#64748b'}}; border:1px solid rgba(255,255,255,0.2); border-top:${{hasHeroVideo ? '2px solid rgba(255,255,255,0.5)' : 'none'}}; border-bottom:${{hasHeroVideo ? '4px solid #047857' : '2px solid rgba(0,0,0,0.5)'}}; padding:1rem 1.4rem; border-radius:0.85rem; font-weight:900; font-size:0.95rem; cursor:${{hasHeroVideo ? 'pointer' : 'not-allowed'}}; display:flex; align-items:center; justify-content:center; gap:0.6rem; box-shadow:${{hasHeroVideo ? '0 10px 25px rgba(0,0,0,0.5), 0 0 20px rgba(16,185,129,0.4), inset 0 1px 0 rgba(255,255,255,0.4)' : 'none'}}; transition:all 0.15s;" onmouseover="if(this.style.cursor==='pointer') {{ this.style.transform='translateY(-2px)'; this.style.boxShadow='0 14px 30px rgba(0,0,0,0.6), 0 0 30px rgba(16,185,129,0.5)'; }}" onmouseout="if(this.style.cursor==='pointer') {{ this.style.transform='none'; this.style.boxShadow='0 10px 25px rgba(0,0,0,0.5), 0 0 20px rgba(16,185,129,0.4)'; }}" onmousedown="if(this.style.cursor==='pointer') {{ this.style.transform='translateY(2px)'; this.style.borderBottomWidth='2px'; }}">
                                    <span>🚀 PUBBLICA SUBITO QUESTO VIDEO SU TIKTOK</span>
                                </button>
                            </div>
                        </div>
                    </div>
                `;

                // 2. MIDDLE CARDS: GLI ALTRI SLOT PENDENTI (2° IN CODA, 3° IN CODA...)
                let middleCardsHtml = '';
                pendingSlots.slice(1).forEach((slot, pIdx) => {{
                    const queuePosition = pIdx + 2;
                    const slotTime = slot.time || defaultTimes[pIdx + 1] || "18:00";
                    const savedVideo = slot.video || "";
                    const hasSlotVideo = !!savedVideo && !allPublishedFilenames.includes(savedVideo);
                    const slotClipNum = savedVideo ? (clipNumberMap[savedVideo] || (slot.originalIdx + 1)) : null;
                    const slotTitleDisplay = savedVideo ? `Clip #${{slotClipNum}} (${{savedVideo}})` : `Clip #${{slot.originalIdx + 1}} (${{originalCamp.name}})`;

                    let slotOptions = '<option value="">-- Seleziona Clip 9:16 --</option>';
                    virginClips.forEach(v => {{
                        const isSel = (v.filename === savedVideo) ? 'selected' : '';
                        const num = clipNumberMap[v.filename] || '?';
                        const isUsedElsewhere = currentSlotVideos.includes(v.filename) && v.filename !== savedVideo;
                        const disabledAttr = isUsedElsewhere ? 'disabled style="color:#64748b;"' : '';
                        const label = isUsedElsewhere ? `🔒 Clip #${{num}}: ${{v.filename}} (Assegnata ad un altro slot)` : `🟢 Clip #${{num}}: ${{v.filename}} (${{(v.size_mb || 0).toFixed(1)}} MB)`;
                        slotOptions += `<option value="${{v.filename}}" ${{isSel}} ${{disabledAttr}}>${{label}}</option>`;
                    }});
                    publishedClips.forEach(v => {{
                        const isSel = (v.filename === savedVideo) ? 'selected' : '';
                        const num = clipNumberMap[v.filename] || '?';
                        slotOptions += `<option value="${{v.filename}}" ${{isSel}} disabled style="color:#64748b;">🔒 Clip #${{num}}: ${{v.filename}} (✅ Già Pubblicata)</option>`;
                    }});

                    middleCardsHtml += `
                        <div class="cascade-slot-card" style="animation-delay:${{0.12 * (pIdx + 1)}}s;">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:0.8rem; margin-bottom:0.8rem;">
                                <div style="display:flex; align-items:center; gap:0.6rem;">
                                    <span style="background:linear-gradient(135deg, #8b5cf6, #6366f1); color:#fff; font-weight:900; font-size:0.75rem; padding:0.25rem 0.65rem; border-radius:0.4rem; box-shadow:0 2px 8px rgba(139,92,246,0.3);">
                                        ⏳ ${{queuePosition}}° IN CODA
                                    </span>
                                    <span style="font-weight:900; font-size:1.05rem; color:#f8fafc;">${{slotTitleDisplay}}</span>
                                </div>
                                <div style="display:flex; align-items:center; gap:0.6rem;">
                                    <div style="display:flex; align-items:center; gap:0.5rem; background:rgba(0,0,0,0.5); padding:0.3rem 0.6rem; border-radius:0.5rem; border:1px solid rgba(255,255,255,0.1);">
                                        <span style="font-size:0.75rem; color:#94a3b8; font-weight:700;">⏰ Orario:</span>
                                        <input type="time" value="${{slotTime}}" onchange="saveCampaignSlotTime('${{campToken}}', ${{slot.originalIdx}}, this.value, this)" style="background:transparent; border:none; color:#38bdf8; font-weight:900; font-size:0.88rem; outline:none; cursor:pointer;">
                                    </div>
                                    <button onclick="removeCampaignSlot('${{campToken}}', ${{slot.originalIdx}})" style="background:rgba(239,68,68,0.15); color:#fca5a5; border:1px solid rgba(239,68,68,0.3); padding:0.35rem 0.65rem; border-radius:0.4rem; cursor:pointer; font-size:0.8rem; font-weight:bold;" title="Elimina questo slot">
                                        🗑️
                                    </button>
                                </div>
                            </div>

                            <div style="display:grid; grid-template-columns:1fr 1.2fr; gap:1rem; align-items:center;">
                                <div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
                                        <label style="font-size:0.72rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">📹 Video Clip:</label>
                                        <span style="font-size:0.7rem; font-weight:800; color:${{hasSlotVideo ? '#34d399' : '#fbbf24'}};">
                                            ${{hasSlotVideo ? '🟢 Clip Pronta' : '⚠️ In Riserva'}}
                                        </span>
                                    </div>
                                    <select onchange="saveCampaignSlotVideo('${{campToken}}', ${{slot.originalIdx}}, this.value)" style="width:100%; background:rgba(0,0,0,0.6); border:1px solid rgba(255,255,255,0.15); color:#f8fafc; padding:0.55rem; border-radius:0.5rem; font-size:0.8rem; font-weight:700;">
                                        ${{slotOptions}}
                                    </select>
                                </div>

                                <div style="display:flex; gap:0.6rem; align-items:center; justify-content:flex-end;">
                                    ${{savedVideo ? `
                                        <a href="/video/${{encodeURIComponent(savedVideo)}}" target="_blank" style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); padding:0.6rem 0.8rem; border-radius:0.5rem; font-size:0.78rem; font-weight:800; text-decoration:none; display:inline-flex; align-items:center; gap:0.3rem;" onmouseover="this.style.background='rgba(56,189,248,0.25)'" onmouseout="this.style.background='rgba(56,189,248,0.15)'">
                                            ▶️ Anteprima
                                        </a>
                                    ` : ''}}
                                    <button onclick="publishSlotToTikTok('${{campToken}}', ${{slot.originalIdx}}, this)" ${{hasSlotVideo ? '' : 'disabled'}} style="background:${{hasSlotVideo ? 'linear-gradient(135deg, #10b981, #059669)' : 'rgba(255,255,255,0.08)'}}; color:${{hasSlotVideo ? '#ffffff' : '#64748b'}}; border:none; padding:0.6rem 1rem; border-radius:0.5rem; font-weight:800; font-size:0.8rem; cursor:${{hasSlotVideo ? 'pointer' : 'not-allowed'}}; display:flex; align-items:center; gap:0.4rem; box-shadow:${{hasSlotVideo ? '0 4px 12px rgba(16,185,129,0.3)' : 'none'}};">
                                        <span>🚀 Pubblica Subito</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                }});

                slotsMainViewHtml = heroCardHtml + middleCardsHtml;
            }}

            // 3. CLIP IN RISERVA NEL MAGAZZINO (SOLO QUELLE VERGINI NON ANCORA ASSEGNATE AGLI SLOT)
            let reserveRowsHtml = '';
            if (trulyReserveClips.length === 0) {{
                reserveRowsHtml = `
                    <div style="text-align:center; padding:1.8rem; background:rgba(0,0,0,0.3); border:1px dashed rgba(56,189,248,0.3); border-radius:0.9rem;">
                        <div style="font-size:1.8rem; margin-bottom:0.3rem;">📦</div>
                        <div style="font-size:0.95rem; font-weight:800; color:#38bdf8;">Tutte le clip pronte (${{virginClips.length}}) sono posizionate negli slot attivi di oggi!</div>
                        <div style="font-size:0.78rem; color:#94a3b8; margin-top:0.2rem;">0 clip in eccedenza in riserva. Quando crei o tagli nuovi video, appariranno qui con numerazione progressiva univoca.</div>
                    </div>
                `;
            }} else {{
                trulyReserveClips.forEach((vClip, rIdx) => {{
                    const globalNum = clipNumberMap[vClip.filename] || (rIdx + 1);
                    reserveRowsHtml += `
                        <div class="cascade-reserve-row" style="animation-delay:${{0.08 * (rIdx + 1)}}s;">
                            <div style="display:flex; align-items:center; gap:0.8rem; min-width:240px;">
                                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; font-weight:900; font-size:0.78rem; padding:0.25rem 0.6rem; border-radius:0.4rem; border:1px solid rgba(56,189,248,0.4);">
                                    Clip #${{globalNum}}
                                </span>
                                <div>
                                    <div style="font-weight:800; font-size:0.88rem; color:#f8fafc;">Clip #${{globalNum}}</div>
                                    <div style="font-size:0.72rem; color:#94a3b8;">${{vClip.filename}} &bull; ${{ (vClip.size_mb || 0).toFixed(1) }} MB</div>
                                </div>
                            </div>

                            <div style="display:flex; align-items:center; gap:0.6rem;">
                                <span style="background:rgba(139,92,246,0.15); color:#c084fc; font-size:0.72rem; font-weight:800; padding:0.25rem 0.6rem; border-radius:0.4rem; border:1px solid rgba(139,92,246,0.3);">
                                    ⏳ Riserva #${{rIdx + 1}} (Pronta a salire)
                                </span>
                                <a href="/video/${{encodeURIComponent(vClip.filename)}}" target="_blank" style="background:rgba(255,255,255,0.08); color:#e2e8f0; border:1px solid rgba(255,255,255,0.15); padding:0.35rem 0.7rem; border-radius:0.4rem; font-size:0.75rem; font-weight:800; text-decoration:none;" onmouseover="this.style.background='rgba(255,255,255,0.15)'" onmouseout="this.style.background='rgba(255,255,255,0.08)'">
                                    ▶️ Guarda
                                </a>
                            </div>
                        </div>
                    `;
                }});
            }}

            // Clip pubblicate archiviate (nascoste di default tramite menu a tendina)
            let publishedRowsHtml = '';
            if (publishedClips.length > 0) {{
                let pubListHtml = '';
                publishedClips.forEach((pClip, pIdx) => {{
                    const globalNum = clipNumberMap[pClip.filename] || (pIdx + 1);
                    pubListHtml += `
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.06); padding:0.7rem 1rem; border-radius:0.6rem;">
                            <div style="display:flex; align-items:center; gap:0.6rem;">
                                <span style="color:#10b981; font-weight:900; font-size:0.85rem;">✅ #${{globalNum}}</span>
                                <div>
                                    <div style="font-weight:700; font-size:0.82rem; color:#cbd5e1;">${{pClip.filename}}</div>
                                    <div style="font-size:0.7rem; color:#64748b;">Archiviato &bull; Non riutilizzabile</div>
                                </div>
                            </div>
                            <div style="display:flex; align-items:center; gap:0.5rem;">
                                <a href="/video/${{encodeURIComponent(pClip.filename)}}" target="_blank" style="background:rgba(255,255,255,0.06); color:#94a3b8; border:1px solid rgba(255,255,255,0.1); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; text-decoration:none;">
                                    ▶️ Rivedi
                                </a>
                            </div>
                        </div>
                    `;
                }});

                publishedRowsHtml = `
                    <details class="published-accordion-dropdown">
                        <summary>
                            <span style="display:flex; align-items:center; gap:0.5rem;">
                                <span>🔒</span>
                                <span>Clip Storiche Già Pubblicate (${{publishedClips.length}})</span>
                            </span>
                            <span style="font-size:0.75rem; color:#94a3b8;">▼ Clicca per visualizzare</span>
                        </summary>
                        <div class="published-accordion-content">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                <span style="font-size:0.75rem; color:#94a3b8;">Queste clip sono già state caricate su TikTok e inviate a Klippify:</span>
                                <button onclick="resetCampaignPublishedClips('${{campToken}}', this)" style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3); padding:0.3rem 0.7rem; border-radius:0.4rem; font-size:0.72rem; font-weight:700; cursor:pointer;">
                                    🧹 Ripristina Clip
                                </button>
                            </div>
                            ${{pubListHtml}}
                        </div>
                    </details>
                `;
            }}

            return `
                <div class="camp-layout-grid">
                    
                    <!-- NAVIGAZIONE LATERALE WIREFRAME -->
                    <div class="camp-subnav-panel">
                        <button id="camp-navbtn-cascade-${{campToken}}" class="camp-subnav-btn active" onclick="switchCampaignSubTab('${{campToken}}', 'cascade')">
                            <span>🌊</span>
                            <span>Coda &amp; Cascata</span>
                        </button>
                        <button id="camp-navbtn-raw-${{campToken}}" class="camp-subnav-btn" onclick="switchCampaignSubTab('${{campToken}}', 'raw')">
                            <span>📦</span>
                            <span>Materia Prima &amp; Taglio (${{rawVideos.length}})</span>
                        </button>
                        <button id="camp-navbtn-prompts-${{campToken}}" class="camp-subnav-btn" onclick="switchCampaignSubTab('${{campToken}}', 'prompts')">
                            <span>💡</span>
                            <span>Prompt &amp; Storyboard (${{scripts.length}})</span>
                        </button>
                        <button id="camp-navbtn-analytics-${{campToken}}" class="camp-subnav-btn" onclick="switchCampaignSubTab('${{campToken}}', 'analytics')">
                            <span>📊</span>
                            <span>Dati &amp; Performance</span>
                        </button>
                        <button id="camp-navbtn-brief-${{campToken}}" class="camp-subnav-btn" onclick="switchCampaignSubTab('${{campToken}}', 'brief')">
                            <span>📋</span>
                            <span>Dettagli Brief</span>
                        </button>
                    </div>

                    <!-- AREA CONTENUTO CENTRALE -->
                    <div>
                        <!-- TOP 2 WIDGETS A RILIEVO -->
                        <div class="camp-top-widgets-grid">
                            <!-- WIDGET 1: STATO PILOTA AUTOMATICO -->
                            <div class="camp-widget-card" style="border-left:4px solid ${{isAutopilotOn ? '#10b981' : '#ef4444'}};">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <span style="font-size:0.75rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Pilota Automatico:</span>
                                    <span id="assembly-autopilot-badge-${{campToken}}" style="background:${{isAutopilotOn ? 'rgba(16,185,129,0.2)' : 'rgba(239,68,68,0.2)'}}; color:${{isAutopilotOn ? '#10b981' : '#ef4444'}}; border:1px solid ${{isAutopilotOn ? 'rgba(16,185,129,0.4)' : 'rgba(239,68,68,0.4)'}}; padding:0.2rem 0.6rem; border-radius:1rem; font-size:0.75rem; font-weight:900;">
                                        ${{isAutopilotOn ? '🟢 ATTIVO' : '⏸ IN PAUSA'}}
                                    </span>
                                </div>
                                <div style="font-size:1.15rem; font-weight:900; color:#fff; display:flex; align-items:center; justify-content:space-between;">
                                    <span>${{isAutopilotOn ? 'Autonomo H24' : 'Manuale'}}</span>
                                    <button onclick="toggleCampaignAutopilot('${{campToken}}')" style="background:rgba(255,255,255,0.08); color:#cbd5e1; border:1px solid rgba(255,255,255,0.15); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800; cursor:pointer;">
                                        ${{isAutopilotOn ? 'Metti in Pausa' : 'Attiva'}}
                                    </button>
                                </div>
                            </div>

                            <!-- WIDGET 2: OBIETTIVO GIORNALIERO -->
                            <div class="camp-widget-card" style="border-left:4px solid #38bdf8;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <span style="font-size:0.75rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Obiettivo Giornaliero:</span>
                                    <span id="assembly-ready-count-${{campToken}}" style="font-size:0.85rem; font-weight:900; color:#38bdf8;">
                                        ${{pendingSlots.length}} da Pubblicare
                                    </span>
                                </div>
                                <div style="display:flex; align-items:center; gap:0.6rem;">
                                    <span style="font-size:0.82rem; color:#cbd5e1;">Target Slot:</span>
                                    <select onchange="updateCampaignTargetCount('${{campToken}}', this.value)" style="background:rgba(0,0,0,0.5); border:1px solid rgba(56,189,248,0.4); color:#38bdf8; font-weight:900; font-size:0.88rem; padding:0.2rem 0.5rem; border-radius:0.4rem; outline:none; cursor:pointer;">
                                        <option value="1" ${{targetCount === 1 ? 'selected' : ''}}>1 video/giorno</option>
                                        <option value="2" ${{targetCount === 2 ? 'selected' : ''}}>2 video/giorno</option>
                                        <option value="3" ${{targetCount === 3 ? 'selected' : ''}}>3 video/giorno</option>
                                        <option value="4" ${{targetCount === 4 ? 'selected' : ''}}>4 video/giorno</option>
                                        <option value="5" ${{targetCount === 5 ? 'selected' : ''}}>5 video/giorno</option>
                                    </select>
                                </div>
                            </div>

                            <!-- WIDGET 3: SOTTOTITOLI & HOOK CARD VIRALE -->
                            <div class="camp-widget-card" style="border-left:4px solid #10b981;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <span style="font-size:0.75rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Sottotitoli &amp; Hook Card:</span>
                                    <span style="font-size:0.78rem; font-weight:900; color:#10b981; background:rgba(16,185,129,0.15); padding:0.15rem 0.5rem; border-radius:0.4rem;">
                                        🟢 Attivi (Hormozi Gold)
                                    </span>
                                </div>
                                <div style="font-size:0.78rem; color:#cbd5e1; display:flex; align-items:center; gap:0.3rem;">
                                    <span>🎓 Hook Card persistente impressa prima della coda</span>
                                </div>
                            </div>

                            <!-- WIDGET 4: STATO CAMPAGNA, PAUSA & TERMINAZIONE (A DESTRA DI SOTTOTITOLI & HOOK CARD) -->
                            <div class="camp-widget-card" id="camp-lifecycle-card-${{campToken}}" style="border-left:4px solid ${{isEnded ? '#ef4444' : isPaused ? '#f59e0b' : '#a855f7'}};">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <span style="font-size:0.75rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Pausa &amp; Termina:</span>
                                    <span id="camp-lifecycle-badge-${{campToken}}" style="font-size:0.72rem; font-weight:900; padding:0.15rem 0.5rem; border-radius:0.4rem; background:${{isEnded ? 'rgba(239,68,68,0.2)' : isPaused ? 'rgba(245,158,11,0.2)' : 'rgba(168,85,247,0.2)'}}; color:${{isEnded ? '#ef4444' : isPaused ? '#f59e0b' : '#c084fc'}}; border:1px solid ${{isEnded ? 'rgba(239,68,68,0.4)' : isPaused ? 'rgba(245,158,11,0.4)' : 'rgba(168,85,247,0.4)'}};">
                                        ${{isEnded ? '🛑 TERMINATA' : isPaused ? '⏸️ IN PAUSA' : '🟢 ATTIVA'}}
                                    </span>
                                </div>
                                <div id="camp-lifecycle-controls-${{campToken}}" style="display:flex; align-items:center; gap:0.35rem; flex-wrap:wrap; margin-top:0.1rem;">
                                    ${{isEnded ? `
                                        <div style="font-size:0.74rem; color:#ef4444; font-weight:700; width:100%;">Pubblicazioni terminate per sempre.</div>
                                        <button onclick="resumeCampaignLifecycle('${{campToken}}')" style="background:rgba(16,185,129,0.2); border:1px solid #10b981; color:#10b981; padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800; cursor:pointer;">
                                            ▶️ Riattiva Campagna
                                        </button>
                                    ` : isPaused ? `
                                        <div style="font-size:0.72rem; color:#fbbf24; font-weight:700; width:100%;">
                                            Pausa fino a: <strong>${{pauseUntilFormatted}}</strong>
                                        </div>
                                        <button onclick="resumeCampaignLifecycle('${{campToken}}')" style="background:linear-gradient(135deg, #10b981, #059669); border:none; color:#fff; padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800; cursor:pointer; box-shadow:0 2px 8px rgba(16,185,129,0.3);">
                                            ▶️ Riprendi Subito
                                        </button>
                                    ` : `
                                        <div style="display:flex; gap:0.3rem; width:100%;">
                                            <select id="pause-days-select-${{campToken}}" style="background:rgba(0,0,0,0.6); border:1px solid rgba(245,158,11,0.5); color:#fbbf24; font-size:0.72rem; font-weight:800; padding:0.2rem 0.35rem; border-radius:0.4rem; outline:none; cursor:pointer; flex:1;">
                                                <option value="1">Pausa 1 Giorno (24h)</option>
                                                <option value="2">Pausa 2 Giorni (48h)</option>
                                                <option value="3">Pausa 3 Giorni</option>
                                                <option value="7">Pausa 1 Settimana</option>
                                            </select>
                                            <button onclick="pauseCampaignLifecycle('${{campToken}}')" style="background:rgba(245,158,11,0.2); border:1px solid #f59e0b; color:#fbbf24; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800; cursor:pointer; white-space:nowrap;" title="Mette in pausa le pubblicazioni automatiche: dal giorno dopo riprendono regolarmente">
                                                ⏸️ Metti in Pausa
                                            </button>
                                        </div>
                                        <button onclick="endCampaignLifecycle('${{campToken}}')" style="background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.35); color:#fca5a5; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.70rem; font-weight:800; cursor:pointer; width:100%; text-align:center;" onmouseover="this.style.background='rgba(239,68,68,0.3)'" onmouseout="this.style.background='rgba(239,68,68,0.12)'" title="Termina per sempre le pubblicazioni di questa campagna">
                                            🛑 Termina per Sempre
                                        </button>
                                    `}}
                                </div>
                            </div>
                        </div>

                        <!-- TAB 1: CODA & CASCATA -->
                        <div id="camp-subtab-cascade-${{campToken}}" style="display:block;">
                            
                            <div class="cascade-waterfall-stream">
                                
                                <!-- BANNER STATO LIVE PER CLIPPING IN CORSO -->
                                <div id="assembly-clipping-live-banner-${{campToken}}" style="display:none; align-items:center; gap:0.8rem; background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.4); border-radius:0.85rem; padding:0.85rem 1.2rem; margin-bottom:1rem; color:#38bdf8; font-weight:800; font-size:0.85rem; box-shadow:0 0 15px rgba(56,189,248,0.25);"></div>

                                <!-- RETTANGOLO DINAMICO "STO PROCESSANDO" (COMPARE SOLO DURANTE L'UPLOAD) -->
                                <div id="assembly-active-processing-box-${{campToken}}" class="processing-active-card" style="display:none;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; margin-bottom:1rem; border-bottom:1px solid rgba(245,158,11,0.3); padding-bottom:0.8rem;">
                                        <div style="display:flex; align-items:center; gap:0.6rem;">
                                            <span class="processing-pulse-badge">
                                                <span class="pulse-dot"></span>
                                                ⚡ IN ELABORAZIONE: STO PROCESSANDO
                                            </span>
                                            <span id="processing-clip-title-${{campToken}}" style="font-weight:900; font-size:1.05rem; color:#fff;">Upload TikTok &amp; Sottomissione Klippify...</span>
                                        </div>
                                        <div style="display:flex; align-items:center; gap:0.6rem;">
                                            <span id="processing-elapsed-timer-${{campToken}}" style="background:rgba(0,0,0,0.6); color:#fbbf24; border:1px solid rgba(245,158,11,0.4); padding:0.3rem 0.7rem; border-radius:0.5rem; font-size:0.8rem; font-weight:900;">⏳ In corso...</span>
                                        </div>
                                    </div>
                                    <div style="display:grid; grid-template-columns:110px 1fr; gap:1.2rem; align-items:center;">
                                        <div style="background:#000; border-radius:0.8rem; padding:0.8rem; text-align:center; border:1px solid rgba(245,158,11,0.4); box-shadow:0 0 15px rgba(245,158,11,0.2);">
                                            <div style="font-size:2.2rem;">🚀</div>
                                            <div style="font-size:0.7rem; color:#fbbf24; font-weight:800; margin-top:0.3rem;">TikTok Studio</div>
                                        </div>
                                        <div>
                                            <div style="font-size:0.95rem; font-weight:800; color:#fff; margin-bottom:0.3rem;" id="processing-status-label-${{campToken}}">
                                                Caricamento video su TikTok Studio, verifica copyright e invio automatico a Klippify...
                                            </div>
                                            <div style="font-size:0.78rem; color:#cbd5e1; margin-bottom:0.7rem;" id="processing-clip-filename-${{campToken}}">
                                                clip.mp4
                                            </div>
                                            <div class="processing-animated-bar">
                                                <div class="processing-bar-fill"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- SLOT IN CODA DELLA GIORNATA (CON LOGICA A SCORRIMENTO) -->
                                ${{slotsMainViewHtml}}

                                <!-- ======================================================== -->
                                <!-- STRISCE COMPATTE IN BASSO (MAGAZZINO CLIP DI RISERVA)   -->
                                <!-- ======================================================== -->
                                <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(56,189,248,0.25); border-radius:1.2rem; padding:1.4rem; margin-top:0.8rem;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1rem;">
                                        <div>
                                            <div style="font-size:1.15rem; font-weight:900; color:#38bdf8; display:flex; align-items:center; gap:0.5rem;">
                                                <span>✂️ Magazzino Clip di Riserva</span>
                                                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; font-size:0.75rem; padding:0.2rem 0.6rem; border-radius:1rem; font-weight:800;">
                                                    ${{virginClips.length}} Pronte
                                                </span>
                                            </div>
                                            <div style="font-size:0.78rem; color:#94a3b8; margin-top:0.2rem;">
                                                Ogni video pubblicato farà scalare automaticamente le clip sottostanti di una posizione verso l'alto!
                                            </div>
                                        </div>
                                    </div>

                                    <div style="display:flex; flex-direction:column; gap:0.6rem;">
                                        ${{reserveRowsHtml}}
                                    </div>

                                    ${{publishedRowsHtml}}
                                </div>

                            </div>
                        </div>

                        <!-- TAB 2: MATERIA PRIMA & TAGLIO (GESTIONE VIDEO LUNGHI) -->
                        <div id="camp-subtab-raw-${{campToken}}" style="display:none;">
                            <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(245,158,11,0.3); border-radius:1.25rem; padding:1.5rem;">
                                
                                <!-- INPUT FILE NASCOSTO PER CARICAMENTO MULTIPLO -->
                                <input type="file" id="source-video-input-assembly-${{campToken}}" accept="video/*" multiple style="display:none;" onchange="uploadSourceVideoFiles(this, '${{campToken}}')">

                                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem; margin-bottom:1.2rem;">
                                    <div>
                                        <div style="font-size:1.2rem; font-weight:800; color:#fbbf24; display:flex; align-items:center; gap:0.5rem;">
                                            <span>📦 Materia Prima: Video Lunghi da Klippare</span>
                                            <span id="assembly-clipping-queue-count-${{campToken}}" style="background:rgba(245,158,11,0.2); color:#fbbf24; font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:0.4rem; font-weight:800;">${{rawVideos.length}} Video</span>
                                        </div>
                                        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:0.3rem;">
                                            Carica i file video completi del brand: Gemini e FFmpeg ritaglieranno le migliori clip verticali 9:16 che entreranno in coda.
                                        </div>
                                    </div>
                                    
                                    <div style="display:flex; gap:0.6rem; flex-wrap:wrap;">
                                        <button id="btn-upload-file-assembly-${{campToken}}" onclick="document.getElementById('source-video-input-assembly-${{campToken}}').click()" style="background:linear-gradient(135deg, #38bdf8, #0284c7); color:#fff; font-weight:800; border:none; padding:0.65rem 1.1rem; border-radius:0.6rem; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; box-shadow:0 4px 12px rgba(56,189,248,0.3); transition:transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
                                            📁 Carica da Computer
                                        </button>
                                        <button onclick="openLocalFolder('${{campToken}}')" style="background:rgba(255,255,255,0.1); color:#fff; font-weight:700; border:1px solid rgba(255,255,255,0.2); padding:0.65rem 0.9rem; border-radius:0.6rem; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                            📂 Apri Cartella
                                        </button>
                                    </div>
                                </div>

                                <!-- SEZIONE GESTIONE SPAZIO & AUTO-CLEANUP MP4 -->
                                <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.25); border-radius:0.9rem; padding:0.9rem 1.2rem; margin-bottom:1.2rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem;">
                                    <div style="display:flex; align-items:center; gap:0.6rem;">
                                        <span style="font-size:1.2rem;">🧹</span>
                                        <div>
                                            <div style="font-size:0.85rem; font-weight:800; color:#34d399;">Auto-Pulizia Spazio Disco Attiva</div>
                                            <div style="font-size:0.75rem; color:#94a3b8;">I video lunghi vengono eliminati dopo il ritaglio 9:16 e le clip dopo la pubblicazione su TikTok.</div>
                                        </div>
                                    </div>
                                    <button onclick="triggerStorageCleanup(this)" style="background:rgba(16,185,129,0.15); color:#34d399; border:1px solid rgba(16,185,129,0.35); font-weight:800; font-size:0.78rem; padding:0.4rem 0.8rem; border-radius:0.5rem; cursor:pointer; transition:all 0.15s;" onmouseover="this.style.background='rgba(16,185,129,0.25)'" onmouseout="this.style.background='rgba(16,185,129,0.15)'">
                                        🧹 Esegui Pulizia Adesso
                                    </button>
                                </div>

                                <!-- SEZIONE DOWNLOAD FONTI ONLINE (YOUTUBE / TIKTOK / INSTAGRAM / DRIVE) -->
                                <div style="background:rgba(0,0,0,0.35); border:1px solid rgba(56,189,248,0.25); border-radius:1rem; padding:1.2rem; margin-bottom:1.5rem;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; margin-bottom:0.8rem;">
                                        <div>
                                            <div style="font-size:0.95rem; font-weight:800; color:#38bdf8; display:flex; align-items:center; gap:0.4rem;">
                                                <span>📡 Fonti Online Automatiche</span>
                                                <span style="font-size:0.68rem; background:rgba(56,189,248,0.2); color:#38bdf8; padding:0.15rem 0.45rem; border-radius:0.3rem; font-weight:700;">YouTube • TikTok • Instagram • Drive</span>
                                            </div>
                                            <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.15rem;">
                                                Incolla il link di un canale YouTube (@creator), profilo TikTok, Instagram Reel o cartella Drive per ispezionare e scaricare con 1 clic.
                                            </div>
                                        </div>
                                        <div id="saved-campaign-sources-${{campToken}}" style="display:flex; flex-wrap:wrap; gap:0.4rem;"></div>
                                    </div>

                                    <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                                        <input type="text" id="source-url-input-${{campToken}}" placeholder="https://www.youtube.com/@CanaleCreator/videos o link TikTok/IG/Drive..." style="flex:1; min-width:260px; background:#0f172a; border:1px solid rgba(56,189,248,0.3); border-radius:0.6rem; padding:0.65rem 0.9rem; color:#fff; font-size:0.82rem; outline:none;" onfocus="this.style.borderColor='#38bdf8'" onblur="this.style.borderColor='rgba(56,189,248,0.3)'">
                                        <button id="btn-inspect-source-${{campToken}}" onclick="inspectSourceUrl('${{campToken}}')" style="background:linear-gradient(135deg, #0284c7, #0369a1); color:#fff; font-weight:800; border:none; padding:0.65rem 1rem; border-radius:0.6rem; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; gap:0.3rem; transition:transform 0.15s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='none'">
                                            🔍 Ispeziona Video
                                        </button>
                                        <button onclick="saveCampaignSourceFromUI('${{campToken}}')" style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); padding:0.65rem 0.9rem; border-radius:0.6rem; font-size:0.82rem; font-weight:700; cursor:pointer; transition:all 0.15s;" title="Salva canale per il monitoraggio periodico" onmouseover="this.style.background='rgba(56,189,248,0.25)'" onmouseout="this.style.background='rgba(56,189,248,0.15)'">
                                            💾 Salva per 24/7
                                        </button>
                                    </div>

                                    <!-- RISULTATI ISPEZIONE VIDEO CON THUMBNAIL -->
                                    <div id="source-inspect-results-${{campToken}}" style="display:none; margin-top:0.8rem;"></div>
                                </div>

                                <div id="assembly-clipping-queue-list-${{campToken}}" style="display:flex; flex-direction:column; gap:0.6rem; margin-top:0.8rem;">
                                    <div style="text-align:center; padding:1rem; color:var(--text-muted); font-size:0.85rem;">⏳ Caricamento coda video lunghi...</div>
                                </div>

                                ${{validLinks.length > 0 ? `
                                    <div style="margin-top:1.5rem; padding-top:1.2rem; border-top:1px solid rgba(255,255,255,0.08);">
                                        <div style="font-size:0.88rem; font-weight:800; color:#38bdf8; margin-bottom:0.6rem;">
                                            🔗 Materiale Ufficiale Brand (Drive / WeTransfer / YouTube):
                                        </div>
                                        ${{allLinksHtml}}
                                    </div>
                                ` : ''}}
                            </div>
                        </div>

                        <!-- TAB: PROMPT & STORYBOARD -->
                        <div id="camp-subtab-prompts-${{campToken}}" style="display:none;">
                            <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(139,92,246,0.3); border-radius:1.25rem; padding:1.5rem; display:flex; flex-direction:column; gap:1.2rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem;">
                                    <div>
                                        <h4 style="color:#c084fc; font-size:1.15rem; font-weight:800; margin:0;">💡 Prompt Gemini Veo &amp; Storyboard AI</h4>
                                        <div style="font-size:0.8rem; color:#cbd5e1; margin-top:0.2rem;">Copie pronte per generare nuovi video su Gemini o ispirare i tagli.</div>
                                    </div>
                                    <span style="background:rgba(139,92,246,0.2); color:#c084fc; border:1px solid rgba(139,92,246,0.4); padding:0.25rem 0.7rem; border-radius:0.5rem; font-size:0.75rem; font-weight:800;">
                                        ${{scripts.length}} Varianti Script
                                    </span>
                                </div>
                                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.2rem;">
                                    ${{scripts.map((sc, sci) => `
                                        <div style="background:rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.08); border-radius:0.9rem; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; gap:1rem;">
                                            <div>
                                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
                                                    <span style="font-weight:900; color:#38bdf8; font-size:0.92rem;">#${{sci+1}} ${{sc.concept_name || 'Variante Script'}}</span>
                                                    <button onclick="copyToClipboard('${{(sc.video_prompt_gemini || '').replace(/'/g, "\\\\'")}}' )" style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.35); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.72rem; font-weight:800; cursor:pointer;">
                                                        📋 Copia Prompt
                                                    </button>
                                                </div>
                                                <div style="font-size:0.78rem; color:#cbd5e1; background:rgba(0,0,0,0.4); padding:0.8rem; border-radius:0.6rem; font-family:monospace; line-height:1.45; border:1px solid rgba(255,255,255,0.05); margin-bottom:0.8rem; max-height:160px; overflow-y:auto;">
                                                    ${{sc.video_prompt_gemini || 'Nessun prompt'}}
                                                </div>
                                                <div style="font-size:0.78rem; color:#a78bfa; font-weight:700;">
                                                    📝 TikTok Caption: <span style="color:#e2e8f0; font-weight:normal;">${{sc.tiktok_caption || ''}}</span>
                                                </div>
                                            </div>
                                        </div>
                                    `).join('')}}
                                </div>
                            </div>
                        </div>

                        <!-- TAB 3: DATI & PERFORMANCE -->
                        <div id="camp-subtab-analytics-${{campToken}}" style="display:none;">
                            <div style="display:flex; flex-direction:column; gap:1.5rem;">
                                ${{dailyStatsHtml}}
                            </div>
                        </div>

                        <!-- TAB 4: REGOLE & BRIEF -->
                        <div id="camp-subtab-brief-${{campToken}}" style="display:none;">
                            <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); border-radius:1.25rem; padding:1.5rem; display:flex; flex-direction:column; gap:1.2rem;">
                                <div>
                                    <h4 style="color:#f8fafc; font-size:1.1rem; font-weight:800; margin:0 0 0.5rem 0;">📋 Brief Ufficiale</h4>
                                    <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.5; background:rgba(0,0,0,0.3); padding:0.9rem; border-radius:0.6rem;">
                                        ${{originalBrief}}
                                    </div>
                                </div>

                                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:1rem;">
                                    <div style="background:rgba(0,0,0,0.3); padding:0.8rem; border-radius:0.6rem;">
                                        <div style="font-size:0.72rem; color:#a78bfa; font-weight:800; text-transform:uppercase;">Hashtag Obbligatori</div>
                                        <div style="font-size:0.85rem; color:#fff; font-weight:700; margin-top:0.3rem;">${{originalHashtags}}</div>
                                    </div>
                                    <div style="background:rgba(0,0,0,0.3); padding:0.8rem; border-radius:0.6rem;">
                                        <div style="font-size:0.72rem; color:#a78bfa; font-weight:800; text-transform:uppercase;">Tag Creator (@)</div>
                                        <div style="font-size:0.85rem; color:#fff; font-weight:700; margin-top:0.3rem;">${{originalMentions}}</div>
                                    </div>
                                    <div style="background:rgba(0,0,0,0.3); padding:0.8rem; border-radius:0.6rem;">
                                        <div style="font-size:0.72rem; color:#a78bfa; font-weight:800; text-transform:uppercase;">Call to Action (CTA)</div>
                                        <div style="font-size:0.85rem; color:#fff; font-weight:700; margin-top:0.3rem;">${{originalCTA}}</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            `;
        }}

        function renderCampaignDetailContent(campToken) {{
            const detailContainer = document.getElementById('my-campaign-detail-content');
            
            const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {{}};
            const item = generatedContent.find(gc => gc.campaign_id === campToken) || {{}};
            const publishedItems = (typeof publishedContent !== 'undefined' ? publishedContent : []).filter(pc => pc.campaign_id === campToken);
            
            const classifiedInfo = activeCampaignsClassified.find(ac => 
                ac.id === campToken || 
                ac.campaign_token === campToken || 
                ac.campaign_id === campToken ||
                (originalCamp.name && ac.name && ac.name.toLowerCase() === originalCamp.name.toLowerCase())
            ) || {{}};
            const isClipping = classifiedInfo.category === 'CLIPPING' || 
                               (classifiedInfo.drive_links && classifiedInfo.drive_links.length > 0) ||
                               (classifiedInfo.all_links && classifiedInfo.all_links.some(l => l.type === 'drive' || l.type === 'wetransfer' || l.type === 'youtube' || l.type === 'reel')) ||
                               (originalCamp.description && (
                                   originalCamp.description.toLowerCase().includes('podcast') || 
                                   originalCamp.description.toLowerCase().includes('clip') ||
                                   originalCamp.description.toLowerCase().includes('taglia') ||
                                   originalCamp.description.toLowerCase().includes('youtube') ||
                                   originalCamp.description.toLowerCase().includes('drive')
                               ));
            
            const originalBrief = originalCamp.description || 'Nessun brief fornito.';
            const originalHashtags = (originalCamp.mandatory_hashtags || []).join(', ') || '#klippify';
            const originalMentions = (originalCamp.mandatory_mentions || []).join(', ') || 'Nessuna';
            const originalCTA = originalCamp.call_to_action || 'Guarda il video completo su Klippify!';
            const originalRules = (originalCamp.rules || ['Segui le linee guida Klippify']).map(r => `<li>✓ ${{r}}</li>`).join('');
            const originalRulesText = (originalCamp.rules || ['Segui le linee guida Klippify']).join(', ');
            
            const budgetRemaining = parseFloat(originalCamp.budget_remaining) || 0;
            const isDepleted = budgetRemaining <= 0 && originalCamp.budget_remaining !== undefined;
            
            const warningBanner = isDepleted ? `
                <div style="background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; border-radius: 1rem; padding: 1.5rem; text-align: center; margin-bottom: 2rem; animation: pulse 2s infinite;">
                    <h3 style="color: #fca5a5; margin-bottom: 0.5rem; font-size: 1.5rem;">🛑 ATTENZIONE: BUDGET CAMPAGNA ESAURITO 🛑</h3>
                    <p style="color: #f8fafc; font-weight: bold;">Questa campagna non ha più fondi residui su Klippify. È sconsigliato produrre o pubblicare altri video.</p>
                </div>
            ` : '';

            // ELENCO COMPLETO DI TUTTI I LINK E RISORSE DELLA CAMPAGNA
            const allLinksRaw = [];
            (classifiedInfo.drive_links || []).forEach(d => allLinksRaw.push({{ type: 'drive', title: d.title || 'Cartella Google Drive / WeTransfer', url: d.url }}));
            (classifiedInfo.resource_links || []).forEach(r => allLinksRaw.push({{ type: 'resource', title: r.title || 'Video / File Risorsa', url: r.url }}));
            (classifiedInfo.all_extracted_links || []).forEach(u => {{
                if (!allLinksRaw.some(x => x.url === u)) {{
                    allLinksRaw.push({{ type: 'link', title: u, url: u }});
                }}
            }});

            // Filtra duplicati e link non rilevanti
            const validLinks = allLinksRaw.filter(l => l.url && !l.url.includes('signin') && !l.url.includes('signup') && !l.url.includes('dashboard'));

            let allLinksHtml = '';
            if (validLinks.length > 0) {{
                allLinksHtml += '<div style="display:flex; flex-direction:column; gap:0.6rem; margin-top:0.8rem;">';
                validLinks.forEach((l, lIdx) => {{
                    let badgeBg = 'rgba(59,130,246,0.2)';
                    let badgeColor = '#60a5fa';
                    let icon = '📁';
                    let typeName = 'Google Drive';

                    if (l.url.includes('we.tl') || l.url.includes('wetransfer')) {{
                        badgeBg = 'rgba(236,72,153,0.2)';
                        badgeColor = '#f472b6';
                        icon = '📦';
                        typeName = 'WeTransfer';
                    }} else if (l.url.includes('youtube.com') || l.url.includes('youtu.be')) {{
                        badgeBg = 'rgba(239,68,68,0.2)';
                        badgeColor = '#f87171';
                        icon = '▶️';
                        typeName = 'YouTube';
                    }} else if (l.url.includes('dropbox')) {{
                        badgeBg = 'rgba(14,165,233,0.2)';
                        badgeColor = '#38bdf8';
                        icon = '📂';
                        typeName = 'Dropbox';
                    }} else {{
                        badgeBg = 'rgba(139,92,246,0.2)';
                        badgeColor = '#c084fc';
                        icon = '🔗';
                        typeName = 'Risorsa Web';
                    }}

                    allLinksHtml += `
                        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.08); border-radius:0.6rem; padding:0.7rem 1rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem;">
                            <div style="display:flex; align-items:center; gap:0.6rem; flex:1; min-width:240px;">
                                <span style="background:${{badgeBg}}; color:${{badgeColor}}; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.75rem; font-weight:800; white-space:nowrap;">
                                    ${{icon}} ${{typeName}}
                                </span>
                                <a href="${{l.url}}" target="_blank" style="color:#e2e8f0; font-size:0.82rem; word-break:break-all; text-decoration:none;" onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'">
                                    ${{l.url}}
                                </a>
                            </div>
                            <a href="${{l.url}}" target="_blank" style="background:rgba(255,255,255,0.1); hover:background:rgba(255,255,255,0.2); color:#fff; text-decoration:none; padding:0.4rem 0.8rem; border-radius:0.4rem; font-size:0.78rem; font-weight:bold; display:flex; align-items:center; gap:0.4rem; transition:background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                🔗 Apri Link
                            </a>
                        </div>
                    `;
                }});
                allLinksHtml += '</div>';
            }} else {{
                allLinksHtml = '<div style="color:var(--text-muted); font-size:0.82rem; margin-top:0.5rem;">Nessun link esterno o Drive fornito per questa campagna.</div>';
            }}

            // Schedulatore e Slot Giornalieri
            const savedSchedule = campaignSchedules[campToken] || {{}};
            const targetCount = savedSchedule.target_count || 3;
            const savedSlots = savedSchedule.slots || [];

            const defaultTimes = ["12:00", "16:30", "20:00", "22:00", "09:30", "14:00", "18:00", "21:00"];

            const scripts = item.scripts && item.scripts.length > 0 ? item.scripts : [
                {{
                    concept_name: isClipping ? "Clip Saliente 1 (9:16)" : "Hook Emotivo & Relatable",
                    video_prompt_gemini: `Vertical 9:16 video, 15-30s. Dynamic TikTok format for ${{originalCamp.name}}. Visual hook in first 2s. Respect rules: ${{originalRulesText}}. Include CTA: ${{originalCTA}}.`,
                    tiktok_caption: `Scopri ${{originalCamp.name}}! ✨ ${{originalHashtags}} ${{originalMentions}}`,
                    storyboard: [
                        {{ duration: "0-3s", description: "Hook visivo forte", text_overlay: "Non ci crederai mai..." }},
                        {{ duration: "3-10s", description: "Sviluppo del concept", text_overlay: "Guarda fino alla fine!" }},
                        {{ duration: "10-15s", description: "Call to Action finale", text_overlay: "${{originalCTA}}" }}
                    ]
                }}
            ];

            let slotsHtml = '';
            for (let i = 0; i < targetCount; i++) {{
                const slotTime = (savedSlots[i] && savedSlots[i].time) ? savedSlots[i].time : (defaultTimes[i] || "12:00");
                const savedVideo = (savedSlots[i] && savedSlots[i].video) ? savedSlots[i].video : "";
                
                const scriptIndex = i % scripts.length;
                const script = scripts[scriptIndex] || {{}};
                const conceptName = script.concept_name || (isClipping ? `Clip Ritagliata ${{i+1}}` : `Slot Video ${{i+1}}`);
                const promptText = script.video_prompt_gemini || `Genera video 9:16 per ${{originalCamp.name}}`;
                const captionText = script.tiktok_caption || `${{originalHashtags}} ${{originalMentions}}`;

                let videoOptionsHtml = '<option value="">-- Seleziona un Video MP4 generato/ritagliato --</option>';
                const campIsolatedVidsClassic = getCampaignIsolatedVideos(campToken);
                campIsolatedVidsClassic.forEach(v => {{
                    const isSel = (v.filename === savedVideo) ? 'selected' : '';
                    videoOptionsHtml += `<option value="${{v.filename}}" ${{isSel}}>${{v.filename}}</option>`;
                }});

                const storyboardHtml = (script.storyboard || []).map((s, si) =>
                    `<div style="display:flex; gap:0.6rem; align-items:flex-start; padding:0.4rem 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:0.75rem;">`
                    + `<div style="min-width:32px; height:32px; border-radius:0.4rem; background:rgba(255,255,255,0.08); display:flex; align-items:center; justify-content:center; font-weight:700;">S${{si+1}}</div>`
                    + `<div><strong style="color:#f8fafc;">⏱ ${{s.duration}}</strong> - <span style="color:#94a3b8;">${{s.description}}</span> <div style="color:#38bdf8; margin-top:0.1rem;">💬 "${{s.text_overlay}}"</div></div></div>`
                ).join('');

                const hasVideo = !!savedVideo;

                let leftColumnHtml = '';
                if (isClipping) {{
                    leftColumnHtml = `
                        <!-- CLIPPING WORKFLOW CARD (PROMPT VEO RIMOSSO) -->
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.25); border-radius:0.8rem; padding:1rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span style="font-weight:800; font-size:0.85rem; color:#fbbf24;">✂️ Dettagli Clip Ritagliata 9:16</span>
                                    <span style="background:rgba(245,158,11,0.2); color:#fbbf24; padding:0.2rem 0.5rem; border-radius:0.4rem; font-size:0.72rem; font-weight:bold;">Da Materiale Sorgente</span>
                                </div>
                                <div style="font-size:0.82rem; color:#e2e8f0; line-height:1.45; background:rgba(0,0,0,0.3); padding:0.6rem; border-radius:0.5rem;">
                                    🎬 <strong>Concept:</strong> ${{conceptName}}<br>
                                    💡 <em>Questa clip viene estratta direttamente dal materiale video sorgente fornito dal brand.</em>
                                </div>
                            </div>

                            <!-- TIKTOK CAPTION BOX -->
                            <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.25); border-radius:0.8rem; padding:1rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span style="font-weight:800; font-size:0.85rem; color:#34d399;">📱 Caption TikTok & Tag Obbligatori</span>
                                    <button onclick="copyToClipboard(decodeURIComponent('${{encodeURIComponent(captionText)}}'), this)" style="background:linear-gradient(135deg,#10b981,#059669); color:#fff; border:none; padding:0.3rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:bold; cursor:pointer;">📋 Copia</button>
                                </div>
                                <div id="slot-caption-${{i}}" style="font-size:0.82rem; color:#e2e8f0; line-height:1.4; background:rgba(0,0,0,0.3); padding:0.6rem; border-radius:0.5rem;">${{captionText}}</div>
                            </div>
                        </div>
                    `;
                }} else {{
                    leftColumnHtml = `
                        <!-- AI GENERATION WORKFLOW (PROMPT GEMINI VEO) -->
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            
                            <!-- PROMPT GEMINI BOX -->
                            <div style="background:rgba(139,92,246,0.06); border:1px solid rgba(139,92,246,0.25); border-radius:0.8rem; padding:1rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span style="font-weight:800; font-size:0.85rem; color:#c084fc;">🤖 Prompt Video per Gemini Veo</span>
                                    <div style="display:flex; gap:0.5rem;">
                                        <button onclick="copyToClipboard(decodeURIComponent('${{encodeURIComponent(promptText)}}'), this)" style="background:rgba(255,255,255,0.1); color:#fff; border:none; padding:0.3rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:bold; cursor:pointer;">📋 Copia</button>
                                        <button onclick="generateVideoFromSlot('${{campToken}}', decodeURIComponent('${{encodeURIComponent(promptText)}}'), this)" style="background:linear-gradient(135deg,#8b5cf6,#4f46e5); color:#fff; border:none; padding:0.3rem 0.8rem; border-radius:0.4rem; font-size:0.75rem; font-weight:bold; cursor:pointer; box-shadow:0 2px 8px rgba(139,92,246,0.4);">🤖 Genera con Bot</button>
                                    </div>
                                </div>
                                <div style="font-size:0.82rem; color:#e2e8f0; line-height:1.45; max-height:90px; overflow-y:auto; background:rgba(0,0,0,0.3); padding:0.6rem; border-radius:0.5rem;">${{promptText}}</div>
                            </div>

                            <!-- TIKTOK CAPTION BOX -->
                            <div style="background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.25); border-radius:0.8rem; padding:1rem;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span style="font-weight:800; font-size:0.85rem; color:#34d399;">📱 Caption TikTok & Tag Obbligatori</span>
                                    <button onclick="copyToClipboard(decodeURIComponent('${{encodeURIComponent(captionText)}}'), this)" style="background:linear-gradient(135deg,#10b981,#059669); color:#fff; border:none; padding:0.3rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:bold; cursor:pointer;">📋 Copia</button>
                                </div>
                                <div id="slot-caption-${{i}}" style="font-size:0.82rem; color:#e2e8f0; line-height:1.4; background:rgba(0,0,0,0.3); padding:0.6rem; border-radius:0.5rem;">${{captionText}}</div>
                            </div>

                            <!-- STORYBOARD PREVIEW -->
                            <details style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:0.8rem;">
                                <summary style="font-size:0.8rem; font-weight:700; color:#38bdf8; cursor:pointer;">🎬 Storyboard Dettagliato (Scene & Testi)</summary>
                                <div style="margin-top:0.6rem; max-height:140px; overflow-y:auto;">
                                    ${{storyboardHtml}}
                                </div>
                            </details>

                        </div>
                    `;
                }}

                slotsHtml += `
                    <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); border-radius:1.2rem; padding:1.5rem; display:flex; flex-direction:column; gap:1.2rem; box-shadow:0 8px 20px rgba(0,0,0,0.3);">
                        
                        <!-- SLOT TOP BAR -->
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:1rem;">
                            <div style="display:flex; align-items:center; gap:0.8rem;">
                                <span style="background:${{isClipping ? 'linear-gradient(135deg, #f59e0b, #d97706)' : 'linear-gradient(135deg, #8b5cf6, #4f46e5)'}}; color:#000; padding:0.3rem 0.8rem; border-radius:0.6rem; font-weight:800; font-size:0.85rem;">
                                    ⏰ Slot ${{i+1}}
                                </span>
                                <div style="display:flex; align-items:center; gap:0.4rem;">
                                    <span style="font-size:0.8rem; color:var(--text-muted);">Orario:</span>
                                    <input type="time" value="${{slotTime}}" onchange="saveCampaignSlotTime('${{campToken}}', ${{i}}, this.value)" style="background:rgba(0,0,0,0.5); border:1px solid rgba(139,92,246,0.4); color:#38bdf8; border-radius:0.4rem; padding:0.25rem 0.5rem; font-weight:bold; font-size:0.85rem;">
                                </div>
                            </div>
                            <div style="display:flex; align-items:center; gap:0.8rem;">
                                <h3 style="margin:0; font-size:1.05rem; color:#fff;">🎬 ${{conceptName}}</h3>
                                <span id="slot-status-badge-${{i}}" style="background:${{hasVideo ? 'rgba(56,189,248,0.2)' : 'rgba(245,158,11,0.2)'}}; color:${{hasVideo ? '#38bdf8' : '#fbbf24'}}; padding:0.2rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700;">
                                    ${{hasVideo ? '🔵 Video Pronto' : '🟡 Da Caricare/Tagliare'}}
                                </span>
                            </div>
                        </div>

                        <!-- 2-COLUMNS WORKFLOW -->
                        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:1.5rem;">
                            
                            <!-- LEFT COLUMN -->
                            ${{leftColumnHtml}}

                            <!-- RIGHT: VIDEO PREVIEW & TIKTOK UPLOAD -->
                            <div style="background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.06); border-radius:0.8rem; padding:1rem; display:flex; flex-direction:column; justify-content:space-between; gap:1rem;">
                                <div>
                                    <span style="font-weight:800; font-size:0.85rem; color:#38bdf8; display:block; margin-bottom:0.6rem;">🎥 Video MP4 Associato (9:16)</span>
                                    <select id="slot-video-select-${{i}}" onchange="onSlotVideoChange(this, ${{i}}, '${{campToken}}')" style="width:100%; background:rgba(15,23,42,0.9); border:1px solid rgba(255,255,255,0.2); color:#fff; border-radius:0.5rem; padding:0.5rem; font-size:0.8rem; margin-bottom:0.8rem;">
                                        ${{videoOptionsHtml}}
                                    </select>
                                    
                                    <video id="slot-video-player-${{i}}" src="${{savedVideo ? '/generated_videos/' + encodeURIComponent(savedVideo) : ''}}" controls preload="metadata" playsinline style="width:100%; max-height:260px; min-height:160px; border-radius:0.6rem; background:#000; display:${{hasVideo ? 'block' : 'none'}}; outline:none; box-shadow:0 4px 14px rgba(0,0,0,0.5);"></video>
                                </div>

                                <div style="display:flex; flex-direction:column; gap:0.5rem;">
                                    <button onclick="publishVideoFromSlot('${{campToken}}', ${{i}}, this)" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; border:none; padding:0.7rem 1rem; border-radius:0.6rem; font-weight:800; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:0.5rem; box-shadow:0 4px 12px rgba(16,185,129,0.3); transition:all 0.2s;">
                                        🚀 Pubblica questo Video su TikTok
                                    </button>
                                    <div style="font-size:0.72rem; color:var(--text-muted); text-align:center;">Invia direttamente a TikTok con titolo e tag precompilati</div>
                                </div>
                            </div>

                        </div>
                    </div>
                `;
            }}

            // Storico Video Inviati ESCLUSIVAMENTE per questa specifica campagna
            const campSubmissions = (typeof klippifySubmissions !== 'undefined' ? klippifySubmissions : []).filter(s => {{
                if (s.campaign_id && (s.campaign_id === campToken || s.campaign_id === originalCamp.id || s.campaign_id === originalCamp.campaign_token)) return true;
                if (originalCamp.name && s.campaign_name && originalCamp.name.trim().toLowerCase() === s.campaign_name.trim().toLowerCase()) return true;
                return false;
            }});

            let publishedHtml = '';
            if (campSubmissions.length === 0) {{
                publishedHtml = `
                    <div style="padding:2.5rem 1.5rem; text-align:center; background:rgba(0,0,0,0.2); border:1px dashed rgba(255,255,255,0.1); border-radius:1rem;">
                        <div style="font-size:2.2rem; margin-bottom:0.5rem;">📭</div>
                        <div style="font-size:1.05rem; font-weight:700; color:#e2e8f0; margin-bottom:0.3rem;">Nessun video inviato per questa campagna</div>
                        <div style="font-size:0.82rem; color:var(--text-muted); max-width:480px; margin:0 auto; line-height:1.4;">Non risultano video sottomessi su Klippify per <strong>${{originalCamp.name || 'questa campagna'}}</strong>. Quando pubblicherai e invierai una clip, comparirà qui con visualizzazioni, mi piace, validazione AI e guadagni reali.</div>
                    </div>
                `;
            }} else {{
                publishedHtml = `<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:1.2rem;">`;
                campSubmissions.forEach(sub => {{
                    const isRejected = sub.status === 'rejected';
                    const isAccepted = sub.status === 'accepted';

                    const statusBadge = isAccepted
                        ? '<span style="background:rgba(16,185,129,0.2); color:#34d399; border:1px solid rgba(16,185,129,0.4); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:800;">✅ Approvato & Verificato AI</span>'
                        : isRejected
                            ? '<span style="background:rgba(239,68,68,0.25); color:#ef4444; border:1px solid rgba(239,68,68,0.5); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:900;">❌ RIFIUTATO DALL&#39;AI</span>'
                            : '<span style="background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid rgba(245,158,11,0.35); padding:0.25rem 0.6rem; border-radius:0.4rem; font-size:0.75rem; font-weight:800;">⏳ In Revisione</span>';
                    
                    const dateFormatted = sub.created_at ? new Date(sub.created_at).toLocaleDateString('it-IT', {{ day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit' }}) : 'N/D';

                    const cardBg = isRejected 
                        ? 'background:linear-gradient(180deg, rgba(30,15,20,0.95), rgba(15,23,42,0.95)); border:1px solid rgba(239,68,68,0.45); box-shadow:0 8px 25px rgba(239,68,68,0.15);' 
                        : isAccepted
                            ? 'background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); box-shadow:0 8px 20px rgba(0,0,0,0.3);'
                            : 'background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); box-shadow:0 8px 20px rgba(0,0,0,0.3);';

                    let aiBoxHtml = '';
                    if (isRejected) {{
                        aiBoxHtml = `
                            <div style="margin-top:0.8rem; background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.45); border-left:4px solid #ef4444; border-radius:0.6rem; padding:0.85rem 1rem;">
                                <div style="font-size:0.85rem; font-weight:900; color:#f87171; display:flex; align-items:center; gap:0.4rem; margin-bottom:0.35rem;">
                                    <span>⚠️ Motivo del Rifiuto (AI Klippify):</span>
                                </div>
                                <div style="font-size:0.82rem; color:#fecaca; line-height:1.45; font-weight:600;">
                                    ${{sub.ai_reasoning || 'Il video non rispetta una o più linee guida obbligatorie della campagna (CTA mancante, durata errata o tag assente).'}}
                                </div>
                            </div>
                        `;
                    }} else if (sub.ai_reasoning) {{
                        aiBoxHtml = `
                            <div style="margin-top:0.8rem; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25); border-left:4px solid #10b981; border-radius:0.6rem; padding:0.7rem 0.9rem; font-size:0.78rem; color:#cbd5e1; line-height:1.4;">
                                <strong style="color:#34d399;">🤖 Verifica AI Klippify:</strong> ${{sub.ai_reasoning}}
                            </div>
                        `;
                    }}

                    publishedHtml += `
                        <div style="${{cardBg}} border-radius:1rem; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; gap:0.8rem;">
                            <div>
                                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:0.5rem; margin-bottom:0.6rem;">
                                    <div>
                                        <div style="font-size:0.78rem; color:#a78bfa; font-weight:800; text-transform:uppercase;">${{sub.campaign_name || 'Campagna Klippify'}}</div>
                                        <div style="font-size:0.72rem; color:#64748b;">ID: ${{sub.id || 'N/D'}}</div>
                                    </div>
                                    ${{statusBadge}}
                                </div>

                                <div style="margin-bottom:0.8rem;">
                                    <a href="${{sub.post_url}}" target="_blank" style="display:flex; align-items:center; justify-content:space-between; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.25); color:#38bdf8; text-decoration:none; padding:0.5rem 0.8rem; border-radius:0.6rem; font-size:0.8rem; font-weight:700; transition:all 0.2s;" onmouseover="this.style.background='rgba(56,189,248,0.2)'" onmouseout="this.style.background='rgba(56,189,248,0.08)'">
                                        <span style="display:flex; align-items:center; gap:0.4rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                                            <span>🔗</span> <span>${{sub.post_url}}</span>
                                        </span>
                                        <span style="font-size:0.75rem; flex-shrink:0; margin-left:0.4rem;">↗</span>
                                    </a>
                                </div>

                                <!-- REAL STATS GRID FROM KLIPPIFY API -->
                                <div style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.05); border-radius:0.7rem; padding:0.8rem; display:grid; grid-template-columns:repeat(3, 1fr); gap:0.6rem; text-align:center;">
                                    <div>
                                        <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Views Reali</div>
                                        <div style="font-size:1.1rem; font-weight:900; color:#38bdf8;">${{(sub.views || 0).toLocaleString()}}</div>
                                    </div>
                                    <div>
                                        <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Likes Reali</div>
                                        <div style="font-size:1.1rem; font-weight:900; color:#f43f5e;">${{(sub.likes || 0).toLocaleString()}}</div>
                                    </div>
                                    <div>
                                        <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Guadagno</div>
                                        <div style="font-size:1.1rem; font-weight:900; color:#34d399;">$${{(sub.earnings || 0).toFixed(2)}}</div>
                                    </div>
                                </div>

                                ${{aiBoxHtml}}
                            </div>

                            <div style="font-size:0.7rem; color:#64748b; border-top:1px solid rgba(255,255,255,0.05); padding-top:0.6rem; display:flex; justify-content:space-between;">
                                <span>📅 Inviato: ${{dateFormatted}}</span>
                                <span>🎵 TikTok API Reale</span>
                            </div>
                        </div>
                    `;
                }});
                publishedHtml += `</div>`;
            }}

            const dailyStatsHtml = buildCampaignDailyStatsHtml(campToken, originalCamp, campSubmissions, targetCount);
            const assemblyPipelineHtml = buildCampaignAssemblyPipelineHtml(
                campToken, originalCamp, item, isClipping, localAvailableVideos, 
                savedSlots, targetCount, campSubmissions, scripts, defaultTimes, 
                budgetRemaining, isDepleted, validLinks, allLinksHtml, dailyStatsHtml
            );

            detailContainer.innerHTML = `
                <!-- TOP VIEW MODE SWITCHER -->
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1.5rem; background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); border-radius:1rem; padding:0.65rem 1.2rem; box-shadow:0 8px 24px rgba(0,0,0,0.3);">
                    <div style="display:flex; align-items:center; gap:0.6rem;">
                        <span style="font-size:0.85rem; font-weight:800; color:#cbd5e1;">🏭 MODALITÀ DASHBOARD:</span>
                        <span style="font-size:0.75rem; background:rgba(16,185,129,0.15); color:#34d399; padding:0.2rem 0.5rem; border-radius:0.4rem; font-weight:800;">Nuovo Sistema Autonomo</span>
                    </div>
                    <div style="display:inline-flex; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.1); border-radius:0.8rem; padding:0.25rem; gap:0.4rem;">
                        <button id="tab-btn-assembly-${{campToken}}" onclick="switchCampaignViewMode('${{campToken}}', 'assembly')" style="background:linear-gradient(135deg, #10b981, #059669); color:#ffffff; border:none; padding:0.45rem 1.1rem; border-radius:0.6rem; font-weight:800; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; box-shadow:0 4px 15px rgba(16,185,129,0.35); transition:all 0.2s;">
                            🏭 Catena di Montaggio (Automatica & Compatta)
                        </button>
                        <button id="tab-btn-classic-${{campToken}}" onclick="switchCampaignViewMode('${{campToken}}', 'classic')" style="background:transparent; color:#94a3b8; border:1px solid rgba(255,255,255,0.1); padding:0.45rem 1.1rem; border-radius:0.6rem; font-weight:800; font-size:0.82rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;">
                            📊 Vista Classica Dettagliata
                        </button>
                    </div>
                </div>

                <!-- 1. VISTA CATENA DI MONTAGGIO AUTOMATICA -->
                ${{assemblyPipelineHtml}}

                <!-- 2. VISTA CLASSICA DETTAGLIATA (PRESERVATA AL 100%) -->
                <div id="camp-classic-view-${{campToken}}" style="display:none;">
                    <div style="background:rgba(30,41,59,0.9); border:1px solid rgba(255,255,255,0.1); border-radius:1.5rem; box-shadow:0 20px 40px rgba(0,0,0,0.4); overflow:hidden; padding:2rem;">
                        
                        ${{warningBanner}}

                        <!-- CAMPAIGN HEADER -->
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.5rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
                            <div>
                                <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem;">
                                    <h2 style="font-size:1.8rem; font-weight:900; color:#f8fafc; margin:0;">${{originalCamp.name}}</h2>
                                    <span style="background:${{isClipping ? 'rgba(245,158,11,0.2)' : 'rgba(139,92,246,0.2)'}}; color:${{isClipping ? '#fbbf24' : '#c084fc'}}; border:1px solid ${{isClipping ? 'rgba(245,158,11,0.4)' : 'rgba(139,92,246,0.4)'}}; padding:0.25rem 0.6rem; border-radius:0.5rem; font-size:0.75rem; font-weight:800;">
                                        ${{isClipping ? '✂️ CLIPPING VIDEO' : '🤖 GENERAZIONE AI'}}
                                    </span>
                                </div>
                                <div style="display:flex; gap:0.6rem; flex-wrap:wrap; font-size:0.85rem;">
                                    <span style="background:rgba(16,185,129,0.15); color:#34d399; padding:0.3rem 0.8rem; border-radius:0.5rem; font-weight:700;">$${{originalCamp.payout_per_1k_views || '?'}}/1k views</span>
                                    <span style="background:rgba(239,68,68,0.15); color:#ef4444; padding:0.3rem 0.8rem; border-radius:0.5rem; font-weight:700;">Budget Residuo: $${{budgetRemaining}}</span>
                                </div>
                            </div>
                            <div style="display:flex; gap:1rem; align-items:center;">
                                <div style="background:linear-gradient(135deg, rgba(245,158,11,0.1), rgba(217,119,6,0.2)); border:1px solid rgba(245,158,11,0.3); padding:0.8rem 1.2rem; border-radius:1rem; text-align:center;">
                                    <div style="font-size:0.72rem; color:#fbbf24; text-transform:uppercase; font-weight:800; margin-bottom:0.2rem;">🎯 Obiettivo Consigliato</div>
                                    <div style="font-size:1.1rem; font-weight:900; color:#fff;">${{item.daily_video_goal || "2-3 video al giorno"}}</div>
                                </div>
                            </div>
                        </div>

                        <!-- STATISTICHE & PERFORMANCE GIORNO PER GIORNO -->
                        ${{dailyStatsHtml}}

                        <!-- REQUISITI KLIPPIFY -->
                        <div style="background:rgba(0,0,0,0.2); border:1px solid rgba(255,255,255,0.05); border-radius:1rem; padding:1.2rem; margin-bottom:1.5rem;">
                            <span style="font-weight:800; font-size:0.95rem; color:#f8fafc; display:block; margin-bottom:0.6rem;">📋 Requisiti Ufficiali Klippify</span>
                            <div style="font-size:0.85rem; color:#cbd5e1; margin-bottom:0.8rem; line-height:1.5;"><strong>Brief:</strong> ${{originalBrief}}</div>
                            <div style="display:flex; flex-wrap:wrap; gap:1.2rem; font-size:0.8rem;">
                                <div><strong style="color:#a78bfa;">Hashtag:</strong> ${{originalHashtags}}</div>
                                <div><strong style="color:#a78bfa;">Tag (@):</strong> ${{originalMentions}}</div>
                                <div><strong style="color:#a78bfa;">CTA:</strong> ${{originalCTA}}</div>
                            </div>
                        </div>

                        <!-- ELENCO COMPLETO DI TUTTI I LINK E RISORSE FORNITI DALLA CAMPAGNA -->
                        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(56,189,248,0.25); border-radius:1rem; padding:1.2rem; margin-bottom:1.5rem;">
                            <span style="font-weight:800; font-size:0.95rem; color:#38bdf8; display:flex; align-items:center; gap:0.5rem; margin-bottom:0.4rem;">
                                <span>📁 Contenuti forniti dal brand</span>
                                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; font-size:0.75rem; padding:0.15rem 0.5rem; border-radius:0.4rem;">${{validLinks.length}} Link Trovati</span>
                            </span>
                            <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:0.6rem;">
                                Tutti i link e i file presenti nella sezione ufficiale "Contenuti forniti dal brand" di Klippify:
                            </div>
                            ${{allLinksHtml}}
                        </div>

                        <!-- PILOTA AUTOMATICO DEDICATO PER QUESTA CAMPAGNA -->
                        <div style="background:linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.9)); border:1px solid rgba(139,92,246,0.4); border-radius:1.2rem; padding:1.5rem; margin-bottom:2rem; box-shadow:0 10px 30px rgba(0,0,0,0.4);">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:1.2rem;">
                                <div>
                                    <div style="font-size:1.25rem; font-weight:900; color:#fff; display:flex; align-items:center; gap:0.6rem;">
                                        <span>🤖 Pilota Automatico per questa Campagna</span>
                                        <span id="camp-autopilot-status-badge-${{campToken}}" style="font-size:0.75rem; background:rgba(239,68,68,0.2); color:#ef4444; border:1px solid rgba(239,68,68,0.4); padding:0.2rem 0.6rem; border-radius:1rem; font-weight:800;">
                                            ⏸ IN PAUSA
                                        </span>
                                    </div>
                                    <div style="font-size:0.82rem; color:var(--text-muted); margin-top:0.3rem;">
                                        Tieni il computer acceso: il bot ritaglierà in automatico i video sorgente mancanti e pubblicherà le clip su TikTok agli orari prestabiliti inviandole subito a Klippify.
                                    </div>
                                </div>

                                <div style="display:flex; gap:0.8rem; align-items:center; flex-wrap:wrap;">
                                    <button onclick="runCampaignAutopilotNow('${{campToken}}', this)" style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.35); padding:0.65rem 1.1rem; border-radius:0.6rem; font-weight:800; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(56,189,248,0.25)'" onmouseout="this.style.background='rgba(56,189,248,0.15)'">
                                        ⚡ Pubblica Subito Prossimo Slot
                                    </button>
                                    <button id="btn-camp-autopilot-toggle-${{campToken}}" onclick="toggleCampaignAutopilot('${{campToken}}')" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; border:none; padding:0.7rem 1.4rem; border-radius:0.6rem; font-weight:900; font-size:0.9rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 15px rgba(16,185,129,0.35); transition:all 0.2s;">
                                        🟢 ATTIVA PILOTA AUTOMATICO
                                    </button>
                                </div>
                            </div>

                            <!-- 3 STATS STRIP SPECIFIC TO THIS CAMPAIGN -->
                            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:1rem; border-top:1px solid rgba(255,255,255,0.08); padding-top:1rem; margin-bottom:1rem;">
                                <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.8rem 1rem; border-left:4px solid #8b5cf6;">
                                    <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Prossima Pubblicazione</div>
                                    <div id="camp-ap-stat-next-run-${{campToken}}" style="font-size:0.95rem; font-weight:800; color:#c084fc; margin-top:0.2rem;">In attesa avvio...</div>
                                </div>
                                <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.8rem 1rem; border-left:4px solid #38bdf8;">
                                    <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Slot Pronti al Posting</div>
                                    <div id="camp-ap-stat-ready-${{campToken}}" style="font-size:1.3rem; font-weight:800; color:#38bdf8; margin-top:0.1rem;">0 / 3</div>
                                </div>
                                <div style="background:rgba(0,0,0,0.3); border-radius:0.6rem; padding:0.8rem 1rem; border-left:4px solid #10b981;">
                                    <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Inviati a Klippify</div>
                                    <div style="font-size:1.3rem; font-weight:800; color:#10b981; margin-top:0.1rem;">${{campSubmissions.length}} Video</div>
                                </div>
                            </div>

                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; background:rgba(0,0,0,0.25); padding:0.8rem 1rem; border-radius:0.6rem; border:1px solid rgba(255,255,255,0.05);">
                                <div style="font-size:0.8rem; color:#cbd5e1; display:flex; align-items:center; gap:0.4rem;">
                                    <span>💡</span>
                                    <span>Configura gli orari e i video negli slot sottostanti: l'autopilota li processerà in sequenza automatica.</span>
                                </div>
                                <button onclick="queueAllCampaignSlots('${{campToken}}', this)" style="background:linear-gradient(135deg, #8b5cf6, #6366f1); color:#fff; border:none; padding:0.45rem 0.9rem; border-radius:0.5rem; font-weight:800; font-size:0.8rem; cursor:pointer; box-shadow:0 2px 10px rgba(139,92,246,0.35);">
                                    📋 Accoda Tutti gli Slot all'Autopilota
                                </button>
                            </div>
                        </div>

                        <!-- CLIPPING HUB & CARICAMENTO VIDEO CON ESPLORA FILE -->
                        ${{isClipping ? `
                            <div style="background:linear-gradient(135deg, rgba(245,158,11,0.08), rgba(217,119,6,0.12)); border:1px solid rgba(245,158,11,0.35); border-radius:1.2rem; padding:1.5rem; margin-bottom:2rem;">
                                
                                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem; margin-bottom:1.2rem;">
                                    <div>
                                        <div style="font-size:1.2rem; font-weight:800; color:#fbbf24; display:flex; align-items:center; gap:0.5rem;">
                                            <span>✂️ Gestione Video Sorgente & Bot Analisi Gemini</span>
                                        </div>
                                        <div style="font-size:0.82rem; color:#cbd5e1; margin-top:0.3rem;">
                                            Carica i video completi del brand e avvia il bot che li carica nella chat <strong>"analisi video klippify"</strong> su Gemini.
                                        </div>
                                    </div>
                                    
                                    <!-- PULSANTI AZIONE: CARICA DA ESPLORA RISORSE E APRI CARTELLA -->
                                    <div style="display:flex; gap:0.8rem; flex-wrap:wrap;">
                                        
                                        <!-- INPUT FILE NASCOSTO PER ESPLORA RISORSE CON SUPPORTO MULTIPLO -->
                                        <input type="file" id="source-video-input-${{campToken}}" accept="video/*" multiple style="display:none;" onchange="uploadSourceVideoFiles(this, '${{campToken}}')">
                                        
                                        <!-- BOTTONE APRI ESPLORA RISORSE PER CARICARE PIÙ VIDEO -->
                                        <button id="btn-upload-file-${{campToken}}" onclick="document.getElementById('source-video-input-${{campToken}}').click()" style="background:linear-gradient(135deg, #38bdf8, #0284c7); color:#fff; font-weight:800; border:none; padding:0.65rem 1.2rem; border-radius:0.7rem; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 12px rgba(56,189,248,0.35); transition:transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
                                            📁 Carica Video (Anche Multipli)
                                        </button>

                                        <!-- BOTTONE APRI CARTELLA LOCALE IN WINDOWS -->
                                        <button onclick="openLocalFolder('${{campToken}}')" style="background:rgba(255,255,255,0.1); color:#fff; font-weight:700; border:1px solid rgba(255,255,255,0.2); padding:0.65rem 1rem; border-radius:0.7rem; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                            📂 Apri Cartella Locale
                                        </button>
                                    </div>
                                </div>

                                <!-- CODA VIDEO DA KLIPPARE (MULTI-VIDEO QUEUE) -->
                                <div style="background:rgba(15,23,42,0.9); border:1px solid rgba(245,158,11,0.35); border-radius:1rem; padding:1.2rem; margin-bottom:1.2rem;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem; margin-bottom:0.8rem;">
                                        <div>
                                            <div style="font-size:1.05rem; font-weight:800; color:#fbbf24; display:flex; align-items:center; gap:0.5rem;">
                                                <span>📋 Coda Video da Klippare</span>
                                                <span id="clipping-queue-count-${{campToken}}" style="background:rgba(245,158,11,0.2); color:#fbbf24; font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:0.4rem; font-weight:800;">0 Video</span>
                                            </div>
                                            <div id="clipping-queue-summary-${{campToken}}" style="font-size:0.78rem; color:var(--text-muted); margin-top:0.2rem;">
                                                Carica più video in coda: il bot li elaborerà in sequenza estraendo automaticamente i migliori momenti 9:16.
                                            </div>
                                        </div>

                                        <button onclick="processEntireClippingQueue('${{campToken}}', this)" style="background:linear-gradient(135deg, #f59e0b, #d97706); color:#000; font-weight:900; border:none; padding:0.65rem 1.2rem; border-radius:0.7rem; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; box-shadow:0 4px 15px rgba(245,158,11,0.35); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                                            ⚡ Klippa Tutta la Coda in Automatico
                                        </button>
                                    </div>

                                    <!-- LISTA DEGLI ELEMENTI IN CODA (RENDERIZZATA VIA JS) -->
                                    <div id="clipping-queue-list-${{campToken}}" style="display:flex; flex-direction:column; gap:0.6rem; margin-top:0.8rem;">
                                        <div style="text-align:center; padding:1rem; color:var(--text-muted); font-size:0.85rem;">⏳ Caricamento coda...</div>
                                    </div>
                                </div>

                                <!-- SELETTORE DEL VIDEO DA MANDARE A GEMINI (SINGOLO) -->
                                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.1); border-radius:0.8rem; padding:1rem; margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                                    <div style="flex:1; min-width:260px;">
                                        <label style="display:block; font-size:0.82rem; font-weight:800; color:#38bdf8; margin-bottom:0.4rem;">
                                            📹 Oppure Seleziona un Singolo Video da Inviare a Gemini:
                                        </label>
                                        <select id="source-video-selector-${{campToken}}" style="width:100%; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.2); color:#fff; padding:0.55rem; border-radius:0.5rem; font-size:0.85rem;">
                                            ${{localAvailableVideos.length > 0 ? localAvailableVideos.map(v => `<option value="${{v.filename}}">${{v.filename}} (${{(v.size_mb || 0).toFixed(1)}} MB)</option>`).join('') : '<option value="">-- Nessun video caricato. Carica prima un video con il pulsante sopra! --</option>'}}
                                        </select>
                                    </div>

                                    <!-- BOTTONE AVVIA ANALISI GEMINI -->
                                    <button onclick="startClippingPipelineForCampaign('${{campToken}}', this)" style="background:rgba(255,255,255,0.1); color:#fff; font-weight:800; border:1px solid rgba(255,255,255,0.25); padding:0.65rem 1.1rem; border-radius:0.7rem; font-size:0.85rem; cursor:pointer; display:flex; align-items:center; gap:0.5rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                        🤖 Klippa Singolo Video
                                    </button>
                                </div>

                                <div style="font-size:0.8rem; color:#94a3b8; background:rgba(0,0,0,0.3); padding:0.8rem; border-radius:0.6rem; border:1px solid rgba(255,255,255,0.05); line-height:1.5;">
                                    💡 <strong>Come funziona la Coda Multi-Video:</strong><br>
                                    1. Clicca su <strong>📁 Carica Video (Anche Multipli)</strong> e seleziona tutti i video che vuoi klippare.<br>
                                    2. I video compariranno nella <strong>📋 Coda Video da Klippare</strong> con il relativo stato.<br>
                                    3. Premi <strong>⚡ Klippa Tutta la Coda in Automatico</strong> (oppure lascia fare all'Autopilota): il bot analizzerà ogni video con Gemini nella chat <em>"analisi video klippify"</em> e salverà le clip 9:16 pronte per il posting!
                                </div>
                            </div>
                        ` : ''}}

                        <!-- DAILY EDITORIAL CONTROLS -->
                        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(139,92,246,0.3); border-radius:1rem; padding:1.2rem; margin-bottom:2rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                            <div>
                                <div style="font-size:1.15rem; font-weight:800; color:#fff; display:flex; align-items:center; gap:0.5rem;">
                                    <span>📅 Piano Editoriale di Oggi</span>
                                    <span style="background:rgba(139,92,246,0.2); color:#c084fc; font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:0.4rem;">Flessibile</span>
                                </div>
                                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">Configura quanti video vuoi produrre oggi e a che ora pubblicarli.</div>
                            </div>

                            <div style="display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
                                <!-- QUANTITY SELECTOR -->
                                <div style="display:flex; align-items:center; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.15); border-radius:0.6rem; padding:0.2rem 0.4rem; gap:0.6rem;">
                                    <span style="font-size:0.82rem; font-weight:700; color:#cbd5e1; padding-left:0.4rem;">Video al Giorno:</span>
                                    <button onclick="changeDailyTarget('${{campToken}}', -1)" style="background:rgba(255,255,255,0.1); color:#fff; border:none; width:28px; height:28px; border-radius:0.4rem; font-weight:bold; cursor:pointer;">-</button>
                                    <span id="target-count-display-${{campToken}}" style="font-size:1.1rem; font-weight:800; color:#c084fc; min-width:24px; text-align:center;">${{targetCount}}</span>
                                    <button onclick="changeDailyTarget('${{campToken}}', 1)" style="background:rgba(255,255,255,0.1); color:#fff; border:none; width:28px; height:28px; border-radius:0.4rem; font-weight:bold; cursor:pointer;">+</button>
                                </div>

                                <button onclick="saveSelectedCampaigns()" style="background:linear-gradient(135deg, #3b82f6, #1d4ed8); color:#fff; border:none; padding:0.65rem 1.2rem; border-radius:0.6rem; font-size:0.85rem; font-weight:800; cursor:pointer; box-shadow:0 4px 12px rgba(59,130,246,0.35);">
                                    💾 Salva Configurazione
                                </button>
                            </div>
                        </div>

                        <!-- SLOTS CARDS -->
                        <div style="display:flex; flex-direction:column; gap:1.5rem; margin-bottom:2rem;">
                            ${{slotsHtml}}
                        </div>

                        <!-- SEZIONE VIDEO PUBBLICATI & MONITORING KLIPPIFY -->
                        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.1); border-radius:1rem; padding:1.5rem;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.2rem; flex-wrap:wrap; gap:0.8rem;">
                                <div>
                                    <h3 style="font-size:1.25rem; font-weight:800; color:#fff; margin:0; display:flex; align-items:center; gap:0.5rem;">
                                        <span>🎬 Storico Video Inviati per questa Campagna</span>
                                        <span style="background:rgba(16,185,129,0.2); color:#34d399; font-size:0.75rem; padding:0.2rem 0.6rem; border-radius:1rem;">${{campSubmissions.length}} Video</span>
                                    </h3>
                                    <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">Visualizzazioni, mi piace, validazioni AI e guadagni tracciati in tempo reale dalle API ufficiali Klippify.</div>
                                </div>
                                <button onclick="refreshCampaignSubmissions('${{campToken}}', this)" style="background:rgba(56,189,248,0.12); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); border-radius:0.5rem; padding:0.45rem 0.9rem; font-size:0.82rem; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:0.4rem; transition:all 0.2s;" onmouseover="this.style.background='rgba(56,189,248,0.25)'" onmouseout="this.style.background='rgba(56,189,248,0.12)'">
                                    🔄 Aggiorna Stato Klippify
                                </button>
                            </div>
                            ${{publishedHtml}}
                        </div>

                    </div>
                </div>
            `;

            loadCampaignAutopilotState(campToken);
            loadClippingQueue(campToken);

            // Applica la modalità di vista salvata (default: Catena di Montaggio)
            try {{
                const savedMode = localStorage.getItem('camp_view_mode_' + campToken) || 'assembly';
                switchCampaignViewMode(campToken, savedMode);
            }} catch(e) {{}}

            setTimeout(() => {{
                const cards = document.querySelectorAll('.kanban-card[data-video-file]');
                cards.forEach(async (card) => {{
                    const filename = card.getAttribute('data-video-file');
                    try {{
                        const res = await fetch(`/api/tiktok/video-stats?filename=${{encodeURIComponent(filename)}}`);
                        const stats = await res.json();
                        if (stats.view_count !== undefined) {{
                            card.querySelector('.stat-views').innerText = stats.view_count.toLocaleString();
                            card.querySelector('.stat-likes').innerText = stats.like_count.toLocaleString();
                        }}
                    }} catch (e) {{
                        console.error('Errore fetch stats', e);
                    }}
                }});
            }}, 500);
        }}

                function closeCampaignDetail() {{
            currentDetailCampToken = null;
            document.getElementById('my-campaign-detail-view').style.display = 'none';
            document.getElementById('my-campaign-detail-content').innerHTML = '';
            document.getElementById('my-campaigns-grid').style.display = 'grid';
        }}


        async function deleteCampaign(campToken, ev) {{
            if (ev) ev.stopPropagation();
            if (!campToken) return;
            const originalCamp = allCampaignsData.find(c => c.campaign_token === campToken || c.id === campToken) || {{}};
            const campName = originalCamp.name || 'questa campagna';
            if (!confirm(`Sei sicuro di voler eliminare "${{campName}}" da "Le Mie Campagne"?`)) {{
                return;
            }}

            try {{
                const res = await fetch('/api/delete-campaign', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ campaign_id: campToken }})
                }});
                const data = await res.json();
                if (data.status === 'ok') {{
                    selectedCampaigns = selectedCampaigns.filter(id => id !== campToken);
                    generatedContent = generatedContent.filter(c => c.campaign_id !== campToken);
                    
                    // Deselect checkbox in Creator Dashboard if present
                    const cb = document.querySelector(`.campaign-checkbox[data-campaign-id="${{campToken}}"]`);
                    if (cb) cb.checked = false;

                    // If currently inside detail view of this campaign, close it
                    if (currentDetailCampToken === campToken) {{
                        closeCampaignDetail();
                    }}

                    // Re-render grid
                    const grid = document.getElementById('my-campaigns-grid');
                    if (grid) {{
                        grid.innerHTML = '';
                        renderMyCampaigns();
                    }}
                }} else {{
                    alert("Errore durante l'eliminazione: " + (data.error || "Errore sconosciuto"));
                }}
            }} catch (e) {{
                console.error("Errore chiamata delete-campaign", e);
                alert("Impossibile contattare il server.");
            }}
        }}


        // Funzione per switchare i tab interni della card campagna
        function switchCampTab(cardId, tab) {{
            document.getElementById(`tab-content-${{cardId}}-pending`).style.display = tab === 'pending' ? 'block' : 'none';
            document.getElementById(`tab-content-${{cardId}}-published`).style.display = tab === 'published' ? 'block' : 'none';
            
            const btnPending = document.getElementById(`tab-btn-${{cardId}}-pending`);
            const btnPublished = document.getElementById(`tab-btn-${{cardId}}-published`);
            
            if(tab === 'pending') {{
                btnPending.style.color = '#38bdf8';
                btnPending.style.borderBottomColor = '#38bdf8';
                btnPublished.style.color = 'var(--text-muted)';
                btnPublished.style.borderBottomColor = 'transparent';
            }} else {{
                btnPublished.style.color = '#10b981';
                btnPublished.style.borderBottomColor = '#10b981';
                btnPending.style.color = 'var(--text-muted)';
                btnPending.style.borderBottomColor = 'transparent';
            }}
        }}

        function filterBySection(targetSection, btn) {{
            document.querySelectorAll('.tab-filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const cards = document.querySelectorAll('#main-cards-grid .card');
            cards.forEach(c => {{
                const sec = c.getAttribute('data-section');
                if (targetSection === 'all' || sec === targetSection) {{
                    c.style.display = 'flex';
                }} else {{
                    c.style.display = 'none';
                }}
            }});
        }}

        function openModal(index) {{
            const c = allCampaignsData[index];
            if (!c) return;

            const token = c.campaign_token || c.id || '';
            const tokenUrl = c.campaign_url || ('https://app.klippify.com/campaigns/' + token);
            const htStr = (c.mandatory_hashtags || []).join(' ');
            const tagStr = (c.mandatory_mentions || []).join(' ');
            const ctaStr = c.call_to_action || '';
            const payout = (c.payout_per_1k_views || 1.0).toFixed(2);
            const poolRem = (c.budget_remaining || 0).toLocaleString();
            const budgetTot = (c.budget_total || 0).toLocaleString();
            const budgetSpent = (c.budget_spent || 0).toLocaleString();
            const progPct = c.budget_progress_percent || '0%';
            const score = c.convenience_score || 50;
            const views = (c.total_views || 0).toLocaleString();
            const creators = c.creators_count || 0;
            const section = c.section || 'Nuove';

            // Match published TikTok videos for this campaign in modal
            const modalPubs = (typeof publishedContent !== 'undefined' ? publishedContent : []).filter(pc => pc.campaign_id === token || pc.campaign_id === c.id);
            let matchedModalVideos = [];
            modalPubs.forEach(mp => {{
                const tv = findMatchingTikTokVideo(token, c.name, mp);
                if (tv && !matchedModalVideos.find(x => x.id === tv.id)) {{
                    matchedModalVideos.push(tv);
                }}
            }});

            if (cachedTikTokVideos && cachedTikTokVideos.length > 0) {{
                cachedTikTokVideos.forEach(tv => {{
                    if (!matchedModalVideos.find(x => x.id === tv.id)) {{
                        const desc = (tv.description || '').toLowerCase();
                        if (c.name && desc.includes(c.name.toLowerCase())) {{
                            matchedModalVideos.push(tv);
                        }} else if (c.mandatory_hashtags && c.mandatory_hashtags.some(ht => desc.includes(ht.toLowerCase()))) {{
                            matchedModalVideos.push(tv);
                        }}
                    }}
                }});
            }}

            let tiktokModalSectionHtml = '';
            if (matchedModalVideos.length > 0) {{
                const cardsHtml = matchedModalVideos.map(v => renderTikTokVideoCard(v, true)).join('');
                tiktokModalSectionHtml = `
                    <div style="background:rgba(15,23,42,0.9); border:1px solid rgba(56,189,248,0.35); border-radius:0.85rem; padding:1.2rem; margin-bottom:1.5rem;">
                        <h3 style="font-size:1rem; color:#38bdf8; margin-bottom:0.8rem; display:flex; align-items:center; gap:0.4rem;">
                            <span>📱 Video TikTok Pubblicati per questa Campagna (${{matchedModalVideos.length}})</span>
                        </h3>
                        <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap:1rem;">
                            ${{cardsHtml}}
                        </div>
                    </div>
                `;
            }} else {{
                tiktokModalSectionHtml = `
                    <div style="background:rgba(15,23,42,0.6); border:1px dashed var(--card-border); border-radius:0.85rem; padding:1rem; margin-bottom:1.5rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.8rem;">
                        <div style="font-size:0.85rem; color:var(--text-muted);">
                            📱 <em>Nessun video TikTok ancora pubblicato per questa campagna.</em>
                        </div>
                        <button onclick="closeModal(); switchMainView('studio');" style="background:linear-gradient(135deg, #8b5cf6, #3b82f6); color:#fff; border:none; padding:0.4rem 0.8rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700; cursor:pointer;">
                            Crea Video in Studio 🎬
                        </button>
                    </div>
                `;
            }}

            const rulesHtml = (c.rules || ['Segui le linee guida ufficiali Klippify']).map(r => `<li>✓ ${{r}}</li>`).join('');

            const modalHtml = `
                <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.8rem;">
                    <div>
                        <span style="background:linear-gradient(90deg, #8b5cf6, #38bdf8); color:#fff; padding:0.25rem 0.7rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700;">TOKEN: ${{token}}</span>
                        <span style="background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); padding:0.25rem 0.7rem; border-radius:0.4rem; font-size:0.75rem; font-weight:700; margin-left:0.5rem;">SEZIONE: ${{section}}</span>
                    </div>
                    <span style="color:var(--accent-emerald); font-weight:600; font-size:0.85rem;">Score: ${{score}}/100</span>
                </div>

                <h2 style="font-size:1.8rem; font-weight:800; color:#fff; margin-bottom:0.3rem;">${{c.name}}</h2>
                <p style="color:var(--text-muted); font-size:0.95rem; margin-bottom:1.5rem;">Brand / Creator: <strong style="color:#fff;">${{c.brand || 'Klippify Partner'}}</strong></p>

                <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1.2rem; border-radius:0.85rem; margin-bottom:1.5rem;">
                    <div style="font-size:0.85rem; font-weight:700; color:var(--accent-cyan); margin-bottom:0.4rem; text-transform:uppercase;">Descrizione Campagna:</div>
                    <p style="color:#e2e8f0; font-size:0.9rem; line-height:1.5;">${{c.description || 'Descrizione estratta dalla pagina ufficiale Klippify.'}}</p>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
                    <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1rem; border-radius:0.75rem;">
                        <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Payout Rate / 1k</div>
                        <div style="font-size:1.4rem; font-weight:700; color:#34d399; margin-top:0.2rem;">$${{payout}} /1k</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1rem; border-radius:0.75rem;">
                        <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Pool Rimanente</div>
                        <div style="font-size:1.4rem; font-weight:700; color:#38bdf8; margin-top:0.2rem;">$${{poolRem}}</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1rem; border-radius:0.75rem;">
                        <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Budget Totale</div>
                        <div style="font-size:1.4rem; font-weight:700; color:#f59e0b; margin-top:0.2rem;">$${{budgetTot}}</div>
                    </div>
                    <div style="background:rgba(15,23,42,0.8); border:1px solid var(--card-border); padding:1rem; border-radius:0.75rem;">
                        <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Views / Clippers</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#fff; margin-top:0.2rem;">${{views}} views | ${{creators}} clippers</div>
                    </div>
                </div>

                <div style="background:rgba(15,23,42,0.8); padding:1rem; border-radius:0.75rem; border:1px solid var(--card-border); margin-bottom:1.5rem;">
                    <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:var(--text-muted); margin-bottom:0.4rem;">
                        <span>Budget Erogato: <strong>$${{budgetSpent}}</strong> di <strong>$${{budgetTot}}</strong></span>
                        <span>Progresso: <strong style="color:#38bdf8;">${{progPct}}</strong></span>
                    </div>
                    <div class="progress-bar-bg" style="height:8px;">
                        <div class="progress-bar-fill" style="width:${{progPct}}"></div>
                    </div>
                </div>

                <div style="background:rgba(15,23,42,0.9); border-radius:0.85rem; padding:1.2rem; border:1px solid var(--card-border); margin-bottom:1.5rem;">
                    <h3 style="font-size:1rem; color:#fff; margin-bottom:0.8rem;">📋 Copia Rapida Requisiti</h3>
                    
                    <div class="copy-item">
                        <div class="copy-header">HASHTAG OBBLIGATORI</div>
                        <div class="copy-flex">
                            <span class="copy-val" id="modal-ht">${{htStr}}</span>
                            <button class="btn-cp" onclick="copyText('modal-ht')">Copia Hashtags</button>
                        </div>
                    </div>
                    <div class="copy-item">
                        <div class="copy-header">TAG ACCOUNT (@)</div>
                        <div class="copy-flex">
                            <span class="copy-val" id="modal-tag">${{tagStr}}</span>
                            <button class="btn-cp" onclick="copyText('modal-tag')">Copia Tag</button>
                        </div>
                    </div>
                    <div class="copy-item">
                        <div class="copy-header">CALL TO ACTION (CTA)</div>
                        <div class="copy-flex">
                            <span class="copy-val" id="modal-cta">${{ctaStr}}</span>
                            <button class="btn-cp" onclick="copyText('modal-cta')">Copia CTA</button>
                        </div>
                    </div>
                </div>

                <div style="margin-bottom:1.5rem;">
                    <h3 style="font-size:0.95rem; color:#fff; margin-bottom:0.5rem;">📜 Regole & Linee Guida Video:</h3>
                    <ul style="list-style:none; color:var(--text-muted); font-size:0.85rem; display:flex; flex-direction:column; gap:0.4rem;">
                        ${{rulesHtml}}
                    </ul>
                </div>

                ${{tiktokModalSectionHtml}}

                <div style="display:flex; gap:1rem; margin-top:1.5rem;">
                    <a href="${{tokenUrl}}" target="_blank" style="flex:1; text-align:center; background:linear-gradient(135deg, #8b5cf6, #6d28d9); color:#fff; padding:0.8rem; border-radius:0.6rem; text-decoration:none; font-weight:700; font-size:0.9rem;">🔗 Apri Pagina Token Ufficiale (${{token}})</a>
                    <button onclick="closeModal()" style="background:rgba(255,255,255,0.1); border:1px solid var(--card-border); color:#fff; padding:0.8rem 1.5rem; border-radius:0.6rem; font-weight:600; cursor:pointer;">Chiudi</button>
                </div>
            `;

            document.getElementById('modal-body').innerHTML = modalHtml;
            document.getElementById('modal-overlay').classList.add('active');
        }}

        function closeModal() {{
            document.getElementById('modal-overlay').classList.remove('active');
        }}

        function closeModalOnOverlay(e) {{
            if (e.target.id === 'modal-overlay') {{
                closeModal();
            }}
        }}

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') closeModal();
        }});

        function copyText(elementId) {{
            const val = document.getElementById(elementId).innerText;
            copyValue(val, event.target);
        }}

        function copyValue(val, btn) {{
            navigator.clipboard.writeText(val).then(() => {{
                const orig = btn.innerText;
                btn.innerText = 'Copiato! ✓';
                btn.style.background = '#10b981';
                btn.style.color = '#fff';
                setTimeout(() => {{
                    btn.innerText = orig;
                    btn.style.background = '';
                    btn.style.color = '';
                }}, 1500);
            }});
        }}

        async function triggerRefresh() {{
            const btn = event.target;
            btn.innerText = '⏳ Scansione in corso...';
            btn.disabled = true;
            try {{
                await fetch('/api/refresh', {{ method: 'POST' }});
                window.location.reload();
            }} catch(e) {{
                alert('Aggiornamento completato! Ricarico...');
                window.location.reload();
            }}
        }}
        async function saveSelectedCampaigns() {{
            const checkboxes = document.querySelectorAll('.campaign-checkbox:checked');
            const selectedTokens = Array.from(checkboxes).map(cb => cb.getAttribute('data-campaign-id'));
            
            const btn = document.getElementById('btn-save-selected');
            const origText = btn.innerHTML;
            
            if (selectedTokens.length === 0) {{
                alert("Non hai selezionato nessuna campagna!");
                return;
            }}

            btn.innerHTML = '⏳ Salvataggio...';
            btn.disabled = true;

            try {{
                const res = await fetch('/api/save-selection', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(selectedTokens)
                }});
                
                if (res.ok) {{
                    btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                    btn.innerHTML = '✅ Salvate! Torna in chat';
                }} else {{
                    btn.style.background = 'red';
                    btn.innerHTML = '❌ Errore';
                }}
            }} catch(e) {{
                alert('Errore nel salvataggio: ' + e);
                btn.innerHTML = origText;
            }}
            
            setTimeout(() => {{
                btn.innerHTML = origText;
                btn.disabled = false;
            }}, 3000);
        }}
    
        async function loadTikTokData() {{
            // Load stats
            try {{
                const res = await fetch('/api/tiktok/stats');
                const data = await res.json();
                if (data.error) throw new Error(data.error);
                
                let avatar = data.avatar_url || 'https://via.placeholder.com/60';
                let username = data.display_name || 'TikTok User';
                let followers = data.follower_count || 0;
                let likes = data.likes_count || 0;
                let videos = data.video_count || 0;

                const statsHtml = `
                    <div class="k-stat-card">
                        <img src="${{avatar}}" style="width:60px; height:60px; border-radius:50%; border:2px solid var(--accent-purple);">
                        <div class="k-stat-info">
                            <div class="k-stat-title">@${{username}}</div>
                            <div class="k-stat-val">${{followers.toLocaleString()}}</div>
                            <div class="k-stat-sub">Followers totali</div>
                        </div>
                    </div>
                    <div class="k-stat-card">
                        <div class="k-stat-icon-wrapper" style="background: rgba(239, 68, 68, 0.15); color: #ef4444;">
                            <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path></svg>
                        </div>
                        <div class="k-stat-info">
                            <div class="k-stat-title">Mi Piace Totali</div>
                            <div class="k-stat-val">${{likes.toLocaleString()}}</div>
                            <div class="k-stat-sub">Su tutti i tuoi video</div>
                        </div>
                    </div>
                    <div class="k-stat-card">
                        <div class="k-stat-icon-wrapper" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8;">
                            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>
                        </div>
                        <div class="k-stat-info">
                            <div class="k-stat-title">Video Pubblicati</div>
                            <div class="k-stat-val">${{videos.toLocaleString()}}</div>
                            <div class="k-stat-sub">Video attivi sul profilo</div>
                        </div>
                    </div>
                `;
                document.getElementById('tiktok-stats-container').innerHTML = statsHtml;
            }} catch(e) {{
                document.getElementById('tiktok-stats-container').innerHTML = `<div style="color:red;">Errore: ${{e.message}}</div>`;
            }}

            // Load videos into select
            try {{
                const res = await fetch('/api/videos');
                const videos = await res.json();
                
                const sel = document.getElementById('tiktok-video-select');
                if (sel) {{
                    if (videos.length === 0) {{
                        sel.innerHTML = '<option value="">Nessun video generato trovato.</option>';
                    }} else {{
                        sel.innerHTML = '<option value="">Seleziona un video da pubblicare...</option>' + 
                            videos.map(v => `<option value="${{v.filename}}">${{v.filename}} (${{(v.size / 1024 / 1024).toFixed(1)}} MB)</option>`).join('');
                    }}
                }}
                
                const campSel = document.getElementById('tiktok-campaign-select');
                if (campSel && selectedCampaigns && selectedCampaigns.length > 0) {{
                    // Populate from selectedCampaigns instead of videos because videos don't have campaign_id in the /api/videos response
                    campSel.innerHTML = '<option value="unknown">Nessuna campagna specifica</option>' + 
                        selectedCampaigns.map(id => `<option value="${{id}}">${{id}}</option>`).join('');
                }}
            }} catch(e) {{
                console.error("Errore caricamento video", e);
            }}

            // 3. Load all published TikTok videos with live stats
            loadTikTokPublishedVideos();
        }}

        async function publishToTikTok() {{
            const selVideo = document.getElementById('tiktok-video-select');
            const selCamp = document.getElementById('tiktok-campaign-select');
            const titleInput = document.getElementById('tiktok-video-title');
            const capInput = document.getElementById('tiktok-video-caption');
            const coverInput = document.getElementById('tiktok-video-cover');
            const btn = document.getElementById('tiktok-publish-btn');
            const status = document.getElementById('tiktok-publish-status');
            
            const filename = selVideo.value;
            const campaignId = selCamp ? selCamp.value : 'unknown';
            const titleStr = titleInput ? titleInput.value.trim() : "";
            const capStr = capInput ? capInput.value.trim() : "";
            const coverTimeSec = coverInput ? parseFloat(coverInput.value) : 1.0;
            
            if (!filename) {{ alert("Seleziona prima un video!"); return; }}
            if (!titleStr) {{ alert("Il Titolo del video è obbligatorio!"); return; }}
            
            const combinedTitle = capStr ? (titleStr + "\\n\\n" + capStr) : titleStr;
            const coverTimeMs = Math.floor((isNaN(coverTimeSec) ? 1.0 : coverTimeSec) * 1000);
            
            btn.disabled = true;
            btn.innerHTML = "⏳ Caricamento in corso... (non chiudere la pagina)";
            btn.style.opacity = "0.7";
            status.innerText = "";
            
            try {{
                const res = await fetch('/api/tiktok/upload', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ 
                        filename: filename, 
                        title: combinedTitle,
                        cover_time_ms: coverTimeMs,
                        campaign_id: campaignId
                    }})
                }});
                
                const data = await res.json();
                if (data.error) throw new Error(data.error);
                
                status.innerText = "✅ Video pubblicato con successo su TikTok!";
                status.style.color = "#10b981";
                if(capInput) capInput.value = "";
                if(titleInput) titleInput.value = "";
                if(selVideo) selVideo.selectedIndex = 0;

                // Reload TikTok videos gallery
                setTimeout(() => {{
                    loadTikTokPublishedVideos(true);
                }}, 3000);
            }} catch (e) {{
                status.innerText = "❌ Errore durante la pubblicazione: " + e.message;
                status.style.color = "#ef4444";
            }}
            
            btn.disabled = false;
            btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg> Pubblica su TikTok 🚀`;
            btn.style.opacity = "1";
        }}

        // Preload TikTok videos and Debug Tasks in background on startup
        document.addEventListener('DOMContentLoaded', () => {{
            setTimeout(() => {{
                loadTikTokPublishedVideos(false);
                loadDebugTasks(false);
            }}, 500);
        }});
        setTimeout(() => {{
            if (!cachedTikTokVideos || cachedTikTokVideos.length === 0) {{
                loadTikTokPublishedVideos(false);
            }}
            loadDebugTasks(false);
        }}, 1500);

    </script>
</body>
</html>
"""

    with open(HTML_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] HTML Report generated: {HTML_REPORT_PATH}")
    return HTML_REPORT_PATH

def generate_markdown_report(campaigns):
    now_str = datetime.now().strftime("%d/%m/%Y alle %H:%M")
    top_camp = campaigns[0] if campaigns else None

    md = f"# ⚡ Report Giornaliero Campagne Klippify ({now_str})\n\n"

    if top_camp:
        payout = top_camp.get("payout_per_1k_views", 1.0)
        pool_rem = top_camp.get("budget_remaining", 0.0)
        budget_tot = top_camp.get("budget_total", 0.0)
        prog_pct = top_camp.get("budget_progress_percent", "0%")
        token = top_camp.get("campaign_token", top_camp.get("id", ""))

        md += f"## 🏆 Campagna Consigliata: **{top_camp['name']}**\n"
        md += f"- **Token ID**: `{token}`\n"
        md += f"- **Sezione**: `{top_camp.get('section', 'Nuove')}`\n"
        md += f"- **Punteggio Convenienza**: `{top_camp.get('convenience_score', 50)}/100`\n"
        md += f"- **Tariffa Payout**: `${payout:.2f}` per 1.000 visualizzazioni\n"
        md += f"- **Pool Rimanente**: `${pool_rem:,.2f}`\n"
        md += f"- **Budget Totale**: `${budget_tot:,.2f}` (Avanzamento `{prog_pct}`)\n"
        md += f"- **Stato File Locali**: `{'✅ Presenti in alestark campain' if top_camp.get('has_local_media') else '⚠️ Non ancora scaricati'}`\n\n"
        
        md += "### 📋 Requisiti Obbligatori da Copiare:\n"
        md += f"- **Hashtags**: `{' '.join(top_camp.get('mandatory_hashtags', []))}`\n"
        md += f"- **Tag Account**: `{' '.join(top_camp.get('mandatory_mentions', []))}`\n"
        md += f"- **Call to Action**: `{top_camp.get('call_to_action', '')}`\n\n"

    md += "## 📊 Classifica Completa Campagne\n\n"
    md += "| Pos | Campagna | Sezione | Token ID | Payout ($/1k) | Pool Rimanente | Budget Totale | Score |\n"
    md += "|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|\n"

    for idx, c in enumerate(campaigns, 1):
        payout = c.get("payout_per_1k_views", 1.0)
        pool_rem = c.get("budget_remaining", 0.0)
        budget_tot = c.get("budget_total", 0.0)
        score = c.get("convenience_score", 50)
        token = c.get("campaign_token", c.get("id", ""))
        sec = c.get("section", "Nuove")
        md += f"| {idx} | **{c['name']}** | {sec} | `{token}` | ${payout:.2f} | ${pool_rem:,.2f} | ${budget_tot:,.2f} | **{score}** |\n"

    with open(MD_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[+] Markdown Report generated: {MD_REPORT_PATH}")
    return MD_REPORT_PATH

if __name__ == "__main__":
    raw_campaigns = fetch_klippify_campaigns()
    ranked_campaigns = analyze_and_rank_campaigns(raw_campaigns)
    dash_data = fetch_klippify_dashboard_data()
    html_file = generate_html_report(ranked_campaigns, dash_data)
    md_file = generate_markdown_report(ranked_campaigns)
