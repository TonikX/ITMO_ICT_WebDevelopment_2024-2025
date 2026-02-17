# Printing House Frontend (Vue.js 3 + TypeScript)

## Описание

Frontend приложение на Vue.js 3 с TypeScript для управления типографией. Взаимодействует с Go REST API через JWT аутентификацию.

## Технологии

- Vue.js 3 (Composition API)
- TypeScript
- Vuetify 3 (Material Design)
- Vite (сборщик)
- Pinia (state management)
- axios (HTTP клиент)
- Vue Router (маршрутизация)

## Структура проекта

```
frontend/
├── src/
│   ├── App.vue
│   ├── main.ts
│   ├── components/        # Переиспользуемые компоненты
│   ├── views/            # Страницы приложения
│   ├── services/         # API сервисы
│   ├── stores/           # Pinia хранилища
│   ├── types/            # TypeScript интерфейсы
│   ├── router/           # Vue Router
│   └── plugins/          # Плагины (Vuetify)
│
├── index.html
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## Компоненты

### Основные страницы (views/)
- Даш-борд - главная страница
- Газеты - управление газетами
- Типографии - управление типографиями
- Тиражи - управление тиражами
- Распределение - распределение газет

### Компоненты (components/)
- NewspaperList - таблица газет
- PrintingHouseList - таблица типографий
- PrintingRunForm - форма создания тиража
- DistributionForm - форма распределения

## API Сервисы

### Файл: services/api.ts

Настроен для работы с Go backend:

```typescript
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8080/api/v1'
});

// JWT Bearer токен автоматически добавляется
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication
export const login = (username: string, password: string) => 
  API.post('/auth/login', { username, password });

export const register = (username: string, email: string, password: string) => 
  API.post('/auth/register', { username, email, password });

export const getCurrentUser = () => 
  API.get('/auth/me');

// Newspapers
export const getNewspapers = () => 
  API.get('/newspapers');

export const createNewspaper = (data: any) => 
  API.post('/newspapers', data);

export const updateNewspaper = (id: number, data: any) => 
  API.put(`/newspapers/${id}`, data);

export const deleteNewspaper = (id: number) => 
  API.delete(`/newspapers/${id}`);

// Printing Houses
export const getPrintingHouses = () => 
  API.get('/printing-houses');

export const createPrintingHouse = (data: any) => 
  API.post('/printing-houses', data);

export const updatePrintingHouse = (id: number, data: any) => 
  API.put(`/printing-houses/${id}`, data);

export const deletePrintingHouse = (id: number) => 
  API.delete(`/printing-houses/${id}`);

// Post Offices
export const getPostOffices = () => 
  API.get('/post-offices');

export const createPostOffice = (data: any) => 
  API.post('/post-offices', data);

export const updatePostOffice = (id: number, data: any) => 
  API.put(`/post-offices/${id}`, data);

export const deletePostOffice = (id: number) => 
  API.delete(`/post-offices/${id}`);

// Distributions
export const getDistributions = () => 
  API.get('/distributions');

export const createDistribution = (data: any) => 
  API.post('/distributions', data);

export const updateDistribution = (id: number, data: any) => 
  API.put(`/distributions/${id}`, data);

export const deleteDistribution = (id: number) => 
  API.delete(`/distributions/${id}`);
```

## State Management (Pinia)

### Auth Store

```typescript
// stores/auth.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
import * as api from '@/services/api';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);
  const token = ref(localStorage.getItem('auth_token'));
  
  const login = async (username: string, password: string) => {
    const response = await api.login(username, password);
    token.value = response.data.token;
    user.value = response.data.user;
    localStorage.setItem('auth_token', response.data.token);
  };
  
  const logout = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem('auth_token');
  };
  
  const fetchCurrentUser = async () => {
    if (token.value) {
      const response = await api.getCurrentUser();
      user.value = response.data;
    }
  };
  
  return {
    user,
    token,
    login,
    logout,
    fetchCurrentUser,
    isAuthenticated: computed(() => !!token.value)
  };
});
```

### Printing Store

```typescript
// stores/printing.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
import * as api from '@/services/api';

export const usePrintingStore = defineStore('printing', () => {
  const newspapers = ref([]);
  const printingHouses = ref([]);
  const postOffices = ref([]);
  const distributions = ref([]);
  
  const fetchNewspapers = async () => {
    const res = await api.getNewspapers();
    newspapers.value = res.data;
  };
  
  const addNewspaper = async (data) => {
    await api.createNewspaper(data);
    await fetchNewspapers();
  };
  
  const fetchPrintingHouses = async () => {
    const res = await api.getPrintingHouses();
    printingHouses.value = res.data;
  };
  
  const fetchPostOffices = async () => {
    const res = await api.getPostOffices();
    postOffices.value = res.data;
  };
  
  const fetchDistributions = async () => {
    const res = await api.getDistributions();
    distributions.value = res.data;
  };
  
  return {
    newspapers,
    printingHouses,
    postOffices,
    distributions,
    fetchNewspapers,
    addNewspaper,
    fetchPrintingHouses,
    fetchPostOffices,
    fetchDistributions
  };
});
```

## Использование в компонентах

```vue
<script setup lang="ts">
import { onMounted } from 'vue';
import { usePrintingStore } from '@/stores/printing';

const store = usePrintingStore();

onMounted(() => {
  store.fetchNewspapers();
});
</script>

<template>
  <div>
    <h1>Газеты</h1>
    <div v-for="newspaper in store.newspapers" :key="newspaper.id">
      <p>{{ newspaper.title }}</p>
      <p>{{ newspaper.editor_last_name }} {{ newspaper.editor_first_name }}</p>
    </div>
  </div>
</template>
```

## Маршруты

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes = [
  {
    path: '/',
    component: HomeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    component: LoginView,
    meta: { guest: true }
  },
  {
    path: '/register',
    component: RegisterView,
    meta: { guest: true }
  },
  {
    path: '/profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/newspapers',
    component: NewspapersView,
    meta: { requiresAuth: true }
  },
  {
    path: '/printing-houses',
    component: PrintingHousesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/post-offices',
    component: PostOfficesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/printing-runs',
    component: PrintingRunsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/distributions',
    component: DistributionsView,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Защита маршрутов
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next('/');
  } else {
    next();
  }
});

export default router;
```

## UI с Vuetify 3

Компоненты используют:
- v-data-table - таблицы
- v-form - формы
- v-dialog - модальные окна
- v-card - карточки
- v-btn - кнопки
- v-text-field - текстовые поля
- v-select - селекты

## Запуск

```bash
cd frontend_go
npm install
npm run dev
```

Доступно: http://localhost:5173

**Быстрый запуск всего стека:**

Linux/Mac:
```bash
./start-fullstack.sh
```

Windows:
```cmd
start-fullstack.bat
```

## Сборка для продакшена

```bash
npm run build
```

Будет создана папка `dist/` с собранным приложением.

## Конфигурация Backend URL

Отредактируйте `src/services/api.ts` для изменения адреса backend:

```typescript
const API = axios.create({
  baseURL: 'http://localhost:8080/api/v1'  // Go backend
});
```

## TypeScript типы

```typescript
// types/index.ts
export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface Newspaper {
  id: number;
  title: string;
  publication_index: string;
  editor_first_name: string;
  editor_last_name: string;
  editor_middle_name?: string;
  price_per_copy: number;
}

export interface PrintingHouse {
  id: number;
  name: string;
  address: string;
  is_active: boolean;
}

export interface PostOffice {
  id: number;
  number: string;
  address: string;
}

export interface Distribution {
  id: number;
  post_office_id: number;
  newspaper_id: number;
  printing_house_id: number;
  quantity: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}
```

## Обработка ошибок

```typescript
try {
  await store.addNewspaper(formData);
  showSuccess('Газета успешно создана');
} catch (error) {
  showError('Ошибка при создании газеты');
  console.error(error);
}
```

## Адаптивность

Приложение полностью адаптивно с использованием Vuetify grid системы:
- Мобильные устройства
- Планшеты
- Десктопы

## Отличия от Python версии

| Аспект | Python Backend | Go Backend |
|--------|----------------|------------|
| API Base URL | `http://localhost:8000` | `http://localhost:8080/api/v1` |
| Auth Header | `Token <token>` | `Bearer <token>` |
| Login Response | `{ auth_token, user_id }` | `{ token, user }` |
| Endpoints | Trailing slash `/` | Без slash |
| Auth Type | Django Token | JWT Token |

## Тестовые пользователи

| Username | Email | Password |
|----------|-------|----------|
| admin | admin@printinghouse.local | password123 |
| testuser | test@printinghouse.local | password123 |

## Основные страницы

- **LoginView** - аутентификация пользователя
- **RegisterView** - регистрация нового пользователя
- **HomeView** - главная страница с dashboard
- **ProfileView** - профиль пользователя
- **NewspapersView** - управление газетами (CRUD)
- **PrintingHousesView** - управление типографиями (CRUD)
- **PostOfficesView** - управление почтовыми отделениями (CRUD)
- **PrintingRunsView** - управление тиражами
- **DistributionsView** - управление распределениями (CRUD)

Дополнительно: [Вернуться к обзору Lr4](index.md)
