"""Тесты для модуля services."""

from datetime import datetime
from src.services import simple_search, search_by_phone, investment_bank


class TestSimpleSearch:
    """Тесты простого поиска."""

    def test_found_by_description(self):
        data = [{"Описание": "Покупка в магазине", "Категория": "Супермаркеты"}]
        result = simple_search(data, "магазин")
        assert len(result) == 1

    def test_not_found(self):
        data = [{"Описание": "Тест", "Категория": "Прочее"}]
        result = simple_search(data, "несуществующее")
        assert len(result) == 0

    def test_case_insensitive(self):
        data = [{"Описание": "Магазин", "Категория": "Супермаркеты"}]
        result = simple_search(data, "магазин")
        assert len(result) == 1


class TestSearchByPhone:
    """Тесты поиска по телефону."""

    def test_phone_found(self):
        data = [{"Описание": "Звонок +7 (900) 123-45-67"}]
        result = search_by_phone(data)
        assert len(result) == 1

    def test_no_phone(self):
        data = [{"Описание": "Обычная покупка"}]
        result = search_by_phone(data)
        assert len(result) == 0


class TestInvestmentBank:
    """Тесты Инвесткопилки."""

    def test_rounding_50(self):
        transactions = [
            {"Дата операции": datetime(2023, 5, 1), "Сумма операции": 1712}
        ]
        saved = investment_bank("2023-05", transactions, 50)
        assert saved == 38.0  # 1750 - 1712
