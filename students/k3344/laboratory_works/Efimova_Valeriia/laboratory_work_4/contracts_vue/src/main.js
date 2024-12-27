import App from './App.vue';


import { createApp } from 'vue';
import { router, vuetify } from './helpers';
import { createPinia } from 'pinia';

const app = createApp(App);

app.use(createPinia());
app.use(vuetify)
app.use(router);

app.mount('#app');

localStorage.setItem("access_token", response.data.access);

axios.defaults.baseURL = "http://localhost:8000/";
axios.defaults.withCredentials = true;

