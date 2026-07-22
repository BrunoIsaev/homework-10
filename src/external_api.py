"""Модуль для работы с внешними API."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction):
    """Конвертирует сумму транзакции в рубли."""
    amount = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]

    if currency_code == "RUB":
        return amount

    if currency_code in ("USD", "EUR") and API_KEY:
        try:
            response = requests.get(
                BASE_URL,
                params={"base": "RUB", "symbols": currency_code},
                headers={"apikey": API_KEY},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            rate = data["rates"][currency_code]
            return round(amount / rate, 2)
        except Exception:
            return amount

    return amount
