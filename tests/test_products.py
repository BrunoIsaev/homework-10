"""Тесты для модуля products (Наследование)."""

import pytest
from src.products import Product, Smartphone, LawnGrass, Category


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


class TestProductAdd:
    """Тесты __add__ для Product."""

    def test_add_basic(self):
        a = Product("Товар A", "Описание", 100.0, 10)
        b = Product("Товар B", "Описание", 200.0, 2)
        assert a + b == 1400.0

    def test_add_type_error(self):
        """Проверка ограничения сложения разных классов."""
        product = Product("Товар", "Описание", 100.0, 10)
        smartphone = Smartphone("iPhone", "Смартфон", 80000, 5, 3.5, "iPhone 15", 256, "Black")
        with pytest.raises(TypeError):
            _ = product + smartphone


class TestSmartphone:
    """Тесты класса Smartphone."""

    def test_smartphone_creation(self):
        phone = Smartphone("iPhone", "Смартфон", 80000, 5, 3.5, "iPhone 15", 256, "Black")
        assert phone.name == "iPhone"
        assert phone.price == 80000
        assert phone.efficiency == 3.5
        assert phone.model == "iPhone 15"
        assert phone.memory == 256
        assert phone.color == "Black"

    def test_smartphone_str(self):
        phone = Smartphone("iPhone", "Смартфон", 80000, 5, 3.5, "iPhone 15", 256, "Black")
        assert str(phone) == "iPhone, 80000 руб. Остаток: 5 шт."

    def test_smartphone_add_same_class(self):
        phone1 = Smartphone("iPhone", "Описание", 80000, 5, 3.5, "iPhone 15", 256, "Black")
        phone2 = Smartphone("Samsung", "Описание", 60000, 3, 3.0, "Galaxy S24", 128, "White")
        result = phone1 + phone2
        assert result == 80000 * 5 + 60000 * 3

    def test_smartphone_add_different_class(self):
        phone = Smartphone("iPhone", "Описание", 80000, 5, 3.5, "iPhone 15", 256, "Black")
        grass = LawnGrass("Трава", "Газонная", 500, 10, "Россия", "14 дней", "Зеленый")
        with pytest.raises(TypeError):
            _ = phone + grass


class TestLawnGrass:
    """Тесты класса LawnGrass."""

    def test_lawn_grass_creation(self):
        grass = LawnGrass("Трава", "Газонная", 500, 10, "Россия", "14 дней", "Зеленый")
        assert grass.name == "Трава"
        assert grass.price == 500
        assert grass.country == "Россия"
        assert grass.germination_period == "14 дней"
        assert grass.color == "Зеленый"

    def test_lawn_grass_str(self):
        grass = LawnGrass("Трава", "Газонная", 500, 10, "Россия", "14 дней", "Зеленый")
        assert str(grass) == "Трава, 500 руб. Остаток: 10 шт."

    def test_lawn_grass_add_same_class(self):
        grass1 = LawnGrass("Трава 1", "Описание", 500, 10, "Россия", "14 дней", "Зеленый")
        grass2 = LawnGrass("Трава 2", "Описание", 600, 5, "США", "10 дней", "Желтый")
        result = grass1 + grass2
        assert result == 500 * 10 + 600 * 5


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
        assert str(cat) == "Электроника, количество продуктов: 7 шт."


class TestCategoryIterator:
    """Тесты итератора для Category."""

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


class TestCategoryAddProductRestriction:
    """Тесты ограничения добавления в категорию."""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_add_product_valid(self):
        """Проверка добавления Product."""
        cat = Category("Тест", "Описание")
        prod = Product("Товар", "Описание", 100, 5)
        cat.add_product(prod)  # Не должно выбросить исключение
        assert len(cat._Category__products) == 1

    def test_add_smartphone_valid(self):
        """Проверка добавления Smartphone (наследник Product)."""
        cat = Category("Смартфоны", "Телефоны")
        phone = Smartphone("iPhone", "Описание", 80000, 5, 3.5, "iPhone 15", 256, "Black")
        cat.add_product(phone)  # Не должно выбросить исключение
        assert len(cat._Category__products) == 1

    def test_add_lawn_grass_valid(self):
        """Проверка добавления LawnGrass (наследник Product)."""
        cat = Category("Трава", "Газонная")
        grass = LawnGrass("Трава", "Описание", 500, 10, "Россия", "14 дней", "Зеленый")
        cat.add_product(grass)  # Не должно выбросить исключение
        assert len(cat._Category__products) == 1

    def test_add_invalid_object(self):
        """Проверка запрета добавления не-Product объектов."""
        cat = Category("Тест", "Описание")
        with pytest.raises(TypeError):
            cat.add_product("Не продукт")

    def test_add_invalid_type(self):
        """Проверка запрета добавления числа."""
        cat = Category("Тест", "Описание")
        with pytest.raises(TypeError):
            cat.add_product(123)
