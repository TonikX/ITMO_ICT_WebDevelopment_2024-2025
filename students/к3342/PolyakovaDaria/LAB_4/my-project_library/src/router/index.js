import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/views/LoginPage.vue';
import RegisterPage from '@/views/RegisterPage.vue';
import ProfilePage from '@/views/ProfilePage.vue';
import ChangePasswordPage from '@/views/ChangePasswordPage.vue';
import BooksPage from '@/views/BooksPage.vue';
import ReadersPage from '@/views/ReadersPage.vue';
import ReadingRoomsPage from '@/views/ReadingRoomsPage.vue';
import MonthlyReportsPage from '@/views/MonthlyReportsPage.vue';
import ReportsPage from '@/views/ReportsPage.vue';
import TransactionsPage from '@/views/TransactionsPage.vue';
import LowStockBooksPage from '@/views/LowStockBooksPage.vue';

const routes = [
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/profile', name: 'Profile', component: ProfilePage },
  { path: '/change-password', name: 'ChangePassword', component: ChangePasswordPage },
  { path: '/', redirect: '/books' },
  { path: '/books', name: 'Books', component: BooksPage },
  { path: '/readers', name: 'Readers', component: ReadersPage },
  { path: '/reading-rooms', name: 'ReadingRooms', component: ReadingRoomsPage },
  { path: '/reports', name: 'MonthlyReports', component: MonthlyReportsPage },
  { path: '/reports/complex', name: 'Reports', component: ReportsPage },
  { path: '/transactions', name: 'Transactions', component: TransactionsPage },
  { path: '/low-stock-books', name: 'LowStockBooks', component: LowStockBooksPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Навигационная защита
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (['Login', 'Register'].includes(to.name)) {
    next();
  } else if (!token) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
