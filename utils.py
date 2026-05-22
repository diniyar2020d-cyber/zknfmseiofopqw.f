import re
from datetime import datetime, timedelta

def format_number(num: int) -> str:
    """Форматирует число с пробелами: 15000 -> 15 000"""
    return f"{num:,}".replace(",", " ")

def parse_number(text: str) -> int:
    """Парсит число из строки с пробелами"""
    return int(re.sub(r"\s+", "", text.strip()))

def get_streak(user_id: int, country: str) -> int:
    """Вычисляет X2, X3 и т.д. для уведомлений"""
    from database import get_last_user_profit
    last = get_last_user_profit(user_id)
    if not last:
        return 1
    last_date = datetime.fromisoformat(last[0])
    today = datetime.now().date()
    if last_date.date() == today:
        return last[1] + 1
    return 1

def get_country_flag(country: str) -> str:
    flags = {
        "Россия": "🇷🇺",
        "Узбекистан": "🇺🇿",
        "Казахстан": "🇰🇿",
        "Таджикистан": "🇹🇯",
        "Украина": "🇺🇦",
        "Беларусь": "🇧🇾"
    }
    return flags.get(country, "🌍")

def days_in_team(join_date_str: str) -> int:
    join_date = datetime.fromisoformat(join_date_str)
    return (datetime.now() - join_date).days

def get_rank_name(rank_code: str) -> str:
    ranks = {
        "LOW": "LOW",
        "MEDIA": "MEDIA",
        "HIGHT": "HIGHT",
        "GOD": "GOD"
    }
    return ranks.get(rank_code, "LOW")