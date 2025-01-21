import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import Profile from '@/views/Profile.vue';
import Contracts from '@/views/Contracts.vue';
import CreateContract from '@/views/CreateContract.vue';
import EditContract from '@/views/EditContract.vue';
import ContractDetails from '@/views/ContractDetails.vue';
import Cars from '@/views/Cars.vue';
import CarDetails from '@/views/CarDetails.vue';
import CreateCar from '@/views/CreateCar.vue';
import EditCar from '@/views/EditCar.vue';
import Clients from '@/views/Clients.vue';
import CreateClient from '@/views/CreateClient.vue';
import EditClient from '@/views/EditClient.vue';
import ClientDetails from '@/views/ClientDetails.vue';
import Employees from '@/views/Employees.vue';
import EmployeeDetails from '@/views/EmployeeDetails.vue';
import EditEmployee from '@/views/EditEmployee.vue';
import CreateEmployee from '@/views/CreateEmployee.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/register', name: 'Register', component: Register },
  { path: '/login', name: 'Login', component: Login },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/contracts', name: 'Contracts', component: Contracts },
  { path: '/contracts/create', name: 'CreateContract', component: CreateContract },
  { path: '/contracts/:id/edit', name: 'EditContract', component: EditContract, props: true },
  { path: '/contracts/:id', name: 'ContractDetails', component: ContractDetails, props: true },
  { path: '/cars', name: 'Cars', component: Cars },
  { path: '/cars/:id', name: 'CarDetails', component: CarDetails, props: true },
  { path: '/cars/create', name: 'CreateCar', component: CreateCar },
  { path: '/cars/edit/:id', name: 'EditCar', component: EditCar },
  { path: '/clients', name: 'Clients', component: Clients },
  { path: '/clients/create', name: 'CreateClient', component: CreateClient },
  { path: '/clients/edit/:id', name: 'EditClient', component: EditClient, props: true },
  { path: '/clients/:id', name: 'ClientDetails', component: ClientDetails, props: true },
  { path: '/employees', name: 'Employees', component: Employees },
  { path: '/employees/:id', name: 'EmployeeDetails', component: EmployeeDetails, props: true },
  { path: '/employees/create', name: 'CreateEmployee', component: CreateEmployee },
  { path: '/employees/edit/:id', name: 'EditEmployee', component: EditEmployee, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
