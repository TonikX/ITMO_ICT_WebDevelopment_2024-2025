# Фронтенд: архитектура и работа

## Общее описание

Фронтенд реализован на **Vue 3 (Composition API)** с использованием **Vuetify** и взаимодействует с Django REST API через **Axios**. Это SPA (single-page application): переходы между страницами происходят без перезагрузки, данные подтягиваются по API.

---

## Структура фронтенд-проекта

```
hotel-frontend/
├── src/
│   ├── views/              # Страницы (экраны)
│   │   ├── LoginView.vue   # Авторизация
│   │   ├── RoomsView.vue   # Управление номерами
│   │   ├── ClientsView.vue # Управление клиентами
│   │   └── StaysView.vue   # Проживания
│   ├── services/
│   │   └── api.js          # Обёртка над Axios для запросов к Django
│   ├── router/
│   │   └── index.ts        # Маршруты (Vue Router)
│   ├── plugins/
│   │   └── vuetify.js      # Настройки Vuetify
│   ├── App.vue             # Корневой компонент приложения
│   └── main.js             # Точка входа (инициализация Vue)
├── package.json
└── vite.config.js
```

Основная логика UI разбита по `views/*.vue`, каждый файл — отдельная страница, которая работает как самостоятельный компонент.

---

## Взаимодействие с API (api.js)

Для работы с Django REST API используется отдельный модуль `src/services/api.js`. В нём создаётся экземпляр Axios с базовым URL и перехватчиком для токена:

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
})

// Перехватчик: добавляет токен ко всем запросам
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default {
  login(data) {
    return api.post('token/login/', data)
  },
  getRooms() {
    return api.get('rooms/')
  },
  createRoom(data) {
    return api.post('rooms/', data)
  },
  getClients() {
    return api.get('clients/')
  },
  createClient(data) {
    return api.post('clients/', data)
  },
  getStays() {
    return api.get('stays/')
  },
  createStay(data) {
    return api.post('stays/', data)
  },
}
```

Все компоненты используют этот модуль, чтобы не дублировать URL и логику добавления токена.

---

## Маршрутизация (router/index.ts)

За навигацию отвечает Vue Router. Каждая страница привязана к URL:

```typescript
import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import RoomsView from '@/views/RoomsView.vue'
import ClientsView from '@/views/ClientsView.vue'
import StaysView from '@/views/StaysView.vue'

const routes = [
  { path: '/login', component: LoginView },
  { path: '/rooms', component: RoomsView },
  { path: '/clients', component: ClientsView },
  { path: '/stays', component: StaysView },
  { path: '/', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
```

Переход между страницами:

- Декларативно: `<v-btn to="/rooms">Номера</v-btn>`
- Программно: `router.push('/rooms')`

---

## Реактивность и структура компонента

Компоненты используют Composition API: `ref`, `computed`, `onMounted`.

Пример (упрощённый вариант `RoomsView.vue`):

```vue
<template>
  <v-container>
    <h1>Номера</h1>

    <v-btn color="primary" @click="dialogCreate = true">
      Добавить номер
    </v-btn>

    <v-data-table
      :headers="headers"
      :items="rooms"
      :loading="loading"
    />

    <v-dialog v-model="dialogCreate" max-width="500">
      <v-card>
        <v-card-title>Новый номер</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="newRoom.number" label="Номер" />
            <v-text-field v-model="newRoom.floor" label="Этаж" />
            <v-text-field v-model="newRoom.type" label="Тип" />
            <v-text-field v-model="newRoom.price_per_day" label="Цена за день" />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="createRoom">Создать</v-btn>
          <v-btn @click="dialogCreate = false">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const rooms = ref([])
const loading = ref(false)
const dialogCreate = ref(false)

const newRoom = ref({
  number: '',
  floor: '',
  type: '',
  price_per_day: '',
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Номер', key: 'number' },
  { title: 'Этаж', key: 'floor' },
  { title: 'Тип', key: 'type' },
  { title: 'Цена за день', key: 'price_per_day' },
]

const loadRooms = async () => {
  loading.value = true
  try {
    const response = await api.getRooms()
    rooms.value = response.data
  } finally {
    loading.value = false
  }
}

const createRoom = async () => {
  await api.createRoom({
    number: Number(newRoom.value.number),
    floor: Number(newRoom.value.floor),
    type: newRoom.value.type,
    price_per_day: Number(newRoom.value.price_per_day),
  })
  dialogCreate.value = false
  newRoom.value = { number: '', floor: '', type: '', price_per_day: '' }
  loadRooms()
}

onMounted(() => {
  loadRooms()
})
</script>
```

Ключевые моменты:

- `ref()` делает переменные реактивными.
- `onMounted()` используется для загрузки данных при открытии страницы.
- `v-model` связывает поля формы с объектами `newRoom`, `newClient`, `newStay`.
- После успешного создания сущности вызывается повторная загрузка списка.

---

## Страница авторизации (LoginView.vue)

Авторизация реализована через Django Djoser и токены. Фронтенд:

```vue
<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Вход</v-card-title>
          <v-card-text>
            <v-form>
              <v-text-field v-model="username" label="Логин" />
              <v-text-field v-model="password" label="Пароль" type="password" />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="handleLogin">Войти</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const username = ref('')
const password = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const response = await api.login({
      username: username.value,
      password: password.value,
    })
    localStorage.setItem('token', response.data.auth_token)
    router.push('/rooms')
  } catch (error) {
    alert('Неверный логин или пароль')
  }
}
</script>
```

После успешного логина токен сохраняется в `localStorage` и автоматически подставляется в заголовки всех запросов.

---

## Страница проживаний (StaysView.vue)

На этой странице отображаются и создаются записи о проживании. Используются связанные данные: клиенты и номера.

Основные моменты:

- При открытии диалога создаются запросы на загрузку списков `clients` и `rooms`.
- В форме используются `v-select` для выбора клиента и номера по их ID.
- Во время POST-запроса на создание проживания на фронте ID конвертируются в числа, а на бэке сериализатор связывает их с объектами через `PrimaryKeyRelatedField`.
- Для отображения в таблице используется сериализатор с кастомным `to_representation`, который отдаёт, например, `client_name` и `room_number`, чтобы во Vue не приходилось разбирать вложенный JSON.

---

## Использование Vuetify

Vuetify даёт готовые компоненты:

- `v-container`, `v-row`, `v-col` — сетка
- `v-btn` — кнопки
- `v-text-field` — текстовые поля
- `v-select` — выпадающие списки
- `v-dialog` — диалоги
- `v-data-table` — таблицы с сортировкой/загрузкой

Пример таблицы:

```vue
<v-data-table
  :headers="headers"
  :items="stays"
  :loading="loading"
/>
```

Если для сложных полей (например, объект клиента) нужен особый вывод, используются слоты:

```vue
<template v-slot:item.client="{ item }">
  {{ item.client_name }}
</template>
```

---

## Поток данных (пример создания проживания)

1. Пользователь открывает `/stays` → компонент `StaysView` монтируется.
2. Вызывается `loadStays()` → GET `/api/v1/stays/` → заполняется `stays`.
3. Пользователь нажимает «Добавить проживание» → открывается диалог, вызываются `loadClients()` и `loadRooms()`.
4. Пользователь выбирает клиента и номер, указывает даты → `v-model` заполняет `newStay`.
5. Нажатие «Создать» вызывает `createStay()` → POST `/api/v1/stays/` с ID клиента и комнаты.
6. Django сохраняет запись и возвращает JSON.
7. Фронтенд закрывает диалог, очищает форму и повторно вызывает `loadStays()`.
8. Таблица автоматически обновляется за счёт реактивности (`stays.value = response.data`).

---

## Кратко о ключевых паттернах

- Все запросы к API вынесены в один модуль (`api.js`).
- Токен авторизации хранится в `localStorage` и подставляется перехватчиком.
- Данные хранятся в `ref()` и обновляют UI при изменении.
- Каждая страница — отдельный `.vue` компонент в `views/`.
- Маршруты определяются в одном месте (`router/index.ts`).
- Для удобства работы с вложенными данными (клиент, номер) используется `to_representation` на стороне Django.
