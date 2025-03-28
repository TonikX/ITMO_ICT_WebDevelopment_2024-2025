import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'

// // Устанавливаем базовый URL для всех запросов
// axios.defaults.baseURL = 'http://127.0.0.1:8000'

// Добавляем axios в глобальные свойства Vue
const app = createApp(App);
app.use(router)
// app.config.globalProperties.$axios = axios;

app.mount('#app');
