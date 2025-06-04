# language.py

import json
from pathlib import Path

LANG_FILE = Path("resources/lang_en.json")

with open(LANG_FILE, "r", encoding="utf-8") as f:
    LANG = json.load(f)

def get_text(key):
    return LANG.get(key, key)
