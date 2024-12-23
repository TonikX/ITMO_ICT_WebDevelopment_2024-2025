import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store'; 
import vuetify from './plugins/vuetify'; 

// Импорт стилей Vuetify и иконок Material Design
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';

const app = createApp(App);

// Подключение плагинов
app.use(router);
app.use(store); // Подключение Vuex
app.use(vuetify);

// Загрузка данных пользователя при запуске приложения
store.dispatch('fetchUser');

app.mount('#app');
