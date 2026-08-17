"""Модуль с основными сущностями интернет-магазина (Обработка исключений)."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление продукта."""
        pass

    @abstractmethod
    def __add__(self, other: 'BaseProduct') -> float:
        """Сложение двух продуктов."""
        pass


class PrintMixin:
    """Миксин для печати информации о создании объекта."""

    def print_creation_info(self, *args, **kwargs):
        """Печатает информацию о создании объекта."""
        class_name = self.__class__.__name__
        args_repr = [repr(arg) for arg in args]
        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        all_args = args_repr + kwargs_repr
        print(f"{class_name}({', '.join(all_args)})")


class Product(PrintMixin, BaseProduct):
    """Класс, представляющий товар в магазине."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int
    ) -> None:
        """Инициализация товара."""
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.print_creation_info(name, description, price, quantity)
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для приватного атрибута цены с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    def __str__(self) -> str:
        """Строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        """Сложение двух товаров: сумма произведений цены на количество.
        Можно складывать только объекты одинакового класса."""
        if type(self) != type(other):
            raise TypeError(
                f"Нельзя сложить {type(self).__name__} и {type(other).__name__}"
            )
        return self.__price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(
        cls,
        product_data: Dict[str, Any],
        existing_products: Optional[List['Product']] = None
    ) -> 'Product':
        """Класс-метод для создания товара из словаря."""
        name = product_data["name"]
        description = product_data["description"]
        price = float(product_data["price"])
        quantity = int(product_data["quantity"])

        # Проверка на дубликаты
        if existing_products:
            for prod in existing_products:
                if prod.name == name:
                    prod.quantity += quantity
                    if price > prod.price:
                        prod.price = price
                    print(f"Товар '{name}' уже существует.")
                    return prod

        return cls(name, description, price, quantity)


class Smartphone(Product):
    """Класс-наследник Product для смартфонов."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str
    ) -> None:
        """Инициализация смартфона."""
        Product.__init__(self, name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс-наследник Product для газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str
    ) -> None:
        """Инициализация газонной травы."""
        Product.__init__(self, name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс, представляющий категорию товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: Optional[List[Product]] = None
    ) -> None:
        """Инициализация категории."""
        self.name = name
        self.description = description
        self.__products: List[Product] = (
            products if products is not None else []
        )

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список товаров."""
        if not isinstance(product, Product):
            raise TypeError(
                f"Нельзя добавить объект типа {type(product).__name__}. "
                "Можно добавлять только Product и его наследников."
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для приватного списка товаров."""
        result = ""
        for prod in self.__products:
            result += str(prod) + "\n"
        return result

    def __str__(self) -> str:
        """Строковое представление категории."""
        total_quantity = sum(prod.quantity for prod in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """Возвращает итератор по товарам."""
        return iter(self.__products)

    def average_price(self) -> float:
        """Подсчитывает средний ценник всех товаров в категории.
        Возвращает 0, если товаров нет."""
        try:
            total = sum(prod.price for prod in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            return 0
