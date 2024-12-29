import { createRouter, createWebHistory } from 'vue-router';
import Welcome from '@/views/Welcome.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import Planes from '@/views/Planes.vue';
import Flights from '@/views/Flights.vue';
import FlightDetail from "@/views/FlightDetail.vue";
import Crews from '@/views/Crews.vue';
import Maintenances from '@/views/Maintenances.vue';
import Routes from '@/views/Routes.vue';
import Employees from '@/views/Employees.vue';
import RouteStats from "@/views/RouteStats.vue";
import PlaneStats from "@/components/reports/PlaneStats.vue";
import Profile from '@/views/Profile.vue';
import ChangePassword from '@/components/user/ChangePassword.vue';
import UpdateProfile from '@/components/user/UpdateProfile.vue';



const routes = [
  { path: '/', name: 'Welcome', component: Welcome },
  { path: '/register', name: 'Register', component: Register },
  { path: '/login', name: 'Login', component: Login },
  { path: '/planes', name: 'Planes', component: Planes },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/change-password', name: 'ChangePassword', component: ChangePassword },
  { path: '/update-profile', name: 'UpdateProfile', component: UpdateProfile },
  { path: '/flights', name: 'Flights', component: Flights },
  { path: `/flights/:flightId`, name: 'FlightDetail', component: FlightDetail, props: true },
  { path: '/routes-stats', name: 'RouteStats', component: RouteStats },
  { path: '/planes-stats', name: 'PlaneStats', component: PlaneStats },
  { path: '/maintenances', name: 'Maintenances', component: Maintenances},
  { path: '/employees', name: 'Employees', component: Employees},
  { path: '/crews', name: 'Crews', component: Crews},
  { path: '/routes', name: 'Routes', component: Routes},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
