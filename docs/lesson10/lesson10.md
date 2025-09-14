# Урок 10. Коты и O-большое

## O-большое

`O(x + 10) = O(x)`

`O(x^2 + x) = O(x^2)`

`O(x! + x^10) = O(x!)`

`O(x^10 + x!) = O(x!)`

`O(10*x^2 ) = O(x^2)`


## Упражнение из ДЗ

```python
def get_cats():
    cats = [True] * 100
    for step in range(2, 100+1):
        for ind in range(step-1, 100, step):
            cats[ind] = not cats[ind]
    return cats


if __name__ == '__main__':
    for i, cat in enumerate(get_cats()):
        print(i+1, cat)
```

```python
def get_number_primes_count(numbers_end):
    """
     Возвращает словарь с разложением каждого числа до numbers_end на простые множители.

     Для каждого числа от 1 до numbers_end (включительно) функция возвращает словарь,
     где ключи - простые числа, а значения - их степени в разложении.

     Args:
         numbers_end (int): Конечное число в диапазоне (включительно).

     Returns:
         dict: Словарь, где ключи - числа от 1 до numbers_end,
               а значения - словари с разложением на простые множители.

     Пример:
         >>> get_number_primes_count(6)
         {
             1: {1: 0},
             2: {2: 1},
             3: {3: 1},
             4: {2: 2},
             5: {5: 1},
             6: {2: 1, 3: 1}
         }
     """
    number_primes_count = {}
    primes = []
    for number in range(1, numbers_end+1):
        if number == 1:
            number_primes_count[1] = {1: 0}
            continue

        for prime in primes:
            if number % prime == 0:
                primes_count = number_primes_count[number // prime].copy()
                if prime not in primes_count:
                    primes_count[prime] = 0
                primes_count[prime] += 1
                number_primes_count[number] = primes_count
                break
        else:
            primes.append(number)
            number_primes_count[number] = {number : 1}
    
    return number_primes_count
        

def get_dividers(primes_count):
    """
    Вычисляет количество делителей числа по его разложению на простые множители.

    Args:
        primes_count (dict): Словарь с разложением числа на простые множители,
                            где ключи - простые числа, значения - их степени.

    Returns:
        int: Количество делителей числа.

    Пример:
        >>> get_dividers({2: 2, 3: 1})  # для числа 12 = 2² × 3¹
        6  # делители: 1, 2, 3, 4, 6, 12
    """
    dividers = 1
    for n_primes in primes_count.values():
        dividers *= n_primes+1
    return dividers


def get_number_dividers_dict(number_primes_count):
    """
    Создает словарь с количеством делителей для каждого числа.

    Args:
        number_primes_count (dict): Словарь с разложением чисел на простые множители,
                                   полученный из get_number_primes_count.

    Returns:
        dict: Словарь, где ключи - числа, а значения - количество их делителей.

    Пример:
        >>> number_primes = get_number_primes_count(6)
        >>> get_number_dividers_dict(number_primes)
        {
            1: 1,
            2: 2,
            3: 2,
            4: 3,
            5: 2,
            6: 4
        }
    """
    return {number: get_dividers(primes_count) for number, primes_count in number_primes_count.items()}

def get_cats_in_hats():
    number_primes_count = get_number_primes_count(100)
    number_dividers_dict = get_number_dividers_dict(number_primes_count)

    cats_in_hats = {}
    for cat_index in range(1, 101):
        cat_passes = number_dividers_dict[cat_index]
        is_hat = cat_passes % 2 == 1
        cats_in_hats[cat_index] = is_hat

    return cats_in_hats


if __name__ == '__main__':
    cats_in_hats = get_cats_in_hats()
    print(cats_in_hats)



```

## Повторение

Что такое худший сценарий работы алгоритма?

Что такое O-большое? Что оно измеряется?

Чему равно О-большое этого алгоритма?
```python
def multiplication_matrix(n):
    return [[(i + 1) * (j + 1) for j in range(n)] for i in range(n)]

n = 5
matrix = multiplication_matrix(n)
```

```python
def get_first_element(arr):
    return arr[0] if arr else None
```

```python
def sum_array(arr):
    total = 0
    for num in arr:
        total += num
    return total
```

```python
def bubble_sort(arr):
    """
    Сортировка пузырьком (Bubble Sort)
    
    Параметры:
    arr (list): Неотсортированный список чисел
    
    Возвращает:
    list: Отсортированный список по возрастанию
    """
    n = len(arr)
    
    # Проходим по массиву n-1 раз
    for i in range(n - 1):
        # Флаг для оптимизации (если массив уже отсортирован)
        swapped = False
        
        # Сравниваем соседние элементы
        for j in range(n - 1 - i):  # Уменьшаем диапазон, т.к. последние i элементов уже на месте
            if arr[j] > arr[j + 1]:
                # Меняем элементы местами
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # Если за проход не было перестановок, массив отсортирован
        if not swapped:
            break
    
    return arr


# Пример использования
unsorted_list = [64, 34, 25, 12, 22, 11, 90]
sorted_list = bubble_sort(unsorted_list.copy())  # Чтобы не изменять исходный список

print("Неотсортированный массив:", unsorted_list)
print("Отсортированный массив:   ", sorted_list)
```

# Домашнее задание

- Реализовать Bogosort
- Выбрать и реализовать проект из списка 