import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import DriversView from '@/views/DriversView.vue';
import RoutesView from '@/views/RoutesView.vue';
import BusesView from '@/views/BusesView.vue';
import ScheduleView from '@/views/ScheduleView.vue';
import ReportsView from '@/views/ReportsView.vue';
import AuthorizationView from '@/views/AuthorizationView.vue'; // Импортируем AuthorizationView

const routes = [
  { path: '/', component: HomeView },
  { path: '/drivers', component: DriversView },
  { path: '/routes', component: RoutesView },
  { path: '/buses', component: BusesView },
  { path: '/schedule', component: ScheduleView },
  { path: '/reports', component: ReportsView },
  { path: '/login', component: AuthorizationView }, // Путь для страницы входа
  { path: '/register', component: AuthorizationView }, // Путь для страницы регистрации
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
