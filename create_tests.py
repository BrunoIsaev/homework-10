"""Скрипт для создания тестовых файлов."""

import os

# Код для test_utils.py
utils_test_code = '''"""Тесты для модуля utils."""

import json
import os
import tempfile
import pytest
from src.utils import load_json


class TestLoadJson:
    """Тесты функции загрузки JSON."""

    def test_load_valid_json(self):
        """Загрузка корректного JSON-файла со списком."""
        data = [{"id": 1}, {"id": 2}]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == data
        finally:
            os.unlink(temp_path)

    def test_load_empty_file(self):
        """Загрузка пустого файла возвращает пустой список."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_load_not_list(self):
        """Загрузка JSON, который не является списком."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"key": "value"}, f)
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_load_file_not_found(self):
        """Загрузка несуществующего файла возвращает пустой список."""
        result = load_json("nonexistent_file.json")
        assert result == []

    def test_load_invalid_json(self):
        """Загрузка некорректного JSON возвращает пустой список."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{invalid json}")
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)
'''

# Код для test_external_api.py
api_test_code = '''"""Тесты для модуля external_api."""

import pytest
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
        mock_response.json.return_value = {"rates": {"USD": 0.0110497}}
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
'''

# Записываем файлы
os.makedirs("tests", exist_ok=True)

with open("tests/test_utils.py", "w", encoding="utf-8") as f:
    f.write(utils_test_code)
print("✅ tests/test_utils.py created!")

with open("tests/test_external_api.py", "w", encoding="utf-8") as f:
    f.write(api_test_code)
print("✅ tests/test_external_api.py created!")

print("\n🎉 Все тестовые файлы созданы успешно!")
