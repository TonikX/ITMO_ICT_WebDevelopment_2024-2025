import { createApp } from 'vue'

import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import router from "./router";
import axios from "axios";

const token = localStorage.getItem('token'); // Достаем токен из локального хранилища
if (token) {
    axios.defaults.headers.common['Authorization'] = `Token ${token}`;
}

createApp(App).use(router).mount('#app')
