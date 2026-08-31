import os
import sys
from pathlib import Path

_RAW_CORE_DIR = Path(__file__).resolve().parent
_RAW_PROJECT_ROOT = _RAW_CORE_DIR.parent

CORE_DIR = _RAW_CORE_DIR
DATA_DIR = _RAW_PROJECT_ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)
SOURCES_DIR = _RAW_PROJECT_ROOT / 'clipping_sources'
SOURCES_DIR.mkdir(exist_ok=True)
VIDEOS_DIR = _RAW_PROJECT_ROOT / 'generated_videos'
VIDEOS_DIR.mkdir(exist_ok=True)
REPORTS_DIR = _RAW_PROJECT_ROOT

for p in [CORE_DIR, _RAW_PROJECT_ROOT]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

class SmartPath(type(Path())):
    def __truediv__(self, key):
        if isinstance(key, str):
            if key.endswith('.json'):
                return DATA_DIR / key
            elif key == 'clipping_sources':
                return SOURCES_DIR
            elif key == 'generated_videos':
                return VIDEOS_DIR
        return super().__truediv__(key)

PROJECT_ROOT = SmartPath(_RAW_PROJECT_ROOT)

def get_data_path(filename: str) -> Path:
    return DATA_DIR / filename
