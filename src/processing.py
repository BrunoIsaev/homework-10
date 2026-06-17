from typing import List, Dict, Any


def filter_by_state(
        operations: List[Dict[str, Any]],
        state: str = 'EXECUTED'
) -> List[Dict[str, Any]]:
    """
    Фильтрует список банковских операций по статусу.

    Args:
        operations: Список словарей с данными об операциях
        state: Статус операции для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Список операций, соответствующих указанному статусу
    """
    return [op for op in operations if op.get('state') == state]


from datetime import datetime


def sort_by_date(
        operations: List[Dict[str, Any]],
        reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список банковских операций по дате.

    Args:
        operations: Список словарей с данными об операциях
        reverse: Порядок сортировки: True - по убыванию, False - по возрастанию (по умолчанию True)

    Returns:
        Отсортированный по дате список операций
    """
    return sorted(
        operations,
        key=lambda x: datetime.fromisoformat(x.get('date', '1970-01-01')),
        reverse=reverse
    )
