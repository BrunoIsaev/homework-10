"""Тесты для модуля products (Инкапсуляция)."""

import pytest
from src.products import Product, Category


class TestProductEncapsulation:
    """Тесты инкапсуляции класса Product."""

    def test_private_price_attribute(self):
        """Проверка, что цена является приватным атрибутом."""
        product = Product("Тест", "Описание", 100.0, 5)
        assert hasattr(product, '_Product__price')
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_price_getter(self):
        """Проверка работы геттера цены."""
        product = Product("Тест", "Описание", 150.50, 10)
        assert product.price == 150.50

    def test_price_setter_valid(self):
        """Проверка сеттера с корректной ценой."""
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = 200.0
        assert product.price == 200.0

    def test_price_setter_invalid(self, capsys):
        """Проверка сеттера с некорректной ценой (<= 0)."""
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = -50.0
        captured = capsys.readouterr()
        msg = "Цена не должна быть нулевая или отрицательная"
        assert msg in captured.out
        assert product.price == 100.0

    def test_new_product_classmethod(self):
        """Проверка класс-метода new_product."""
        data = {
            "name": "Ноутбук",
            "description": "Игровой",
            "price": 50000,
            "quantity": 2
        }
        product = Product.new_product(data)
        assert isinstance(product, Product)
        assert product.name == "Ноутбук"
        assert product.price == 50000.0

    def test_new_product_duplicate(self):
        """Проверка обработки дубликатов в new_product."""
        data1 = {
            "name": "Мышь",
            "description": "Беспроводная",
            "price": 1000,
            "quantity": 5
        }
        data2 = {
            "name": "Мышь",
            "description": "Проводная",
            "price": 1500,
            "quantity": 3
        }

        existing = [Product.new_product(data1)]
        duplicate = Product.new_product(data2, existing)

        assert duplicate is existing[0]
        assert duplicate.quantity == 8
        assert duplicate.price == 1500.0


class TestCategoryEncapsulation:
    """Тесты инкапсуляции класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_private_products_attribute(self):
        """Проверка, что список товаров приватный."""
        cat = Category("Электроника", "Гаджеты")
        assert hasattr(cat, '_Category__products')
        with pytest.raises(AttributeError):
            _ = cat.__products

    def test_add_product_method(self):
        """Проверка метода add_product."""
        cat = Category("Книги", "Литература")
        prod = Product("Python", "Учебник", 500.0, 10)

        cat.add_product(prod)
        assert len(cat._Category__products) == 1
        assert Category.product_count == 1

    def test_products_getter_format(self):
        """Проверка формата вывода геттера products."""
        cat = Category("Одежда", "Футболки")
        prod = Product("Футболка", "Хлопок", 80.0, 15)
        cat.add_product(prod)

        result = cat.products
        expected = "Футболка, 80.0 руб. Остаток: 15 шт.\n"
        assert result == expected

    def test_category_count_increment(self):
        """Проверка автоматического увеличения счетчика категорий."""
        assert Category.category_count == 0
        Category("Кат 1", "Опис")
        assert Category.category_count == 1
