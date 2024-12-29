import { createRouter, createWebHistory } from 'vue-router'

import Start from '@/views/Start.vue'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Profile from '@/views/Profile.vue'
import Clients from '@/views/Clients.vue'
import Staff from '@/views/Staff.vue'
import Rooms from '@/views/Rooms.vue'
import Stays from '@/views/Stays.vue'
import Cleanings from '@/views/Cleanings.vue'
import Schedules from '@/views/Schedules.vue'
import Report from '@/views/Report.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/start', name: 'start', component: Start },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/profile', name: 'profile', component: Profile },
  { path: '/clients', name: 'clients', component: Clients },
  { path: '/staff', name: 'staff', component: Staff },
  { path: '/rooms', name: 'rooms', component: Rooms },
  { path: '/stays', name: 'stays', component: Stays },
  { path: '/cleanings', name: 'cleanings', component: Cleanings },
  { path: '/schedules', name: 'schedules', component: Schedules },
  { path: '/report', name: 'report', component: Report }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  // Если пользователь не авторизован и не на /login, /register или /start, перенаправляем на /start
  if (!token && to.name !== 'login' && to.name !== 'register' && to.name !== 'start') {
    next('/start')
  } else {
    next()
  }
})
  
export default router