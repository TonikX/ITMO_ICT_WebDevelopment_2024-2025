import Vue from 'vue';
import VueRouter from 'vue-router';
import Flights from '../views/Flights.vue';
import Routes from '../views/Routes.vue';
import Employees from '../views/Employees.vue';
import Airplanes from '../views/Airplanes.vue';
import Profile from '../views/Profile.vue';
import Login from '../views/Login.vue'
import FlightDetail from '../views/FlightDetail.vue'
import RouteDetail from '../views/RouteDetail.vue'
import EmployeeDetail from '../views/EmployeeDetail.vue'
import AirplaneDetail from '../views/AirplaneDetail.vue'
import Requests from '../views/Requests.vue'
import Home from '../views/Home.vue'

Vue.use(VueRouter);

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/', name: 'Home', component: Home, meta: { requiresAuth: true } },
  { path: '/flights', name: 'Flights', component: Flights, meta: { requiresAuth: true } },
  { path: '/flights/:id', name: 'FlightDetail', component: FlightDetail, meta: { requiresAuth: true } },
  { path: '/routes', name: 'Routes', component: Routes, meta: { requiresAuth: true, requiresAdmin: true  } },
  { path: '/routes/:id', name: 'RouteDetail', component: RouteDetail, meta: { requiresAuth: true, requiresAdmin: true  } },
  { path: '/employees', name: 'Employees', component: Employees, meta: { requiresAuth: true, requiresAdmin: true  } },
  { path: '/employees/:id', name: 'EmployeeDetail', component: EmployeeDetail, meta: { requiresAuth: true, requiresAdmin: true  } },
  { path: '/airplanes', name: 'Airplanes', component: Airplanes, meta: { requiresAuth: true, requiresAdmin: true  } },
  { path: '/airplanes/:id', name: 'AirplaneDetail', component: AirplaneDetail, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/requests', name: 'Requests', component: Requests, meta: { requiresAuth: true, requiresAdmin: true } },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});
router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        const token = localStorage.getItem('access_token');
        const userString = localStorage.getItem('user');
        const user = userString ? JSON.parse(userString) : null;
        if (token) {
            if(to.matched.some(record => record.meta.requiresAdmin)) {
                if(user && user.is_admin){
                    next()
                } else {
                    next('/')
                }
            } else {
                next()
            }
        } else {
            next('/login');
        }
    } else {
        next();
    }
});
export default router;
