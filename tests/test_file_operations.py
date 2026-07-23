"""Тесты для модуля file_operations."""

from unittest.mock import MagicMock, patch

import pandas as pd

from src.file_operations import read_csv_transactions, read_excel_transactions


class TestReadCsvTransactions:
    """Тесты функции чтения CSV."""

    @patch("src.file_operations.pd.read_csv")
    def test_read_csv_success(self, mock_read_csv):
        """Успешное чтение CSV возвращает список словарей."""
        # Создаем мок DataFrame
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200}
        ]
        mock_read_csv.return_value = mock_df

        result = read_csv_transactions("data/test.csv")

        assert result == [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
        mock_read_csv.assert_called_once_with("data/test.csv")

    @patch("src.file_operations.pd.read_csv")
    def test_read_csv_file_not_found(self, mock_read_csv):
        """При отсутствии файла возвращается пустой список."""
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        result = read_csv_transactions("nonexistent.csv")

        assert result == []

    @patch("src.file_operations.pd.read_csv")
    def test_read_csv_other_error(self, mock_read_csv):
        """При другой ошибке возвращается пустой список."""
        mock_read_csv.side_effect = Exception("Some error")

        result = read_csv_transactions("data/bad.csv")

        assert result == []


class TestReadExcelTransactions:
    """Тесты функции чтения Excel."""

    @patch("src.file_operations.pd.read_excel")
    def test_read_excel_success(self, mock_read_excel):
        """Успешное чтение Excel возвращает список словарей."""
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [
            {"id": 3, "amount": 300}
        ]
        mock_read_excel.return_value = mock_df

        result = read_excel_transactions("data/test.xlsx")

        assert result == [{"id": 3, "amount": 300}]
        mock_read_excel.assert_called_once_with("data/test.xlsx")

    @patch("src.file_operations.pd.read_excel")
    def test_read_excel_file_not_found(self, mock_read_excel):
        """При отсутствии файла возвращается пустой список."""
        mock_read_excel.side_effect = FileNotFoundError("File not found")

        result = read_excel_transactions("nonexistent.xlsx")

        assert result == []

    @patch("src.file_operations.pd.read_excel")
    def test_read_excel_other_error(self, mock_read_excel):
        """При другой ошибке возвращается пустой список."""
        mock_read_excel.side_effect = Exception("Some error")

        result = read_excel_transactions("data/bad.xlsx")

        assert result == []
