import { createRouter, createWebHistory } from 'vue-router'

// Импортируем все страницы (компоненты-представления)
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Dashboard from './views/Dashboard.vue'
import Books from './views/Books.vue'
import Readers from './views/Readers.vue'
import Borrowings from './views/Borrowings.vue'
import Rooms from './views/Rooms.vue'


// ============================================================
// МАРШРУТЫ ПРИЛОЖЕНИЯ
//
// Каждый маршрут — это объект с:
//   path      — URL в браузере (например, /books)
//   component — какой Vue-компонент загрузить
//   meta      — дополнительные данные (например, requiresAuth)
// ============================================================

const routes = [
  // Корневой путь — перенаправляет на страницу входа
  { path: '/', redirect: '/login' },

  // Страница входа — доступна без авторизации
  { path: '/login', component: Login },

  // Страница регистрации — доступна без авторизации
  { path: '/register', component: Register },

  // Главная страница (дашборд) — требует авторизации
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },

  // Страница книг — требует авторизации
  { path: '/books', component: Books, meta: { requiresAuth: true } },

  // Страница читателей — требует авторизации
  { path: '/readers', component: Readers, meta: { requiresAuth: true } },

  // Страница выдачи книг — требует авторизации
  { path: '/borrowings', component: Borrowings, meta: { requiresAuth: true } },

  // Страница читальных залов — требует авторизации
  { path: '/rooms', component: Rooms, meta: { requiresAuth: true } },
]

// Создаём роутер с историей на основе HTML5 History API
// (createWebHistory — красивые URL без символа #)
const router = createRouter({
  history: createWebHistory(),
  routes,
})


// ============================================================
// НАВИГАЦИОННЫЙ GUARD — защита маршрутов
//
// Вызывается перед каждым переходом на новую страницу.
// Если страница требует авторизации (requiresAuth: true),
// но токена нет → редирект на /login.
// ============================================================

router.beforeEach((to, _from, next) => {
  // Проверяем: есть ли токен в localStorage
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    // Нет токена — отправляем на страницу входа
    next('/login')
  } else {
    // Токен есть — разрешаем переход
    next()
  }
})

export default router
