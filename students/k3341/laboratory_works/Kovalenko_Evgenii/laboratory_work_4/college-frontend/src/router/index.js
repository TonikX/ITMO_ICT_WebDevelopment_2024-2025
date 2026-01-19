import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/teachers',
    name: 'Teachers',
    component: () => import('@/views/Teachers.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/students',
    name: 'Students',
    component: () => import('@/views/Students.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: () => import('@/views/Schedule.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/grades',
    name: 'Grades',
    component: () => import('@/views/Grades.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/Reports.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/subjects',
    name: 'Subjects',
    component: () => import('@/views/Subjects.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/groups',
    name: 'Groups',
    component: () => import('@/views/Groups.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/classrooms',
    name: 'Classrooms',
    component: () => import('@/views/Classrooms.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/queries',
    name: 'Queries',
    component: () => import('@/views/Queries.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.meta.requiresAuth
  const requiresGuest = to.meta.requiresGuest

  if (requiresAuth && !token) {
    next('/login')
  } else if (requiresGuest && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router