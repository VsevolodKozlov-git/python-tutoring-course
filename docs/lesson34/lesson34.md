# Урок 34. Основы HTML: часть 2

## Повторяем ДЗ

#### Зачем атрибут `alt` изображению?

#### Зачем указывать аудио/видео в разных форматах?

#### Зачем нужны метатеги?

#### Зачем нужно указывать viewport? Что означают `width` и `initial-scale`?

#### Зачем используется тег `<link>`?

#### Чем `<span>` отличается от `<div>`?

#### Зачем нужны формы на сайте?

#### Какие типы полей вы знаете?

#### Зачем нужны атрибуты `type`, `name`, `value` у `<input>`?

#### Радиокнопки: что произойдет, если изменить `name` у второй радиокнопки на `test`?

```html
<body>
    <form action="/people">
       <label>
            html:
            <input type="radio" name="language" value="html">
       </label>
        <label>
            css:
            <input type="radio" name="test" value="css">
       </label>
    </form>
</body>
```


#### Чем `<select>` отличается от радиокнопок с точки зрения функционала?

#### Зачем нужны `disabled` пункты в `<select>`?

#### Что делает эта форма?

```html
    <form action="/people" id="people-form">
        <label>
            Логин:
            <input type="text" name="username">
        </label>

        <br>

        <label>
            Пароль:
            <input type="password" name="password">
        </label>

        <br>
        <label>
            Персонаж
        <select name="MK11">
            <option value="null" disabled>choose your fighter</option>
            <option value="scorpion">scorpion</option>
            <option value="subzero">subzero</option>
        </select>
        </label>
    </form>

    <button form="people-form" type="reset">Убрать все</button>
    <button form="people-form" type="submit" formmethod="post">Отправить</button>
```

#### Почему `<div id="...">` хуже семантических тегов?

#### Объясните смысл семантических тегов: `header`, `nav`, `main`, `section`, `article`, `footer`

#### Чем `<section>` отличается от `<article>`?

#### Что такое микроразметка? Зачем она нужна?

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

Пройти [курс](https://code-basics.com/ru/languages/css) до "Базовые правила типографики" включительно