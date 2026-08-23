# Урок: Pydantic — валидация и конвертация данных

В этом уроке мы подробно рассмотрим библиотеку Pydantic: научимся создавать модели данных, выполнять автоматическую валидацию и конвертацию, а также использовать продвинутые валидаторы для собственных проверок.

## Что такое Pydantic

Pydantic решает две ключевые задачи:

1. **Валидация** — проверка данных на соответствие ожидаемой структуре и типам.
2. **Конвертация** — преобразование данных между различными форматами (словарь, модель, JSON).

Библиотека часто используется совместно с FastAPI, но может применяться и в любом другом Python-проекте. FastAPI активно использует Pydantic для обработки входящих и исходящих данных в endpoint’ах, однако Pydantic самодостаточен и позволяет предотвращать ошибки на раннем этапе.

## Создание модели и базовая валидация

Модель Pydantic описывается как класс-наследник `BaseModel`. Каждое поле модели объявляется с аннотацией типа. Pydantic автоматически проверяет типы и при необходимости преобразует входные данные.

Пример базовой модели:

```python
from pydantic import BaseModel

class MovieData(BaseModel):
    title: str
    views: int
```

Теперь можно создать экземпляр модели, передав значения полей как именованные аргументы. Pydantic проверит, что `title` — строка, а `views` — целое число. Если переданные данные не соответствуют ожиданиям, будет выброшено исключение `ValidationError`.

```python
movie = MovieData(title="Титаник", views=100)
print(movie)
# title='Титаник' views=100
```

## Конвертация: словарь ↔ модель

Одно из главных преимуществ Pydantic — возможность легко преобразовывать словари в модели и обратно. FastAPI использует это под капотом: входящий JSON (словарь) превращается в модель Pydantic, валидируется, а исходящая модель сериализуется обратно в JSON.

Пример конвертации:

```python
from pydantic import BaseModel

class MovieData(BaseModel):
    title: str
    views: int

def conversion_demo():
    d = {"title": "Титаник", "views": 100}
    model = MovieData.model_validate(d)   # словарь -> модель
    print(model)
    # title='Титаник' views=100

    d_from_model = model.model_dump()     # модель -> словарь
    print(d_from_model)
    # {'title': 'Титаник', 'views': 100}
```

## Работа с моделями в функциях

Функция может принимать модель Pydantic как тип аргумента. Это гарантирует, что на вход поступят уже провалидированные данные, а IDE будет предоставлять автодополнение для полей модели.

```python
from typing import List
from pydantic import BaseModel

class MovieData(BaseModel):
    title: str
    views: int

def get_sum_of_views(data_list: list[MovieData]) -> int:
    result = 0
    for movie in data_list:
        result += movie.views   # IDE подскажет, что у movie есть поле views
    return result

movies = [
    MovieData(title="Титаник", views=100),
    MovieData(title="Бойцовский клуб", views=10),
]
print(get_sum_of_views(movies))  # 110
```

## Автоматическое преобразование типов

Pydantic по умолчанию пытается привести входные данные к объявленному типу. Например, если поле объявлено как `int`, а на вход приходит строка `"100"`, она будет преобразована в число. Если преобразование невозможно (например, строка `"abc"`), возникает ошибка валидации.

Успешное преобразование:

```python
data = {"title": "Титаник", "views": "100"}  # views передано строкой
movie = MovieData.model_validate(data)
print(movie.views, type(movie.views))  # 100 <class 'int'>
```

Ошибка при невозможном преобразовании:

```python
data = {"title": "Титаник", "views": "abc"}
try:
    MovieData.model_validate(data)
except Exception as e:
    print(e)
    # validation error for MovieData
    # views
    #   Input should be a valid integer, unable to parse string as an integer
```

## Расширенная валидация: BeforeValidator и AfterValidator

Для более тонкой настройки проверок используются `BeforeValidator` и `AfterValidator`. Они позволяют выполнить пользовательскую функцию до или после основной валидации Pydantic.

- **BeforeValidator** — вызывается до стандартной валидации. Удобен для предварительной обработки данных (например, убрать символ `$`).
- **AfterValidator** — вызывается после успешной стандартной валидации. Подходит для проверки ограничений (например, число должно быть неотрицательным).

Важное правило: функции, передаваемые в валидаторы, должны возвращать **значение** (исходное или преобразованное), а не булево значение. Возврат `True`/`False` является ошибкой, потому что валидаторы также отвечают за преобразование данных.

### Пример правильных валидаторов

```python
from typing import Annotated
from pydantic import BaseModel, BeforeValidator, AfterValidator

def non_negative(number: int) -> int:
    """Проверяет, что число неотрицательное, иначе вызывает ошибку."""
    if number < 0:
        raise ValueError("Должно быть >= 0")
    return number  # возвращаем само значение

def convert_from_dollars(money_str: str) -> int:
    """Убирает знак доллара из строки и преобразует в int."""
    if money_str.endswith("$"):
        money_str = money_str[:-1]
    return int(money_str)

class MovieData(BaseModel):
    title: str
    views: Annotated[int, AfterValidator(non_negative)]          # после валидации
    gross: Annotated[int, BeforeValidator(convert_from_dollars)] # до валидации
```

Теперь модель автоматически применит собственные проверки:

```python
# Успешный случай
movie = MovieData.model_validate({
    "title": "Титаник",
    "views": 100,
    "gross": "10$"
})
print(movie)
# title='Титаник' views=100 gross=10

# Ошибка: views отрицательное
try:
    MovieData.model_validate({"title": "Плохой фильм", "views": -5, "gross": "1$"})
except Exception as e:
    print(e)
    # validation error for MovieData
    # views
    #   Value error, Должно быть >= 0
```

### Неправильный валидатор (антипример)

```python
def bad_validator(value):
    return value >= 0  # возвращает True/False, а не значение

# Такой валидатор приведёт к ошибке, потому что после валидации Pydantic
# попытается использовать возвращённое булево значение как int.
```

## Практический пример: обработка денежных значений

Часто данные приходят в неудобном формате. Например, сумма может быть строкой с символом валюты. С помощью `BeforeValidator` можно выполнить предварительное преобразование, чтобы Pydantic затем работал уже с корректным типом.

В модели выше поле `gross` описано как `Annotated[int, BeforeValidator(convert_from_dollars)]`. Это означает, что до стандартной валидации будет вызвана функция `convert_from_dollars`, которая из строки `"10$"` сделает `int(10)`. Затем Pydantic проверит, что полученное значение действительно целое число, и присвоит его полю.

```python
def conversion_demo():
    d = {"title": "Титаник", "views": 100, "gross": "10$"}
    model = MovieData.model_validate(d)
    print(model.gross, type(model.gross))  # 10 <class 'int'>
```

## Итоги

- Pydantic — библиотека для валидации и конвертации данных, широко используемая с FastAPI и самостоятельно.
- Модель создаётся как класс `BaseModel` с аннотациями типов.
- Pydantic автоматически проверяет и преобразует типы (например, строку `"100"` в `int`).
- Словари преобразуются в модели через `model_validate()`, модели в словари — через `model_dump()`.
- Для собственных проверок используются `BeforeValidator` и `AfterValidator`.
- Функции-валидаторы должны возвращать значение (возможно изменённое), а не `True`/`False`.
- Ошибки валидации выбрасываются в виде `ValidationError` и содержат подробное описание.