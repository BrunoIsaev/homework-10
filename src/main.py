"""Главный модуль программы для работы с банковскими транзакциями."""

import json
from typing import List, Dict, Any

from src.bank_operations import process_bank_search
from src.file_operations import read_csv_transactions, read_excel_transactions


def load_json_transactions(filepath: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def filter_by_status(
    data: List[Dict[str, Any]], status: str
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу (регистронезависимо)."""
    return [
        item for item in data
        if item.get("state", "").upper() == status.upper()
    ]


def sort_by_date(
    data: List[Dict[str, Any]], ascending: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""
    return sorted(
        data,
        key=lambda x: x.get("date", ""),
        reverse=not ascending
    )


def filter_by_currency(
    data: List[Dict[str, Any]], currency: str = "RUB"
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по валюте."""
    result = []
    for item in data:
        amount_info = item.get("operationAmount", {})
        curr_code = amount_info.get("currency", {}).get("code", "")
        if curr_code.upper() == currency.upper():
            result.append(item)
    return result


def format_transaction(item: Dict[str, Any]) -> str:
    """Форматирует одну транзакцию для вывода в консоль."""
    date = item.get("date", "")[:10]
    description = item.get("description", "")

    from_info = item.get("from", "")
    to_info = item.get("to", "")
    accounts = ""
    if from_info and to_info:
        accounts = f"{from_info} -> {to_info}"
    elif from_info:
        accounts = from_info
    elif to_info:
        accounts = to_info

    amount_info = item.get("operationAmount", {})
    amount = amount_info.get("amount", 0)
    currency = amount_info.get("currency", {}).get("name", "")

    lines = [f"{date} {description}"]
    if accounts:
        lines.append(accounts)
    lines.append(f"Сумма: {amount} {currency}")
    return "\n".join(lines) + "\n"


def get_user_input(prompt: str, options: List[str]) -> str:
    """Запрашивает ввод у пользователя, пока не получит корректный ответ."""
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in [opt.lower() for opt in options]:
            return user_input
        opts_str = ", ".join(options)
        print(f"Некорректный ввод. Доступные варианты: {opts_str}")


def main() -> None:
    """Основная функция программы с пользовательским интерфейсом."""
    print("Привет! Добро пожаловать в программу работы")
    print("с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = get_user_input("Ваш выбор (1/2/3): ", ["1", "2", "3"])

    data: List[Dict[str, Any]] = []
    file_type = ""

    if choice == "1":
        file_type = "JSON"
        filepath = input("Введите путь к JSON-файлу: ").strip()
        data = load_json_transactions(filepath)
    elif choice == "2":
        file_type = "CSV"
        filepath = input("Введите путь к CSV-файлу: ").strip()
        data = read_csv_transactions(filepath)
    elif choice == "3":
        file_type = "XLSX"
        filepath = input("Введите путь к XLSX-файлу: ").strip()
        data = read_excel_transactions(filepath)

    print(f"Для обработки выбран {file_type}-файл.")
    print(f"Загружено операций: {len(data)}")

    if not data:
        print("Не удалось загрузить данные или файл пуст.")
        return

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    print()
    print("Введите статус, по которому необходимо")
    print("выполнить фильтрацию.")
    statuses_str = ", ".join(valid_statuses)
    print(f"Доступные для фильтровки статусы: {statuses_str}")

    while True:
        status = input("Статус: ").strip().upper()
        if status in valid_statuses:
            break
        print(f'Статус операции "{status}" недоступен.')

    data = filter_by_status(data, status)
    print(f'Операции отфильтрованы по статусу "{status}"')

    # Сортировка по дате
    sort_choice = get_user_input(
        "\nОтсортировать операции по дате? Да/Нет: ",
        ["да", "нет"]
    )
    if sort_choice.lower() == "да":
        order = get_user_input(
            "Отсортировать по возрастанию или по убыванию? ",
            ["по возрастанию", "по убыванию"]
        )
        ascending = order == "по возрастанию"
        data = sort_by_date(data, ascending)
        direction = "по возрастанию" if ascending else "по убыванию"
        print(f"Операции отсортированы {direction}")

    # Фильтрация по валюте
    rub_only = get_user_input(
        "\nВыводить только рублевые транзакции? Да/Нет: ",
        ["да", "нет"]
    )
    if rub_only.lower() == "да":
        data = filter_by_currency(data, "RUB")
        print("Оставлены только рублевые транзакции")

    # Поиск по описанию
    search_choice = get_user_input(
        "\nОтфильтровать список транзакций по "
        "определенному слову в описании? Да/Нет: ",
        ["да", "нет"]
    )
    if search_choice.lower() == "да":
        search_str = input("Введите слово для поиска: ").strip()
        data = process_bank_search(data, search_str)
        print(f'Выполнен поиск по слову "{search_str}"')

    # Вывод результатов
    print()
    print("Распечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(data)}")

    if not data:
        msg = "Не найдено ни одной транзакции, "
        msg += "подходящей под ваши условия фильтрации"
        print(msg)
    else:
        for i, item in enumerate(data, 1):
            print(f"\n{i}.")
            print(format_transaction(item))


if __name__ == "__main__":
    main()
