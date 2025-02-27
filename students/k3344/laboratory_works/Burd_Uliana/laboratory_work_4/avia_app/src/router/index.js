import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '../components/LoginForm.vue';
import RegisterForm from '../components/RegisterForm.vue';
import ProfileForm from '../components/ProfileForm.vue';
import CrewMemberForm from '../components/CrewMemberList.vue';
import EmployeeForm from '../components/EmployeeList.vue';
import AircraftForm from '../components/AircraftList.vue';
import FlightForm from '../components/FlightList.vue';
const routes = [
  { path: '/login', component: LoginForm },
  { path: '/register', component: RegisterForm },
  { path: '/auth/profile/:id', name: 'user-profile', component: ProfileForm, props: true },
  { path: '/', redirect: '/login' },
  { path: '/aircrafts', component: AircraftForm },
  { path: '/crewmembers', component: CrewMemberForm },
  { path: '/flights', component:  FlightForm },
  { path: '/employees', component: EmployeeForm },
  {
        path: '/profile',
        name: 'ProfileForm',
        component: ProfileForm,
        meta: { requiresAuth: true },
      },
    ];

    const router = createRouter({
      history: createWebHistory(),
      routes,
    });


    router.beforeEach((to, from, next) => {
        const isAuthenticated = !!localStorage.getItem('token');


      if (to.meta.requiresAuth && !isAuthenticated) {

        next('/login');
      } else {

        next();
      }
    });


export default router;