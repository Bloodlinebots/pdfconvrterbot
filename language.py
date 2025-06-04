import json
import os
from telegram import ReplyKeyboardMarkup

LANG_FOLDER = "resources"
DEFAULT_LANG = "en"

SUPPORTED_LANGS = {
    "English🇺🇸": "en",
    "Hindi 🇮🇳": "hi",
    "Urdu 🇸🇦": "ur",
    "Russian 🇷🇺": "ru"
}

LANGUAGES = {}

for lang_code in SUPPORTED_LANGS.values():
    path = os.path.join(LANG_FOLDER, f"lang_{lang_code}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            LANGUAGES[lang_code] = json.load(f)
    else:
        LANGUAGES[lang_code] = {}

def get_text(user_data: dict, key: str) -> str:
    """
    Return the translated string for the given key and user language.
    Fallback to English and then to the key itself.
    """
    lang = user_data.get("lang") or DEFAULT_LANG
    return (
        LANGUAGES.get(lang, {}).get(key) or
        LANGUAGES[DEFAULT_LANG].get(key) or
        key
    )

def get_lang_keyboard() -> ReplyKeyboardMarkup:
    """
    Returns a language selection keyboard markup.
    """
    return ReplyKeyboardMarkup(
        [[lang] for lang in SUPPORTED_LANGS.keys()],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_lang_code(lang_name: str) -> str:
    """
    Converts human-readable language name to language code.
    """
    return SUPPORTED_LANGS.get(lang_name, DEFAULT_LANG)
