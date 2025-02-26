import { createRouter, createWebHistory } from 'vue-router'

import Start from '@/components/Start.vue'
import Home from '@/components/Home.vue'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Profile from '@/components/Profile.vue'
import Clients from '@/components/Clients.vue'
import Staff from '@/components/Staff.vue'
import Rooms from '@/components/Rooms.vue'
import Stays from '@/components/Stays.vue'
import Schedules from '@/components/Schedules.vue'
import Report from '@/components/Report.vue'

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
  { path: '/schedules', name: 'schedules', component: Schedules },
  { path: '/report', name: 'report', component: Report }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  console.log(to.name)
  // Если пользователь не авторизован и не на /login, /register или /start, перенаправляем на /start
  if (!token && to.name !== 'login' && to.name !== 'register' && to.name !== 'start') {
    next()
  } else {
    next()
  }
})
  
export default router