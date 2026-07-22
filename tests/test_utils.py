"""Тесты для модуля utils."""

import json
import os
import tempfile
from src.utils import load_json


class TestLoadJson:
    """Тесты функции загрузки JSON."""

    def test_load_valid_json(self):
        """Загрузка корректного JSON-файла со списком."""
        data = [{"id": 1}, {"id": 2}]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == data
        finally:
            os.unlink(temp_path)

    def test_load_empty_file(self):
        """Загрузка пустого файла возвращает пустой список."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("")
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_load_not_list(self):
        """Загрузка JSON, который не является списком."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump({"key": "value"}, f)
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_load_file_not_found(self):
        """Загрузка несуществующего файла."""
        result = load_json("nonexistent_file.json")
        assert result == []

    def test_load_invalid_json(self):
        """Загрузка некорректного JSON."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("{invalid json}")
            temp_path = f.name

        try:
            result = load_json(temp_path)
            assert result == []
        finally:
            os.unlink(temp_path)
