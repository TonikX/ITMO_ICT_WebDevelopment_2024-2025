import { createRouter, createWebHistory } from 'vue-router';
import WorkshopView from '@/views/WorkshopView.vue';
import CellsList from '@/views/CellsList.vue';
import EmployeesList from '@/views/EmployeesList.vue';
import ChickensList from '@/views/ChickensList.vue'; 
import BreedsList from '@/views/BreedsList.vue';
import PerformanceReports from '@/views/Reports.vue';
import Diets from '@/views/Diets.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/cells',
      name: 'CellsList',
      component: CellsList,
    },
    {
      path: '/employees',
      name: 'EmployeesList',
      component: EmployeesList,
    },
    {
      path: '/chickens',
      name: 'ChickensList',
      component: ChickensList,
    },
    {
      path: '/breeds',
      name: 'BreedsList',
      component: BreedsList,
    },
    {
      path: '/workshops',
      name: 'WorkshopList',
      component: WorkshopView,
    },
    {
        path: '/diets',
        name: 'Diets',
        component: Diets,
    },
    {
      path: '/reports',
      name: 'PerformanceReports',
      component: PerformanceReports,
    },
  ],
});

export default router;