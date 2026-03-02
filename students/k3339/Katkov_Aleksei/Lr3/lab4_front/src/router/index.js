import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import CategoriesView from "../views/CategoriesView.vue";
import TasksView from "../views/TasksView.vue";
import ProfileView from "../views/ProfileView.vue";

import { token } from "../authState";

function isAuthed() {
  return !!token.value;
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: () => (isAuthed() ? "/tasks" : "/login"),
    },

    { path: "/login", component: LoginView },
    { path: "/register", component: RegisterView },

    { path: "/profile", component: ProfileView, meta: { auth: true } },
    { path: "/categories", component: CategoriesView, meta: { auth: true } },
    { path: "/tasks", component: TasksView, meta: { auth: true } },

    { path: "/:pathMatch(.*)*", redirect: "/" },
  ],
});

router.beforeEach((to) => {
  const authed = isAuthed();

  if (to.meta.auth && !authed) return "/login";

  if (authed && (to.path === "/login" || to.path === "/register")) return "/tasks";
});

export default router;
