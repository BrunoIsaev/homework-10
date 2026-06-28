"""Тесты для модуля generators."""

import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


@pytest.fixture
def transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


class TestFilterByCurrency:
    """Тесты функции filter_by_currency."""

    def test_filter_usd(self, transactions):
        """Фильтрация транзакций по валюте USD."""
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 3
        for t in result:
            assert t["operationAmount"]["currency"]["code"] == "USD"

    def test_filter_rub(self, transactions):
        """Фильтрация транзакций по валюте RUB."""
        result = list(filter_by_currency(transactions, "RUB"))
        assert len(result) == 2
        for t in result:
            assert t["operationAmount"]["currency"]["code"] == "RUB"

    def test_filter_no_match(self, transactions):
        """Фильтрация по несуществующей валюте."""
        result = list(filter_by_currency(transactions, "EUR"))
        assert result == []

    def test_empty_transactions(self):
        """Пустой список транзакций."""
        result = list(filter_by_currency([], "USD"))
        assert result == []

    @pytest.mark.parametrize(
        "currency, expected_count",
        [("USD", 3), ("RUB", 2), ("EUR", 0)],
    )
    def test_parametrized_filter(
        self, transactions, currency, expected_count
    ):
        """Параметризованный тест фильтрации."""
        result = list(filter_by_currency(transactions, currency))
        assert len(result) == expected_count


class TestTransactionDescriptions:
    """Тесты генератора transaction_descriptions."""

    def test_descriptions_count(self, transactions):
        """Количество описаний равно количеству транзакций."""
        result = list(transaction_descriptions(transactions))
        assert len(result) == len(transactions)

    def test_descriptions_values(self, transactions):
        """Описания соответствуют полям description."""
        result = list(transaction_descriptions(transactions))
        expected = [t["description"] for t in transactions]
        assert result == expected

    def test_empty_transactions(self):
        """Пустой список возвращает пустой генератор."""
        result = list(transaction_descriptions([]))
        assert result == []

    @pytest.mark.parametrize(
        "input_data, expected",
        [
            (
                [{"description": "Тест 1"}, {"description": "Тест 2"}],
                ["Тест 1", "Тест 2"],
            ),
            ([{"description": "Один"}], ["Один"]),
            ([], []),
        ],
    )
    def test_parametrized_descriptions(self, input_data, expected):
        """Параметризованный тест описаний."""
        result = list(transaction_descriptions(input_data))
        assert result == expected


class TestCardNumberGenerator:
    """Тесты генератора card_number_generator."""

    def test_basic_range(self):
        """Генерация номеров карт в диапазоне 1-5."""
        result = list(card_number_generator(1, 5))
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]
        assert result == expected

    def test_single_value(self):
        """Генерация одного номера карты."""
        result = list(card_number_generator(1, 1))
        assert result == ["0000 0000 0000 0001"]

    def test_format(self):
        """Проверка формата номера карты."""
        result = list(card_number_generator(1234, 1234))
        assert result[0] == "0000 0000 0000 1234"
        parts = result[0].split(" ")
        assert len(parts) == 4
        for part in parts:
            assert len(part) == 4
            assert part.isdigit()

    def test_large_numbers(self):
        """Генерация больших номеров карт."""
        result = list(card_number_generator(
            9999999999999999, 9999999999999999
        ))
        assert result == ["9999 9999 9999 9999"]

    @pytest.mark.parametrize(
        "start, stop, expected_first, expected_last",
        [
            (1, 3, "0000 0000 0000 0001",
             "0000 0000 0000 0003"),
            (100, 102, "0000 0000 0000 0100",
             "0000 0000 0000 0102"),
        ],
    )
    def test_parametrized_generator(
        self, start, stop, expected_first, expected_last
    ):
        """Параметризованный тест генератора карт."""
        result = list(card_number_generator(start, stop))
        assert result[0] == expected_first
        assert result[-1] == expected_last
        assert len(result) == stop - start + 1
