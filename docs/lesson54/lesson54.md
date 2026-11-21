# Урок 54. Добавить название

## Проверка ДЗ

Разбираем решение домашнего задания с [урока 53](../lesson53/lesson53.md) — «Бестселлер»:

[Условие задания](https://education.yandex.ru/ege/inf/task/ae105bf0-7e72-4cac-97e0-aba1e85ee5b9)

На занятии посмотрим тесты, которые вы сохранили при проверке — на примере из текста задачи и на граничных случаях, — и разберём, где в решении с ошибкой спрятана ошибка.

Что делает код: по записям о товарах (цена, продан/в наличии) собирает для каждого товара цену, число проданных и остаток, считает среднюю цену по всем записям, оставляет товары с ценой выше средней и по правилам из условия находит бестселлер. Выводит выручку (продано × цена) и остаток товара.

<details>
<summary>Решение с ошибкой</summary>

```python
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=False)
class ArticleData:
    sold: int = 0
    price: int = -1
    remained: int = 0

article_data_dict = defaultdict(ArticleData)
sum_prices = 0
n_prices = 0

with open('26_5.txt', 'r') as f:
    f.readline()

    while (line := f.readline()):
        art, price, available = list(map(int, line.split()))
        article_data = article_data_dict[art]
        article_data.price = price
        if available:
            article_data.remained += 1
        else:
            article_data.sold += 1

        sum_prices += price
        n_prices += 1

mean_price = sum_prices / n_prices

article_data_values = list(article_data_dict.values())
article_data_values = list(filter(lambda x: x.price > mean_price, article_data_values))

bestseller = max(article_data_values, key=lambda x: [x.sold, x.price, x.remained])

income = bestseller.sold * bestseller.price
remained = bestseller.remained
print(income)
print(remained)
```

</details>

<details>
<summary>Разбор ошибки</summary>

Ключ функции `max`: `key=lambda x: [x.sold, x.price, x.remained]`. Сравнение идёт по трём позициям: сначала максимум проданных, потом максимум цены, и наконец — максимум остатка. А по условию при равенстве первых двух нужно выбрать товар с **минимальным** остатком. Чтобы через `max` выбрать минимум, нужно максимизировать отрицание: `key=lambda x: [x.sold, x.price, -x.remained]`.
</details>

<details>
<summary>Правильное решение</summary>

```python
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=False)
class ArticleData:
    sold: int = 0
    price: int = -1
    remained: int = 0

article_data_dict = defaultdict(ArticleData)
sum_prices = 0
n_prices = 0

with open('26_5.txt', 'r') as f:
    f.readline()

    while (line := f.readline()):
        art, price, available = list(map(int, line.split()))
        article_data = article_data_dict[art]
        article_data.price = price
        if available:
            article_data.remained += 1
        else:
            article_data.sold += 1

        sum_prices += price
        n_prices += 1

mean_price = sum_prices / n_prices

article_data_values = list(article_data_dict.values())
article_data_values = list(filter(lambda x: x.price > mean_price, article_data_values))

bestseller = max(article_data_values, key=lambda x: [x.sold, x.price, -x.remained])

income = bestseller.sold * bestseller.price
remained = bestseller.remained
print(income)
print(remained)
```

</details>
