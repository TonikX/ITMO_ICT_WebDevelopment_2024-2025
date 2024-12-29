import {createRouter, createWebHistory} from "vue-router";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import {tokenStore} from "@/stores/token.js";
import AgencyView from "@/views/agency/AgencyView.vue";
import BrokerOrdersView from "@/views/broker/BrokerOrdersView.vue";
import ProductsView from "@/views/products/ProductsView.vue";
import ProductsDetailView from "@/views/products/ProductsDetailView.vue";
import BrokerStatisticsView from "@/views/broker/BrokerStatisticsView.vue";
import BrokerOrderDetailView from "@/views/broker/BrokerOrderDetailView.vue";
import AgencyDetailView from "@/views/agency/AgencyDetailView.vue";
import ManufacturerView from "@/views/manufacturer/ManufacturerView.vue";
import ManufacturerDetailView from "@/views/manufacturer/ManufacturerDetailView.vue";


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
        path: '/agency',
        component: AgencyView
    },
    {
        path: '/manufacturers',
        component: ManufacturerView
    },
    {
        path: '/manufacturers/:id',
        component: ManufacturerDetailView
    },
    {
        path: '/agency/:id',
        component: AgencyDetailView
    },
    {
        path: '/orders',
        component: BrokerOrdersView
    },
    {
        path: '/orders/:id',
        component: BrokerOrderDetailView
    },
    {
        path: '/products',
        component: ProductsView
    },
    {
        path: '/products/:id',
        component: ProductsDetailView
    },
    {
        path: '/statistics',
        component: BrokerStatisticsView
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
