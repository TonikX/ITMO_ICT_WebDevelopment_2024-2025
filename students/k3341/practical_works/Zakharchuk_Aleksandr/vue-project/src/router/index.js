import { createRouter, createWebHistory } from 'vue-router'
import Hello from '@/components/Hello.vue'
import Warriors from '@/views/Warriors.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/hi',
      name: 'hi',
      component: Hello,
    },
    {
      path: '/warriors',
      name: 'warriors',
      component: Warriors,
    }
  ],
})

export default router
