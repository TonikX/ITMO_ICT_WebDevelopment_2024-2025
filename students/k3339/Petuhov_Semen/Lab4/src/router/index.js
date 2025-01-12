import { createRouter, createWebHistory } from 'vue-router';
import AuthView from "@/views/SignUpView.vue";
import LoginView from "@/views/LoginView.vue"; // Добавили импорт нового компонента для страницы входа
import ManageFlights from "@/views/ManageFlights.vue"; // Новый компонент для управления рейсами
import AddFlight from "@/components/AddFlight.vue"; // Новый компонент для добавления рейса
import ManageCrews from "@/views/ManageCrew.vue";
import ManageAircrafts from '@/views/ManageAircrafts.vue';
import ManageSchedules from '@/views/ManageSchedules.vue';

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/signup', component: AuthView },
    { path: '/login', component: LoginView },
    { path: '/dashboard', component: () => import('@/views/AdminDashboard.vue') },
    { path: "/manage-flights", component: ManageFlights },
    { path: "/manage-crew", component: ManageCrews },
    { path: "/add-flight", component: AddFlight },
    { path: '/manage-aircrafts', component: ManageAircrafts, name: 'planes' },
    { path: '/manage-schedules', component: ManageSchedules, name: 'schedules' },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
