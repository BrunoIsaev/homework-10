# homework-10

Homework project for processing banking data

## Description

Проект для обработки банковских операций клиента.

## Installation

Клонируйте репозиторий и установите зависимости.

## Usage

### filter_by_state

Фильтрует операции по статусу. По умолчанию ищет EXECUTED.

Пример:
filter_by_state(operations, state="EXECUTED")

### sort_by_date

Сортирует операции по дате. По умолчанию по убыванию.

Пример:
sort_by_date(operations, reverse=True)
