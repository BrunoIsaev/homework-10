"""Модуль для маскировки конфиденциальных данных."""

import logging

# Настройка логгера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаем handler для записи в файл
file_handler = logging.FileHandler(
    "logs/masks.log", mode="w", encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)


def get_masked_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты.

    Args:
        card_number: Номер карты в виде строки.

    Returns:
        Замаскированный номер карты (первые 6 и последние 4 цифры видны).

    Raises:
        ValueError: Если номер карты некорректен.
    """
    logger.info("Попытка маскировки номера карты")

    if not card_number or not card_number.isdigit():
        logger.error("Некорректный номер карты: %s", card_number)
        raise ValueError("Некорректный номер карты")

    if len(card_number) != 16:
        logger.error(
            "Длина номера карты должна быть 16 цифр, получено: %d",
            len(card_number),
        )
        raise ValueError("Длина номера карты должна быть 16 цифр")

    masked = f"{card_number[:6]}{'*' * 7}{card_number[-4:]}"
    logger.info("Номер карты успешно замаскирован")
    return masked


def get_masked_account(account_number: str) -> str:
    """Маскирует номер счета.

    Args:
        account_number: Номер счета в виде строки.

    Returns:
        Замаскированный номер счета (последние 4 цифры видны).

    Raises:
        ValueError: Если номер счета некорректен.
    """
    logger.info("Попытка маскировки номера счета")

    if not account_number or not account_number.isdigit():
        logger.error("Некорректный номер счета: %s", account_number)
        raise ValueError("Некорректный номер счета")

    if len(account_number) < 4:
        logger.error("Номер счета слишком короткий: %s", account_number)
        raise ValueError("Номер счета слишком короткий")

    masked = f"{'*' * (len(account_number) - 4)}{account_number[-4:]}"
    logger.info("Номер счета успешно замаскирован")
    return masked
