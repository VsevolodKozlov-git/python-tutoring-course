# Урок 7. Как решать задачи?

## Повторение материаала

### Циклы

#### Что такое вложенный цикл?
Что выведет код ниже? Сколько раз выполнится 3-я строка?
```python
for outer in range(10):
	for inner in range(10):
		print(f'внешний цикл: {outer}, внутренний: {inner}')
```
#### Для чего вам может понадобиться вложенный цикл?

#### Зачем else циклу?
Что выведет этот код
```python
word = 'helloWorld1111'
for letter in word:
	if not letter.isalpha():
		print('I am in break')
		break
else:
	print('I am in else')
```


## Код задач с прошлого урока

### Сложность пароля
```python
def is_any_digit(password: str):
    for char in password:
        if char.isdigit():
            return True
    return False

def is_any_lower_case(password: str):
    for char in password:
        if char.isalpha() and char.islower():
            return True
    return False

def is_any_upper_case(password: str):
    for char in password:
        if char.isalpha() and char.isupper():
            return True
    return False

def is_strong_password(password: str):
    return (len(password) >= 8
            and is_any_digit(password)
            and is_any_lower_case(password)
            and is_any_upper_case(password))
```

```python
def is_strong_password(password):
    if len(password) < 8:
        return False

    for char in password:
        if char.isdigit():
            break
    else:
        return False

    for char in password:
        if char.islower():
            break
    else:
        return False

    for char in password:
        if char.isupper():
            break
    else:
        return False

    return True
```

### Палиндромы

```python
def is_palindrom(word):
    start = 0
    end = len(word) - 1
    while start < end:
        if word[start] != word[end]:
            return False
        start += 1
        end -= 1
    return True
```


### Поиск подстрок в строке

```python
def find_custom(string, substring):
    for start in range(len(string) - len(substring) + 1):
        end = start+len(substring)
        if substring == string[start:end]:
            return start
    return -1
```

## Как решать задачи?

- Понять на примерах, что требуется в задаче
- Обобщить задачу
- Придумать решение словами
- Продумать граничные случаи
- Написать код
- Протестировать код


**Задача:**

Вася решил написать программу, чтобы решать примеры по математике. Эта программа должна получать на вход строку, которая содержит:

- пробелы
- символы + и -
- целые числа

Программа должна выводить результат арифметического выржания

**Код**

```python
def perform_math(number1, number2, operator):
    if operator == '-':
        return  number1 - number2
    elif operator == '+':
        return  number1 + number2
    else:
        return ValueError('Оператор должен быть + или -')

def compute_str(str_input):
    accumulated = 0
    current_symbol = '+'
    current_number = 0
    str_input = str_input.replace(' ', '')
    for char in str_input:
        if char.isdigit():
            current_number = current_number * 10 + int(char)
        else:
            accumulated = perform_math(accumulated, current_number, current_symbol)
            current_symbol = char
            current_number = 0
    accumulated = perform_math(accumulated, current_number, current_symbol)

    return accumulated
```

## Домашнее задание

Прочитайте главы 8.6 - 9.5