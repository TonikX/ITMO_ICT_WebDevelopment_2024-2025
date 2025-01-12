import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // Подключение маршрутизатора
import Toast from 'vue-toastification';  // Подключаем Toast
import 'vue-toastification/dist/index.css';

// Импорт Vuetify
import { createVuetify } from "vuetify";
import "vuetify/styles"; // Стили Vuetify

// Опциональный импорт иконок Material Design Icons (MDI)
import "@mdi/font/css/materialdesignicons.css";

// Создание Vuetify
const vuetify = createVuetify();

// Создание приложения
createApp(App)
    .use(router)  // Используем маршрутизатор
    .use(vuetify)  // Используем Vuetify
    .use(Toast)    // Используем Toast
    .mount("#app");  // Монтируем приложение
