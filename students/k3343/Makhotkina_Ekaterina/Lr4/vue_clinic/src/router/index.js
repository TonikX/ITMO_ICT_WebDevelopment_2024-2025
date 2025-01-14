import {createRouter, createWebHistory} from 'vue-router';
import Login from '@/components/Auth/Login.vue';
import Register from '@/components/Auth/Register.vue';
import MedicalCardList from "@/components/MedicalCardList.vue";
import Patient from "@/components/Patient.vue";
import EmployeeList from "@/components/EmployeeList.vue";
import Diagnosis from "@/components/Diagnosis.vue";
import Appointment from "@/components/Appointment.vue";
import Report from '@/components/Report.vue';
import Services from "@/components/Services.vue";
import Home from "@/components/Home.vue";


const routes = [
  { path: '/register', name: 'Register', component: Register },
  { path: '/login', name: 'Login', component: Login },
  {
    path: "/medical-cards",
    name: "MedicalCards",
    component: MedicalCardList,
  },
  {
    path: "/patient",
    name: "Patient",
    component: Patient,
  },
  {
    path: "/employees",
    name: "Employee",
    component: EmployeeList,
  },
  {
    path: "/diagnosis",
    name: "Diagnosis",
    component: Diagnosis,
  },
  {
    path: "/appointments",
    name: "Appointment",
    component: Appointment,
  },
  {
    path: "/report",
    name: "RheumatologistPhones",
    component: Report,
  },
  {
    path: "/services",
    name: "Services",
    component: Services,
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});



router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('authToken');
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Login' });
    } else {
      next();
    }
  } else {
    next();
  }
});
export default router;
