import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/components/LoginPage.vue';
import RegisterPage from '@/components/RegisterPage.vue';
import MainPage from '@/components/MainPage.vue';
import UserProfile from '@/components/UserProfile.vue';
import AddBooking from '@/components/AddBooking.vue';
import BookingInfo from '@/components/BookingInfo.vue';
import BookingList from '@/components/BookingList.vue';
import AddRest from '@/components/AddRest.vue';
import AddTable from '@/components/AddTable.vue';
import TableList from '@/components/TableList.vue';
import AddReview from '@/components/AddReview.vue';
import TableInfo from '@/components/TableInfo.vue';
import ReviewInfo from '@/components/ReviewInfo.vue';
import ReviewList from '@/components/ReviewList.vue';
import RestInfo from '@/components/RestInfo.vue';
import RestList from '@/components/RestList.vue';

const routes = [
  {
    path: '/',
    name: 'main',
    component: MainPage
  },
  { path: '/profile', component: UserProfile, name: 'UserProfile' },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  { path: '/restaurants', component: RestList, name: 'RestList' },
  { path: '/add-restaurant', component: AddRest, name: 'AddRest' },
  { path: '/restaurant/:id', component: RestInfo, name: 'RestInfo' },

  { path: '/tables', component: TableList, name: 'TableList' },
  { path: '/add-table', component: AddTable, name: 'AddTable' },
  { path: '/table/:id', component: TableInfo, name: 'TableInfo' },

  { path: '/reviews', component: ReviewList, name: 'ReviewList' },
  { path: '/add-review', component: AddReview, name: 'AddReview' },
  { path: '/review/:id', component: ReviewInfo, name: 'ReviewInfo' },

  { path: '/bookings', component: BookingList, name: 'BookingList' },
  { path: '/add-booking', component: AddBooking, name: 'AddBooking' },
  { path: '/booking/:id', component: BookingInfo, name: 'BookingInfo' },

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;