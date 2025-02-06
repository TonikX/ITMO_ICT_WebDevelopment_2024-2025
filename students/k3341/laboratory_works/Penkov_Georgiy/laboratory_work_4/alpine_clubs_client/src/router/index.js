import { createWebHistory, createRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import AscentsView from '../views/AscentsView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import AscentDetailView from '@/views/AscentDetailView.vue'
import MyAscents from '@/views/MyAscents.vue'
import ClubsTable from '@/views/ClubsTable.vue'
import ClubDetailView from '@/views/ClubDetailView.vue'
import ReportView from '@/views/ReportView.vue'

const routes = [
  { path: '/', component: AscentsView},
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView},
  { path: '/me', component: ProfileView , meta: {auth: true} },
  { path: '/ascents/:id', component: AscentDetailView , props: true },
  { path: '/ascents/me', component: MyAscents, meta: {auth: true}},
  { path: '/clubs/', component: ClubsTable},
  { path: '/clubs/:id', component: ClubDetailView, props: true},
  { path: '/report', component: ReportView},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.auth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router