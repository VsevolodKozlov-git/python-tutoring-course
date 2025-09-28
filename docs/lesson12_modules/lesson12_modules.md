# Урок 13. ООП и модули

## Используем ООП

```python
import random


class InputValidator:
    def is_choice_difficulty_valid(self, choice):
        raise NotImplementedError("This method must be implemented in subclass")

    def is_guessed_symbol_valid(self, symbol, guessed_letters):
        raise NotImplementedError("This method must be implemented in subclass")


class InputValidatorSingleLetter(InputValidator):
    def is_choice_difficulty_valid(self, choice):
        return choice in ['1', '2', '3']

    def is_guessed_symbol_valid(self, symbol, guessed_letters):
        if len(symbol) != 1:
            print("Нужно ввести одну букву")
            return False
        if not symbol.isalpha():
            print("Введите букву")
            return False
        if symbol in guessed_letters:
            print("Вы эту букву уже вводили")
            return False
        if symbol not in "йцукенгшщзхъфывапролджэячсмитьбю":
            print("Вы ввели английскую букву")
            return False
        return True


class RandomWord:
    def __init__(self, words):
        self.words = words
        self.word = self.generate_word()
        self.guessed_symbols = ['_'] * len(self.word)
        self.guessed_letters = []

    def generate_word(self):
        return random.choice(self.words).lower()

    def is_symbol_in_word(self, symbol):
        return symbol in self.word

    def fill_symbols_in_word(self, symbol):
        for i in range(len(self.word)):
            if self.word[i] == symbol:
                self.guessed_symbols[i] = symbol

    def get_word(self):
        return self.word

    def get_word_with_guessed_symbols(self):
        return self.guessed_symbols


class HangmanGame:
    def __init__(self, validator_class, word_generator_class, difficulty_options):
        self.validator = validator_class()
        self.word_generator_class = word_generator_class

        # Dictionary with difficulty options

        self.difficulty_options = difficulty_options
        self.tries = 0
        self.word_generator = None

    def run(self):
        self.choice_difficulty()
        print(f"""
        Игра началась! Слово состоит из {len(self.word_generator.word)} букв
        У тебя {self.tries} попыток""")

        while self.tries > 0:
            print(f"""
            Слово: {self.word_generator.get_word_with_guessed_symbols()}
            Осталось попыток: {self.tries}
            Использованные буквы: {self.word_generator.guessed_letters}""")

            if self.input_guessed_letter():
                if "_" not in self.word_generator.guessed_symbols:
                    print(f"Поздравляю! Ты угадал слово {self.word_generator.get_word().upper()}")
                    return

        print(f"Вы проиграли! Загаданное слово было {self.word_generator.get_word().upper()}")

    def choice_difficulty(self):
        print("""Выберите сложность игры!""")
        for key, value in self.difficulty_options.items():
            print(f"        {key} - {value['name']} ({value['tries']} попыток)")

        while True:
            choice = input("Ваш выбор сложности 1-3: ")
            if self.validator.is_choice_difficulty_valid(choice):
                break
            print("Неверный ввод. Пожалуйста, введите 1, 2 или 3")

        difficulty = self.difficulty_options[choice]
        self.word_generator = self.word_generator_class(difficulty['words'])
        self.tries = difficulty['tries']

    def input_guessed_letter(self):
        while True:
            letter = input("Введите букву: ").lower()
            if self.validator.is_guessed_symbol_valid(letter, self.word_generator.guessed_letters):
                break

        self.word_generator.guessed_letters.append(letter)

        if self.word_generator.is_symbol_in_word(letter):
            print("Есть такая буква!")
            self.word_generator.fill_symbols_in_word(letter)
        else:
            print("Такой буквы нет")
            self.tries -= 1
            return False
        return True


if __name__ == "__main__":
    difficulty_option = {
            '1': {
                'name': 'Лёгкий',
                'tries': 8,
                'words': [
                    "дом", "кот", "нос", "рот", "сын", "час", "год", "сон",
                    "сок", "суп", "зуб", "дуб", "лес", "рис", "мир"
                ]
            },
            '2': {
                'name': 'Средний',
                'tries': 7,
                'words': [
                    "танец", "рамка", "речка", "ночка", "ветка", "доска",
                    "полка", "сетка", "лента", "линия", "штора", "кнопка",
                    "метро", "озеро", "арбуз"
                ]
            },
            '3': {
                'name': 'Сложный',
                'tries': 6,
                'words': [
                    "абрикос", "багетка", "ведёрко", "гарнитур", "дельфин",
                    "ежевика", "животное", "забота", "известие", "капитан",
                    "лампада", "мастерок", "огурец", "портрет", "ракетка"
                ]
            }
        }
    game = HangmanGame(InputValidatorSingleLetter, RandomWord, difficulty_option)
    game.run()
```

## Повторение модулей


#### Импорт модулей

Пусть у нас есть модуль `sub`, в котором есть методы `print_sub`. В модуле `main` написан следующий код. Продолжите его:
```python
import sub

# Что надо написать, чтобы вызвать print_sub
```

```python
from sub import print_sub

# Что надо написать, чтобы вызвать print_sub
```

```python
import sub as new_name

# Что надо написать, чтобы вызвать print_sub
```

```python
from sub import print_sub as print_with_new_name

# Что надо написать, чтобы вызвать print_sub
```


#### Почему имена файлов для модулей в python не могут начинаться с цифры?


#### В каких ситуациях, может потребоваться использоание `as` во время импорта?

#### Что такое `пакет`(`package`)? Чем `package` отличается от модуля?

####  Импорт пакетов
Допустим у меня такая файловая структура
```
- main.py
- package
    - __init__.py
    - pack_mod.py
```

В `pack_mod.py` находится функция `print_hello`

Как мне её вызвать из `main.py`?


#### Зачем нужен файл `__init__.py` в package? Обязателен ли он?


##  Дополнительные материалы

### Как питон находит пакеты и модули?

```python
import sys

# Все пути поиска модулей
print("Пути поиска модулей:")
for path in sys.path:
    print(path)
```

### Зачем `if __name__ == "__main__":`?


## Домашнее задание

Прочитайте главу 12.1 - 12.4 включительно