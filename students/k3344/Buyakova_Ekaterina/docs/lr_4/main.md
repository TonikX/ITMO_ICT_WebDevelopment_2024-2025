# Отчет по лабораторной работе №4

## Цель работы
Реализовать клиентскую часть средствами Vue.js.

## Задача лабораторной работы
Реализовать интерфейсы авторизации, регистрации и изменения учётных данных и настроить взаимодействие с серверной частью. Реализовать клиентские интерфейсы и настроить взаимодействие с серверной частью. Подключить vuetify или аналогичную библиотеку.

## Описание работы разработанных интерфейсов

### Папка components
В папке components содержатся компоненты Vue.js, использующие Vuetify для создания интерфейсов. Есть футер для приложения, содержащий ссылки на ресурсы, которые связаны с Vuetify. Есть компонент для регистрации, авторизации, домашняя страница.

### Папка models
Папка содержит интерфейсы, которые могут использоваться для представления данных в системе управления гостиницей, включая модули бронирование, управление клиентами, расписание уборок и мониторинг номеров.
Модель для представления расписания уборок (cleaning-schedule.ts):
```typescript
export default interface CleaningSchedule {
  id: number,
  staff_name: string,
  floor: number,
  day_of_week: string,
  staff: number,
  client: number
}
```
Поля:
- id (number): Уникальный идентификатор записи расписания
- staff_name (string): имя сотрудника, ответственного за уборку
- floor (number): этаж, где выполняется уборка
- day_of_week (string): день недели для уборки
- staff (number): ID сотрудника
- client (number): ID клиента (если применимо)

### Папка plugins
1. ***axios.ts*** - конфигурация клиента Axios для работы с API:
```typescript
import axios from 'axios';

const axiosApi = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  withCredentials: true,
});

axiosApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default axiosApi;
```
- baseURL: указывает базовый URL API
- withCredentials: включает отправку cookies с запросами
- interceptors.request: добавляет токен авторизации из localStorage в заголовки каждого запроса

2. ***index.ts*** - регистрация плагинов для Vue приложения:
```typescript
import vuetify from './vuetify'
import pinia from '../stores'
import router from '../router'

// Types
import type { App } from 'vue'

export function registerPlugins (app: App) {
  app
    .use(vuetify)
    .use(router)
    .use(pinia)
}
```
- Функция registerPlugins регистрирует ключевые плагины
- vuetify: для UI компонентов
- router: для маршрутизации
- pinia: для управления состоянием

3. ***vuetify.ts*** - настройка Vuetify для использования в проекте:
```typescript
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';

// Composables
import { createVuetify } from 'vuetify';

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'dark',
  },
});
```
- Подключение стилей
- Material Design Icons: @mdi/font/css/materialdesignicons.css
- Стили Vuetify: vuetify/styles
- createVuetify: создание экземпляра Vuetify с темой по умолчанию (dark)

### Папка router
Файл используется для настройки маршрутов в приложении Vue.js при помощи библиотеки vue-router.
```typescript
import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/components/LoginPage.vue';
import RegisterPage from '@/components/RegisterPage.vue';
import HomePage from '@/components/HomePage.vue';
import StaffPage from '@/components/StaffPage.vue';
import ClientsPage from '@/components/ClientsPage.vue';
import RoomsPage from '@/components/RoomsPage.vue';
import RoomInfoPage from '@/components/RoomInfoPage.vue';
import CleaningSchedule from '@/components/CleaningSchedule.vue';
import HotelReportPage from '@/components/HotelReportPage.vue';
import ReservationPage from '@/components/ReservationPage.vue';

const routes = [
  { path: "/", component: HomePage, name: "Home" },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/staff', name: 'Staff', component: StaffPage },
  { path: '/clients', name: 'Clients', component: ClientsPage },
  { path: '/rooms', name: 'Rooms', component: RoomsPage },
  { path: '/rooms/:roomId', name: 'RoomInfo', component: RoomInfoPage, props: true},
  { path: '/cleaning-schedule', name: 'CleaningSchedule', component: CleaningSchedule},
  { path: '/report', name: 'ReportPage', component: HotelReportPage},
  { path: '/reservations', name: 'ReservationPage', component: ReservationPage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
```
Список маршрутов задаётся в массиве routes. Каждый маршрут имеет следующие свойства:
- path: URL-адрес маршрута
- name: уникальное имя маршрута
- component: компонент, который будет отображаться при переходе по маршруту
- props (опционально): передача параметров маршрута как пропсов в компонент
 
### App.vue
Корневой компонент приложения,который подключает глобальные стили и структуру через Vuetify (v-app, v-main).
Он управляет маршрутизацией с помощью компонента router-view, который динамически отображает активный компонент на основе маршрута.

### main.ts
Главный файл, который инициализирует Vue.js приложение. В нём подключаются плагины, маршруты и корневой компонент, а затем приложение монтируется в DOM.
1. Создание и настройка приложения:
```typescript
const app = createApp(App)
```
Создаётся экземпляр приложения на основе корневого компонента App.vue
2. Подключение маршрутов и плагинов:
```typescript
app.use(router)
registerPlugins(app)
```
app.use(router): Подключает маршрутизацию для управления переходами между страницами.
registerPlugins(app): Подключает зарегистрированные плагины, такие как Vuetify, Pinia и другие.
3. Монтаж приложения
```typescript
app.mount('#app')
```
Приложение монтируется в DOM-элемент с id="app", который обычно объявляется в файле index.html.
