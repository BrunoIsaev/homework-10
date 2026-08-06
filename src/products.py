"""Модуль с основными сущностями интернет-магазина (Инкапсуляция)."""

from typing import List, Optional, Dict, Any


class Product:
    """Класс, представляющий товар в магазине."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int
    ) -> None:
        """Инициализация товара."""
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
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

        # Проверка на дубликаты (доп. задание)
        if existing_products:
            for prod in existing_products:
                if prod.name == name:
                    prod.quantity += quantity
                    if price > prod.price:
                        prod.price = price
                    print(f"Товар '{name}' уже существует.")
                    return prod

        return cls(name, description, price, quantity)


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
        # Приватный список товаров
        self.__products: List[Product] = (
            products if products is not None else []
        )

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список товаров."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для приватного списка товаров."""
        result = ""
        for prod in self.__products:
            line = (
                f"{prod.name}, {prod.price} руб. "
                f"Остаток: {prod.quantity} шт.\n"
            )
            result += line
        return result
