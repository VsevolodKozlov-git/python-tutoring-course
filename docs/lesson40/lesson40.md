# Урок 40. Vue.JS урок 1

## Повторение ДЗ

#### Что делает этот код?

```
<script setup>
import { ref } from 'vue'

let id = 0

const inputBookName = ref(null)
const inputBookDescription = ref(null)

const books = ref([
  { id: id++, title: 'Гарри Поттер', description: 'Книга 1' },
  { id: id++, title: 'Таня Гроттер', description: 'Книга 2' },
])

const addBook = () => {
  books.value.push({
    id: id++,
    title: inputBookName.value,
    description: inputBookDescription.value,
  })
  inputBookName.value = null
  inputBookDescription.value = null
}
</script>

<template>
  <form @submit.prevent="addBook">
    <input v-model="inputBookName" required />
    <input v-model="inputBookDescription" required />
    <button>Добавить задачу</button>
  </form>
  <div v-for="book in books" :key="book.id">
    <h3>{{ book.title }}</h3>
    <p>{{ book.description }}</p>
  </div>
</template>

<style lang="css" scoped></style>
```

#### Что такое реактивность?

#### Что такое ref? Что такое reactive? Чем ref отличается от reactive?

#### ref в деталях

Является ли код ниже реактивным?
```js
const arr = ref([1, 2, 3])
arr.push(4)
```

Является ли код ниже реактивным?
```js
const arr = ref([1, 2, 3])
arr.value.push(4)
```

Является ли код ниже реактивным?
```js
const arr = ref([1, 2, 3])
arr.value = [1, 3]
```

Является ли код ниже реактивным?
```js
const counterRef = ref(0)
let counter = counterRef.value
counter++
```

Является ли код ниже реактивным?
```js
const counterRef = ref(0)
const addOne = (value) => value++
addOne(counterRef.value)
```

Является ли код ниже реактивным?
```js
const counterRef = ref(0)
const addOneRef = (inputRef) => inputRef.value++
addOneRef(counterRef)
```


#### reactive в деталях

Является ли код ниже реактивным?
```js
const arr = reactive([1, 2, 3])
arr.push(4)
```

Является ли код ниже реактивным?
```js
const arr = reactive([1, 2, 3])
arr = [2, 3]
```

#### Для чего нужен computed? Можно ли обойтись без него в коде?

#### Для чего нужен watch? 

#### Для чего `id` в `v-for`? Можно ли обойтись без него?

#### Как переиспользовать код Vue.JS при помощи компонент?

#### Зачем нужны  props?

#### Могут ли props быть реактивными?

#### Зачем нужен slot?

#### Зачем нужен emit?

## Из чего состоит проект на Vue.JS?

[Демонстрационный проект](https://github.com/VsevolodKozlov-git/vue-tutoring-demo-project)

## Домашнее задание

- Установить в VS Code: Eslint, Prettier ESlint

- Прочитайте "Основы" до отрисовки списков включительно: [ссылка](https://ru.vuejs.org/guide/essentials/application.html). Это материал как в туториале прошлого урока, только более подробно. Если некоторые вещи непонятны - ничего страшного

- Перенесите ваш проект HTML на Vue.JS