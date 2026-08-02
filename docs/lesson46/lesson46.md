# Урок. FastAPI: создание API на Python

В этом уроке мы познакомимся с фреймворком FastAPI — современным инструментом для быстрой разработки веб-API на Python. Вы научитесь устанавливать необходимые пакеты, создавать конечные точки (эндпоинты), обрабатывать параметры запросов, возвращать ошибки и принимать данные через POST-запросы с помощью моделей Pydantic.

## Установка FastAPI и uvicorn

Для работы потребуется две библиотеки: сам фреймворк FastAPI и ASGI-сервер uvicorn, который будет принимать HTTP-запросы и передавать их приложению.

**Документация:** [FastAPI — First Steps](https://fastapi.tiangolo.com/ru/tutorial/first-steps/)  
Установка выполняется через `pip`:

```bash
pip install fastapi[standard]
pip install uvicorn
```

**Зачем нужен ASGI-сервер?** FastAPI — это фреймворк, который описывает логику обработки запросов. Однако он не умеет самостоятельно принимать сетевые соединения и разбирать сырые HTTP-пакеты. Эту задачу берёт на себя uvicorn: он слушает порт, получает запрос, передаёт его в приложение FastAPI, получает HTTP-ответ и отправляет обратно клиенту. Таким образом, uvicorn выступает прослойкой между внешним миром и вашим Python-кодом.

## Первое приложение на FastAPI

Минимальное приложение состоит из импорта класса `FastAPI`, создания его экземпляра (обычно называют `app`) и объявления эндпоинтов с помощью декораторов.

Создадим файл `api.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def home():
    return {'msg': 'hello world'}
```

Декоратор `@app.get('/')` превращает обычную асинхронную функцию `home` в GET-эндпоинт. Всё, что возвращает функция (словарь, список, Pydantic-модель), FastAPI автоматически преобразует в JSON-ответ.

## Запуск приложения

Для запуска создадим отдельный файл `main.py`, который будет точкой входа. В нём мы импортируем объект `app` из `api` и запускаем uvicorn.

```python
import uvicorn
from api import app

if __name__ == '__main__':
    uvicorn.run(
        app='api:app',   # путь к модулю и переменной приложения
        host='0.0.0.0',
        port=8100,       # порт
        reload=True,     # автоматическая перезагрузка при изменениях кода
        timeout_graceful_shutdown=0,
        log_level='debug'
    )
```

После выполнения `python main.py` сервер запустится, и при переходе по адресу `http://localhost:8100` вы увидите `{"msg": "hello world"}`.

## Автоматическая документация

FastAPI автоматически генерирует интерактивную документацию Swagger UI по адресу `http://localhost:8100/docs`. Там можно посмотреть все доступные эндпоинты, их параметры и даже выполнить запросы прямо из браузера — без необходимости в Postman или curl.

## Обработка параметров пути и ошибок

Чтобы получить конкретный ресурс по его идентификатору, в пути эндпоинта указывается параметр в фигурных скобках, например `/movie/{movie_id}`. FastAPI автоматически извлекает значение и передаёт его в функцию.

Если запись не найдена, вместо громоздкого ручного формирования ответа можно выбросить исключение `HTTPException` — фреймворк сам вернёт клиенту корректный HTTP-статус с описанием.

```python
from fastapi import FastAPI, HTTPException

# тестовые данные
movies = [
    {'id': 1, 'title': 'Властелин колец', 'views': 100},
    {'id': 2, 'title': 'Гарри Поттер', 'views': 80},
    {'id': 3, 'title': 'Лицо со шрамом', 'views': 70},
]

@app.get('/movie/{movie_id}')
async def get_movie_by_id(movie_id: int):
    found = [movie for movie in movies if movie['id'] == movie_id]
    if len(found) == 0:
        raise HTTPException(status_code=404, detail='Не найден фильм по id')
    if len(found) > 1:
        # Исключение общего вида – для внутренних ошибок, не передаётся клиенту как HTTPException
        raise ValueError('Найдено несколько фильмов по одному id, они не уникальны')
    return found[0]
```

**Правила:**
- Параметр пути объявляется в строке декоратора в фигурных скобках, а в функции — с таким же именем и ожидаемым типом (`int`, `str` и др.).
- При возникновении ситуации «не найдено» используйте `HTTPException(status_code=404, detail=...)`.
- Внутренние ошибки (например, дубликаты в данных) можно выбрасывать обычными исключениями Python, но лучше явно возвращать 5xx через `HTTPException`.

## Query-параметры

Query-параметры передаются в URL после вопросительного знака: `/movie?offset=10&limit=5`. В FastAPI их реализация предельно проста: достаточно добавить аргументы в функцию эндпоинта.

```python
@app.get('/movie')
async def get_movies_all(offset: int = 0, limit: int | None = None, views: int | None = None):
    movies_selected = movies[offset:]
    if limit:
        movies_selected = movies_selected[:limit]

    if views is not None:
        movies_selected = [movie for movie in movies_selected if movie['views'] == views]

    return movies_selected
```

- `offset` и `limit` реализуют простую пагинацию: `offset` задаёт сдвиг от начала списка, `limit` — максимальное количество возвращаемых записей.
- Параметру `views` можно задать значение по умолчанию `None`, чтобы фильтрация по количеству просмотров применялась только тогда, когда параметр передан явно.
- Типизация `int | None` означает, что параметр необязателен, и если он не указан, его значение будет `None`.

## POST-запросы и модели Pydantic

Для создания новых записей используется POST-запрос. В отличие от GET, он содержит тело с данными. Чтобы описать структуру ожидаемых данных, применяются модели Pydantic.

**Документация:** [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)

Создадим модель `MovieData` с полями `title` и `views`, а затем эндпоинт, который принимает её в качестве параметра.

```python
from pydantic import BaseModel

class MovieData(BaseModel):
    title: str
    views: int

# глобальная переменная для имитации автоинкремента id
movie_id_max = 3

@app.post('/movie')
async def post_movie(movie_data: MovieData):
    global movie_id_max
    movie_id_max += 1

    new_movie = {
        'id': movie_id_max,
        'title': movie_data.title,
        'views': movie_data.views
    }

    movies.append(new_movie)
    return new_movie
```

FastAPI автоматически валидирует тело запроса: если поля отсутствуют или имеют неверный тип, клиент получит ошибку 422 с подробным описанием. Внутри функции мы работаем с обычным объектом Python, получая доступ к полям через точку (`movie_data.title`).

## Полный код примера

Ниже представлен готовый файл `api.py`, объединяющий все рассмотренные эндпоинты. Для запуска используйте приведённый выше `main.py`, импортировав из этого модуля `app`.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

movies = [
    {'id': 1, 'title': 'Властелин колец', 'views': 100},
    {'id': 2, 'title': 'Гарри Поттер', 'views': 80},
    {'id': 3, 'title': 'Лицо со шрамом', 'views': 70},
]

movie_id_max = 3

@app.get('/')
async def home():
    return {'msg': 'hello world'}

@app.get('/movie/{movie_id}')
async def get_movie_by_id(movie_id: int):
    found = [movie for movie in movies if movie['id'] == movie_id]
    if len(found) == 0:
        raise HTTPException(status_code=404, detail='Не найден фильм по id')
    if len(found) > 1:
        raise ValueError('Найдено несколько фильмов по одному id, они не уникальны')
    return found[0]

@app.get('/movie')
async def get_movies_all(offset: int = 0, limit: int | None = None, views: int | None = None):
    movies_selected = movies[offset:]
    if limit:
        movies_selected = movies_selected[:limit]
    if views is not None:
        movies_selected = [movie for movie in movies_selected if movie['views'] == views]
    return movies_selected

class MovieData(BaseModel):
    title: str
    views: int

@app.post('/movie')
async def post_movie(movie_data: MovieData):
    global movie_id_max
    movie_id_max += 1
    new_movie = {
        'id': movie_id_max,
        'title': movie_data.title,
        'views': movie_data.views
    }
    movies.append(new_movie)
    return new_movie
```

## Итоги

- FastAPI — современный и быстрый фреймворк для создания API на Python, использующий стандартные аннотации типов.
- Для работы приложения необходим ASGI-сервер (например, uvicorn), который принимает HTTP-запросы и взаимодействует с FastAPI.
- Эндпоинты объявляются с помощью декораторов `@app.get()`, `@app.post()` и т.д.; внутри — обычные асинхронные функции.
- Параметры пути захватываются через фигурные скобки `{param}`, а query-параметры — через аргументы функции.
- Для возврата HTTP-ошибок используется `HTTPException`, не нужно вручную формировать статус-коды ответа.
- Pydantic-модели позволяют описать структуру тела запроса и автоматически валидировать входящие данные.
- FastAPI автоматически генерирует интерактивную документацию Swagger по адресу `/docs`.

### [Ссылка на код с урока](https://github.com/VsevolodKozlov-git/tutoring-fastapi/tree/main)

## Домашнее задание

1. Прочитайте статью про [декораторы](https://habr.com/ru/companies/otus/articles/727590/)
2. Выполните задание по декоратора ниже
3. Добавьте в приложение эндпоинт `PUT /movie/{movie_id}`, который обновляет информацию о фильме по `id`. Тело запроса должно содержать новые значения `title` и `views` (можно использовать ту же модель `MovieData`). Если фильм не найден — возвращайте 404.
4. Реализуйте эндпоинт `DELETE /movie/{movie_id}` для удаления фильма из списка. При успешном удалении  возвращайте  удалённый объект
5. Протестируйте все методы через автоматическую документацию `/docs` и убедитесь, что ошибки возвращаются с понятными описаниями.

**Условие:**  
Реализуйте два декоратора:

1. `@log_call` — выводит в консоль имя вызываемой функции и переданные аргументы (позиционные и именованные) перед её выполнением.
2. `@timer` — замеряет время выполнения функции (используйте `time.perf_counter()`) и выводит результат в секундах с точностью до 4 знаков после запятой.
    

**Задача:**  
Напишите декоратор `@timer` и примените его к функции, которая вычисляет сумму чисел от 1 до N с помощью цикла.  
Затем напишите декоратор `@log_call` и примените его к функции, которая проверяет, является ли число простым.

**Дополнительное требование:**  
Используйте `functools.wraps`, чтобы сохранить метаданные функций.