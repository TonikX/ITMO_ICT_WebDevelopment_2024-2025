import Warriors from "@/views/Warriors.vue";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
  {
    path: '/warriors',
    component: Warriors
  },
]

const router = createRouter({
  history: createWebHistory(), routes
})

export default router
