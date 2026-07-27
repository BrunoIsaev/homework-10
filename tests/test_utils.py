"""Тесты для модуля utils."""

import pytest
from src.utils import get_greeting


class TestGetGreeting:
    """Тесты функции приветствия."""

    def test_morning(self):
        assert get_greeting("2023-05-20 08:00:00") == "Доброе утро"

    def test_day(self):
        assert get_greeting("2023-05-20 14:00:00") == "Добрый день"

    def test_evening(self):
        assert get_greeting("2023-05-20 20:00:00") == "Добрый вечер"

    def test_night(self):
        assert get_greeting("2023-05-20 02:00:00") == "Доброй ночи"
