import { createRouter, createWebHistory } from 'vue-router'
import { useStore } from 'vuex'
import MainView from '@/views/MainView.vue'
import HensView from '@/views/HensView.vue'
import EmployeesView from '@/views/EmployeesView.vue'
import CagesView from '@/views/CagesView.vue'
import DietsView from '@/views/DietsView.vue'
import BreedsView from '@/views/BreedsView.vue'
import ReviewsView from '@/views/ReviewsView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'
import ProfileView from '@/views/ProfileView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'main',
    //   component: MainView,
    // },
    {
      path: '/login/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/logout/',
      name: 'logout',
      component: LogoutView,
    },
    {
      path: '/profile/',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/hens/',
      name: 'hens',
      component: HensView,
      meta: { requiresAuth: true }
    },
    {
      path: '/employees/',
      name: 'employees',
      component: EmployeesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/cages/',
      name: 'cages',
      component: CagesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/diets/',
      name: 'diets',
      component: DietsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/breeds/',
      name: 'breeds',
      component: BreedsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/reviews/',
      name: 'reviews',
      component: ReviewsView,
      meta: { requiresAuth: true }
    },
  ],
})

router.beforeEach((to, from, next) => {
  const store = useStore();
  const accessToken = store.state.accessToken;
  if (to.meta.requiresAuth && !accessToken) {
    next({ name: 'login' });
  } else {
    next(); // Переходим на запрашиваемый маршрут
  }
});

export default router
