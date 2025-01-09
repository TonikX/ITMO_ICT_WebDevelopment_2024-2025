# Отчет по лабораторной работе №4

## **Тема**: Реализация клиентской части приложения средствами Vue.js

## **Цель работы**: 
Разработать клиентскую часть веб-приложения для взаимодействия с серверной частью, реализованной на Django REST Framework, используя Vue.js.

## **Ход работы**

## ** Реализация компонентов**

### ** Основные компоненты**

#### **LoginView.vue**
- **Назначение**: Позволяет пользователю авторизоваться в системе.
- **Логика обработки**:
  1. Отправляет `POST`-запрос на `/auth/token/login/` с введенными данными.
  2. Сохраняет токен авторизации в `localStorage` и Vuex.
  3. Перенаправляет пользователя на главную страницу.

#### **RegisterView.vue**
- **Назначение**: Позволяет зарегистрировать нового пользователя.
- **Логика обработки**:
  1. Проверяет, совпадают ли введенные пароли.
  2. Отправляет `POST`-запрос на `/auth/users/` с данными регистрации.
  3. При успешной регистрации перенаправляет пользователя на страницу входа.

---

### ** Другие компоненты **
- **Назначение**: Отображение различных сущностей приложения:
  - Клиенты.
  - Сотрудники.
  - Автомобили.
  - Контракты.
  - Услуги.

- **Особенности**:
  - Компоненты разработаны с использованием библиотеки Vuetify для стилизации и адаптивности.
  - Легко переиспользуемая структура для отображения данных с сервера.

### Маршрутизация

Реализован файл `router/index.js` для настройки маршрутов в приложении:

```javascript
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import { isAuthenticated } from '@/composables/useAuth.js';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        // Главная страница
        { path: '/', name: 'Home', component: HomeView },
        
        // Страница входа
        {
            path: '/login',
            name: 'Login',
            component: () => import('../views/LoginView.vue'),
            beforeEnter: (to, from, next) => {
                isAuthenticated.value ? next('/') : next();
            },
        },
        
        // Страница регистрации
        {
            path: '/register',
            name: 'Register',
            component: () => import('../views/RegisterView.vue'),
            beforeEnter: (to, from, next) => {
                isAuthenticated.value ? next('/') : next();
            },
        },
    ],
});

export default router;
```


### Настройка авторизации 

В папке `composables` созданы вспомогательные файлы для обработки авторизации.

Файл `useAuth.js`:
Хранение токена авторизации.
Проверка, авторизован ли пользователь.

```javascript
import { ref, computed } from 'vue';

export const authToken = ref(localStorage.getItem('authToken'));
export const isAuthenticated = computed(() => !!authToken.value);

export const setAuthToken = (token) => {
    authToken.value = token;
    localStorage.setItem('authToken', token);
};

export const clearAuthToken = () => {
    authToken.value = null;
    localStorage.removeItem('authToken');
};

```

Файл `axios.js`:
Настроены перехватчики для автоматического добавления токена в запросы:
```javascript
import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

axiosInstance.interceptors.request.use((config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

export default axiosInstance;
```

### Интеграция с серверной частью 
Настройка CORS в Django (`settings.py`):
Для обеспечения работы приложения на разных источниках (клиентская и серверная части):

```python
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOW_ALL_ORIGINS = True
```

## Вывод
В ходе лабораторной работы была разработана клиентская часть приложения для автосервиса. Приложение поддерживает регистрацию и авторизацию пользователей, а также взаимодействует с серверной частью на Django REST Framework.