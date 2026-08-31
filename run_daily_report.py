import sys
import webbrowser
from pathlib import Path

# Add current directory to path
BASE_DIR = Path(r"C:\Users\HP\Desktop\contenuti klippify")
sys.path.append(str(BASE_DIR))

from klippify_scraper import fetch_klippify_campaigns, analyze_and_rank_campaigns
from generate_report import generate_html_report, generate_markdown_report

def main():
    print("=" * 60)
    print("   Klippify Daily Campaign Intelligence & Report System")
    print("=" * 60)
    
    print("\n[1/3] Fetching campaign data & scanning local folder...")
    raw_campaigns = fetch_klippify_campaigns(use_cache_if_available=False)
    
    print("\n[2/3] Calculating convenience scores & ranking campaigns...")
    ranked_campaigns = analyze_and_rank_campaigns(raw_campaigns)
    
    top = ranked_campaigns[0]
    print(f"\n[TOP CAMPAIGN OF THE DAY]: {top['name']}")
    print(f"   > Payout: ${top['payout_per_1k_views']:.2f} / 1.000 views")
    print(f"   > Score: {top['convenience_score']} / 100")
    print(f"   > Hashtag: {' '.join(top['mandatory_hashtags'])}")
    print(f"   > CTA: {top['call_to_action']}")
    print(f"   > Media Locale: {'PRONTO IN CARTELLA [OK]' if top['has_local_media'] else 'DA SCARICARE [INFO]'}")

    print("\n[3/3] Generating Dashboard & Markdown Reports...")
    html_path = generate_html_report(ranked_campaigns)
    md_path = generate_markdown_report(ranked_campaigns)
    
    print("\n[+] Opening Interactive HTML Report in your browser...")
    webbrowser.open(f"file:///{html_path}")
    print("=" * 60)
    print(f"SUCCESS: Report updated at {html_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
