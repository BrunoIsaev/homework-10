# homework-10
Homework project for processing banking data

## Модуль generators

Модуль содержит генераторы для эффективной обработки больших объёмов данных транзакций.

### Функции

#### filter_by_currency(transactions, currency)
Фильтрует транзакции по заданной валюте и возвращает итератор.

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction["description"])
