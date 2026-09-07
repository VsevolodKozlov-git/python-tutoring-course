# Урок 48 (подготовка). Переменные окружения, HTTP-запросы и даты

В этом уроке мы разберём три темы, которые понадобятся для проектного урока: хранение секретных данных в `.env`, выполнение HTTP-запросов из Python с помощью `httpx` и преобразование unix-timestamp в читаемые даты.

---

## CORS

```python
origins = [
    "http://localhost:8100",
    "http://127.0.0.1:8100",  # на случай, если frontend обращается через 127.0.0.1
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # список разрешённых источников
    allow_credentials=True,         # разрешить передачу cookies и заголовков авторизации
    allow_methods=["*"],            # разрешить все HTTP-методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],            # разрешить все заголовки
)
```

Как работает middleware:

- frontend отправил запрос
- fastAPI получил запрос
- middleware промежуточные шаги
    - проверка CORS
    - проверка авторизации
        - есть ли в запросе Bearer token
        - если ок, получить username пользователя
- Работает фукнция async def home()
- Постобработчики 
    - Добавить поле с датой, когда запрос вернул ответ

## Переменные окружения и `.env`

### Что такое переменные окружения

Переменные окружения — это именованные значения, доступные процессу операционной системы. Их можно задать в системе, но в Python-проектах принято хранить их в специальном файле `.env` рядом с кодом.

### Зачем нужен `.env`

В проектах часто используются секретные данные: API-ключи, пароли, токены. Хранить их прямо в коде нельзя по двум причинам:

1. **Безопасность** — если код попадёт к кому-то ещё, ключ будет скомпрометирован.
2. **Гибкость** — на разных компьютерах (ваш, сервер, компьютер другого разработчика) ключи могут отличаться. С `.env` каждый хранит свой ключ локально, а код остаётся одинаковым.

### Формат файла `.env`

Файл `.env` — это текстовый файл, в котором каждая строка задаёт одну переменную в формате `ИМЯ=значение`:

```env
STEAM_API_KEY=tpZuyiSiaMbJtq2x0K8w
SERVER_PORT=8100
DEBUG=True
```

### Библиотека `python-dotenv`

Для загрузки переменных из `.env` в Python используется библиотека `python-dotenv`.

Установка:

```bash
pip install python-dotenv
```

Пример использования. Создадим файл `.env`:

```env
STEAM_API_KEY=tpZuyiSiaMbJtq2x0K8w
```

И файл `config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # загружает переменные из файла .env

api_key = os.getenv("STEAM_API_KEY")
print(api_key)
# tpZuyiSiaMbJtq2x0K8w
```

`os.getenv("ИМЯ")` возвращает значение переменной окружения в виде строки или `None`, если переменная не найдена.

**Важно:** файл `.env` нельзя выкладывать в общий доступ. Каждый разработчик создаёт свой `.env` локально.

**Упражнения:**

1. Создайте файл `.env` с переменной `STEAM_API_KEY` и любым значением. Загрузите её в Python-коде и выведите в консоль.
2. Что вернёт `os.getenv("НЕСУЩЕСТВУЮЩАЯ_ПЕРЕМЕННАЯ")`? Проверьте.
3. Подумайте, почему `os.getenv` возвращает `None`, а не выбрасывает ошибку, когда переменная не найдена. В каких случаях это полезно?

---

## HTTP-запросы из Python с помощью `httpx`

### Зачем нужен `httpx`

`httpx` — это современная библиотека для выполнения HTTP-запросов из Python. Она похожа на `requests`, но поддерживает как синхронные, так и асинхронные запросы, и хорошо работает вместе с FastAPI.

Установка:

```bash
pip install httpx
```

### Простой GET-запрос

```python
import httpx

response = httpx.get("https://httpbin.org/get")
print(response.status_code)  # 200
print(response.json())        # {"args": {}, "headers": {...}, ...}
```

`httpx.get(url)` выполняет GET-запрос и возвращает объект `Response`. У ответа есть:

- `response.status_code` — HTTP-статус (200, 404, 500 и т.д.)
- `response.json()` — тело ответа, преобразованное из JSON в словарь Python
- `response.text` — тело ответа в виде строки

### Передача query-параметров

Query-параметры можно передавать через аргумент `params` — это удобнее и безопаснее, чем склеивать строку вручную:

```python
import httpx

response = httpx.get(
    "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/",
    params={
        "appid": 730,
        "key": "tpZuyiSiaMbJtq2x0K8w",
    }
)
print(response.json())
# {"response": {"player_count": 858733, "result": 1}}
```

`httpx` сам подставит параметры в URL: результат будет эквивалентен запросу `...?appid=730&key=tpZuyiSiaMbJtq2x0K8w`.

### Динамическое добавление API-ключа

В реальном проекте ключ хранится в `.env`, а не в коде. Комбинируя `dotenv` и `httpx`, можно динамически подставлять ключ в запрос:

```python
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("STEAM_API_KEY")

response = httpx.get(
    "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/",
    params={
        "appid": 730,
        "key": api_key,
    }
)
data = response.json()
print(data["response"]["player_count"])
# 858733
```

### Проверка статуса ответа

Внешний API может вернуть ошибку: сервер недоступен, неверный appID, превышен лимит запросов. Проверять статус ответа можно двумя способами.

Способ 1 — проверка `status_code`:

```python
response = httpx.get("https://store.steampowered.com/api/appdetails", params={"appids": 730})

if response.status_code != 200:
    print("Ошибка API:", response.status_code)
else:
    data = response.json()
```

Способ 2 — `raise_for_status()`, который выбросит исключение при HTTP-ошибке (4xx, 5xx):

```python
response = httpx.get("https://store.steampowered.com/api/appdetails", params={"appids": 730})
response.raise_for_status()  # выбросит HTTPStatusError, если статус не 2xx
data = response.json()
```

**Упражнения:**

1. Выполните GET-запрос к `https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/` с параметрами `appid=730`, `count=2` и ключом из `.env`. Выведите заголовки новостей.
2. Что произойдёт, если передать неверный `appid` (например, `999999999`) в запрос к `appdetails`? Проверьте статус-код и содержимое ответа.
3. Выполните запрос к несуществующему URL. Какую ошибку выбросит `raise_for_status()`?

---

## Unix-timestamp и работа с датами

### Что такое unix-timestamp

Unix-timestamp — это количество секунд, прошедших с 1 января 1970 года (UTC). Это универсальный способ представления времени, который используется во многих API.

Например, Steam API возвращает дату новости как число:

```json
{"date": 1787614760}
```

Это означает «1787614760 секунд с 1 января 1970 года».

### Преобразование в читаемую дату

Для работы с датами в Python используется встроенный модуль `datetime`.

```python
from datetime import datetime

ts = 1787614760
dt = datetime.fromtimestamp(ts)
print(dt)
# 2026-09-06 01:39:20
```

`datetime.fromtimestamp(ts)` принимает unix-timestamp и возвращает объект `datetime`, с которым удобно работать.

### Форматирование даты

Метод `strftime` (string format time) форматирует `datetime` в строку по заданному шаблону:

```python
from datetime import datetime

ts = 1787614760
dt = datetime.fromtimestamp(ts)

print(dt.strftime("%d.%m.%Y"))
# 06.09.2026

print(dt.strftime("%Y-%m-%d %H:%M"))
# 2026-09-06 01:39
```

Основные коды форматирования:

| Код | Значение | Пример |
|---|---|---|
| `%d` | День месяца (01–31) | `06` |
| `%m` | Месяц (01–12) | `09` |
| `%Y` | Год (4 цифры) | `2026` |
| `%H` | Часы (00–23) | `01` |
| `%M` | Минуты (00–59) | `39` |

### Пример: обработка дат из Steam API

```python
import httpx
from datetime import datetime

response = httpx.get(
    "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/",
    params={"appid": 730, "count": 3, "key": "tpZuyiSiaMbJtq2x0K8w"}
)
data = response.json()

for item in data["appnews"]["newsitems"]:
    date_str = datetime.fromtimestamp(item["date"]).strftime("%d.%m.%Y")
    print(f"{date_str} — {item['title']}")
# 06.09.2026 — Counter-Strike 2 Update
# 31.08.2026 — Counter-Strike 2 Update
# ...
```

**Упражнения:**

1. Преобразуйте число `1609459200` в дату и отформатируйте как `ДД.ММ.ГГГГ`.
2. Получите текущее время в виде unix-timestamp с помощью `datetime.now().timestamp()`. Преобразуйте обратно в читаемую дату.
3. В ответе Steam API поле `date` содержит `1787182593`. Отформатируйте его как `ГГГГ-ММ-ДД ЧЧ:ММ`.

---

## Обработка ошибок HTTP-запросов

При обращении к внешнему API может произойти что угодно: сервер недоступен, превышен лимит запросов, передан неверный appID. Бэкенд должен обрабатывать эти ситуации и возвращать клиенту понятные ошибки, а не падать.

### Основные типы ошибок

| Ситуация | Что происходит | Как обработать |
|---|---|---|
| Сервер недоступен / таймаут | `httpx` выбрасывает `httpx.ConnectError` или `httpx.TimeoutException` | `try/except` |
| HTTP-ошибка (4xx, 5xx) | `response.status_code` не равен 200 | Проверка `status_code` или `raise_for_status()` |
| API вернул `success: false` | HTTP-статус 200, но в данных `{"success": false}` | Проверка поля `success` в ответе |

### Пример обработки ошибок

```python
import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()
api_key = os.getenv("STEAM_API_KEY")


def get_game_info(appid: int) -> dict:
    try:
        response = httpx.get(
            "https://store.steampowered.com/api/appdetails",
            params={"appids": appid, "l": "russian"}
        )
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Steam API недоступен")

    data = response.json()
    app_data = data[str(appid)]

    if not app_data.get("success"):
        raise HTTPException(status_code=404, detail="Игра не найдена")

    return app_data["data"]


print(get_game_info(730)["name"])
# Counter-Strike 2

print(get_game_info(999999999))
# HTTPException: 404 — Игра не найдена
```

Разбор:

- `try/except httpx.HTTPError` перехватывает сетевые ошибки и HTTP-ошибки (если используется `raise_for_status()`).
- `HTTPException(502)` — сервер-посредник (бэкенд) получил ошибку от внешнего API. Клиент понимает, что проблема не в его запросе, а во внешнем сервисе.
- `app_data.get("success")` — Steam Store API возвращает HTTP 200 даже для несуществующих игр, но с `"success": false`. Поэтому проверять нужно содержимое ответа, а не только статус-код.

---

## Итоги

- Переменные окружения хранятся в файле `.env` и загружаются через `python-dotenv` с помощью `load_dotenv()` и `os.getenv()`.
- `httpx` выполняет HTTP-запросы; query-параметры передаются через словарь `params`, что удобнее и безопаснее ручной склейки URL.
- Unix-timestamp — секунды с 1 января 1970; преобразуется в дату через `datetime.fromtimestamp()` и форматируется через `strftime()`.
- При обращении к внешнему API нужно обрабатывать три уровня ошибок: сетевые (через `try/except`), HTTP-статусы (через `raise_for_status()`) и логические (проверка полей ответа вроде `success`).