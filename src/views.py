"""Модуль для генерации JSON-ответов веб-страниц."""

import logging
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import requests

from src.utils import load_user_settings, get_greeting

logger = logging.getLogger(__name__)


def filter_data_by_month(df: pd.DataFrame, date_str: str) -> pd.DataFrame:
    """Фильтрует DataFrame по текущему месяцу входящей даты."""
    try:
        target_date = pd.to_datetime(date_str)
        start_month = target_date.replace(day=1)
        # Конец месяца (первый день следующего месяца)
        if target_date.month == 12:
            end_month = target_date.replace(year=target_date.year + 1, month=1, day=1)
        else:
            end_month = target_date.replace(month=target_date.month + 1, day=1)
            
        mask = (df["Дата операции"] >= start_month) & (df["Дата операции"] < end_month)
        return df[mask].copy()
    except Exception as e:
        logger.error(f"Ошибка фильтрации по дате {date_str}: {e}")
        return df


def process_cards(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Группирует траты по картам и считает кешбэк."""
    cards_data = []
    if "Номер карты" not in transactions.columns or "Сумма операции" not in transactions.columns:
        return cards_data

    grouped = transactions.groupby("Номер карты")
    for card_num, group in grouped:
        # Считаем только расходы (отрицательные суммы делаем положительными для отображения трат)
        expenses = group[group["Сумма операции"] < 0]["Сумма операции"].sum()
        total_spent = abs(expenses)
        
        cashback = round(total_spent * 0.01, 2)  # 1% кешбэк
        last_digits = str(card_num)[-4:] if len(str(card_num)) >= 4 else str(card_num)
        
        cards_data.append({
            "last_digits": last_digits,
            "total_spent": round(total_spent, 2),
            "cashback": cashback
        })
    return cards_data


def process_top_transactions(transactions: pd.DataFrame, top_n: int = 5) -> List[Dict[str, Any]]:
    """Формирует топ-N транзакций по сумме платежа."""
    top_transactions = []
    if "Сумма платежа" not in transactions.columns:
        return top_transactions

    sorted_df = transactions.sort_values(by="Сумма платежа", ascending=False).head(top_n)
    
    for _, row in sorted_df.iterrows():
        date_fmt = row["Дата операции"].strftime("%d.%m.%Y") if pd.notna(row["Дата операции"]) else ""
        top_transactions.append({
            "date": date_fmt,
            "amount": round(float(row["Сумма платежа"]), 2),
            "category": row.get("Категория", ""),
            "description": row.get("Описание", "")
        })
    return top_transactions


def get_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    """Получает курсы валют через API ЦБ РФ."""
    rates = []
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=10)
        data = response.json()
        for curr in currencies:
            if curr in data["Valute"]:
                rates.append({"currency": curr, "rate": data["Valute"][curr]["Value"]})
    except Exception as e:
        logger.warning(f"Не удалось получить курсы валют: {e}")
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    """Получает цены акций (используем мок, т.к. бесплатные API требуют ключей)."""
    prices = []
    mock_prices = {
        "AAPL": 150.12, "AMZN": 3173.18, "GOOGL": 2742.39,
        "MSFT": 296.71, "TSLA": 1007.08
    }
    for stock in stocks:
        price = mock_prices.get(stock, 0.0)
        if price > 0:
            prices.append({"stock": stock, "price": price})
    return prices


def get_main_page_data(date_str: str, transactions_df: pd.DataFrame) -> Dict[str, Any]:
    """Генерирует JSON-ответ для главной страницы."""
    logger.info(f"Генерация данных для главной страницы за дату: {date_str}")
    
    # 1. Фильтруем данные по месяцу (как в ТЗ)
    filtered_df = filter_data_by_month(transactions_df, date_str)
    
    # 2. Приветствие
    greeting = get_greeting(date_str)
    
    # 3. Данные по картам (вынесено в отдельную функцию)
    cards_data = process_cards(filtered_df)
    
    # 4. Топ-5 транзакций (вынесено в отдельную функцию)
    top_transactions = process_top_transactions(filtered_df)
    
    # 5. Курсы валют и акции
    settings = load_user_settings()
    currency_rates = get_currency_rates(settings.get("user_currencies", []))
    stock_prices = get_stock_prices(settings.get("user_stocks", []))
    
    return {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
