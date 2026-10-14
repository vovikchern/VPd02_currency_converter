import requests


def get_currency_rates(currency_code: str) -> dict:
    """Получает курсы валют с API"""
    URL = f"https://open.er-api.com/v6/latest/{currency_code}"

    try:
        response = requests.get(URL)
        if response.status_code != 200:
            print(f"Ошибка: Не удалось получить данные о валюте. Статус код: {response.status_code}")
            return None

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: Не удалось подключиться к API. {e}")
        return None


def convert_currency(amount: float, from_currency: str, to_currency: str, rates: dict) -> float:
    """Конвертирует сумму из одной валюты в другую"""
    if from_currency not in rates or to_currency not in rates:
        return None

    amount_in_base = amount / rates[from_currency]
    result = amount_in_base * rates[to_currency]

    return round(result, 4)
