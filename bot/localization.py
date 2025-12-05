import json
import pathlib
from typing import Dict

_LOCALES: Dict[str, dict] = {}


def load_locales(locales_dir: str | None = None) -> None:
    global _LOCALES
    base = pathlib.Path(locales_dir or pathlib.Path(__file__).resolve().parents[1] / 'locales')
    for code in ('ru', 'tj'):
        path = base / f"{code}.json"
        if path.exists():
            with path.open('r', encoding='utf-8') as f:
                _LOCALES[code] = json.load(f)
        else:
            _LOCALES[code] = {}


def T(key: str, lang: str = 'ru', default: str | None = None) -> str:
    d = _LOCALES.get(lang, {})
    parts = key.split('.') if key else []
    cur = d
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            return default if default is not None else key
        cur = cur[p]
    return cur if isinstance(cur, str) else (default if default is not None else key)


def get_locale(lang: str) -> dict:
    return _LOCALES.get(lang, {})

