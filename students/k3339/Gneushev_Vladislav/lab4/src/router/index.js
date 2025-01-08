import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/pages/auth/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/drivers',
      name: 'DriversList',
      component: () => import('@/pages/drivers/DriversList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/drivers/add',
      name: 'AddDriver',
      component: () => import('@/pages/drivers/AddDriver.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/drivers/:id',
      name: 'DriverDetails',
      component: () => import('@/pages/drivers/DriverDetails.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/buses',
      name: 'BusesList',
      component: () => import('@/pages/buses/BusesList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/buses/add',
      name: 'AddBus',
      component: () => import('@/pages/buses/AddBus.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/routes',
      name: 'RoutesList',
      component: () => import('@/pages/routes/RoutesList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/routes/add',
      name: 'AddRoute',
      component: () => import('@/pages/routes/AddRoute.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/pages/profile/Profile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/assignments',
      name: 'AssignmentsList',
      component: () => import('@/pages/assignments/AssignmentsList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/assignments/add',
      name: 'AddAssignment',
      component: () => import('@/pages/assignments/AddAssignment.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/',
      redirect: '/drivers'
    }
  ]
})

// Флаг для отслеживания первой навигации
let isFirstNavigation = true

router.beforeEach(async (to, from, next) => {
  // Если это первая навигация, ждем инициализации auth
  if (isFirstNavigation) {
    isFirstNavigation = false
    await store.dispatch('auth/initAuth')
  }

  const isAuthenticated = store.state.auth.isAuthenticated
  
  if (to.path === '/login') {
    if (isAuthenticated) {
      next('/drivers')
    } else {
      next()
    }
  } else {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!isAuthenticated) {
        next('/login')
      } else {
        next()
      }
    } else {
      next()
    }
  }
})

export default router 