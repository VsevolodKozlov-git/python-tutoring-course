
# Урок 20. Решаем 17 и 24 из ЕГЭ

## Материал урока

### Задание 17

#### Задание 17.1

[Ссылка](https://education.yandex.ru/ege/inf/task/fb7f9b9c-b9ea-4a95-8113-dc19be6bbf06)


Код:
```python
with open('17.txt', 'r') as f:
    nums = [int(line) for line in f.readlines()]

min_35_value = float('inf')

for num in nums:
    if num > 0 and num % 35 == 0 and num < min_35_value:
        min_35_value = num

cnt = 0
max_sum = -float('inf')
for i in range(len(nums) - 1):
    val1 = nums[i]
    val2 = nums[i+1]
    if val1 != val2 and abs(val1 - val2) % min_35_value == 0:
        cnt += 1
        cur_sum = val1 + val2
        if cur_sum > max_sum:
            max_sum = cur_sum

print(cnt)
print(max_sum)
```

#### Задание 17.2

[Ссылка](https://education.yandex.ru/ege/inf/task/03cda718-1367-46f9-a662-1e8f41746f71)

Как определить, что число пятизначное?

Как понять, что число оканчивается на 37?

Как найти квадрат максимального пятизначного элемента последовательности, оканчивающегося на 37?

#### Задание 17.3

[Ссылка](https://education.yandex.ru/ege/inf/task/532e532a-8eb5-40bc-804b-6e5cee270727)


#### Задание 17.4
(№ 4898) (Е. Джобс) В файле [17-271.txt](https://kpolyakov.spb.ru/cms/files/ege-seq/17-271.txt) содержится последовательность целых чисел. Элементы последовательности могут принимать целые значения от -10 000 до 10 000 включительно. Определите и запишите в ответе сначала количество пар элементов, сумма последних цифр которых равна 7, затем максимальную сумму элементов таких из найденных пар, в которых оба значения меньше среднего арифметического всех элементов обрабатываемой последовательности. В данной задаче под парой подразумевается два идущих подряд элемента последовательности.
Например, рассмотрим последовательность из шести элементов: 12; 18; 2; -15; 11; 16. Подходит две пары: (2; -15), (11; 16). Среднее арифметическое всех элементов последовательности равно 9. Следовательно искомая сумма равна 2 + (–15) = –13. Ответ: 2 –13.


#### Задание 17.5

[Ссылка](https://education.yandex.ru/ege/inf/task/ad327404-5a19-4231-a238-c95270a529c3)

код:
```python
with open('17 (2).txt', 'r') as f:
    nums = [int(line) for line in f.readlines()]

mean = sum(nums) / len(nums)

max_sum = -float('inf')
above_mean = 0

for i in range(1, len(nums) - 2):
    outer_1 = nums[i-1]
    inner_1 = nums[i]
    inner_2 = nums[i+1]
    outer_2 = nums[i+2]

    if inner_1 * inner_2 > outer_1 * outer_2:
        cur_sum = inner_1 + inner_2
        max_sum = max(max_sum, cur_sum)
        if inner_1 > mean or inner_2 > mean:
            above_mean += 1

print(f'{max_sum} {above_mean}')
```

#### Задание 17.6

[Ссылка](https://education.yandex.ru/ege/inf/task/568e6793-fe55-44eb-8e94-17787b5a6853)

### Задание 24

#### Задание 24.1

[Ссылка](https://education.yandex.ru/ege/inf/task/0a0f7d8d-f00c-4f0d-bcf2-b54fbbc4ea5c)

Код:
```python
with open('24.txt') as f:
    max_seq = 0
    letter = None
    start_index = None
    cur_index = 0
    while char := f.read(1):
        stop_flag = False
        if start_index is None and char.isnumeric():
            char = int(char)
            if char % 2 == 0:
                start_index = cur_index
        elif start_index is not None:
            if char.isnumeric():
                stop_flag = True
                char = int(char)
                if char % 2 == 0:
                    cur_seq = cur_index - start_index + 1
                    max_seq = max(cur_seq, max_seq)
            else:
                if letter is None:
                    letter = char
                elif letter != char:
                    stop_flag = True

        if stop_flag:
            start_index = None
            letter = None

        cur_index += 1

print(max_seq)
```


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

17.1. Легко

[ссылка](https://education.yandex.ru/ege/inf/task/7a1920ba-8e25-4c9b-ad1f-4f12d81514ab)

17.2. Легко

[ссылка](https://education.yandex.ru/ege/inf/task/6a2e2ee9-21a1-40b9-a6d1-f57446214527)

17.3. Среднее

[ссылка](https://education.yandex.ru/ege/inf/task/de7994f7-d8fe-4848-a91b-b9e7f7490d67)

24.1. Сложнее среднего

[ссылка](https://education.yandex.ru/ege/inf/task/97e2f438-d6ce-4c55-95f5-8384f58faea4)

24.2. Сложнее среднего

[ссылка](https://education.yandex.ru/ege/inf/task/105730a4-97f7-485b-a86a-76c11682aa85)

24.3. Сложное

[ссылка](https://education.yandex.ru/ege/inf/task/a23593f7-9ba4-422d-89f0-587d3bbacbb6)