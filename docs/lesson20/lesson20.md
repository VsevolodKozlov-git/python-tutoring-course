
# Урок 20. Решаем 17 из ЕГЭ

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


Код:
```python
"""
Найти:
- макс 
- 5-знаков
- оканчивается на 37

Фильтр пар:
- только один 5 знаков
- (i + j) ** 2 > max_37 ** 2
"""

with open('17 (5).txt', mode='r') as f:
    nums = [int(line) for line in f.readlines()]

def is_5(num):
    num = abs(num)
    cnt = 0
    while num != 0:
        num //= 10
        cnt += 1
    return cnt == 5

def is_end_37(num):
    return num % 100 == 37

max_37 = -float('inf')

for i in nums:
    if is_5(i) and is_end_37(i):
        max_37 = max(i, max_37)

cnt = 0
max_sum = -float('inf')
for i in range(len(nums) - 1):
    num1 = nums[i]
    num2 = nums[i+1]

    if is_5(num1) != is_5(num2) and (num1 + num2) ** 2 > max_37 ** 2:
        cnt += 1
        max_sum = max(num1 + num2, max_sum)

print(f'{cnt} {max_sum}')
```

## Домашнее задание

Если выполнить не получится - не страшно, главное попробуйте. На уроке поделитесь своими наработками, вместе мы их добьем до решения.


17.1. Легко

[ссылка](https://education.yandex.ru/ege/inf/task/7a1920ba-8e25-4c9b-ad1f-4f12d81514ab)

17.2. Легко

[ссылка](https://education.yandex.ru/ege/inf/task/6a2e2ee9-21a1-40b9-a6d1-f57446214527)

17.3. Среднее

[ссылка](https://education.yandex.ru/ege/inf/task/de7994f7-d8fe-4848-a91b-b9e7f7490d67)