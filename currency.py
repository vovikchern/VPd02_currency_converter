import requests
import json
import os
from datetime import datetime

from api_client import get_currency_rates
from storage import save_to_file, read_from_file, is_cache_valid

DISPLAY_CURRENCIES = ["USD", "RUB", "EUR", "GBP"]


if __name__ == "__main__":
    path = "currency_rates.json"

    if is_cache_valid(path):
        print("Используем кэш...")
        data = read_from_file(path)
    else:
        print("Обновляем данные...")
        base_currency = input("Введите базовую валюту (например, USD): ").upper()
        data = get_currency_rates(base_currency)
        if data:
            save_to_file(data, path)

    if data:
        print(f"\nКурсы для {data['base_code']}:")
        for currency in DISPLAY_CURRENCIES:
            print(f"  {currency}: {data['rates'].get(currency, 'N/A')}")
