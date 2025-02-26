import { createRouter, createWebHistory } from 'vue-router';
import RoomsView from '../views/RoomsView.vue';
import RoomDetails from '../components/RoomDetails.vue';
import LoginView from '../views/LoginView.vue';
import SignupView from '../views/SignupView.vue';
import ClientsView from '../views/ClientsView.vue';
import BookingsView from '../views/BookingsView.vue';
import CleaningSchedulesView from '../views/CleaningSchedulesView.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupView,
  },
  {
    path: '/rooms',
    name: 'Rooms',
    component: RoomsView,
  },
  {
    path: '/rooms/:id',
    name: 'RoomDetails',
    component: RoomDetails,
  },
  {
    path: '/clients',
    name: 'Clients',
    component: ClientsView,
  },
  {
    path: '/bookings',
    name: 'Bookings',
    component: BookingsView,
  },
  {
    path: '/cleaning-schedules',
    name: 'CleaningSchedules',
    component: CleaningSchedulesView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;