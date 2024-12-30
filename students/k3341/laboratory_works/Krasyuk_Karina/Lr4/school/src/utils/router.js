import {createRouter, createWebHistory} from "vue-router";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import {tokenStore} from "@/stores/token.js";
import TeacherView from "@/views/TeacherView.vue";
import StudentView from "@/views/StudentView.vue";
import ScheduleView from "@/views/ScheduleView.vue";
import RoomView from "@/views/RoomView.vue";
import ReportView from "@/views/ReportView.vue";


const routes = [
    {
        name: 'Login',
        path: '/login',
        component: LoginView
    },
    {
        name: 'Register',
        path: '/register',
        component: RegisterView
    },
    {
        path: '/teachers',
        component: TeacherView
    },
    {
        path: '/students',
        component: StudentView
    },
    {
        path: '/schedule',
        component: ScheduleView
    },
    {
        path: '/rooms',
        component: RoomView
    },
    {
        path: '/report',
        component: ReportView
    }
]

const router = createRouter({
    history: createWebHistory(), routes
})

export default router

router.beforeEach((to, from, next) => {
    const token = tokenStore().token;

    if (to.name !== 'Login' && to.name !== 'Register' && !token) {
        next({name: 'Login'});
    } else {
        next();
    }
});
