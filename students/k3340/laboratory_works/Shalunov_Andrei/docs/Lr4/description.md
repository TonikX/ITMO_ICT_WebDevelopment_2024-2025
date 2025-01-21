# Отчет по лабораторной работе №4

## **Тема**: Реализация клиентской части приложения средствами Vue.js

## **Цель работы**: 
Разработать клиентскую часть веб-приложения для взаимодействия с серверной частью, реализованной на Django REST Framework, используя Vue.js.

## **Ход работы**

## ** Реализация компонентов**

### ** Основные компоненты**

#### **Login.vue**
- **Назначение**: Позволяет пользователю авторизоваться в системе.
- **Логика обработки**:
  1. Отправляет `POST`-запрос на `/auth/token/login/` с введенными данными.
  2. Сохраняет токен авторизации в `localStorage` и Vuex.
  3. Перенаправляет пользователя на главную страницу.

#### **Register.vue**
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


- **Особенности**:
  - Компоненты разработаны с использованием библиотеки Vuetify для стилизации и адаптивности.
  - Легко переиспользуемая структура для отображения данных с сервера.

### Маршрутизация

Реализован файл `router/index.js` для настройки маршрутов в приложении:

```javascript
import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import Profile from '@/views/Profile.vue';
import Contracts from '@/views/Contracts.vue';
import CreateContract from '@/views/CreateContract.vue';
import EditContract from '@/views/EditContract.vue';
import ContractDetails from '@/views/ContractDetails.vue';
import Cars from '@/views/Cars.vue';
import CarDetails from '@/views/CarDetails.vue';
import CreateCar from '@/views/CreateCar.vue';
import EditCar from '@/views/EditCar.vue';
import Clients from '@/views/Clients.vue';
import CreateClient from '@/views/CreateClient.vue';
import EditClient from '@/views/EditClient.vue';
import ClientDetails from '@/views/ClientDetails.vue';
import Employees from '@/views/Employees.vue';
import EmployeeDetails from '@/views/EmployeeDetails.vue';
import EditEmployee from '@/views/EditEmployee.vue';
import CreateEmployee from '@/views/CreateEmployee.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/register', name: 'Register', component: Register },
  { path: '/login', name: 'Login', component: Login },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/contracts', name: 'Contracts', component: Contracts },
  { path: '/contracts/create', name: 'CreateContract', component: CreateContract },
  { path: '/contracts/:id/edit', name: 'EditContract', component: EditContract, props: true },
  { path: '/contracts/:id', name: 'ContractDetails', component: ContractDetails, props: true },
  { path: '/cars', name: 'Cars', component: Cars },
  { path: '/cars/:id', name: 'CarDetails', component: CarDetails, props: true },
  { path: '/cars/create', name: 'CreateCar', component: CreateCar },
  { path: '/cars/edit/:id', name: 'EditCar', component: EditCar },
  { path: '/clients', name: 'Clients', component: Clients },
  { path: '/clients/create', name: 'CreateClient', component: CreateClient },
  { path: '/clients/edit/:id', name: 'EditClient', component: EditClient, props: true },
  { path: '/clients/:id', name: 'ClientDetails', component: ClientDetails, props: true },
  { path: '/employees', name: 'Employees', component: Employees },
  { path: '/employees/:id', name: 'EmployeeDetails', component: EmployeeDetails, props: true },
  { path: '/employees/create', name: 'CreateEmployee', component: CreateEmployee },
  { path: '/employees/edit/:id', name: 'EditEmployee', component: EditEmployee, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
```


### Настройка авторизации 

В папке `composables` созданы вспомогательные файлы для обработки авторизации.

Файл `token.js`:
Хранение токена авторизации.
Проверка, авторизован ли пользователь.

```javascript
import {ref, computed} from 'vue';

export const TokenRef = ref(localStorage.getItem('AuthToken'));

export const IsAuthenticated = computed(() => !!TokenRef.value);

export const SetAuthToken = (token) => {
    TokenRef.value = token;
    localStorage.setItem('AuthToken', token);
};

export const ClearAuthToken = () => {
    TokenRef.value = null;
    localStorage.removeItem('AuthToken');
};
```

Файл `AxiosInstance.js`:
Настроены перехватчики для автоматического добавления токена в запросы:
```javascript
import axios from "axios";

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    timeout: 5000,
});

export default instance
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