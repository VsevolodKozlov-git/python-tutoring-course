# Урок 42. Vue: props, slots и работа с API

В этом уроке мы разберём три ключевых механизма Vue, которые позволяют создавать гибкие и переиспользуемые компоненты, а также получать данные с сервера.

---

## Props — передача параметров в компонент

**Документация:** [Props в Vue 3](https://ru.vuejs.org/guide/components/props)

`props` — это параметры, которые мы передаём в компонент, чтобы управлять его поведением и внешним видом.  
Ближайшая аналогия — аргументы функции в Python или JavaScript. Внутри компонента вы используете переданные props точно так же, как локальные переменные.

### Простейший пример: кнопка с состоянием `disabled`

Если передать `disabled = false`, кнопка активна и на неё можно нажать.  
Если `disabled = true`, кнопка становится неактивной.

Мы также можем передать текст кнопки через prop `text`.

**Компонент кнопки `MButton.vue`:**

```vue
<template>
  <button class="green-btn" :disabled="disabled">
    {{ text }}
  </button>
</template>

<script setup>
const props = defineProps({
  disabled: {
    type: Boolean,
    required: false,
    default: false,
  },
  text: {
    type: String,
    required: true,
  },
})
</script>
```

**Использование:**

```vue
<MButton text="Это текст кнопки" :disabled="false" />
```

### Когда использовать двоеточие (`:`) в props?

Поведение атрибутов зависит от того, хотите ли вы передать статическую строку или результат JavaScript-выражения.

- **Без двоеточия** (`text="Привет"`) — передаётся **строка** «как есть». Такой синтаксис удобен только для строковых значений.
- **С двоеточием** (`:disabled="false"`, `:count="5"`) — Vue вычисляет всё, что внутри кавычек, как JavaScript-код. Это позволяет передавать числа, булевы значения, массивы, объекты, переменные и даже вызовы функций.

**Примеры:**

```vue
<!-- Строка передаётся без двоеточия -->
<MButton text="Нажми меня" />

<!-- Булево значение — обязательно с двоеточием, иначе "false" станет строкой -->
<MButton :disabled="false" />

<!-- Число — с двоеточием -->
<MyPagination :total="100" />

<!-- Массив — с двоеточием -->
<MyList :items="['один', 'два']" />

<!-- Объект — с двоеточием -->
<UserCard :user="{ name: 'Анна', age: 30 }" />
```

**Простое правило:** как только вам нужно передать что-то отличное от строки — ставьте двоеточие.

---

## Slots — передача HTML-содержимого

**Документация:** [Slots в Vue 3](https://ru.vuejs.org/guide/components/slots.html)

Если `props` позволяют передавать **значения** (строки, числа, объекты), то `slots` служат для передачи **готовых кусков HTML** (разметки) внутрь компонента.

### Один слот по умолчанию

Представьте, что нам нужен компонент, который просто центрирует любое переданное содержимое по горизонтали. Мы можем реализовать его с помощью слота по умолчанию.

**Компонент `MCenterHorizontal.vue`:**

```vue
<template>
  <div class="center-horizontal">
    <slot />
  </div>
</template>

<script setup>
// Никакой дополнительной логики не требуется
</script>

<style scoped>
.center-horizontal {
  display: flex;
  justify-content: center;
}
</style>
```

**Использование:**

```vue
<MCenterHorizontal>
  <p>Этот текст будет отцентрирован</p>
  <button>Кнопка тоже</button>
</MCenterHorizontal>
```

Всё, что мы помещаем между открывающим и закрывающим тегом `<MCenterHorizontal>`, попадает в `<slot />` и рендерится внутри центрирующего контейнера.

### Именованные слоты

Часто компоненту нужно несколько областей для вставки разного контента, например, карточка с заголовком и телом. Для этого используются **именованные слоты** (`named slots`).

**Компонент карточки `MCard.vue`:**

```vue
<template>
  <div class="center-horizontal">
    <div class="card">
      <h3><slot name="header"></slot></h3>
      <div class="card-content">
        <slot name="content"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
// Можно импортировать другие компоненты, если нужно
</script>

<style scoped>
.center-horizontal {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.card {
  max-width: 85%;
  min-width: 800px;
  border: none;
  border-radius: 24px;
  background-color: #1c1f1f;
  padding: 12px 24px;
  color: #fff;
}
</style>
```

**Использование именованных слотов:**

```vue
<MCard>
  <template #header>Параметры запроса</template>
  <template #content>
    <div>Фильтр 1</div>
    <div>Фильтр 2</div>
  </template>
</MCard>
```

---

## API — получение данных с сервера

### Что такое API?

**API** (Application Programming Interface) — программный интерфейс приложения.  
Простая аналогия: пульт от телевизора — это API, через который вы взаимодействуете с телевизором. Разработчики создают «пульт» для своего сервера, чтобы другие программы могли получать или отправлять данные.

Мы будем использовать **REST API** — самый распространённый подход:

- Общение идёт по протоколу **HTTP** (тот самый, на котором работает весь интернет).
- Сервер возвращает данные в формате **JSON** (JavaScript Object Notation) — текстовое представление объектов JavaScript, очень похожее на словари в Python.

### Наше тестовое API

Мы поработаем с бесплатным сервисом, который отдаёт случайные факты о кошках:  
`https://meowfacts.herokuapp.com/`

Откройте эту ссылку в браузере. Вы увидите что-то вроде:

```json
{"data":["Cats can drink sea water in order to survive."]}
```

При перезагрузке страницы факт меняется — это результат HTTP-запроса к серверу.

### Как выполнить HTTP-запрос из JavaScript?

В браузере есть встроенная функция `fetch`, но мы воспользуемся более удобной библиотекой **Axios**.  
Установим её в проект:

```bash
npm install axios
```

Теперь создадим компонент, который получает факт и показывает его на странице.

**Компонент `CatFact.vue`:**

```vue
<template>
  <div class="cat-fact">
    <button @click="getFact">Получить новый факт</button>
    <p v-if="catFact" class="fact-text">{{ catFact }}</p>
    <p v-else>Нажмите кнопку, чтобы загрузить факт</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const catFact = ref(null)

const getFact = async () => {
  try {
    // await приостанавливает выполнение, пока не придёт ответ
    const response = await axios.get('https://meowfacts.herokuapp.com/')
    // Ответ axios автоматически парсит JSON, поэтому response.data — уже объект
    catFact.value = response.data.data[0]
  } catch (error) {
    console.error('Ошибка при получении факта:', error)
    catFact.value = 'Не удалось загрузить факт :('
  }
}
</script>

<style scoped>
.cat-fact {
  margin: 20px;
  text-align: center;
}
button {
  padding: 8px 16px;
  margin-bottom: 12px;
  cursor: pointer;
}
.fact-text {
  font-style: italic;
}
</style>
```

```vue
<CatFact />
```

**Объяснение ключевых моментов:**

- `async` — ключевое слово, которое делает функцию асинхронной. Теперь внутри неё можно использовать `await`.
- `await` — говорит JavaScript: «Дождись, пока эта операция завершится, и только потом иди дальше». Мы ждём ответа от API.
- `axios.get(url)` — выполняет HTTP-метод GET (получение данных) по указанному адресу.
- `response.data` — axios автоматически превращает JSON-строку в настоящий JavaScript-объект.
- Обработка ошибок через `try...catch` позволяет не «уронить» всё приложение, если сервер недоступен.

---

## Итоги



- **props** — для передачи значений (как аргументы функции).
- **slots** — для передачи HTML-кусков; слот по умолчанию и именованные слоты (`<slot name="...">` + `<template #...>`).
- **API** — способ общения между программами; мы используем REST API, HTTP и библиотеку Axios для выполнения запросов и отображения данных.

Комбинируя эти три механизма, вы можете создавать мощные и удобные интерфейсы на Vue.


## Домашнее задание

Код с занятия доступен [здесь](https://github.com/VsevolodKozlov-git/vue-tutoring-demo-project)

1. Для вашего приложения напишите переиспользуемые компоненты:
   1. Обязательно используйте `props`
   2. Обязательно используйте `slots`, причем так, чтобы хотя бы в одном компоненте было несколько `slots`
2. Сделайте отдельный `view`, в котором по нажатии кнопки будет отсылаться запрос на API: [ссылка на API](https://meowfacts.herokuapp.com/). 