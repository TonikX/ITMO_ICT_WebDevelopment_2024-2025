import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import {isAuthenticated} from "@/composables/useAuth.js";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {path: '/', name: 'home', component: HomeView},
        {
            path: "/register", name: "Register", component: () => import('../views/RegisterView.vue'),
            beforeEnter: (to, from, next) => {
                isAuthenticated.value ? next('/') : next();
            },
        },
        {
            path: "/login",
            name: "Login",
            component: () => import('../views/LoginView.vue'),
            beforeEnter: (to, from, next) => {
                isAuthenticated.value ? next('/') : next();
            },
        },
        {
            path: '/recipe/:recipeId/edit',
            name: 'edit Recipe',
            component: () => import('../views/EditRecipeView.vue'),
        },
        {
            path: '/recipe/:recipeId/delete',
            name: 'Delete recipe',
            component: () => import('../views/DeleteRecipeView.vue')
        },
        {
            path: '/recipe/create',
            name: 'Create recipe',
            component: () => import('../views/CreateRecipe.vue')
        },
        {
            path: '/recipe',
            name: 'Recipe',
            component: () => import('../views/AllRecipesView.vue')
        },
        {
            path: '/recipe/:recipeId',
            name: 'recipe info',
            component: () => import('../views/RecipePage.vue'),
            props: true
        },
        {
            path: '/favorite',
            name: 'Favorites',
            component: () => import('../views/FavoritesView.vue'),
            beforeEnter: (to, from, next) => {
                !isAuthenticated.value ? next('/') : next();
            }
        },
        {
            path: '/account',
            name: 'account',
            component: () => import('../views/AccountView.vue'),
            beforeEnter: (to, from, next) => {
                !isAuthenticated.value ? next('/') : next();
            }
        },

        // 404 not found
        {
            path: '/:pathMatch(.*)*', name:
                'NotFound', component:
                () => import('../views/NotFound.vue')
        },
    ],
})
export default router
