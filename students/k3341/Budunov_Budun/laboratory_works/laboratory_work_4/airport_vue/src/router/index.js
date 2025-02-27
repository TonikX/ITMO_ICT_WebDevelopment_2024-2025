import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import EmployeesView from '../views/EmployeesView.vue'
import EmployeeDetail from '../views/EmployeeDetail.vue'
import FlightsView from '../views/FlightsView.vue'
import FlightDetail from '../views/FlightDetail.vue'
import RoutesView from '../views/RoutesView.vue'
import RouteDetail from '../views/RouteDetail.vue'
import TransitsView from '../views/TransitsView.vue'
import TransitDetail from '../views/TransitDetail.vue'
import AirplanesView from '../views/AirplanesView.vue'
import AirplaneDetail from '../views/AirplaneDetail.vue'
import CrewsView from '../views/CrewsView.vue'
import CrewDetail from '../views/CrewDetail.vue'
import ProfileView from '../views/ProfileView.vue'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    component: LoginView
  },
  {
    path: '/home',
    component: HomeView
  },
  {
    path: '/employees',
    component: EmployeesView,
    meta: { isAdmin: true }
  },
  {
    path: '/employees/:id',
    component: EmployeeDetail,
    meta: { isAdmin: true }
  },
  {
    path: '/flights',
    component: FlightsView
  },
  {
    path: '/flights/:id',
    component: FlightDetail
  },
  {
    path: '/routes',
    component: RoutesView,
    meta: { isAdmin: true }
  },
  {
    path: '/routes/:id',
    component: RouteDetail,
    meta: { isAdmin: true }
  },
  {
    path: '/transits',
    component: TransitsView,
    meta: { isAdmin: true }
  },
  {
    path: '/transits/:id',
    component: TransitDetail,
    meta: { isAdmin: true }
  },
  {
    path: '/airplanes',
    component: AirplanesView,
    meta: { isAdmin: true }
  },
  {
    path: '/airplanes/:id',
    component: AirplaneDetail,
    meta: { isAdmin: true }
  },
  {
    path: '/crews',
    component: CrewsView,
    meta: { isAdmin: true }
  },
  {
    path: '/crews/:id',
    component: CrewDetail,
    meta: { isAdmin: true }
  },
  {
    path: '/profile',
    component: ProfileView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAdmin = localStorage.getItem('isAdmin')
  const isLoggedIn = localStorage.getItem('isLoggedIn')

  if (to.path === '/login' && isLoggedIn) {
    next('/home')
  } else if (to.meta.isAdmin && isAdmin !== 'true') {
    next('/flights')
  } else if (to.path !== '/login' && !isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
