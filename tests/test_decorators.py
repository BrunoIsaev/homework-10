"""Тесты для модуля decorators."""

import pytest

from src.decorators import log


class TestLogDecorator:
    """Тесты декоратора log."""

    def test_log_to_console_success(self, capsys):
        """Проверка логирования успешного вызова в консоль."""

        @log()
        def add(a, b):
            return a + b

        result = add(2, 3)
        captured = capsys.readouterr()

        assert result == 5
        assert "add ok" in captured.out

    def test_log_to_console_error(self, capsys):
        """Проверка логирования ошибки в консоль."""

        @log()
        def divide(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        captured = capsys.readouterr()
        assert "divide error:" in captured.out
        assert "Inputs: (10, 0), {}" in captured.out

    def test_log_to_file_success(self, tmp_path):
        """Проверка записи успешного вызова в файл."""
        log_file = tmp_path / "success_log.txt"
        log_file.touch()

        @log(filename=str(log_file))
        def multiply(x, y):
            return x * y

        multiply(4, 5)

        content = log_file.read_text(encoding="utf-8")
        assert "multiply ok" in content

    def test_log_to_file_error(self, tmp_path):
        """Проверка записи ошибки в файл."""
        log_file = tmp_path / "error_log.txt"
        log_file.touch()

        @log(filename=str(log_file))
        def subtract(a, b):
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            subtract(10, 5)

        content = log_file.read_text(encoding="utf-8")
        assert "subtract error:" in content
        assert "Inputs: (10, 5), {}" in content

    def test_log_with_kwargs(self, capsys):
        """Проверка логирования с именованными аргументами."""

        @log()
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}"

        greet("Alice", greeting="Hi")
        captured = capsys.readouterr()

        assert "greet ok" in captured.out
