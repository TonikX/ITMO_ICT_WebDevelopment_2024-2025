import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/components/LoginPage.vue';
import RegisterPage from '@/components/RegisterPage.vue';
import MainPage from '@/components/MainPage.vue';
import UserProfile from '@/components/UserProfile.vue';
import AddCustomer from '@/components/AddCustomer.vue';
import CustomerInfo from '@/components/CustomerInfo.vue';
import CustomerList from '@/components/CustomerList.vue';
import CustomerCars from '@/components/CustomerCars.vue';
import AddCar from '@/components/AddCar.vue';
import ServiceList from '@/components/ServiceList.vue';
import AddService from '@/components/AddService.vue';
import EmployeeInfo from '@/components/EmployeeInfo.vue';
import AddEmployee from '@/components/AddEmployee.vue';
import EmployeeList from '@/components/EmployeeList.vue';
import OrderCreate from '@/components/AddOrder.vue';
import OrderInfo from '@/components/OrderInfo.vue';
import OrderList from '@/components/OrderList.vue';
import AddPayment from '@/components/AddPayment.vue';
import PaymentDetails from '@/components/PaymentInfo.vue';
import PaymentList from '@/components/PaymentList.vue';

const routes = [
  {
    path: '/main',
    name: 'main',
    component: MainPage
  },
  { path: '/add-customer', component: AddCustomer, name: 'AddCustomer' },
  { path: '/customer/:id', component: CustomerInfo, name: 'CustomerInfo' },
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
  { path: '/profile', component: UserProfile, name: 'UserProfile' },
  { path: '/customers', component: CustomerList, name: 'CustomerList' },
  { path: '/customer-cars/:id', component: CustomerCars, name: 'CustomerCars' },
  { path: '/add-car/:id', component: AddCar, name: 'AddCar' },
  {
      path: '/services',
      name: 'services',
      component: ServiceList,
    },
    {
      path: '/add-service',
      name: 'add-service',
      component: AddService,
    },
    {
      path: '/employees/:id',
      name: 'employee-info',
      component: EmployeeInfo,
      props: true,
    },
    {
      path: '/employees/add',
      name: 'add-employee',
      component: AddEmployee,
    },
    {
    path: '/employees',
    name: 'employeeList',
    component: EmployeeList
  },
  {
      path: '/orders/create',
      name: 'order-create',
      component: OrderCreate,
    },
    {
      path: '/orders/:id',
      name: 'order-info',
      component: OrderInfo,
      props: true,
    },
    {
      path: '/orders',
      name: 'order-list',
      component: OrderList,
    },
    {
    path: '/payments',
    name: 'PaymentList',
    component: PaymentList
  },
  {
    path: '/payments/create',
    name: 'PaymentCreate',
    component: AddPayment
  },
  {
    path: '/payments/:id',
    name: 'PaymentDetails',
    component: PaymentDetails
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;