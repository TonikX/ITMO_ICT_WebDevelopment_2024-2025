import { createRouter, createWebHistory } from 'vue-router';
import SignupPage from '../views/SignupPage.vue';
import LoginPage from '../views/LoginPage.vue';
import AccountPage from '@/views/AccountPage.vue';
import ClientsPage from '@/views/ClientsPage.vue';
import OrdersPage from '@/views/OrdersPage.vue';
import PaymentsPage from '@/views/PaymentsPage.vue';
import ChangePasswordPage from '@/views/ChangePasswordPage.vue';
import EmployeesPage from '@/views/EmployeesPage.vue';
import LogoutPage from '@/views/LogoutPage.vue';
import ReportsPage from '@/views/ReportsPage.vue';
import ServicesPage from '@/views/ServicesPage.vue';
import OrderFormPage from '@/views/OrderFormPage.vue';
import MainPage from '@/views/MainPage.vue';
import AdminMainPage from '@/views/AdminMainPage.vue';
import AdminServicesPage from '@/views/AdminServicesPage.vue';
import QuarterlyReport from '@/views/QuarterlyReport.vue';
import CompletedOrders from '@/views/CompletedOrders.vue';
import ServicesList from '@/views/ServicesList.vue';
import AdminOrders from '@/views/AdminOrders.vue';
import AdminOrderEdit from '@/views/AdminOrderEdit.vue';
import AdminOrderCreate from '@/views/AdminOrderCreate.vue';
import PaymentsByPeriod from '@/views/PaymentsByPeriod.vue';
import OrdersByClient from '@/views/OrdersByClient.vue';
import CompletedEmployee from '@/views/CompletedEmployee.vue';

const routes = [
  { path: '/', component: MainPage },
  { path: '/admin', component: AdminMainPage},
  { path: '/admin-services', component: AdminServicesPage},
  { path: '/admin-orders', component: AdminOrders},
  { path: '/admin-orders/new', component: AdminOrderCreate},
  { path: '/admin-orders/edit/:id', component: AdminOrderEdit},
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignupPage },
  { path: '/profile', component: AccountPage },
  { path: '/clients', component: ClientsPage },
  { path: '/orders', component: OrdersPage },
  { path: '/payments', component: PaymentsPage },
  { path: '/change-password', component: ChangePasswordPage },
  { path: '/logout', component: LogoutPage },
  { path: '/employees', component: EmployeesPage },
  { path: '/reports', component: ReportsPage },
  { path: '/reports/quarterly', component: QuarterlyReport},
  { path: '/reports/completed-orders', component: CompletedOrders},
  { path: '/reports/services-list', component: ServicesList},
  { path: '/reports/payments-by-period', component: PaymentsByPeriod},
  { path: '/reports/orders-by-client', component: OrdersByClient},
  { path: '/reports/employee-orders-completed', component: CompletedEmployee},
  { path: '/services', component: ServicesPage },
  { path: '/orders/new', component: OrderFormPage },
  { path: '/orders/edit/:id', component: OrderFormPage, props: true},
  // { path: '/:pathMatch(.*)*', component: NotFoundPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
