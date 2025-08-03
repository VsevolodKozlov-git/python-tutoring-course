## Код заданий из ДЗ

#### 8.8
```python
from random import random


def get_attempts_to_both():
    is_head = False
    is_tail = False
    n_attempts = 0

    while not (is_head and is_tail):
        n_attempts += 1
        if random() > 0.5:
            is_head = True
        else:
            is_tail = True

    return n_attempts


def get_mean_attempts(n_experiments):
    n_attempts = 0
    for i in range(n_experiments):
        n_attempts += get_attempts_to_both()
    return n_attempts / n_experiments


if __name__ == '__main__':
    print(get_mean_attempts(int(1e5)))
```

#### 8.9
```python
from math import ceil  
from random import random  
  
def is_candidate_wins(probabilities):  
    wins = 0  
    for win_prob in probabilities:  
        if random() <= win_prob:  
            wins += 1  
  
    need_to_win = ceil(len(probabilities) / 2)  
    return wins >= need_to_win  
  
  
def get_win_probability(n_experiments, probabilities):  
    n_wins = 0  
    for _ in range(n_experiments):  
        n_wins += int(is_candidate_wins(probabilities))  
    return n_wins / n_experiments  
  
if __name__ == '__main__':  
    print(get_win_probability(10000, [0.87,0.65,0.17]))
```



## Вопросы для повторения
#### Зачем нужно обрабатывать исключения?

Ниже пример, когда обрабатывать исключения необходимо, ведь мы должны объяснить пользователю, что он не прав
```python
while True:  
    try:  
        inp_value = int(input())  
        break  
    except ValueError:  
        print('Введите число, а не строку')
```

#### Какие исключения вы знаете?

#### Зачем вызывать исключения самому?

#### Придумайте 3 способа создать список из чисел от 0 до 9?
```python
print([i for i in range(10)])  
  
a = []  
for i in range(10):  
    a.append(i)  
print(a)  
  
print(list(range(10)))
```

#### Что общего между списком, строкой и кортежем?

#### В чем разница между списком и кортежем?

#### Зачем нужны пустая строка, пустой список и пустой кортеж?

#### Что значит, что объект итерируемый?

#### Как проверить, что значение есть в последовательности? Зачем это может понадобиться?

#### Как вернуть несколько значений из функции?

#### Как изменить элементы списка?

#### Как добавить значение в список?

#### Как удалить значение из списка?

## Домашнееизадание

[Видео про псевдослучайные числа](https://youtu.be/mVF8NDM-reg?si=IHo38FPcqD6OCQWO)

[Статья про генераторы списков](https://pyhub.ru/python/lecture-8-24-50/?ysclid=mdvklduyzu520919413)

Главы 9.4-9.10 из книги

