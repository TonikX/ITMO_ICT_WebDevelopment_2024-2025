import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import AnimalListView from '../views/AnimalListView.vue'
import AnimalDetailView from '../views/AnimalDetailView.vue'
import AnimalCreateView from '../views/AnimalCreateView.vue'
import AnimalEditView from '../views/AnimalEditView.vue'
import DepartmentAnimalCountView from '../views/DepartmentAnimalCountView.vue'
import EmptyEnclosuresView from '../views/EmptyEnclosuresView.vue'
import LeaseReportView from '../views/LeaseReportView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true } },
    { path: '/animals', name: 'animals', component: AnimalListView },
    { path: '/animals/create', name: 'create-animal', component: AnimalCreateView, meta: { requiresAuth: true } },
    { path: '/animals/:id', name: 'animal-detail', component: AnimalDetailView },
    { path: '/animals/:id/edit', name: 'animal-edit', component: AnimalEditView, meta: { requiresAuth: true } },
    { path: '/reports/animal-count', name: 'animal-count', component: DepartmentAnimalCountView },
    { path: '/reports/empty-enclosures', name: 'empty-enclosures', component: EmptyEnclosuresView },
    { path: '/reports/lease-report', name: 'lease-report', component: LeaseReportView },
  ],
})

// Защита маршрутов, требующих авторизации
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router