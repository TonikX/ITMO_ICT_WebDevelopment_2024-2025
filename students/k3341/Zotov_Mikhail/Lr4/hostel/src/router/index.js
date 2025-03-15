import {createRouter, createWebHistory} from 'vue-router'
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import EmployeesView from "@/views/EmployeesView.vue";
import RoomsView from "@/views/RoomsView.vue";
import ClientsView from "@/views/ClientsView.vue";
import CheckInsView from "@/views/CheckInsView.vue";
import ReportsView from "@/views/ReportsView.vue";

const routes = [
  {path: '/', name: 'HomeView', component: HomeView},
  {path: '/login', name: 'LoginView', component: LoginView},
  {path: '/register', name: 'RegisterView', component: RegisterView},
  {path: '/employees', name: 'EmployeesView', component: EmployeesView},
  {path: '/rooms', name: 'RoomsView', component: RoomsView},
  {path: '/clients', name: 'ClientsView', component: ClientsView},
  {path: '/check-ins', name: 'CheckInsView', component: CheckInsView},
  {path: '/reports', name: 'ReportsView', component: ReportsView},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
