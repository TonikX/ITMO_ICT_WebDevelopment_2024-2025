import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import {isAuthenticated} from "@/composables/tokenActions.js";
import AllWorkoutsView from "@/views/AllWorkoutsView.vue";

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
        {path: '/workouts', name: 'allWorkouts', component: AllWorkoutsView},
        {
            path: '/workouts/:workoutId',
            name: 'workout info',
            component: () => import('../views/workoutDetails.vue'),
            props: true
        },
        {
            path: '/workouts/:workoutId/delete',
            name: 'delete workout',
            component: () => import('../views/DeleteWorkout.vue'),
            props: true
        },
        {
            path: '/workouts/:workoutId/edit',
            name: 'edit workout',
            component: () => import('../views/EditWorkout.vue'),
            props: true
        },
        {
            path: '/favorites',
            name: 'Favorites',
            component: () => import('../views/FavoritesView.vue'),
            beforeEnter: (to, from, next) => {
                !isAuthenticated.value ? next('/') : next();
            }
        },
        {
            path: '/done',
            name: 'Done',
            component: () => import('../views/DoneView.vue'),
            beforeEnter: (to, from, next) => {
                !isAuthenticated.value ? next('/') : next();
            }
        },
        {
            path: '/comments',
            name: 'Comments',
            component: () => import('../views/CommentView.vue'),
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

        {
            path: '/account/posts',
            name: 'posts',
            component: () => import('../views/yourPostsView.vue'),
            beforeEnter: (to, from, next) => {
                !isAuthenticated.value ? next('/') : next();
            }
        },
        {
            path: '/account/publish',
            name: 'publish',
            component: () => import('../views/publishPostView.vue'),
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
