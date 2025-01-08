import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index';
import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';
import { authState } from './store/auth';
import axios from 'axios';



import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const vuetify = createVuetify({
  components,
  directives,
});

axios.defaults.baseURL = 'http://127.0.0.1:8000'; // Укажите адрес вашего бэкенда


const app = createApp(App);

app.config.globalProperties.$axios = axios;
app.config.globalProperties.$token = localStorage.getItem('token') || null;
app.config.globalProperties.$authState = authState;


app.use(router);
app.use(vuetify);
app.mount('#app');