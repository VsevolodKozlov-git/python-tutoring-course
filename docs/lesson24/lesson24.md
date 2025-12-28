
# Урок 24. Мы дошли до решения 24-го из ЕГЭ

## Материал урока

### 24

#### Задание 24.2


[Ссылка](https://education.yandex.ru/ege/inf/task/f831021e-44d1-4765-bf94-0e713ed047f1)


```python
with open('24(4).txt') as file:
    input_str = file.read()
    

y_2025 = []
cnt_2025 = 0
ind = 0

while ind < len(input_str):
    if input_str[ind:ind+4] == '2025':
        cnt_2025 += 1
        ind += 3
    elif input_str[ind] == 'Y':
        y_2025.append([ind, cnt_2025])
    
    ind += 1

max_length = 0

step = 80
for index_end in range(step, len(y_2025)+1):
    index_start = index_end - (step + 1)
    if index_start == -1:
        y_start = 0
        start_2025 = 0
    else:
        y_start = y_2025[index_start][0] + 1
        start_2025 = y_2025[index_start][1]

    if index_end == len(y_2025):
        y_end = len(input_str) - 1
        end_2025 = cnt_2025
    else:
        y_end = y_2025[index_end][0] - 1
        end_2025 = y_2025[index_end][1]
    
    between_2025 = end_2025 - start_2025
    
    if between_2025 >= 90:
        cur_length = y_end - y_start + 1
        max_length = max(cur_length, max_length)
```

## Домашнее задание

24.1 Сложное

[ссылка](https://education.yandex.ru/ege/inf/task/a23593f7-9ba4-422d-89f0-587d3bbacbb6)