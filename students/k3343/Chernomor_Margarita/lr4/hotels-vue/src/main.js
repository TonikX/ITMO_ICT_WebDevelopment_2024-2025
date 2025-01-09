import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createVuetify } from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import 'vuetify/styles';
import * as components from 'vuetify/components'; // Импорт всех компонентов
import * as directives from 'vuetify/directives'; // Импорт всех директив

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme: {
        dark: false,
        colors: {
          primary: '#6b4226', // Основной цвет
          secondary: '#a67c52', // Дополнительный цвет
          background: '#f5f5dc', // Фон
          surface: '#ffffff',
          error: '#b00020',
          success: '#388e3c',
        },
      },
    },
  },
});

const app = createApp(App);


app.use(router).use(vuetify).mount('#app');
