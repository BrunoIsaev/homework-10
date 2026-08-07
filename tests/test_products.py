"""Тесты для модуля products (Инкапсуляция + магические методы)."""

import pytest
from src.products import Product, Category


class TestProductEncapsulation:
    """Тесты инкапсуляции класса Product."""

    def test_private_price_attribute(self):
        product = Product("Тест", "Описание", 100.0, 5)
        assert hasattr(product, '_Product__price')
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_price_getter(self):
        product = Product("Тест", "Описание", 150.50, 10)
        assert product.price == 150.50

    def test_price_setter_valid(self):
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = 200.0
        assert product.price == 200.0

    def test_price_setter_invalid(self, capsys):
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = -50.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0

    def test_new_product_classmethod(self):
        data = {"name": "Ноутбук", "description": "Игровой", "price": 50000, "quantity": 2}
        product = Product.new_product(data)
        assert isinstance(product, Product)
        assert product.name == "Ноутбук"
        assert product.price == 50000.0

    def test_new_product_duplicate(self):
        data1 = {"name": "Мышь", "description": "Беспроводная", "price": 1000, "quantity": 5}
        data2 = {"name": "Мышь", "description": "Проводная", "price": 1500, "quantity": 3}
        existing = [Product.new_product(data1)]
        duplicate = Product.new_product(data2, existing)
        assert duplicate is existing[0]
        assert duplicate.quantity == 8
        assert duplicate.price == 1500.0


class TestProductStr:
    """Тесты __str__ для Product."""

    def test_str_format(self):
        product = Product("Футболка", "Хлопок", 80.0, 15)
        assert str(product) == "Футболка, 80.0 руб. Остаток: 15 шт."

    def test_str_integer_price(self):
        product = Product("Книга", "Учебник", 500, 10)
        assert str(product) == "Книга, 500 руб. Остаток: 10 шт."


class TestProductAdd:
    """Тесты __add__ для Product."""

    def test_add_basic(self):
        a = Product("Товар A", "Описание", 100.0, 10)
        b = Product("Товар B", "Описание", 200.0, 2)
        assert a + b == 1400.0

    def test_add_same_product(self):
        a = Product("Товар", "Описание", 50.0, 5)
        assert a + a == 500.0

    def test_add_type_error(self):
        a = Product("Товар", "Описание", 100.0, 10)
        with pytest.raises(TypeError):
            _ = a + 100


class TestCategoryEncapsulation:
    """Тесты инкапсуляции класса Category."""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_private_products_attribute(self):
        cat = Category("Электроника", "Гаджеты")
        assert hasattr(cat, '_Category__products')
        with pytest.raises(AttributeError):
            _ = cat.__products

    def test_add_product_method(self):
        cat = Category("Книги", "Литература")
        prod = Product("Python", "Учебник", 500.0, 10)
        cat.add_product(prod)
        assert len(cat._Category__products) == 1
        assert Category.product_count == 1

    def test_products_getter_format(self):
        cat = Category("Одежда", "Футболки")
        prod = Product("Футболка", "Хлопок", 80.0, 15)
        cat.add_product(prod)
        result = cat.products
        assert "Футболка, 80.0 руб. Остаток: 15 шт." in result

    def test_category_count_increment(self):
        assert Category.category_count == 0
        Category("Кат 1", "Опис")
        assert Category.category_count == 1


class TestCategoryStr:
    """Тесты __str__ для Category."""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_str_empty_category(self):
        cat = Category("Пустая", "Без товаров")
        assert str(cat) == "Пустая, количество продуктов: 0 шт."

    def test_str_with_products(self):
        cat = Category("Электроника", "Гаджеты")
        cat.add_product(Product("Телефон", "Смартфон", 30000, 5))
        cat.add_product(Product("Ноутбук", "Игровой", 80000, 2))
        # 5 + 2 = 7
        assert str(cat) == "Электроника, количество продуктов: 7 шт."


class TestCategoryIterator:
    """Тесты итератора для Category (доп. задание)."""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_iterate_over_products(self):
        cat = Category("Книги", "Литература")
        cat.add_product(Product("Книга 1", "Описание", 100, 5))
        cat.add_product(Product("Книга 2", "Описание", 200, 3))

        products = list(cat)
        assert len(products) == 2
        assert products[0].name == "Книга 1"
        assert products[1].name == "Книга 2"

    def test_for_loop(self):
        cat = Category("Тест", "Описание")
        cat.add_product(Product("A", "Описание", 10, 1))
        cat.add_product(Product("B", "Описание", 20, 2))

        names = []
        for prod in cat:
            names.append(prod.name)
        assert names == ["A", "B"]
