# homework-10
Homework project for processing banking data


## Работа с CSV и Excel файлами (Домашка 15)

Добавлена поддержка чтения финансовых транзакций из форматов CSV и XLSX с использованием библиотеки pandas.

### Новые функции (src/file_operations.py)
- **read_csv_transactions(filepath)**: Считывает операции из CSV-файла и возвращает список словарей.
- **read_excel_transactions(filepath)**: Считывает операции из Excel-файла (.xlsx) и возвращает список словарей.

### Тестирование
- Написаны тесты с использованием mock и patch для изоляции от реальных файлов.
- Покрыты успешные сценарии и обработка ошибок (FileNotFoundError, Exception).
- Проверено через flake8 и isort.
