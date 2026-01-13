
# Урок 25. Другой тип 24-го из ЕГЭ

## Материал урока

### В чем пишут код на ЕГЭ

![alt text]({EB7A460D-3EF5-4A2B-8D13-3639956B1D34}.png)

### Решение номера из ДЗ

[ссылка](https://education.yandex.ru/ege/inf/task/a23593f7-9ba4-422d-89f0-587d3bbacbb6)


Способ с списком индексов:
```python
"""
K9 не больше 150 раз. Не оканчивается символом D.

- Написать функцию. Начало и Конец. Ищет отсутствие символа D.
- Найти места с K9.
"""

def main(s, step): 
    def find_not_d(start, end):
        for ind in range(end, start-1, -1):
            if s[ind] != 'D':
                return ind
        raise ValueError('Не найдена строка без D')

    def get_symbols(start, end):
        return end - start + 1

    k9_indexes = []
    i = 0
    while i < len(s):
        if s[i: i+2] == 'K9':
            k9_indexes.append(i)
            i += 1
        i += 1

    if len(k9_indexes) < step:
        end = find_not_d(0, len(s)-1)
        return get_symbols(0, end)

    max_length = 0
    for index_end in range(step, len(k9_indexes)+1):
        index_start = index_end - (step + 1)
        if index_start == -1:
            start = 0
        else:
            start = k9_indexes[index_start] + 1

        if index_end == len(k9_indexes):
            end = len(s) - 1
        else:
            end = k9_indexes[index_end]

        end_not_d = find_not_d(start, end)
        cur_length = get_symbols(start, end_not_d)
        max_length = max(cur_length, max_length)

    return max_length

with open('24 (5).txt') as f:
    s = f.read()
    
print(main(s, 150))

# tests = [
#     ('K9K9K9', 2, 5),
#     ('K9K9D', 2, 4),
#     ('K9K9DF', 2, 6),
#     ('K9D', 2, 2),
#     ('K9D2', 2, 4),
#     ('K9K9FK9DK9', 2, 8),
# ]

# for s, step, expected in tests:
#     actual = main(s, step)
#     if expected != actual:
#         print(f"""
# s = {s}
# step = {step}
# expected = {expected}
# actual = {actual}
# """)
```

Способ с префиксной суммой:
```python
with open('24(4).txt', 'r') as f:
    s = f.read().strip()

n = len(s)



pref = [0] * (n + 1)
for i in range(1, n + 1):
    pref[i] = pref[i - 1]
    if i >= 2 and s[i - 2] == 'K' and s[i - 1] == '9':
        pref[i] += 1



def count_K9(l, r):
    if r - 1 < l:
        return 0
    return pref[r - 1] - pref[l]


max_len = 0

right = 0
for left in range(n):
    # right = left
    while right <= n:
        cnt = count_K9(left, right)
        if cnt > 150:
            break
        right += 1
    candidate_end = right - 1
    while candidate_end > left and s[candidate_end - 1] == 'D':
        candidate_end -= 1
    if candidate_end > left:
        max_len = max(max_len, candidate_end - left)

print(max_len)
```

### 24.3
[Ссылка](https://education.yandex.ru/ege/inf/task/79093caa-18f3-4e6f-80d5-7e4135f2741a)


```python
"""
Начинается с A, заканчивается Z(единственная)
Содержит ровно 50 латинских букв
Сумма цифр кратна 7

[{ index, sum_pref,  vowels_pref, as_data: [{index, sum_pref, vowels_pref}] }]
"""


def main(s, vowels_condition):
    vowels = {'A', 'E', 'I', 'O', 'U'}
    
    sum_pref = 0
    vowels_pref = 0
    zs_data = []
    current_as = []
    
    for i, ch in enumerate(s):
        if ch in vowels:
            vowels_pref += 1
        if ch.isdigit():
            sum_pref += int(ch)
            
        if ch == 'A':
            a_data = {
                'index': i,
                'sum_pref': sum_pref,
                'vowels_pref': vowels_pref
            }
            current_as.append(a_data)
        
        elif ch == 'Z':
            z_data = {
                'index': i,
                'sum_pref': sum_pref,
                'vowels_pref': vowels_pref,
                'as_data': current_as
            }
            zs_data.append(z_data)
            current_as = []
    
    max_len = 0

    # Ищем максимальную последовательность
    for z in zs_data:
        z_index = z['index']
        z_sum = z['sum_pref']
        z_vowels = z['vowels_pref']
        
        for a in z['as_data']:
            a_index = a['index']
            a_sum = a['sum_pref']
            a_vowels = a['vowels_pref']
            
            vowels_diff = z_vowels - a_vowels + 1
            sum_diff = z_sum - a_sum
            
            if vowels_diff == vowels_condition and sum_diff % 7 == 0:
                length = z_index - a_index + 1
                if length > max_len: 
                    max_len = length
    
    return max_len


def test():
    tests = [
        ("A" + "E"*49 + "Z", 50, 51),
        ("A" + "E"*25 + "3" + "E"*24 + "Z", 50, 0),
        ("A" + "E"*25 + "7" + "E"*24 + "Z", 50, 52),
        ("A123Z", 1, 0),  # 0 гласных, сумма 1+2+3=6 не кратна 7
        ("A7Z", 1, 3),  # 0 гласных, сумма 7 кратна 7
        ("A" + "B"*10 + "Z", 1, 12),  # нет гласных вообще
        ("AXZ", 1, 3),  # 1 гласная, но не та
        ("AEXIZ", 3, 5),  # 3 гласные (A, E, I) и нет цифр
    ]
    
    for s, vowels_condition, expected in tests:
        actual = main(s, vowels_condition)
        if expected != actual:
            print(f"""
s = {s}
vowels_condition = {vowels_condition}
expected = {expected}
actual = {actual}
""")
    
if __name__ == "__main__":

    with open('24 (6).txt') as f:
        s = f.read()
    
    vowels_condition = 50
    result = main(s, vowels_condition)
    
    print(f"Максимальная длина последовательности: {result}")
    
    # test()
```


## Домашнее задание

[Ссылка](https://education.yandex.ru/ege/inf/task/a24ce8b0-6d3c-4963-af6e-dfbc118b2d1c)