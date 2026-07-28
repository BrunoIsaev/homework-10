"""Тесты для модуля products (Product и Category)."""

from src.products import Product, Category


class TestProduct:
    """Тесты класса Product."""

    def test_product_creation(self):
        """Проверка корректной инициализации товара."""
        product = Product("Смартфон", "Мощный смартфон", 50000.0, 10)
        assert product.name == "Смартфон"
        assert product.description == "Мощный смартфон"
        assert product.price == 50000.0
        assert product.quantity == 10

    def test_product_float_price(self):
        """Проверка, что цена может быть дробной."""
        product = Product("Чехол", "Силиконовый чехол", 999.99, 50)
        assert product.price == 999.99


class TestCategory:
    """Тесты класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_creation(self):
        """Проверка корректной инициализации категории."""
        cat = Category("Электроника", "Гаджеты и техника")
        assert cat.name == "Электроника"
        assert cat.description == "Гаджеты и техника"
        assert cat.products == []

    def test_category_with_products(self):
        """Проверка инициализации категории с товарами."""
        p1 = Product("Ноутбук", "Игровой ноутбук", 100000.0, 5)
        p2 = Product("Мышь", "Беспроводная мышь", 2000.0, 20)
        cat = Category("Компьютеры", "ПК и периферия", [p1, p2])

        assert len(cat.products) == 2
        assert cat.products[0].name == "Ноутбук"
        assert cat.products[1].name == "Мышь"

    def test_category_count_increment(self):
        """Проверка автоматического увеличения счетчика категорий."""
        assert Category.category_count == 0

        Category("Категория 1", "Описание 1")
        assert Category.category_count == 1

        Category("Категория 2", "Описание 2")
        assert Category.category_count == 2

    def test_product_count_increment(self):
        """Проверка автоматического увеличения счетчика товаров."""
        assert Category.product_count == 0

        p1 = Product("Товар 1", "Описание", 100.0, 1)
        p2 = Product("Товар 2", "Описание", 200.0, 2)

        Category("Кат 1", "Опис", [p1, p2])
        assert Category.product_count == 2

        Category("Кат 2", "Опис", [p1])
        assert Category.product_count == 3

    def test_empty_category_product_count(self):
        """Проверка, что пустая категория не увеличивает счетчик товаров."""
        Category("Пустая категория", "Нет товаров")
        assert Category.product_count == 0
