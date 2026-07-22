# homework-10
Homework project for processing banking data


## Модуль decorators

Модуль содержит декораторы для логирования работы функций.

### Декоратор log

Декоратор `log` автоматически регистрирует детали выполнения функций: имя функции, результат или информацию об ошибках.

**Параметры:**
- `filename` (опционально) — имя файла для записи логов. Если не указан, логи выводятся в консоль.

**Пример использования:**

```python
from src.decorators import log

# Логирование в файл
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)
# В файле mylog.txt появится: my_function ok

# Логирование в консоль
@log()
def another_function(a, b):
    return a / b

another_function(10, 0)
# В консоли: another_function error: division by zero. Inputs: (10, 0), {}
```

### Тестирование

Покрытие кода модуля decorators составляет **100%**.

Запуск тестов:
```bash
PYTHONPATH=. pytest --cov=src.decorators --cov-report=html -v
```


## Модули utils и external_api (Домашка 13)

Модули для работы с JSON-файлами и конвертации валют через внешнее API.

### Функция load_json (src/utils.py)
Загружает данные из JSON-файла. Возвращает список словарей или пустой список при ошибках.

### Функция convert_to_rub (src/external_api.py)
Конвертирует сумму транзакции в рубли. Для USD/EUR обращается к Exchange Rates Data API.
Ключ API хранится в переменной окружения EXCHANGE_RATE_API_KEY (.env).

### Тестирование
- Написаны тесты с использованием mock и patch.
- Покрытие кода проверено через pytest-cov.
- Проверено через flake8 (0 ошибок) и isort.
