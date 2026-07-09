"""Модуль с декораторами для логирования."""

import functools


def log(filename=None):
    """Декоратор для логирования вызовов функций и их результатов.

    Args:
        filename: Имя файла для записи логов.
                  Если None, логи выводятся в консоль.

    Returns:
        Декоратор, который оборачивает целевую функцию.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
            except Exception as e:
                # Формируем сообщение об ошибке
                err_msg = f"{func.__name__} error: {e}"
                inputs_msg = f"Inputs: {args}, {kwargs}"
                log_message = f"{err_msg}. {inputs_msg}"

                # Записываем лог до выброса исключения
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)
                raise

                # Логируем успешное выполнение
            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(log_message + "\n")
            else:
                print(log_message)

            return result

        return wrapper

    return decorator
