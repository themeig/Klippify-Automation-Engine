import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORE = ROOT / 'core'
for p in [CORE, ROOT]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.server import *

if __name__ == '__main__':
    run_server()
