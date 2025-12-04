
# Урок 22. Продолжаем решать 24-е

## Материал урока

### 24

#### Задание 24.2


[Ссылка](https://education.yandex.ru/ege/inf/task/f831021e-44d1-4765-bf94-0e713ed047f1)

Код:
```python


with open('24 (2).txt') as f:
    y_cnt_2025 = []
    cnt_2025 = 0
    index_2025 = 0
    word_2025 = '2025'
    index = 0
    while char := f.read(1):
        if word_2025[index_2025] == char:
            index_2025 += 1
        else:
            index_2025 = 0

        if index_2025 == 4:
            index_2025 = 0
            cnt_2025 += 1

        if char == 'Y':
            y_cnt_2025.append((index, cnt_2025))
            index_2025 = 0

        index += 1

max_seq = 0
start_index = 0
start_cnt_2025 = 0

for i in range(80, len(y_cnt_2025)):
    end_index, end_cnt_2025 = y_cnt_2025[i]
    if end_cnt_2025 - start_cnt_2025 >= 90:
        cur_seq = end_index - start_index
        max_seq = max(max_seq, cur_seq)

    start_index, start_cnt_2025 = y_cnt_2025[i-80]
    start_index += 1

print(max_seq)
```

## Домашнее задание

24.1 Сложное

[ссылка](https://education.yandex.ru/ege/inf/task/a23593f7-9ba4-422d-89f0-587d3bbacbb6)