from typing import Dict, Any

USER_DATA: Dict[int, Dict[str, Any]] = {}


def get_user_lang(user_id: int) -> str:
    """Get user language from in-memory state."""
    return USER_DATA.get(user_id, {}).get("language", "ru")
