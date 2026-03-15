# Урок 32. На чем стоит веб-программирование

## Материал урока

### 1. Установка редактора кода (VS Code)

*   Для написания кода нам понадобится среда разработки — редактор VS Code (Visual Studio Code).
*   Это универсальный редактор, подходит не только для веба, но и для других языков (например, Python).
*   Скачай VS Code по [ссылке](https://code.visualstudio.com/download)
*   После установки можно настроить внешний вид (тему) под себя в разделе настроек.

### 2. Установка расширения Live Server(Five Server)

*   Чтобы увидеть результат работы сразу, без ручной перезагрузки страницы в браузере, нужно установить специальное расширение.
*   В VS Code перейди во вкладку с расширениями, найди **Live Server** и установи его.
*   Когда ты создашь HTML-файл, нажми `Ctrl+Shift+P` начни вводить `five-server`. Выбери `Five-Server: start`

### 3. Роль HTML, CSS и JavaScript в браузере
*   Браузер понимает только эти три технологии. Это фундамент веб-разработки.
*   **HTML (язык разметки):** Это «скелет» или дорожная разметка страницы. Он показывает, где заголовок, где параграф, где таблица. Отвечает только за структуру.
*   **CSS (язык стилей):** Это «красота» и внешний вид. Он задает цвета, шрифты, размеры и расположение элементов на странице.
*   **JavaScript (язык программирования):** Это «функционал» и действие. Благодаря ему страница реагирует на нажатие кнопок и другие действия пользователя. В отличие от HTML и CSS, это полноценный язык программирования.

Ниже содержание страницы с урока

`index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Что такое html?</title>
    <script defer src="script.js"></script>
</head>
<body>
    <header>
        <div class="header-title">Курсы по программированию от Антона Чигура</div>
        <div class="header-navigation">
            <div class="navigation-item">Курсы</div>
            <div class="navigation-item">Тренажеры</div>      
            <div class="navigation-item">Анекдоты</div>      
        </div>
    </header>
    <h1>Что такое HTML?</h1>

    <article>
        <p class="definition">
        HTML (HyperText Markup Language) — это стандартный язык разметки документов, используемый для создания структуры веб-страниц. Он определяет, где находятся заголовки, абзацы, ссылки, изображения и другие элементы, позволяя браузеру правильно отобразить контент. Это основа веб-разработки, но HTML не является языком программирования.
        </p>
        
        <p>
            <div class="question">А почему html не язык программирования?</div>
            <div class="answer">HTML (HyperText Markup Language) не является языком программирования, так как это язык разметки, предназначенный для структурирования и отображения контента в браузере. В отличие от языков программирования, HTML не умеет выполнять вычисления, обрабатывать логику (if/else), использовать переменные или циклы.</div>
        </p>

        <button onclick="buttonClick()">Тыкни на меня</button>
    </article>

</body>
</html>
```

`style.css`:
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background-color: #f5f5f5;        /* light gray backdrop */
  font-family: Arial, Helvetica, system-ui, sans-serif;
  line-height: 1.6;                 /* comfortable reading line height */
  color: #111;                      /* near-black for default text */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;              /* centers child horizontally (header, h1, article) */
}

/* Header */
header {
  background-color: #333;           /* dark gray */
  color: #fff;                      /* white text */
  display: flex;
  align-items: center;
  justify-content: space-between;    /* title left, navigation right */
  padding: 1rem 2rem;
  width: 100%;                      /* full width of viewport */
}

.header-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.header-navigation {
  display: flex;
  gap: 1.5rem;                      /* space between navigation items */
}

.navigation-item {
  color: #fff;
  padding: 0.25rem 0;
  cursor: default;                  /* since they're not links, but style as interactive */
  transition: text-decoration 0.2s ease;
}

/* Subtle hover effect: underline */
.navigation-item:hover {
  text-decoration: underline;
  text-underline-offset: 4px;
}

/* Main Heading (h1) – centered, dark gray */
h1 {
  color: #333;
  text-align: center;
  margin: 2rem 0 1rem;
  font-size: 2.2rem;
  font-weight: 500;
  line-height: 1.2;
}

/* Article – main content card */
article {
  background-color: #fff;           /* pure white background */
  max-width: 800px;
  width: 90%;                       /* responsive fallback */
  margin: 0 auto 2rem;              /* center horizontally, bottom spacing */
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* subtle gray shadow */
}

/* Definition paragraph */
.definition {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  color: #222;                      /* slightly softer than pure black */
}

/* Paragraph that contains the question/answer divs */
/* We keep its bottom margin for spacing, but inner divs provide their own margins */
p {
  margin-bottom: 1.5rem;
}

/* Question block */
.question {
  font-weight: bold;
  font-size: 1.2rem;
  color: #333;                      /* dark gray */
  margin-bottom: 0.5rem;
}

/* Answer block */
.answer {
  font-size: 1rem;
  line-height: 1.6;
  color: #000;                      /* pure black for maximum contrast */
}

/* Additional spacing for any content inside article */
article > *:last-child {
  margin-bottom: 0;                 /* remove extra margin from last element */
}
```

`script.js:`
```js
let buttonClicked = false;

function buttonClick(){
    const headerTitle = document.getElementsByClassName('header-title');
    if (buttonClicked){
        headerTitle[0].style.backgroundColor = '';
    }
    else {
        headerTitle[0].style.backgroundColor = 'red';
    }
    
    buttonClicked = !buttonClicked;
}
```

### 4. Взаимодействие трех технологий
*   Попробуй удалить CSS-файл из проекта — страница станет «некрасивой».
*   Попробуй удалить JavaScript — например, кнопка перестанет нажиматься.
*   HTML (скелет) остается всегда, а CSS и JavaScript добавляют ему вид и поведение.

### 5. Как работает серверная часть на примере Python

HTML, CSS и JavaScript отвечают за то, что пользователь видит в браузере и с чем взаимодействует. Но откуда берутся данные, например, список друзей или новые сообщения? За это отвечает серверная часть, которую часто пишут на языках вроде Python.

Представь, что ты заходишь в социальную сеть и открываешь страницу со своими сообщениями. Вот что происходит за кулисами:

1.  **Запрос от браузера.** Когда страница загружается, JavaScript, работающий в твоём браузере, отправляет запрос на сервер. Этот запрос звучит примерно так: «Дай все сообщения для пользователя Вася».

2.  **Обработка на сервере (Python).** Запрос прилетает на сервер, где работает программа на Python. Python-программа:
    *   Проверяет, действительно ли это Вася (авторизация).
    *   Обращается к базе данных, где хранятся все сообщения.
    *   Достаёт оттуда только те сообщения, которые адресованы Васе.
    *   Упаковывает эти сообщения в удобный формат (чаще всего JSON — это как список с текстом и датами).

3.  **Ответ сервера.** Сервер отправляет этот пакет с данными обратно в браузер.

4.  **Отображение данных.** JavaScript в браузере получает данные и, используя HTML и CSS, «рисует» их на странице: подставляет текст сообщений в нужные блоки, применяет стили, чтобы было красиво.

Таким образом, Python выступает в роли «мозга», который хранит данные и выполняет сложную логику (кто кому что написал, какие права доступа), а HTML/CSS/JS — это «лицо», которое показывает результат пользователю в удобном и красивом виде.

## Домашнее задание 

- Установите и настройте VS code
- Пройдите [тренажер](https://code-basics.com/ru/languages/html)  до пункта "Вставка компьютерного кода в HTML" включительно
- Сами напишите простую html-страницу на произвольную тему. Опционально можете добавить стили. Стили можно сгенерировать при помощи deepseek или другой LLM