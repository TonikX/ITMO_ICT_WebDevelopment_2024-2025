import { createRouter, createWebHistory } from 'vue-router'
import PetsView from '../views/PetsView.vue'
import HabitedsView from '../views/HabitedsView.vue'
import DietsView from '../views/DietsView.vue'
import RentedInView from '../views/RentedInView.vue'
import RegisterView from '../views/Account/RegistredView.vue'
import LoginView from '../views/Account/LoginView.vue'
import UserEtidView from '../views/Account/UserEtidView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'pets',
      component: PetsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/habiteds',
      name: 'habiteds',
      component: HabitedsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/diet',
      name: 'diet',
      component: DietsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/report',
      name: 'reportRentIn',
      component: RentedInView,
      meta: { requiresAuth: true }
    },
    {
      path: '/register',
      component: RegisterView
    },
    {
      path: '/login',
      component: LoginView
    },
    {
      path: '/user',
      component: UserEtidView,
      meta: { requiresAuth: true }
    },
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token');

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ path: '/login' });
  } else {
    next();
  }
});

export default router
