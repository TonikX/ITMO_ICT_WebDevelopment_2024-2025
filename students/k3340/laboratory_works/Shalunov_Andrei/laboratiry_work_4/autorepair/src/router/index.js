import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/Home.vue';
import { isAuthenticated } from "@/composables/useAuth.js";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },

    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/RegisterView.vue'),
      beforeEnter: (to, from, next) => {
        isAuthenticated.value ? next('/') : next();
      },
    },

    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      beforeEnter: (to, from, next) => {
        isAuthenticated.value ? next('/') : next();
      },
    },

    {
      path: '/clients',
      name: 'Clients',
      component: () => import('@/views/Clients.vue'),
      beforeEnter: (to, from, next) => {
        !isAuthenticated.value ? next('/login') : next();
      },
    },

    {
      path: '/employees',
      name: 'Employees',
      component: () => import('@/views/Employees.vue'),
      beforeEnter: (to, from, next) => {
        !isAuthenticated.value ? next('/login') : next();
      },
    },

    {
      path: '/automobiles',
      name: 'Automobiles',
      component: () => import('@/views/Automobiles.vue'),
      beforeEnter: (to, from, next) => {
        !isAuthenticated.value ? next('/login') : next();
      },
    },

    {
      path: '/contracts',
      name: 'Contracts',
      component: () => import('@/views/Contracts.vue'),
      beforeEnter: (to, from, next) => {
        !isAuthenticated.value ? next('/login') : next();
      },
    },


    {
      path: '/services',
      name: 'Services',
      component: () => import('@/views/Services.vue'),
      beforeEnter: (to, from, next) => {
        !isAuthenticated.value ? next('/login') : next();
      },
    },


    // {
    //   path: '/:pathMatch(.*)*',
    //   name: 'NotFound',
    //   component: () => import('@/views/NotFoundView.vue'),
    // },
  ],
});

export default router;
