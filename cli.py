from api_client import get_currency_rates, convert_currency
from storage import save_to_file, read_from_file, is_cache_valid, get_cached_base_currency

DISPLAY_CURRENCIES = ["USD", "RUB", "EUR", "GBP"]


def validate_currency(currency_code: str, rates: dict) -> bool:
    """Проверяет, существует ли код валюты в списке доступных"""
    return currency_code in rates


def main():
    path = "currency_rates.json"

    base_currency = input("Введите базовую валюту (например, USD): ").upper()

    if is_cache_valid(path):
        cached_base = get_cached_base_currency(path)
        if cached_base == base_currency:
            print("Используем кэш...")
            data = read_from_file(path)
        else:
            print(f"Кэш содержит данные для {cached_base}, обновляем для {base_currency}...")
            data = get_currency_rates(base_currency)
            if data:
                save_to_file(data, path)
    else:
        print("Обновляем данные...")
        data = get_currency_rates(base_currency)
        if data:
            save_to_file(data, path)

    if not data:
        print("Не удалось получить данные о курсах валют.")
        return

    rates = data["rates"]
    print(f"\nКурсы для {data['base_code']}:")
    for currency in DISPLAY_CURRENCIES:
        print(f"  {currency}: {rates.get(currency, 'N/A')}")

    print("\n--- Конвертер валют ---")
    from_currency = input("Из валюты (код): ").upper()

    if not validate_currency(from_currency, rates):
        print(f"Ошибка: валюта '{from_currency}' не найдена в списке доступных.")
        return

    to_currency = input("В валюту (код): ").upper()

    if not validate_currency(to_currency, rates):
        print(f"Ошибка: валюта '{to_currency}' не найдена в списке доступных.")
        return

    try:
        amount = float(input("Сумма: "))
    except ValueError:
        print("Ошибка: введите корректное число.")
        return

    result = convert_currency(amount, from_currency, to_currency, rates)
    print(f"\n{amount} {from_currency} = {result} {to_currency}")


if __name__ == "__main__":
    main()
