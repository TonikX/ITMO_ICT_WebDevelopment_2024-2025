import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/Home.vue'
import {IsAuthenticated} from "@/composables/token.js";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: "/register", name: "Register", component: () => import('../views/Register.vue'),
            beforeEnter: (to, from, next) => {
                IsAuthenticated.value ? next('/') : next();
            },
        },
        {
            path: "/login",
            name: "Login",
            component: () => import('../views/Login.vue'),
            beforeEnter: (to, from, next) => {
                IsAuthenticated.value ? next('/') : next();
            },
        },
        {
            path: '/tenant',
            name: 'Tenant menu',
            component: () => import('../views/TenantMenu.vue'),
        },
        {
            path: '/tenant/:propId',
            name: 'PropertyInfo',
            component: () => import('../views/PropertyDetails.vue'),
        },
        {
            path: '/tenant/history',
            name: 'Lease History',
            component: () => import('../views/LeaseHistory.vue'),
        },
        {
            path: '/tenant/history/:rentId',
            name: 'Lease details',
            component: () => import('../views/LeaseDetails.vue'),
        },
        {
            path: '/landlord/me',
            name: 'Your info',
            component: () => import('../views/MyLandlordInfo.vue'),
        },
        {
            path: '/landlord/me/:landId/edit',
            name: 'edit your property',
            component: () => import('../views/EditProperty.vue'),
        },
        {
            path: '/landlord/me/:landId/delete',
            name: 'delete your property',
            component: () => import('../views/DeleteProperty.vue'),
        },
        {
            path: '/landlord/register',
            name: 'Create new property',
            component: () => import('../views/CreateProperty.vue'),
        },
        {
            path: '/landlord/:landId',
            name: 'Landlord info',
            component: () => import('../views/LandlordInfo.vue'),
        },
        {
            path: '/landlord/archive',
            name: 'Your archive',
            component: () => import('../views/LandlordArchive.vue'),
        },

        {
            path: '/:pathMatch(.*)*', name:
                'NotFound', component:
                () => import('../views/NotFound.vue')
        },
    ],
})
// TODO add property crud

export default router
