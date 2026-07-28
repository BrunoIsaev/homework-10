"""Модуль с основными сущностями интернет-магазина."""

import json
from typing import List, Optional


class Product:
    """Класс, представляющий товар в магазине."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int
    ) -> None:
        """Инициализация товара.

        Args:
            name: Название товара.
            description: Описание товара.
            price: Цена товара (может быть дробной).
            quantity: Количество товара на складе (целое число).
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс, представляющий категорию товаров."""

    # Атрибуты класса для общей статистики
    category_count: int = 0
    product_count: int = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: Optional[List[Product]] = None
    ) -> None:
        """Инициализация категории.

        Args:
            name: Название категории.
            description: Описание категории.
            products: Список объектов Product в этой категории.
        """
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Обновляем атрибуты класса при создании нового объекта
        Category.category_count += 1
        Category.product_count += len(self.products)


def load_products_from_json(filepath: str) -> List[Category]:
    """Загружает данные о категориях и товарах из JSON-файла.

    Args:
        filepath: Путь к JSON-файлу.

    Returns:
        Список объектов Category с вложенными объектами Product.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        categories = []
        for cat_data in data:
            products = [
                Product(
                    name=p["name"],
                    description=p["description"],
                    price=float(p["price"]),
                    quantity=int(p["quantity"])
                )
                for p in cat_data.get("products", [])
            ]
            categories.append(
                Category(
                    name=cat_data["name"],
                    description=cat_data["description"],
                    products=products
                )
            )
        return categories

    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Ошибка чтения JSON: {e}")
        return []
