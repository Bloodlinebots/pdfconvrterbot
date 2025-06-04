import json
import os
from telegram import ReplyKeyboardMarkup

# Folder where language files are stored
LANG_FOLDER = "resources"

# Default language
DEFAULT_LANG = "en"

# Supported languages
SUPPORTED_LANGS = {
    "English🇺🇸": "en",
    "Hindi 🇮🇳": "hi",
    "Urdu 🇸🇦": "ur",
    "Russian 🇷🇺": "ru"
}

# Load all language files into memory
LANGUAGES = {}

for lang_code in SUPPORTED_LANGS.values():
    path = os.path.join(LANG_FOLDER, f"lang_{lang_code}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            LANGUAGES[lang_code] = json.load(f)
    else:
        LANGUAGES[lang_code] = {}

def get_text(user_data, key):
    """
    Return the translated string for the given key and user language.
    Fallback to English and then the key itself.
    """
    lang = user_data.get("lang", DEFAULT_LANG)
    return (
        LANGUAGES.get(lang, {}).get(key) or
        LANGUAGES[DEFAULT_LANG].get(key) or
        key
    )

def get_lang_keyboard():
    """
    Returns a language selection keyboard.
    """
    return ReplyKeyboardMarkup(
        [[lang] for lang in SUPPORTED_LANGS.keys()],
        resize_keyboard=True
    )

def get_lang_code(lang_name):
    """
    Converts human-readable language name to code.
    """
    return SUPPORTED_LANGS.get(lang_name, DEFAULT_LANG)
