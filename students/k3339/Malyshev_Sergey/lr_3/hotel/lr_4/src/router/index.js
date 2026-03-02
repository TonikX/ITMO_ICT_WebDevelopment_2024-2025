import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/rooms',
    name: 'rooms',
    component: () => import('../views/RoomsView.vue')
  },
  {
  path: '/guests',
  name: 'guests',
  component: () => import('../views/GuestsView.vue')
  },
  {
  path: '/bookings',
  name: 'bookings',
  component: () => import('../views/BookingsView.vue')
  },
  {
  path: '/reports/quarter',
  name: 'reports-quarter',
  component: () => import('../views/ReportsView.vue')
  },
  {
  path: '/profile',
  name: 'profile',
  component: () => import('../views/ProfileView.vue')
  },
  {
  path: '/bookings/create',
  name: 'bookings-create',
  component: () => import('../views/BookingsCreate.vue')
  },
  {
  path: '/guests/create',
  name: 'guests-create',
  component: () => import('../views/GuestsCreate.vue')
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
