import { createRouter, createWebHistory } from "vue-router";

import Home from "../pages/Home.vue";
import Rooms from "../pages/Rooms.vue";
import Stays from "../pages/Stays.vue";
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import Profile from "../pages/Profile.vue";

const routes = [
  { path: "/", component: Home },      // ← главная с датами
  { path: "/rooms", component: Rooms },
  { path: "/stays", component: Stays },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/profile", component: Profile },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
