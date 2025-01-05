import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/components/LoginPage.vue';
import RegisterPage from '@/components/RegisterPage.vue';
import HomePage from '@/components/HomePage.vue';
import StaffPage from '@/components/StaffPage.vue';
import ClientsPage from '@/components/ClientsPage.vue';
import RoomsPage from '@/components/RoomsPage.vue';
import RoomInfoPage from '@/components/RoomInfoPage.vue';
import CleaningSchedule from '@/components/CleaningSchedule.vue';
import HotelReportPage from '@/components/HotelReportPage.vue';
import ReservationPage from '@/components/ReservationPage.vue';

const routes = [
  { path: "/", component: HomePage, name: "Home" },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/staff', name: 'Staff', component: StaffPage },
  { path: '/clients', name: 'Clients', component: ClientsPage },
  { path: '/rooms', name: 'Rooms', component: RoomsPage },
  { path: '/rooms/:roomId', name: 'RoomInfo', component: RoomInfoPage, props: true},
  { path: '/cleaning-schedule', name: 'CleaningSchedule', component: CleaningSchedule},
  { path: '/report', name: 'ReportPage', component: HotelReportPage},
  { path: '/reservations', name: 'ReservationPage', component: ReservationPage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
