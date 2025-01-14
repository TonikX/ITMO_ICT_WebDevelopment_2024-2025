import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../pages/Main.vue'
import LoginPage from '../pages/Login.vue'
import SportsmenPage from '../pages/Sportsmen.vue'
import SchedulePage from "../pages/Schedule.vue";
import CoachesPage from "../pages/Coaches.vue";
import SectionsPage from "../pages/Sections.vue";
import ReportsPage from "@/pages/Reports.vue";
import RegistrationPage from "@/pages/Registration.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login',
      name: 'Login',
      component: LoginPage },

    { path: '/register',
      name: 'Registration',
      component: RegistrationPage },

    { path: '/',
      name: 'Main',
      component: MainPage,
      meta: { requiresAuth: true } },

    { path: '/sportsmen',
      name: 'Sportsmen',
      component: SportsmenPage },

    { path: '/schedule',
      name: 'Schedule',
      component: SchedulePage },

    { path: '/coaches',
      name: 'Coaches',
      component: CoachesPage },

    { path: '/sections',
      name: 'Sections',
      component: SectionsPage },

    { path: '/reports',
      name: 'Reports',
      component: ReportsPage },
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('authToken') !== null;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
