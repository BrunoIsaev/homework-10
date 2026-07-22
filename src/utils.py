"""Модуль с утилитами для работы с данными."""

import json


def load_json(filepath):
    """Загружает данные из JSON-файла по указанному пути.

    Args:
        filepath: Путь к JSON-файлу.

    Returns:
        Список словарей с данными транзакций.
        Возвращает пустой список, если файл не найден,
        пуст или содержит не список.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data
        return []

    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []
