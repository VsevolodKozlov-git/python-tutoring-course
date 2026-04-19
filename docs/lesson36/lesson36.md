# Урок 36. Основы CSS: часть 2

## Повторяем ДЗ



#### Отличается ли чем-то запись в одну строчку css-свойств от нескольких css-свойств?

#### В чем разница между padding и margin?

#### Что обозначает 4 подряд перечисленных значения для padding?

#### В чем разница между border-box и content-box?

#### flex-box
- Какая ось будет главной, а какая второстепенной при `flex-direction:row`?
- Как будут выравнены элементы при `flex-direction:row` и `justify-content: center`?
- Что делают flex-grow и flex-shrink?



#### Относительные и абсолютные величины
- Зачем использовать относительные величины, а не абсолютные в css?
- Чем rem отличается от em?
- Относительно чего работают проценты в css?

Фокусы с rem:
```css
html {
  /* 10px */
  font-size: 62.5%;
}

.title-block {
  /* 10rem * 10px = 100px */
  width: 10rem;
  /* 2rem * 10px = 20px */
  font-size: 2rem;
}

@media (max-width: 640px) {
  html {
    /* 8px */
    font-size: 50%;
  }
}
```


#### Медиа-запросы

- Зачем нужны медиа-запросы?
- Что означает `max-width` и `min-width` в медиа запросе?
- Есть ли разница между 
```css
	@media (max-width: 1000px) {
		.flex {
			background-color: red;
		}
	}
```

и 
```css
.flex {
	@media (max-width: 1000px) {
		background-color: red;
	}
}
```

#### Зачем нужны переменные в css?

#### Позиционирование

- чем `absolute` отличается от `relative`?
- чем `fixed` отличается от `absolute`?
