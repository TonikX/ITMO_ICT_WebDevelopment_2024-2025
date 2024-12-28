import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import {isAuthenticated} from "@/composables/useAuth.js";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {path: '/', name: 'home', component: HomeView},
        {
            path: '/about', name: 'about', component: () => import('../views/AboutView.vue'),
        },
        {
            path: "/register", name: "Register", component: import('../views/RegisterView.vue'),
            beforeEnter: (to, from, next) => {
                isAuthenticated.value ? next('/') : next();
            },
        },
        {
            path: "/login", name:
                "Login", component:
                import('../views/LoginView.vue'),
            beforeEnter: (to, from, next) => {
                isAuthenticated.value ? next('/') : next();
            },
        },
        {
            path: '/recipe/:recipeId',
            name: 'recipe info',
            component: import('../views/RecipePage.vue'),
            props: true
        },

        // 404 not found
        {
            path: '/:pathMatch(.*)*', name:
                'NotFound', component:
                import('../views/NotFound.vue')
        },
    ],
})
// TODO create recipe view (read, comment if authenticated)
// TODO account management: publish new recipes
// TODO local storage favorites? 
export default router
