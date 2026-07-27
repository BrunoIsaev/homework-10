"""Тесты для модуля reports."""

import pandas as pd
from src.reports import spending_by_category


class TestSpendingByCategory:
    """Тесты отчета по категориям."""

    def test_filter_by_category(self):
        data = {
            "Дата операции": pd.to_datetime(["2023-05-01", "2023-05-02"]),
            "Категория": ["Супермаркеты", "Рестораны"],
            "Сумма операции": [100, 200]
        }
        df = pd.DataFrame(data)
        result = spending_by_category(df, "Супермаркеты", "2023-05-02")
        assert len(result) == 1
        assert result.iloc[0]["Категория"] == "Супермаркеты"

    def test_empty_result(self):
        data = {
            "Дата операции": pd.to_datetime(["2023-05-01"]),
            "Категория": ["Супермаркеты"],
            "Сумма операции": [100]
        }
        df = pd.DataFrame(data)
        result = spending_by_category(df, "Несуществующая", "2023-05-02")
        assert len(result) == 0
