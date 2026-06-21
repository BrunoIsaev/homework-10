import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тесты для функции mask_account_card."""

    def test_card_number_masking(self):
        """Тест маскирования номера карты."""
        assert mask_account_card("1234567890123456") == "1234 56** **** 3456"

    def test_account_number_masking(self):
        """Тест маскирования номера счёта."""
        assert mask_account_card("12345678901234567890") == "**7890"

    def test_empty_string(self):
        """Тест пустой строки."""
        assert mask_account_card("") is None

    def test_short_string(self):
        """Тест короткой строки."""
        assert mask_account_card("123") is None

    def test_none_value(self):
        """Тест None значения."""
        assert mask_account_card(None) is None

    @pytest.mark.parametrize("data,expected", [
        ("1234567890123456", "1234 56** **** 3456"),
        ("4276380012345678", "4276 38** **** 5678"),
        ("12345678901234567890", "**7890"),
        ("98765432109876543210", "**3210"),
    ])
    def test_different_cards_and_accounts(self, data, expected):
        """Параметризованный тест для разных карт и счетов."""
        assert mask_account_card(data) == expected


class TestGetDate:
    """Тесты для функции get_date."""

    def test_valid_date(self):
        """Тест корректной даты."""
        assert get_date("2024-01-15") == "15.01.2024"

    def test_another_valid_date(self):
        """Тест другой корректной даты."""
        assert get_date("2024-12-31") == "31.12.2024"

    def test_empty_string(self):
        """Тест пустой строки."""
        assert get_date("") is None

    def test_none_value(self):
        """Тест None значения."""
        assert get_date(None) is None

    def test_invalid_date_format(self):
        """Тест некорректного формата даты."""
        assert get_date("invalid-date") is None

    @pytest.mark.parametrize("date_string,expected", [
        ("2024-01-15", "15.01.2024"),
        ("2024-06-20", "20.06.2024"),
        ("2023-12-01", "01.12.2023"),
    ])
    def test_different_dates(self, date_string, expected):
        """Параметризованный тест для разных дат."""
        assert get_date(date_string) == expected
