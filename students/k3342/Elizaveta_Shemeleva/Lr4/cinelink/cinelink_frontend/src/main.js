import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";
import router from "@/router";
import axios from "axios";
import { useAuthStore } from "@/stores/auth"; // Import the auth store
import "@/assets/css/header.css";
import "@/assets/css/theme.css";
import "@mdi/font/css/materialdesignicons.css";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

app.config.globalProperties.$axios = axios;
axios.defaults.baseURL = "http://localhost:8000/api/";

// Request interceptor for adding the Authorization header
axios.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Token ${authStore.token}`;
  } else {
    delete config.headers.Authorization;
  }
  return config;
});

// Response interceptor to handle 401 errors
axios.interceptors.response.use(
  (response) => response,
  (error) => {
      console.log("meow!", error.response.status);
    if (error.response && error.response.status === 401) {
      router.push("/login");
    }
    return Promise.reject(error);
  }
);

app.mount("#app");