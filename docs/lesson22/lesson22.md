
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



```python
with open('24(3).txt', 'r') as f:
    text = f.read()
    
index = 0
y_pos = []
cnt_2025_global = 0
while index < len(text):
    if text[index] == 'Y':
        y_pos.append([index, cnt_2025_global])
        index += 1
    elif text[index:index+4] == '2025':
        cnt_2025_global += 1
        index += 4
    else:
        index += 1

max_length = 0 
for index_end in range(80, len(y_pos)+1):
    index_start = index_end - 81
    
    if index_start <  0:
        y_index_start = 0
        cnt_2025_start = 0
    else:
        y_index_start, cnt_2025_start = y_pos[index_start]
        y_index_start += 1
    
    if index_end == len(y_pos):
        y_index_end = len(text) - 1
        cnt_2025_end = cnt_2025_global
    else:
        y_index_end, cnt_2025_end = y_pos[index_end]
        y_index_end -= 1

    cnt_2025_between = cnt_2025_end - cnt_2025_start
    if cnt_2025_between >= 90:
        cur_length = y_index_end - y_index_start + 1
        max_length = max(max_length, cur_length)

print(max_length)
````
## Домашнее задание

24.1 Сложное

[ссылка](https://education.yandex.ru/ege/inf/task/a23593f7-9ba4-422d-89f0-587d3bbacbb6)