from typing import Optional


def get_mask_card_number(card_number: str) -> Optional[str]:
    """
    Маскирует номер банковской карты.

    Args:
        card_number: Номер карты для маскирования

    Returns:
        Замаскированный номер карты или None, если номер некорректен
    """
    if not card_number or len(card_number) < 4:
        return None

    digits = ''.join(filter(str.isdigit, card_number))

    if len(digits) < 4:
        return None

    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account_number: str) -> Optional[str]:
    """
    Маскирует номер счёта.

    Args:
        account_number: Номер счёта для маскирования

    Returns:
        Замаскированный номер счёта или None, если номер некорректен
    """
    if not account_number or len(account_number) < 4:
        return None

    digits = ''.join(filter(str.isdigit, account_number))

    if len(digits) < 4:
        return None

    return f"**{digits[-4:]}"
