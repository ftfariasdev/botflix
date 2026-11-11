import json
from pathlib import Path

LOCALE_DIR = Path(__file__).parent.parent / "source" / "locale"
DEFAULT_LANG = "en"

# loads every locale file once, at import time
_translations = {
    f.stem: json.loads(f.read_text(encoding="utf-8"))
    for f in LOCALE_DIR.glob("*.json")
}


def normalize_lang(code: str | None) -> str:
    """'pt-BR' -> 'pt', 'en-US' -> 'en', unknown -> DEFAULT_LANG."""
    lang = (code or DEFAULT_LANG).split("-")[0].lower()
    return lang if lang in _translations else DEFAULT_LANG


def t(key: str, lang: str | None = None, **params) -> str:
    """Translate a dotted key, e.g. t("MENU.OPTION_1", "pt") or t("WELCOME", "en", username="Ana")."""
    parts = key.upper().split(".")
    for candidate in (normalize_lang(lang), DEFAULT_LANG):
        node = _translations[candidate]
        for part in parts:
            node = node.get(part) if isinstance(node, dict) else None
        if isinstance(node, str):
            return node.format(**params)
    return key
