"""Модуль с утилитами для работы с данными."""

import json
import logging

# Настройка логгера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаем handler для записи в файл
file_handler = logging.FileHandler(
    "logs/utils.log", mode="w", encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)


def load_json(filepath):
    """Загружает данные из JSON-файла по указанному пути.

    Args:
        filepath: Путь к JSON-файлу.

    Returns:
        Список словарей с данными транзакций.
        Возвращает пустой список, если файл не найден,
        пуст или содержит не список.
    """
    logger.info("Попытка загрузки JSON-файла: %s", filepath)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            logger.info(
                "Файл успешно загружен. Найдено записей: %d", len(data)
            )
            return data

        logger.error("JSON-файл содержит не список: %s", filepath)
        return []

    except FileNotFoundError:
        logger.error("Файл не найден: %s", filepath)
        return []
    except json.JSONDecodeError as e:
        logger.error(
            "Ошибка декодирования JSON в файле %s: %s", filepath, e
        )
        return []
    except OSError as e:
        logger.error("Ошибка при чтении файла %s: %s", filepath, e)
        return []
