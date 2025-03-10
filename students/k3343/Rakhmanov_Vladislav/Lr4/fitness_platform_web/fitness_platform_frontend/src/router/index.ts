import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: "/register", name: "register", component: () => import("@/views/Register.vue"),
    },
    {
      path: "/login", name: "login", component: () => import("@/views/Login.vue"),
    },
    {
      path: "/workouts", name: "workouts", component: () => import("@/views/WorkoutList.vue"),
    },
    {
      path: "/workouts/:id/", name: "workouts details", component: () => import("@/views/WorkoutDetails.vue"),
    },
    {
      path: "/workouts/:id/edit",
      name: "EditWorkout",
      component: () => import("@/views/EditWorkout.vue"),
    },
    {
      path: "/workouts/new",
      name: "CreateWorkout",
      component: () => import("@/views/CreateWorkout.vue"),
    },
    {
      path: "/progress",
      name: "ProgressListCreate",
      component: () => import("@/views/ProgresListCreate.vue"),
    },
    {
      path: '/blogposts',
      name: "blogposts",
      component: () => import("@/views/BlogPostList.vue")
    },
    {path: '/account', name: "account", component: () => import('@/views/AccountView.vue')}
  ],
})

export default router
