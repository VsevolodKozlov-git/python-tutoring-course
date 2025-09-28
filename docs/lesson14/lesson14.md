
# Урок 14. Работа с файловой системой

## Повторение материала  

#### Что такое файловая система?

####  В чем отличие файловой системы Windows от Linux? Назовите 2 отличия

#### Абсолютные и относительный путь к файлу                      

Пусть у нас есть следующая структура файловой системы
```
C:/
├── Users/
│ └── Иванов/
│ ├── Документы/
│ │ └── проект_математика.py
│ └── Загрузки/
│ └── данные.txt
├── Program Files/
└── Windows/
```

Текущая рабочая директория: `C:/Users/Иванов/Документы/`

1. Каким будет абсолютный путь к файлу `данные.txt`?
2. Каким будет относительный путь к файлу `данные.txt`:
3. В каких ситуациях удобнее использовать относительный путь, а в каких абсолютный?
4. Каким методом можно определить, что путь абсолютный?


#### Работа с путем windows в python.

Пусть нам надо открыть файл по пути `C:\Users\vsevolod\.gitconfig`

Вопросы:

- С какими проблемами мы столкнемся если напишем:
```python
import  pathlib
path = pathlib.Path("C:\Users\vsevolod\.gitconfig")
```

- Какие есть 2 способа решить эти проблемы?


#### Использование `pathlib.Path.cwd`

- Что делает эта функция?

- Что будет, если, находясь по пути `C:\Users\vsevolod`, я выполню команду:
```
python examples\print_cwd.py
```
который содержит:
```python
import pathlib

print(pathlib.Path.cwd())
```

Если хотим, чтобы всегда выводилось одно и то же, то можем написать:
```python
import pathlib

print(pathlib.Path(__file__))
```

#### Как получить путь к файлу `.gitignore`, который находится в домашней папке?

#### Ползаем по директориям

Пусть мы имеем следующий код:
```python
import pathlib
home = pathlib.Path('C:/Users/vsevolod')
```

- Как получить родительскую директорий переменной `home`?
- Как получить список родительских директорий `home`?
- Как проверить, что в этой директории существует файл `.gitignore`


#### Создание директорий
Пусть мы имеем следующий код:
```python
import pathlib
home = pathlib.Path('C:/Users/vsevolod')
```

- Как проверить, что в `home` нет директории `dir1`? 
- Как создать директорию `dir1`? 
- Как создать файл `example` внутри `dir1`? 
- Что произойдет если попробовать создать `dir1`, когда она существует?

#### Поиск файлов

Пусть мы имеем следующий код:
```python
import pathlib
home = pathlib.Path('C:/Users/vsevolod')
```

- Как вывести все файлы в `home`? 
- Как вывести все файлы с расширением `.txt` в `home`? 
- Как найти все файлы с расширением `.txt` в `home` и всех директориях внутри `home`? Какие есть 2 способа это сделать?


#### Удаление файлов и директорий

- Какой метод удаляет файл?
- Какие 2 метода удаляют директории? Чем они отличаются?

## Упражнение из ДЗ

```python
from pathlib import Path

def main():
    cwd = Path.cwd()
    image_dir = cwd / 'images'

    if not image_dir.exists():
        image_dir.mkdir()

    image_extensions = ['gif', 'png', 'jpg']
    image_files = find_files_by_extension(cwd, image_extensions)
    print(f'Найдены изображения: {image_files}')
    move_files(image_dir, image_files)

def find_files_by_extension(root_dir, extensions):
    image_paths = []
    for extension in extensions:
        paths = root_dir.rglob(f'*.{extension}')
        image_paths.extend(paths)

    return image_paths

def move_files(target_dir, files):
    for file in files:
        new_path = target_dir / file.name
        if new_path.exists():
            print(f'Файл {file.name} уже существует. Произведена замена')
        file.replace(new_path)


if __name__ == '__main__':
    main()
```

## Домашнее задание

Прочитайте главы 12.5-12.8 включительно