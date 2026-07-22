"""Тесты для модуля external_api."""

from unittest.mock import patch, MagicMock
from src.external_api import convert_to_rub


class TestConvertToRub:
    """Тесты функции конвертации валют."""

    def test_convert_rub_no_api_call(self):
        """Рубли не требуют обращения к API."""
        transaction = {
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"code": "RUB"}
            }
        }
        result = convert_to_rub(transaction)
        assert result == 1000.0

    @patch("src.external_api.requests.get")
    def test_convert_usd_success(self, mock_get):
        """Успешная конвертация USD через API."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "rates": {"USD": 0.0110497}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }

        result = convert_to_rub(transaction)
        assert abs(result - 9050.0) < 0.1

    @patch("src.external_api.requests.get")
    def test_convert_api_error(self, mock_get):
        """При ошибке API возвращается исходная сумма."""
        mock_get.side_effect = Exception("Network Error")

        transaction = {
            "operationAmount": {
                "amount": "50.00",
                "currency": {"code": "EUR"}
            }
        }

        result = convert_to_rub(transaction)
        assert result == 50.0

    def test_convert_unknown_currency(self):
        """Неизвестная валюта возвращает исходную сумму."""
        transaction = {
            "operationAmount": {
                "amount": "75.00",
                "currency": {"code": "GBP"}
            }
        }
        result = convert_to_rub(transaction)
        assert result == 75.0
