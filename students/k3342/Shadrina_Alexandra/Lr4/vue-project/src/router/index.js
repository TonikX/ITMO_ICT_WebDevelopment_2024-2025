import { createRouter, createWebHistory } from 'vue-router'
import RegistrationForm from "@/components/RegistrationForm.vue";
import Login from "@/components/Login.vue";
import Home from "@/views/Home.vue";
import Profile from "@/views/Profile.vue";
import RecipePage from "@/views/RecipePage.vue";
import SearchRecipes from "@/components/SearchRecipes.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/search',
      name: 'Search',
      component: SearchRecipes,
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      meta: { requiresAuth: true },
    },
    {
      path: '/auth/users/',
      name: 'Register',
      component: RegistrationForm,
    },
    {
      path: '/auth/token/login/',
      name: 'Login',
      component: Login,
    },
    {
      path: '/add/recipe/',
      name: 'Add Recipe',
      component: () => import("@/components/AddRecipe.vue"),
    },
    {
      path: '/recipes/:id', // Параметр :id
      name: 'RecipePage',
      component: RecipePage,
      props: true, // Передаем айдишку как проп
  },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("auth_token");

  if (to.matched.some(record => record.meta.requiresAuth) && !token) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router
