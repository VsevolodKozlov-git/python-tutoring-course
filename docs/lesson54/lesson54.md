# Урок 54. Продолжаем решать и проверять 26-е задание

Продолжаем тему проверки кода и задания 26. Сначала разберём решение домашнего задания и тесты, которые вы сохранили, а затем решим ещё одно задание 26 и найдём ошибки в предложенном решении.

## Проверка ДЗ

Разбираем решение домашнего задания с [урока 53](../lesson53/lesson53.md) — «Бестселлер»:

[Условие задания](https://education.yandex.ru/ege/inf/task/ae105bf0-7e72-4cac-97e0-aba1e85ee5b9)

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

---

## Задача. Разбор капчи

Теперь по той же схеме: читаем код, ищем ошибки, проверяем на граничных случаях.

[Условие задания](https://education.yandex.ru/ege/inf/task/58670e09-0a33-4eb9-b7ce-532642d09e3f)

<details>
<summary>Решение с ошибкой</summary>

```python
with open('26_1.txt', 'r') as f:
    line = f.readline()
    n_workers = int(line.split()[0])
    requests = []
    while (line := f.readline()):
        requests.append(int(line))


workers_end_time = [0] * n_workers
all_done_requests = 0
last_done_requests = 0

for second in requests:
    for ind, end_time in enumerate(workers_end_time):
        if end_time < second:
            if ind == (n_workers - 1):
                last_done_requests += 1
            workers_end_time[ind] = second + 60
            all_done_requests += 1
            break

print(f'Всего заказов {all_done_requests}')
print(f'Минимальное заказов одним мастером {last_done_requests}')
```

</details>

**Вопрос:** где ошибки?

<details>
<summary>Разбор ошибки</summary>

1. Нет `requests.sort()` — заказы обрабатываются в том порядке, в котором стоят в файле, а не в хронологическом. Поздний заказ может занять мастера раньше раннего, и подсчёт пойдёт не так.
2. `end_time < second` вместо `end_time <= second` — это **граничный случай**: если мастер освобождается ровно в ту же секунду, когда поступил заказ, он успевает его взять. Строгое сравнение такие заказы теряет. На «обычных» тестах ошибка может не проявиться, а вот тест «один мастер, заказ пришёл ровно в секунду освобождения» её сразу показывает.
</details>

<details>
<summary>Правильное решение</summary>

```python
with open('26_1.txt', 'r') as f:
    line = f.readline()
    n_workers = int(line.split()[0])
    requests = []
    while (line := f.readline()):
        requests.append(int(line))

requests.sort()

workers_end_time = [0] * n_workers
all_done_requests = 0
last_done_requests = 0

for second in requests:
    for ind, end_time in enumerate(workers_end_time):
        if end_time <= second:
            if ind == (n_workers - 1):
                last_done_requests += 1
            workers_end_time[ind] = second + 60
            all_done_requests += 1
            break

print(f'Всего заказов {all_done_requests}')
print(f'Минимальное заказов одним мастером {last_done_requests}')
```

</details>
