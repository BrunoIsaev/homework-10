"""Модуль с утилитами для работы с данными транзакций."""

import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_transactions(filepath: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла в DataFrame."""
    try:
        # Корректируем путь относительно папки src/
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.path.dirname(__file__), "..", filepath)
            
        logger.info(f"Загрузка транзакций из файла: {filepath}")
        df = pd.read_excel(filepath)
        
        # Автоматическое определение формата даты (решает проблему со временем)
        if "Дата операции" in df.columns:
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
            
        logger.info(f"Успешно загружено {len(df)} транзакций.")
        return df
    except FileNotFoundError:
        logger.error(f"Файл не найден: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {filepath}: {e}")
        return pd.DataFrame()


def get_greeting(date_str: Optional[str] = None) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    if date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    else:
        dt = datetime.now()

    hour = dt.hour
    if 6 <= hour < 12: return "Доброе утро"
    elif 12 <= hour < 18: return "Добрый день"
    elif 18 <= hour < 23: return "Добрый вечер"
    else: return "Доброй ночи"


def load_user_settings(filepath: str = "user_settings.json") -> Dict[str, Any]:
    """Загружает пользовательские настройки из JSON-файла."""
    try:
        # Корректируем путь, так как вызов идет из src/
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.path.dirname(__file__), "..", filepath)
            
        with open(filepath, "r", encoding="utf-8") as f:
            settings = json.load(f)
        return settings
    except FileNotFoundError:
        logger.warning(f"Файл настроек не найден: {filepath}. Используются значения по умолчанию.")
        return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]}
    except json.JSONDecodeError:
        logger.error(f"Ошибка чтения JSON в файле {filepath}")
        return {"user_currencies": [], "user_stocks": []}
