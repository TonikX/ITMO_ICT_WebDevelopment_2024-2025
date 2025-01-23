import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: () => import('../views/MainPage.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginPage.vue'),
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignupPage.vue'),
    },
    {
      path: '/useraccount',
      name: 'useraccount',
      component: () => import('../views/UserAccount.vue'),
    },
    {
      path: '/employeraccount',
      name: 'employeraccount',
      component: () => import('../views/EmployerAccount.vue'),
    },
    {
      path: '/vacancydetails',
      name: 'vacancydetails',
      component: () => import('../views/VacancyDetails.vue'),
    },
  ],
})

export default router
