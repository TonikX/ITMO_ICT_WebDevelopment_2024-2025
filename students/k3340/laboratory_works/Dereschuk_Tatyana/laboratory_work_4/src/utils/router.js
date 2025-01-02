import {createRouter, createWebHistory} from "vue-router";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import {tokenStore} from "@/stores/token.js";
import MountainView from "@/views/mountain/MountainView.vue";
import AlpinistView from "@/views/alpinist/AlpinistView.vue";
import ReportView from "@/views/ReportView.vue";
import AlpinistDetailView from "@/views/alpinist/AlpinistDetailView.vue";
import MountainDetailView from "@/views/mountain/MountainDetailView.vue";
import AscendingView from "@/views/ascending/AscendingView.vue";
import AscendingDetailView from "@/views/ascending/AscendingDetailView.vue";


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
        path: '/mountains',
        component: MountainView
    },
    {
      path: '/mountains/:id',
      component: MountainDetailView
    },
    {
        path: '/alpinists',
        component: AlpinistView
    },
    {
        path: '/alpinists/:id',
        component: AlpinistDetailView
    },
    {
        path: '/ascendings',
        component: AscendingView
    },
    {
        path: '/ascendings/:id',
        component: AscendingDetailView
    },
    {
        path: '/reports',
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
