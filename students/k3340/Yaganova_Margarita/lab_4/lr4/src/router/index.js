import Hello from "@/components/Hello.vue";
import Warriors from "@/views/Warriors.vue"
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: '/hi',
    component: Hello
  },
  {
    path: '/skills',
    component: Warriors
  }
]

const router = createRouter({
  history: createWebHistory(), routes
})

export default router

