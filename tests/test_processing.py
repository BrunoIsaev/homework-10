import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations():
    """Фикстура с тестовыми данными операций."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},
        {"id": 2, "state": "PENDING", "date": "2024-01-16"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-17"},
        {"id": 4, "state": "CANCELED", "date": "2024-01-18"},
    ]


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    def test_filter_executed(self, sample_operations):
        """Тест фильтрации по статусу EXECUTED."""
        result = filter_by_state(sample_operations, "EXECUTED")
        assert len(result) == 2
        assert all(op["state"] == "EXECUTED" for op in result)

    def test_filter_pending(self, sample_operations):
        """Тест фильтрации по статусу PENDING."""
        result = filter_by_state(sample_operations, "PENDING")
        assert len(result) == 1
        assert result[0]["state"] == "PENDING"

    def test_filter_not_found(self, sample_operations):
        """Тест фильтрации по несуществующему статусу."""
        result = filter_by_state(sample_operations, "NOT_EXIST")
        assert len(result) == 0

    def test_empty_list(self):
        """Тест пустого списка операций."""
        result = filter_by_state([], "EXECUTED")
        assert len(result) == 0

    @pytest.mark.parametrize("state,expected_count", [
        ("EXECUTED", 2),
        ("PENDING", 1),
        ("CANCELED", 1),
        ("NOT_EXIST", 0),
    ])
    def test_different_states(self, sample_operations, state, expected_count):
        """Параметризованный тест для разных статусов."""
        result = filter_by_state(sample_operations, state)
        assert len(result) == expected_count


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_descending(self, sample_operations):
        """Тест сортировки по убыванию."""
        result = sort_by_date(sample_operations)
        assert result[0]["date"] == "2024-01-18"
        assert result[-1]["date"] == "2024-01-15"

    def test_sort_ascending(self, sample_operations):
        """Тест сортировки по возрастанию."""
        result = sort_by_date(sample_operations, reverse=False)
        assert result[0]["date"] == "2024-01-15"
        assert result[-1]["date"] == "2024-01-18"

    def test_empty_list(self):
        """Тест пустого списка операций."""
        result = sort_by_date([])
        assert len(result) == 0

    def test_same_dates(self):
        """Тест сортировки операций с одинаковыми датами."""
        operations = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},
            {"id": 2, "state": "PENDING", "date": "2024-01-15"},
        ]
        result = sort_by_date(operations)
        assert len(result) == 2

    @pytest.mark.parametrize(
        "reverse,first_date,last_date", [
            (True, "2024-01-18", "2024-01-15"),
            (False, "2024-01-15", "2024-01-18"),
        ],
    )
    def test_sort_direction(
        self, sample_operations, reverse, first_date, last_date
    ):
        """Параметризованный тест направления сортировки."""
        result = sort_by_date(sample_operations, reverse=reverse)
        assert result[0]["date"] == first_date
        assert result[-1]["date"] == last_date
