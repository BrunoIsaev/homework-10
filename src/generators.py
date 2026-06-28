"""Модуль с генераторами для обработки транзакций."""


def filter_by_currency(transactions, currency):
    """Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с транзакциями.
        currency: Код валюты для фильтрации (например, 'USD').

    Yields:
        Словарь транзакции, если её валюта совпадает с заданной.
    """
    for transaction in transactions:
        curr = transaction.get("operationAmount", {})
        curr = curr.get("currency", {})
        if curr.get("code") == currency:
            yield transaction


def transaction_descriptions(transactions):
    """Генерирует описания транзакций по очереди.

    Args:
        transactions: Список словарей с транзакциями.

    Yields:
        Строка с описанием каждой транзакции.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start, stop):
    """Генерирует номера банковских карт в заданном диапазоне.

    Args:
        start: Начальное значение диапазона (включительно).
        stop: Конечное значение диапазона (включительно).

    Yields:
        Строка с номером карты в формате 'XXXX XXXX XXXX XXXX'.
    """
    for number in range(start, stop + 1):
        formatted = f"{number:016d}"
        yield (
            formatted[:4] + " "
            + formatted[4:8] + " "
            + formatted[8:12] + " "
            + formatted[12:]
        )
