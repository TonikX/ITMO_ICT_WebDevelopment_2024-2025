import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/WelcomeView.vue'),
  },

  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/buses',
    name: 'BusList',
    component: () => import('@/views/BusList.vue'),
  },
  {
      path: '/buses/:id',
      name: 'BusDetails',
      component: () => import('@/views/BusDetails.vue'),
    },
  {
    path: '/drivers',
    name: 'DriverList',
    component: () => import('@/views/DriverList.vue'),
  },
  {
    path: '/routes',
    name: 'RouteList',
    component: () => import('@/views/RouteList.vue'),
  },
  {
    path: '/routes/:route_number/edit',
    name: 'RouteDetails',
    component: () => import('@/views/RouteDetails.vue'),
  },
  {
    path: '/schedules',
    name: 'ScheduleList',
    component: () => import('@/views/ScheduleList.vue'),
  },
  {
    path: "/schedules/:id",
    name: "ScheduleDetails",
    component: () => import('@/views/ScheduleDetails.vue'),
    props: true,
  },
    {
    path: '/incidents',
    name: 'IncidentList',
    component: () => import('@/views/IncidentList.vue'),
  },
  {
  path: '/incidents/:id',
  name: 'IncidentDetails',
  component: () => import('@/views/IncidentDetails.vue'),
},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
