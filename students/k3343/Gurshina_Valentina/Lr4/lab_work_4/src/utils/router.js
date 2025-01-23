import {createRouter, createWebHistory} from "vue-router";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import ClientView from "@/views/ClientView.vue";
import ScheduleView from "@/views/ScheduleView.vue";
import EmployeeView from "@/views/EmployeeView.vue";
import RoomView from "@/views/RoomView.vue";
import ReportView from "@/views/ReportView.vue";
import ProfileView from "@/views/ProfileView.vue";
import RoomDetail from "@/views/RoomDetailView.vue";
import BookingView from "@/views/BookingView.vue";
import {tokenStore} from "@/stores/token.js";


const routes = [
    {
        name: 'Login',
        path: '/auth/token/login/',
        component: LoginView
    },
    {
        name: 'Register',
        path: '',
        component: RegisterView
    },
    {
        path: '/clients',
        component: ClientView
    },
    {
        path: '/schedule',
        component: ScheduleView
    },
    {
        path: '/employees',
        component: EmployeeView
    },
    {
        path: '/rooms',
        component: RoomView
    },
    {
        path: '/rooms/:id',
        component: RoomDetail
    },
    {
        path: '/reservations',
        component: BookingView
    },
    {
        path: '/report',
        component: ReportView
    },
    {
        path: '/profile',
        component: ProfileView
    }
]

const router = createRouter({
    history: createWebHistory(), routes
})

export default router

router.beforeEach((to, from, next) => {
    const token = tokenStore().token;

    if (to.name !== 'Login' && to.name !== 'Register' && !token) {
        next({ name: 'Login' });
    } else {
        next();
    }
});
