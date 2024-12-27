import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores';
import { LoginComponent, RegisterComponent, HomeComponent, AddContractComponent } from "@/components";

const routes = [
  { path: '/login', component: LoginComponent },
  { path: '/register', component: RegisterComponent },
  { path: '/', component: HomeComponent },
  { path: '/add_contract', component: AddContractComponent }
]

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})


router.beforeEach(async (to) => {
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const auth = useAuthStore();

  if (auth.access && (to.path.startsWith('/login') || to.path.startsWith('/register'))) {
    return {
      path: '/',
      query: to.query,
    };
  }

  else if (authRequired && !auth.access) {
    auth.returnUrl = to.fullPath;
    return {
      path: '/login',
      query: to.query,
    };
  }
});
