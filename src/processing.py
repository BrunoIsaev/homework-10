from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(
    operations: List[Dict[str, Any]],
    state: str = 'EXECUTED'
) -> List[Dict[str, Any]]:
    """
    Фильтрует список банковских операций по статусу.

    Args:
        operations: Список словарей с данными
        state: Статус операции для фильтрации

    Returns:
        Список операций с указанным статусом
    """
    return [
        op for op in operations
        if op.get('state') == state
    ]


def sort_by_date(
    operations: List[Dict[str, Any]],
    reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список банковских операций по дате.

    Args:
        operations: Список словарей с данными
        reverse: Порядок сортировки

    Returns:
        Отсортированный по дате список операций
    """
    return sorted(
        operations,
        key=lambda x: datetime.fromisoformat(
            x.get('date', '1970-01-01')
        ),
        reverse=reverse
    )
