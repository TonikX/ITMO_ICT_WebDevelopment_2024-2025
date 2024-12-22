import Hello from "@/components/Hello.vue";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
  {
    path: '/hi',
    component: Hello
  },
]

const router = createRouter({
  history: createWebHistory(), routes
})

export default router
