import { createRouter, createWebHistory } from "vue-router";
import IndexPage from "../views/IndexPage.vue";
import AboutPage from "../views/AboutPage.vue";
import ContactPage from "../views/ContactPage.vue";
import SearchPage from "../views/SearchPage.vue";
import PropertyPage from "../views/PropertyPage.vue";
import MessagesPage from "../views/MessagesPage.vue";
import ProfilePage from "../views/ProfilePage.vue";
import AuthPage from "../views/AuthPage.vue";
import PropertySettings from "@/views/PropertySettings.vue";

const routes = [
  { path: "/", name: "Home", component: IndexPage },
  { path: "/about", name: "About", component: AboutPage },
  { path: "/contact", name: "Contact", component: ContactPage },
  { path: "/search", name: "Search", component: SearchPage },
  { path: "/property/:id", name: "Property", component: PropertyPage },
  { path: "/messages", name: "Messages", component: MessagesPage },
  { path: "/profile", name: "Profile", component: ProfilePage },
  { path: "/auth", name: "Auth", component: AuthPage },
  { path: "/propertySettings", name: "PropertySettings", component: PropertySettings }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
