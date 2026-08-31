import sys
import os
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from tiktok_uploader import run_uploader

video_path = os.path.abspath(r"generated_videos\clip_SaraDizdari_slot1_v2.mp4")
title = "3.210€ di fatturato con Shopify dedicando pochissimo tempo! 🚀 Guarda la video-lezione gratuita sul profilo di @saradizdari_ecom per scoprire come iniziare! 💡✨ #saradizdari #negozidigitali #ecommerce #shopify #klippify #dropshipping"
campaign_id = "6a71c6f7245627c68999eae2"

print("="*60)
print("AVVIO TEST UPLOAD TIKTOK VISIVO")
print(f"Video: {video_path}")
print(f"Campagna: {campaign_id}")
print("="*60)

run_uploader(
    video_path=video_path,
    title=title,
    cover_time_sec=1.0,
    is_auto=True,
    campaign_id=campaign_id
)

print("\nPremi INVIO per terminare...")
input()
