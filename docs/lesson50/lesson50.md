# Урок 50. Аутентификация в FastAPI

В этом уроке мы применим знания о JWT и хешировании паролей на практике — реализуем аутентификацию в FastAPI. Вы узнаете про `Annotated`-типы, инъекцию зависимостей через `Depends` и `HTTPBearer`, а в домашнем задании самостоятельно построите цепочку аутентификации от регистрации до защищённого профиля.

---

## Часть 0. Повторение

Перед стартом убедитесь, что вы помните ключевые концепции из [урока 49](../lesson49/lesson49.md).

**Для чего используются JWT-токены?**

<details>
<summary>Ответ</summary>

JWT-токены используются для передачи данных между клиентом и сервером в безопасном виде. Сервер создаёт токен, кладёт в него данные (например, имя пользователя) и подписывает секретным ключом. Клиент отправляет токен с каждым запросом, чтобы сервер знал, кто делает запрос.
</details>

**Шифруются ли данные в JWT?**

<details>
<summary>Ответ</summary>

Нет. Данные в JWT не зашифрованы — их может прочитать любой, у кого есть токен. JWT гарантирует не конфиденциальность, а целостность: подпись гарантирует, что данные не были изменены без секретного ключа.
</details>

**Почему JWT-токен нельзя подделать без секретного ключа?**

<details>
<summary>Ответ</summary>

Потому что подпись вычисляется с помощью секретного ключа. Если изменить данные в токене, подпись перестанет совпадать. Чтобы пересчитать подпись для новых данных, нужен секретный ключ, который есть только у сервера.
</details>

**Какие базовые поля есть в JWT?**

<details>
<summary>Ответ</summary>

- `sub` (subject) — идентификатор пользователя (мы кладём туда `username`)
- `iat` (issued at) — когда токен выдан
- `exp` (expiration) — когда токен истекает
</details>

**Чем хеширование отличается от шифрования?**

<details>
<summary>Ответ</summary>

Хеширование — одностороннее: из хеша нельзя восстановить исходные данные. Шифрование — двустороннее: зашифрованные данные можно расшифровать с помощью ключа. Пароли хешируют, а не шифруют, потому что серверу не нужно знать пароль — ему нужно только уметь его проверить.
</details>

**Зачем хешировать пароли?**

<details>
<summary>Ответ</summary>

Если хранить пароли в открытом виде, утечка базы данных скомпрометирует все пароли. Хеш невозможно обратить, поэтому при утечке базы злоумышленник получит набор хешей, из которых нельзя восстановить пароли.
</details>

**Что такое «соль» в алгоритме хеширования? Зачем она нужна?**

<details>
<summary>Ответ</summary>

Соль — случайная строка, которая добавляется к паролю перед хешированием. Благодаря соли одинаковые пароли дают разные хеши. Это защищает от атак по радужным таблицам — заранее вычисленным хешам популярных паролей.
</details>

---

## Часть 1. Новый материал

### 1.1 Annotated-типы

#### Что такое Annotated

`Annotated` — это способ приложить к типу дополнительные данные (метаданные). Тип остаётся тем же, но к нему «приклеивается» дополнительная информация.

Пример:

```python
from typing import Annotated

age: Annotated[int, "возраст пользователя в годах"] = 25
print(age)
# 25
print(type(age))
# <class 'int'>
```

`age` ведёт себя как обычный `int`. Строка `"возраст пользователя в годах"` — это метаданные. В рамках самого Python `Annotated` **не значит ничего** — Python просто игнорирует метаданные. Но сторонние библиотеки могут их читать и использовать.

#### Где это уже встречалось

В [уроке 47](../lesson47/lesson47.md) мы использовали `Annotated` с Pydantic-валидаторами:

```python
from typing import Annotated
from pydantic import BaseModel, AfterValidator

def non_negative(number: int) -> int:
    if number < 0:
        raise ValueError("Должно быть >= 0")
    return number

class MovieData(BaseModel):
    views: Annotated[int, AfterValidator(non_negative)]
```

Pydantic читает метаданные (`AfterValidator(non_negative)`) и применяет валидатор к полю. Сам Python не делает ничего — вся логика в Pydantic.

#### Подготовка к FastAPI

FastAPI тоже читает метаданные в `Annotated`. Когда FastAPI видит `Annotated[тип, Depends(функция)]`, он вызывает функцию и подаёт результат в endpoint. Об этом — в следующем разделе.

**Упражнение:**

Что выведет этот код?

```python
from typing import Annotated

name: Annotated[str, "имя пользователя"] = "Alice"
print(type(name))
```

<details>
<summary>Ответ</summary>

```
<class 'str'>
```

`Annotated` не меняет тип. `name` — обычная строка. Метаданные `"имя пользователя"` игнорируются Python.
</details>

---

### 1.2 Инъекция зависимостей через Depends

#### Идея

Вместо того чтобы писать всю логику в одном endpoint, мы разбиваем её на функции-зависимости. FastAPI сам вызывает их и подаёт результат в endpoint.

Пример с одной зависимостью:

```python
from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

def add_1(a: int):
    return a + 1

@app.post('/test')
async def dependency_test(a: Annotated[int, Depends(add_1)]):
    return a
```

Когда приходит запрос `POST /test?a=5`, FastAPI:

1. Видит `Depends(add_1)` в аннотации параметра `a`
2. Вызывает `add_1(a=5)` — получает `6`
3. Передаёт `6` в `dependency_test` как аргумент `a`
4. Возвращает `6`

Это то же самое, что написать вручную:

```python
@app.post('/test')
async def without_dependency(a: int):
    a = add_1(a)
    return a
```

Результат одинаковый, но с `Depends` логика вынесена в отдельную функцию, которую можно переиспользовать.

#### Цепочка зависимостей

Одна зависимость может зависеть от другой. FastAPI сам выстраивает цепочку вызовов.

```python
def add_2(a: int):
    return a + 2

def add_3(a: Annotated[int, Depends(add_2)]):
    return a + 1

@app.post('/test')
async def dependency_test(a: Annotated[int, Depends(add_3)]):
    return a
```

Что происходит при запросе `POST /test?a=5`:

```
запрос (a=5)
    ↓
add_2(5) → 7
    ↓
add_3(7) → 8
    ↓
dependency_test(8) → 8
    ↓
ответ: 8
```

FastAPI сам определяет порядок вызовов по зависимостям.

**Упражнение:**

Как бы выглядел этот код без `Depends` — просто вызовами функций?

<details>
<summary>Ответ</summary>

```python
def add_2(a: int):
    """Добавляет 2 к числу."""
    return a + 2

def add_3(a: int):
    """Добавляет 2 (через add_2), затем ещё 1."""
    result = add_2(a)
    return result + 1

@app.post('/test')
async def without_dependency(a: int):
    return add_3(a)
```

</details>

#### Зачем это нужно

- **Переиспользование** — одна зависимость используется в нескольких endpoints
- **Чистота** — endpoint содержит только бизнес-логику, вся подготовка данных — в зависимостях
- **Тестирование** — зависимость можно подменить (например, вместо реального токена передать тестовый)


---

### 1.3 HTTPBearer — извлечение токена из запроса

#### Как передаётся токен

Когда клиент аутентифицируется, он отправляет токен в HTTP-заголовке `Authorization`. Заголовок — это метаданные запроса, которые идут перед телом. Пример сырого HTTP-запроса:

```http
GET /profile HTTP/1.1
Host: localhost:8100
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbGljZSJ9.abc123
Content-Type: application/json
```

Токен передаётся в формате `Bearer <token>`. Слово `Bearer` — это тип токена (в нашем случае JWT), а после него идёт сама строка токена.

**Упражнение:**

Мы знаем, что токен приходит в заголовке `Authorization`. Но как получить этот заголовок в FastAPI — не парсить же сырой HTTP вручную?

<details>
<summary>Ответ</summary>

FastAPI предоставляет класс `HTTPBearer` из `fastapi.security`, который делает это за нас. Его не нужно вызывать вручную — он подключается через `Depends`, и FastAPI сам извлекает токен из заголовка.
</details>

#### HTTPBearer

`HTTPBearer` — это класс из `fastapi.security`, который читает заголовок `Authorization: Bearer <token>` и достаёт сам токен. Возвращает объект `HTTPAuthorizationCredentials` с полем `.credentials` — это строка токена.

Простейший endpoint, возвращающий токен из запроса:

```python
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()

@app.get('/token')
async def get_token_from_request(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    return {"token": credentials.credentials}
```

Когда приходит запрос с заголовком `Authorization: Bearer eyJhbG...`, FastAPI:

1. Видит `Depends(security)` — вызывает `HTTPBearer`
2. `HTTPBearer` читает заголовок `Authorization`, извлекает токен `eyJhbG...`
3. Возвращает объект `HTTPAuthorizationCredentials`, у которого `.credentials = "eyJhbG..."`
4. Передаёт этот объект в endpoint как `credentials`

#### Авторизация в Swagger

Чтобы протестировать этот endpoint в Swagger (`/docs`), нажмите кнопку **Authorize** в правом верхнем углу. Вставьте токен (без слова `Bearer`) в поле ввода и нажмите Confirm. Теперь Swagger будет автоматически добавлять заголовок `Authorization: Bearer <token>` ко всем запросам.

#### Автоматическая ошибка

Если в запросе нет заголовка `Authorization` — FastAPI сам вернёт ошибку 403. Не нужно писать `if token is None: raise ...`. `HTTPBearer` делает это автоматически.

#### Связь с предыдущим материалом

В [домашнем задании урока 49](../lesson49/lesson49.md) вы написали функцию `decode_token`, которая принимает строку-токен и делает `jwt.decode`. В домашнем задании этого урока вы построите цепочку:

```
HTTPBearer → get_token_data → get_user → /profile
```

`HTTPBearer` извлечёт токен из заголовка, `get_token_data` вызовет `decode_token` и вернёт Pydantic-модель с данными из токена, `get_user` найдёт пользователя по этим данным.

**Упражнение:**

Что произойдёт, если отправить запрос к endpoint выше без заголовка `Authorization`?

<details>
<summary>Ответ</summary>

FastAPI вернёт ошибку 403 автоматически. `HTTPBearer` проверяет наличие заголовка `Authorization: Bearer <token>` и если его нет — выбрасывает ошибку. Нам не нужно проверять это вручную.
</details>

---

## Итоги

- `Annotated` — способ приложить метаданные к типу. Python игнорирует метаданные, но библиотеки (Pydantic, FastAPI) могут их читать и использовать.
- `Depends` — FastAPI автоматически вызывает функцию-зависимость и подаёт результат в endpoint. Код становится чище, зависимости переиспользуются.
- Цепочка зависимостей: одна зависимость может зависеть от другой. FastAPI сам выстраивает порядок вызовов.
- `HTTPBearer` извлекает токен из заголовка `Authorization: Bearer <token>`. Возвращает `HTTPAuthorizationCredentials` с полем `.credentials`. Без заголовка — автоматически 403.
- Аутентификация в FastAPI — цепочка зависимостей: `HTTPBearer → get_token_data → get_user → endpoint`.

---

## Домашнее задание

Задания расположены от простого к сложному.

Материалы, которые пригодятся:

- [Урок 49. Аутентификация: хеширование и JWT](../lesson49/lesson49.md) — `pwdlib`, `pyjwt`, singleton, абстракции, `utils/auth` (домашнее задание 5), `UserJson` (домашнее задание 6)
- [Урок 47. Pydantic](../lesson47/lesson47.md) — `BaseModel`, `model_validate`, `model_dump`
- [Урок 46. FastAPI](../lesson46/lesson46.md) — эндпоинты, `HTTPException`, query-параметры, POST-запросы

В этом задании вы используете функции из домашнего задания урока 49:

- `decode_token(token: str) -> dict` — из ДЗ урока 49, делает `jwt.decode`, бросает `HTTPException` при ошибке
- `get_token(data: dict) -> str` — создаёт JWT-токен
- `get_hashed_password(password: str) -> str` — хеширует пароль
- `is_hashed_equal(plain_password: str, hashed_password: str) -> bool` — проверяет пароль
- `UserJson(UserStorage)` — хранилище пользователей в JSON-файле

Структура проекта:

```
backend/
  api.py              — эндпоинты
  schemas/user.py     — Pydantic-модели (придумайте сами)
  utils/auth.py       — из ДЗ урока 49
  utils/user.py       — get_token_data, get_user
  model/user.py       — UserStorage (ABC), UserJson (из ДЗ урока 49)
  main.py             — uvicorn.run
  .env                — SECRET_KEY, ALGORITHM, EXP_DATE
```

### Задание 1. Цепочка из 1 зависимости

Напишите endpoint `GET /normalize?text=...`, который принимает query-параметр `text` и возвращает строку, приведённую к нижнему регистру и очищенную от пробелов по краям (`strip` + `lower`).

Логику нормализации вынесите в функцию-зависимость. Endpoint должен принимать результат через `Annotated[str, Depends(...)]`.

```python
# Запрос: GET /normalize?text=  Hello World  
# Ожидаемый ответ: "hello world"
```

### Задание 2. Цепочка из 2 зависимостей

Напишите endpoint `GET /price?raw=...`, который принимает query-параметр `raw` — строку цены (например, `"999₽"` или `"$1299"`). Endpoint должен вернуть итоговую цену после применения скидки 10%.

Реализуйте две функции-зависимости:

1. Первая — принимает строку, удаляет символы валюты (`₽` и `$`), преобразует в `int`
2. Вторая — зависит от первой, применяет скидку 10% (округлите вниз до целого)

Endpoint принимает результат второй зависимости через `Annotated[int, Depends(...)]`.

```python
# Запрос: GET /price?raw=1000₽
# Ожидаемый ответ: 900

# Запрос: GET /price?raw=$500
# Ожидаемый ответ: 450
```

### Задание 3. Функция `get_token_data`

Напишите функцию `get_token_data` в модуле `utils/user.py`. Это зависимость, которая:

1. Через `Depends(HTTPBearer())` получает `HTTPAuthorizationCredentials`
2. Достаёт строку токена из `credentials.credentials`
3. Вызывает `decode_token(token)` из `utils/auth.py` (из ДЗ урока 49)
4. Если `decode_token` бросил `PyJWTError` — выбрасывает `HTTPException`:

```python
raise HTTPException(
    status_code=401,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)
```

5. Возвращает Pydantic-модель с данными из токена. Модель придумайте сами — она должна содержать поле `sub: str` (username пользователя)

### Задание 4. Функция `get_user`

Напишите функцию `get_user` в модуле `utils/user.py`. Это зависимость, которая:

1. Через `Depends(get_token_data)` получает модель с данными токена
2. Достаёт `sub` (username) из модели
3. Ищет пользователя в `UserJson` по username
4. Если пользователь не найден — `raise HTTPException(status_code=401, detail='User not found')`
5. Возвращает Pydantic-модель с публичными данными пользователя (без хеша пароля). Модель придумайте сами

### Задание 5. Endpoint `/register`

Напишите endpoint `POST /register` в `api.py`. Используйте Pydantic-модель для тела запроса (придумайте сами — должны быть `username`, `password`, `first_name`, `second_name`).

Логика:

1. Проверить, что username не занят — если занят, `HTTPException(400, 'Username already exists')`
2. Захешировать пароль через `get_hashed_password` из `utils/auth.py`
3. Создать пользователя в `UserJson` (передать хеш пароля, не сам пароль)
4. Вернуть Pydantic-модель с публичными данными (без пароля и хеша)

```python
# Запрос: POST /register
# Тело: {"username": "alice", "password": "secret123", "first_name": "Alice", "second_name": "Smith"}
# Ожидаемый ответ: {"username": "alice", "first_name": "Alice", "second_name": "Smith"}
# Статус: 201
```

### Задание 6. Endpoint `/login`

Напишите endpoint `POST /login` в `api.py`. Используйте Pydantic-модель для тела запроса (придумайте сами — должны быть `username` и `password`).

Логика:

1. Найти пользователя в `UserJson` по username
2. Если не найден — `HTTPException(401, 'login or password is incorrect')`
3. Проверить пароль через `is_hashed_equal` из `utils/auth.py`
4. Если пароль неверный — `HTTPException(401, 'login or password is incorrect')`
5. Создать токен через `get_token({'sub': username})` из `utils/auth.py`
6. Вернуть `{'access_token': токен, 'token_type': 'Bearer'}`

```python
# Запрос: POST /login
# Тело: {"username": "alice", "password": "secret123"}
# Ожидаемый ответ: {"access_token": "eyJhbG...", "token_type": "Bearer"}

# Запрос: POST /login
# Тело: {"username": "alice", "password": "wrong"}
# Ожидаемый ответ: 401 — login or password is incorrect
```

### Задание 7. Endpoint `/profile`

Напишите endpoint `GET /profile` в `api.py`. Endpoint использует `get_user` через `Annotated` + `Depends` и возвращает данные текущего пользователя.

```python
# Запрос: GET /profile
# Заголовок: Authorization: Bearer eyJhbG...
# Ожидаемый ответ: {"username": "alice", "first_name": "Alice", "second_name": "Smith"}

# Запрос: GET /profile (без заголовка Authorization)
# Ожидаемый ответ: 403
```

### Задание 8. Тестирование через Swagger

1. Запустите сервер (`python main.py`)
2. Откройте `http://localhost:8100/docs`
3. Зарегистрируйте пользователя через `POST /register`
4. Нажмите кнопку **Authorize** в Swagger, введите токен, полученный из `POST /login`
5. Выполните запрос `GET /profile` — убедитесь, что вернулись данные вашего пользователя
6. Выполните запрос `GET /profile` без авторизации (очистите токен в Authorize) — убедитесь, что возвращается 403
7. Выполните запрос `GET /profile` с неверным токеном — убедитесь, что возвращается 401
