import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORE = ROOT / 'core'
for p in [CORE, ROOT]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.generate_report import *

if __name__ == '__main__':
    raw = fetch_klippify_campaigns()
    ranked = analyze_and_rank_campaigns(raw)
    dash = fetch_klippify_dashboard_data()
    generate_html_report(ranked, dash)
    generate_markdown_report(ranked)
