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
