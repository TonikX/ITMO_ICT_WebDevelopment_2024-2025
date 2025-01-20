import {createRouter, createWebHistory} from "vue-router";
import RegistrationForm from "@/components/auth/RegistrationForm.vue";
import LoginForm from "@/components/auth/LoginForm.vue";
import Home from "@/components/Home.vue";
import {useAuthStore} from "@/stores/auth.js";
import MovieManager from "@/components/movie/MovieManager.vue";
import HallManager from "@/components/hall/HallManager.vue";
import SessionManager from "@/components/session/SessionManager.vue";
import SessionBoard from "@/components/session/SessionBoard.vue";
import TicketCreation from "@/components/ticket/TicketCreation.vue";
import UserTickets from "@/components/ticket/UserTickets.vue";

const routes = [
    {
        path: "/register",
        name: "Register",
        component: RegistrationForm,
    },
    {
        path: "/login",
        name: "Login",
        component: LoginForm,
    },
    {
        path: "/",
        name: "Home",
        component: Home,
        meta: {requiresAuth: true},
    },
    {
        path: "/movies",
        name: "Movies",
        component: MovieManager,
        meta: {requiresAuth: true},
    },
    {
        path: "/halls",
        name: "Halls",
        component: HallManager,
        meta: {requiresAuth: true},
    },
    {
        path: "/sessions",
        name: "Sessions",
        component: SessionManager,
        meta: {requiresAuth: true},
    },
    {
        path: "/session-board",
        name: "Session Board",
        component: SessionBoard,
        meta: {requiresAuth: true},
    },
    {
        path: '/sessions/:sessionId/buy',
        name: 'TicketCreation',
        component: TicketCreation,
        props: true,
    },
    {
        path: '/tickets',
        name: 'UserTickets',
        component: UserTickets,
        props: true,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore();

    if (!authStore.user && authStore.accessToken) {
        await authStore.fetchUser();
    }

    if (to.meta.requiresAuth && !authStore.accessToken) {
        next('/login');
    } else {
        next();
    }
});
export default router;
