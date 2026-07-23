"""Тесты для модуля bank_operations."""

from src.bank_operations import process_bank_operations, process_bank_search


class TestProcessBankSearch:
    """Тесты функции поиска по описанию."""

    def test_search_found(self):
        """Поиск находит совпадения в описании."""
        data = [
            {"description": "Перевод организации"},
            {"description": "Открытие вклада"},
            {"description": "Перевод со счета"}
        ]
        result = process_bank_search(data, "Перевод")
        assert len(result) == 2
        assert result[0]["description"] == "Перевод организации"
        assert result[1]["description"] == "Перевод со счета"

    def test_search_not_found(self):
        """Поиск не находит совпадений."""
        data = [
            {"description": "Открытие вклада"},
            {"description": "Пополнение счета"}
        ]
        result = process_bank_search(data, "НеexistentWord")
        assert result == []

    def test_search_case_insensitive(self):
        """Поиск регистронезависимый."""
        data = [{"description": "Перевод организации"}]
        result = process_bank_search(data, "перевод")
        assert len(result) == 1

    def test_search_empty_data(self):
        """Поиск в пустом списке возвращает пустой список."""
        result = process_bank_search([], "test")
        assert result == []

    def test_search_missing_description(self):
        """Элемент без поля description не вызывает ошибку."""
        data = [{"id": 1}, {"description": "Test"}]
        result = process_bank_search(data, "Test")
        assert len(result) == 1


class TestProcessBankOperations:
    """Тесты функции подсчета категорий."""

    def test_count_categories(self):
        """Подсчет количества операций по категориям."""
        data = [
            {"description": "Перевод"},
            {"description": "Перевод"},
            {"description": "Оплата"},
            {"description": "Перевод"}
        ]
        categories = ["Перевод", "Оплата"]
        result = process_bank_operations(data, categories)
        assert result == {"Перевод": 3, "Оплата": 1}

    def test_count_zero_category(self):
        """Категория без операций имеет значение 0."""
        data = [{"description": "Перевод"}]
        categories = ["Перевод", "Неизвестная"]
        result = process_bank_operations(data, categories)
        assert result["Неизвестная"] == 0

    def test_count_empty_data(self):
        """Подсчет на пустом списке возвращает нули."""
        categories = ["A", "B"]
        result = process_bank_operations([], categories)
        assert result == {"A": 0, "B": 0}

    def test_count_missing_description(self):
        """Элементы без description считаются как пустая строка."""
        data = [{"id": 1}, {"description": "Test"}]
        categories = ["", "Test"]
        result = process_bank_operations(data, categories)
        assert result[""] == 1
        assert result["Test"] == 1
