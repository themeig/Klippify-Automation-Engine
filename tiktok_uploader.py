import sys
from pathlib import Path

# Add core directory to sys.path
_CORE_DIR = Path(__file__).resolve().parent / "core"
if str(_CORE_DIR_ not in sys.path:
    sys.path.insert(0, str(_CORE_DIR))

import tiktok_uploader

if __name__ == "__main__":
    tiktok_uploader.main()
