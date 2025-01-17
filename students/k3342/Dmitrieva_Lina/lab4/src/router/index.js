import { createRouter, createWebHistory } from 'vue-router';

// Маршруты
const routes = [
  { path: "/", name: "Home", component: () => import("../views/HomePage.vue") },
  { path: "/newspapers", name: "Newspapers", component: () => import("../views/NewspapersPage.vue"), meta: { requiresAuth: true } },
  { path: "/printshops", name: "PrintShops", component: () => import("../views/PrintShopsPage.vue"), meta: { requiresAuth: true } },
  { path: "/deliveries", name: "Deliveries", component: () => import("../views/DeliveriesPage.vue"), meta: { requiresAuth: true } },
  { path: "/reports", name: "Reports", component: () => import("../views/ReportsPage.vue"), meta: { requiresAuth: true } },
  { path: "/login", name: "Login", component: () => import("../views/LoginPage.vue") },
  { path: "/employees", name: "Employees", component: () => import("../views/EmployeesPage.vue"), meta: { requiresAuth: true, role: ['admin'] } },
];

// Создание маршрутизатора
const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); // Проверяем, есть ли токен
  const userRole = localStorage.getItem('role'); // Получаем роль пользователя из localStorage

  // Проверка авторизации
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' }); // Перенаправление на страницу входа, если не авторизован
  } else if (to.meta.role && !to.meta.role.includes(userRole)) {
    // Если есть ограничение по роли и роль не совпадает, перенаправляем на главную страницу
    next({ name: 'Home' });
  } else {
    next(); // Разрешаем переход на страницу
  }
});

export default router;
