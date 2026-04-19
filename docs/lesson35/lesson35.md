# Урок 35. Основы CSS: часть 1

## Повторяем ДЗ
#### Какие 3 способа указать стили для html имеются?

#### Почему таблицы стилей называются каскадными?

#### Правила наследования стилей

```html
<div style="border: 3px solid red; padding: 10px;">
    Родитель с красной рамкой
    <p>Этот текст внутри параграфа</p>
</div>
```

Вопрос: Будет ли у тега `<p>` красная рамка? Почему?


```html
<section style="color: navy; border-left: 5px solid orange;">
    <h2>Заголовок новости</h2>
    <p>Текст самой новости, очень интересный.</p>
</section>
```
Вопросы:
- Какого цвета будет текст в теге `<h2>`?
- Появится ли оранжевая вертикальная полоса слева от заголовка?

```html
<ul style="border: 2px solid blue; padding: 10px;">
    <li>Пункт 1</li>
    <li>Пункт 2</li>
    <li>Пункт 3</li>
</ul>
```

Вопрос: как сделать так, чтобы каждый элемент был обеведен синей рамкой?

#### Имеют ли html-теги стили по умолчанию?

#### Зачем нужны классы, почему нельзя обойтись id и тегами?

#### Приоритет классов

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        p {
            color: blue;
            font-size: 20px;
        }
    </style>
</head>
<body>
    <p style="color: red;">Какого цвета будет этот текст?</p>
</body>
</html>
```

**Вопрос:** Каким цветом отобразится текст внутри тега `<p>`? Объясните, почему один стиль победил другой.

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        #main {
            background-color: lightcoral;
        }
        .box {
            background-color: lightblue;
            width: 200px;
            height: 100px;
            border: 1px solid black;
        }
    </style>
</head>
<body>
    <div id="main" class="box">Цвет фона?</div>
</body>
</html>
```

**Вопрос:** Какой цвет фона будет у этого `<div>` — коралловый (`lightcoral`) или голубой (`lightblue`)? Почему?

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        p {
            color: gray;
            font-weight: normal;
        }
        .highlight {
            color: green;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <p class="highlight">Этот параграф с классом highlight.</p>
    <p>Обычный параграф.</p>
</body>
</html>
```

**Вопрос:** Какими цветом и начертанием шрифта будет отображаться первый параграф? Почему он не серый, как задано для всех `<p>`

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .btn {
            padding: 10px 20px;
            background-color: lightgray;
            border: 2px solid gray;
            color: black;
        }
        .primary {
            background-color: blue;
            color: white;
        }
        .btn.primary {
            background-color: darkblue;
            border-color: navy;
        }
    </style>
</head>
<body>
    <button class="btn">Обычная кнопка</button>
    <button class="btn primary">Важная кнопка</button>
</body>
</html>
```

**Вопрос:** Какой цвет фона будет у кнопки с классами `btn primary`? Какое CSS-правило победит и почему?

#### Как цвет задается в 16-ричной системе исчисления?

#### Как выровнять текст на html-странице?

#### Как регулировать жирность текста?

#### Какие есть способы сделать текст курсивным?

#### Зачем нужен атрибут `text-decoration`?

#### Зачем нужен атрибут `line-height`?

#### Зачем указывать несколько шрифтов?

```html
<style>
  .new-font {
    font-family: Arial, Futura, sans-serif;
  }
</style>
```

---

## Удобство разработки

### Какие горячие клавиши помогают в навигации по тексту в редакторе?

- `Ctrl+← / →` – перемещение по словам.
    
- `Ctrl+Shift+← / →` – выделение по словам.
    
- `PgUp / PgDn` – быстрый скроллинг по странице.
    
- (В VS Code также `Ctrl+E` для поиска файлов, `Ctrl+Shift+P` для командной палитры.)
    

### Что такое Emmet и как он ускоряет вёрстку?

- Emmet – плагин для автоматического развёртывания HTML/CSS сокращений.    
- Изучить основные фишки можно по [статье на Skillbox](https://skillbox.ru/media/code/uskoryaem-vyerstku-ispolzuya-emmet/).
    

### Какие возможности VS Code повышают удобство разработки?

- Быстрое перемещение между файлами: `Ctrl+E`
- Режим сплит-экрана, чтобы редактировать несколько файлов одновременно.
- Вызов Emmet через `Ctrl+Shift+P`
- Настройка собственных сочетаний клавиш


## Домашнее задание

Пройти [курс](https://code-basics.com/ru/languages/css)