from datetime import datetime
from typing import Optional

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> Optional[str]:
    """
    Маскирует номер карты или счёта в зависимости от типа.

    Args:
        data: Строка с номером карты или счёта

    Returns:
        Замаскированный номер или None
    """
    if not data:
        return None

    cleaned = data.strip()

    if len(cleaned) < 4:
        return None

    digits = ''.join(filter(str.isdigit, cleaned))

    if len(digits) < 4:
        return None

    # Если 13-19 цифр — это карта, иначе счёт
    if 13 <= len(digits) <= 19:
        return get_mask_card_number(digits)
    else:
        return get_mask_account(digits)


def get_date(date_string: str) -> Optional[str]:
    """
    Преобразует дату из строки в формат ДД.ММ.ГГГГ.

    Args:
        date_string: Дата в формате ISO (YYYY-MM-DD)

    Returns:
        Дата в формате ДД.ММ.ГГГГ или None
    """
    if not date_string:
        return None

    try:
        date_obj = datetime.fromisoformat(date_string)
        return date_obj.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return None
