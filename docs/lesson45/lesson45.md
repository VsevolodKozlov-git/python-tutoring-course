# Урок 45. UI-киты на примере Nuxt UI

В этом уроке мы разберём, что такое UI-киты, зачем они нужны и как работать с одним из них — Nuxt UI. На практике увидим, как использовать готовые компоненты для быстрой разработки интерфейсов/

---

## Что такое UI-кит и зачем он нужен

UI-кит (от англ. *User Interface Kit*) — это набор готовых переиспользуемых компонентов интерфейса, разработанных другими программистами. Вместо того чтобы каждый раз писать кнопки, поля ввода, таблицы и навигационные панели с нуля, вы берёте готовые компоненты и настраиваете их под свои задачи.

**Документация:** [Nuxt UI — официальный сайт](https://ui.nuxt.com)

UI-киты особенно полезны для сложных элементов:
- навигационные меню с вложенностью;
- таблицы с сортировкой и фильтрацией;
- формы с валидацией;
- модальные окна, уведомления, выпадающие списки.

Создатели библиотек делают их максимально гибкими, чтобы покрыть потребности разных проектов. В документации подробно описан каждый компонент, его пропсы и примеры использования.

---

## Установка Nuxt UI в проект

Чтобы начать использовать Nuxt UI в вашем Vue-проекте, достаточно следовать официальной инструкции по установке.

**Документация:** [Установка Nuxt UI для Vue](https://ui.nuxt.com/docs/getting-started/installation/vue)

После установки все компоненты становятся глобально доступными. Например, компонент кнопки можно использовать прямо в шаблоне:

```vue
<template>
  <UButton label="Нажми меня" color="primary" />
</template>
```

---

## Работа с компонентами Nuxt UI

Основной принцип работы с любым UI-китом — **использовать компоненты из документации**. Вы ищете нужный элемент, смотрите пример кода и адаптируете его под свой проект.

**Документация:** [Все компоненты Nuxt UI](https://ui.nuxt.com/docs/components)

### Самый простой компонент: Кнопка `UButton`

**Документация:** [UButton](https://ui.nuxt.com/docs/components/button)

Компонент кнопки имеет множество пропсов для настройки внешнего вида и поведения, вот некоторые из них, остальные найдете в документации:
- `label` — текст кнопки;
- `color` — цветовая схема;
- `disabled` — состояние неактивности.
- `to` - на что ссылается кнопка

Примеры использования:

```vue
<!-- Простая кнопка -->
<UButton label="Сохранить" color="primary" />

<!-- Кнопка в состоянии загрузки -->
<UButton label="Загрузка..." loading />

<!-- Кнопка-ссылка -->
<UButton label="Перейти" to="/profile" />
```

---

## Пример: форма фильтрации персонажей

Рассмотрим полноценный пример, в котором используются несколько компонентов Nuxt UI: форма, поле формы, селекты, кнопка и таблица.

### Полный код примера:

```vue
<template>
  <UForm :validate="validateForm" :state="formValues" @submit="getCharacters" class="space-y-4">
    <UFormField label="Раса" name="race">
      <USelect v-model="formValues.race" :items="raceItems" class="min-w-30" />
    </UFormField>

    <UFormField label="Пол" name="gender">
      <USelect v-model="formValues.gender" :items="genderItems" class="min-w-30" />
    </UFormField>

    <UButton type="submit">Найти персонажей</UButton>
  </UForm>

  <UTable v-if="characters" :data="characters" :columns="tableColumns" />
</template>

<script setup>
import axios from 'axios'
import { h, ref } from 'vue'
import UBadge from '@nuxt/ui/components/Badge.vue'

// Хук для всплывающих уведомлений (из Nuxt UI)
const toast = useToast()

const formValues = ref({ race: null, gender: null })

const raceItems = [
  { label: 'Орк', value: 'Orcs' },
  { label: 'Эльф', value: 'Elf' },
  { label: 'Хоббит', value: 'Hobbit' },
  { label: 'Человек', value: 'Human' },
]

const genderItems = [
  { label: 'Мужчина', value: 'Male' },
  { label: 'Женщина', value: 'Female' },
]

const tableColumns = [
  {
    accessorKey: 'name',
    header: 'Имя',
  },
  {
    accessorKey: 'death',
    header: 'Умер?',
    // Продвинутый пример: кастомная ячейка с использованием UBadge
    cell: ({ row }) => {
      const death = row.getValue('death')
      const props = {}
      let text
      if (death === null) {
        props.color = 'error'
        text = 'No data'
      } else {
        props.color = 'success'
        text = death
      }
      return h(UBadge, props, text)
    },
  },
]

// Валидация формы — возвращает массив ошибок
const validateForm = () => {
  const errors = []
  if (!formValues.value.race) {
    errors.push({ name: 'race', message: 'Поле обязательно' })
  }
  if (!formValues.value.gender) {
    errors.push({ name: 'gender', message: 'Поле обязательно' })
  }
  return errors
}

const characters = ref(null)

const getCharacters = async () => {
  const params = {}

  // Формируем параметры запроса только из заполненных полей
  for (const [key, value] of Object.entries(formValues.value)) {
    if (value) {
      params[key] = value
    }
  }

  const charactersRequest = await axios.get('https://the-one-api.dev/v2/character', {
    headers: {
      Authorization: 'Bearer tpZuyiSiaMbJtq2x0K8w',
    },
    params,
  })

  characters.value = charactersRequest.data.docs
  toast.add({ title: 'Успех', description: 'Данные успешно получены', color: 'success' })
}
</script>
```

---

### Разбор использованных UI-компонентов

Ниже кратко описаны все компоненты из примера со ссылками на документацию.

### `UForm`
**Документация:** [UForm](https://ui.nuxt.com/docs/components/form)

Обёртка для формы, которая управляет состоянием полей и валидацией. Принимает:
- `state` — реактивный объект со значениями полей;
- `validate` — функция, возвращающая массив ошибок валидации;
- `@submit` — событие, вызываемое при успешной отправке (без ошибок).

### `UFormField`
**Документация:** [UFormField](https://ui.nuxt.com/docs/components/form-field)

Отдельное поле внутри формы. Связывает метку (`label`) и поле ввода через атрибут `name`. Помогает отображать сообщения об ошибках для конкретного поля.

### `USelect`
**Документация:** [USelect](https://ui.nuxt.com/docs/components/select)

Выпадающий список для выбора одного значения из набора. Принимает:
- `v-model` — текущее выбранное значение;
- `items` — массив объектов с `label` и `value`.

### `UButton`
**Документация:** [UButton](https://ui.nuxt.com/docs/components/button)

Кнопка с поддержкой множества стилей и состояний. В примере используется для отправки формы (`type="submit"`).

### `UTable`
**Документация:** [UTable](https://ui.nuxt.com/docs/components/table)

Таблица для отображения структурированных данных. Принимает:
- `data` — массив объектов с данными;
- `columns` — массив с описанием столбцов (ключ `accessorKey` и заголовок `header`).
Поддерживает кастомную отрисовку ячеек через функцию `cell`.

### `UBadge`
**Документация:** [UBadge](https://ui.nuxt.com/docs/components/badge)

Компонент для отображения статусов или небольших меток. Поддерживает цвета (`color`) и различные варианты внешнего вида. В примере используется внутри таблицы для визуализации значения «Умер?».

### `useToast` (уведомления)
**Документация:** [useToast](https://ui.nuxt.com/docs/components/toast)

Используется показа всплывающих уведомлений в правом нижнем углу. Вызов `toast.add({ title, description, color })` создаёт уведомление с заданными параметрами.

---

## Итоги

- UI-кит — это набор готовых компонентов, ускоряющих разработку интерфейсов.
- **Nuxt UI** — популярный UI-кит для Vue/Nuxt проектов, имеющий обширную документацию.
- Использование UI-кита требует постоянного обращения к документации и практики.
- Формы в Nuxt UI поддерживают встроенную валидацию через функцию `validate`.


## Домашнее задание

[Github с кодом занятия](https://github.com/VsevolodKozlov-git/vue-tutoring-demo-project)

1. Установите Nuxt UI в свой Vue-проект (или создайте новый проект с Nuxt UI).
2. Создайте форму и таблицу, аналогичную разобранной, но для создания продукта из прошлого домашнего задания
   1. Помимо компонент из урока вам потребуется [UInput](https://ui.nuxt.com/docs/components/input) 
3. Поэкспериментируйте с разными пропсами кнопок и полей ввода — попробуйте изменить цвета, размеры, добавить иконки.