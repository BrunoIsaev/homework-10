"""Тесты для модуля views."""

import pandas as pd
from src.views import get_main_page_data


class TestMainPageData:
    """Тесты генерации данных главной страницы."""

    def test_greeting_present(self):
        df = pd.DataFrame()
        result = get_main_page_data("2023-05-20 10:00:00", df)
        assert result["greeting"] == "Доброе утро"

    def test_empty_transactions(self):
        df = pd.DataFrame()
        result = get_main_page_data("2023-05-20 10:00:00", df)
        assert result["cards"] == []
        assert result["top_transactions"] == []
