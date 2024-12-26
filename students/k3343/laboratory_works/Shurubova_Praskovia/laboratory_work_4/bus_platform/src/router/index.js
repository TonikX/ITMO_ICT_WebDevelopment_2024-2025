import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
import HomeView from '@/views/HomeView.vue';
import DriverList from '@/views/DriverList.vue';
import DriverDetail from '@/views/DriverDetail.vue';
import RouteList from '@/views/RouteList.vue';
import RouteDetail from '@/views/RouteDetail.vue';
import BusList from '@/views/BusList.vue';
import BusDetail from '@/views/BusDetail.vue';
import ScheduleList from '@/views/ScheduleList.vue';
import ScheduleDetail from '@/views/ScheduleDetail.vue';
import AssignmentList from '@/views/AssignmentList.vue';
import AssignmentDetail from '@/views/AssignmentDetail.vue';
import MaintenanceList from '@/views/MaintenanceList.vue';
import MaintenanceDetail from '@/views/MaintenanceDetail.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
  },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/drivers', name: 'DriverList', component: DriverList },
  { path: "/drivers/:id", name: 'DriverDetail', component: DriverDetail },
  { path: '/routes', name: 'RouteList', component: RouteList },
  { path: '/routes/:id', name: 'RouteDetail', component: RouteDetail },
  { path: '/buses', name: 'BusList', component: BusList },
  { path: '/buses/:id', name: 'BusDetail', component: BusDetail },
  { path: '/driver-schedules', name: 'ScheduleList', component: ScheduleList },
  { path: '/driver-schedule/:id', name: 'ScheduleDetail', component: ScheduleDetail },
  { path: '/assignment', name: 'AssignmentList', component: AssignmentList },
  { path: '/assignment/:id', name: 'AssignmentDetail', component: AssignmentDetail },
  { path: '/maintenances', name: 'MaintenanceList', component: MaintenanceList },
  { path: '/maintenance/:id/update', name: 'MaintenanceDetail', component: MaintenanceDetail },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
