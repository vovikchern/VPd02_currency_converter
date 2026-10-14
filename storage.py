import json
import os
from datetime import datetime


def save_to_file(data: dict, path="currency_rates.json"):
    """Сохраняет данные в JSON файл"""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_from_file(path="currency_rates.json"):
    """Читает данные из JSON файла"""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_cache_valid(path="currency_rates.json", max_age_hours=24) -> bool:
    """Проверяет, актуален ли кэш (моложе указанного количества часов)"""
    if not os.path.exists(path):
        return False

    file_age = datetime.now().timestamp() - os.path.getmtime(path)
    return file_age < max_age_hours * 3600


def get_cached_base_currency(path="currency_rates.json") -> str:
    """Получает базовую валюту из кэша"""
    if not os.path.exists(path):
        return None
    
    data = read_from_file(path)
    return data.get("base_code")
