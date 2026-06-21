import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number."""

    def test_valid_card_number(self):
        """Тест корректного маскирования номера карты."""
        assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

    def test_card_number_with_spaces(self):
        """Тест маскирования номера карты с пробелами."""
        assert get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"

    def test_short_card_number(self):
        """Тест номера карты короче минимальной длины."""
        assert get_mask_card_number("123") is None

    def test_empty_card_number(self):
        """Тест пустой строки."""
        assert get_mask_card_number("") is None

    def test_none_card_number(self):
        """Тест None значения."""
        assert get_mask_card_number(None) is None

    @pytest.mark.parametrize("card_number,expected", [
        ("1234567890123456", "1234 56** **** 3456"),
        ("4276380012345678", "4276 38** **** 5678"),
        ("5555555555554444", "5555 55** **** 4444"),
    ])
    def test_different_card_numbers(self, card_number, expected):
        """Параметризованный тест для разных номеров карт."""
        assert get_mask_card_number(card_number) == expected


class TestGetMaskAccount:
    """Тесты для функции get_mask_account."""

    def test_valid_account_number(self):
        """Тест корректного маскирования номера счёта."""
        assert get_mask_account("12345678901234567890") == "**7890"

    def test_short_account_number(self):
        """Тест номера счёта короче минимальной длины."""
        assert get_mask_account("123") is None

    def test_empty_account_number(self):
        """Тест пустой строки."""
        assert get_mask_account("") is None

    def test_none_account_number(self):
        """Тест None значения."""
        assert get_mask_account(None) is None

    @pytest.mark.parametrize("account_number,expected", [
        ("12345678901234567890", "**7890"),
        ("98765432109876543210", "**3210"),
        ("11112222333344445555", "**5555"),
    ])
    def test_different_account_numbers(self, account_number, expected):
        """Параметризованный тест для разных номеров счетов."""
        assert get_mask_account(account_number) == expected
