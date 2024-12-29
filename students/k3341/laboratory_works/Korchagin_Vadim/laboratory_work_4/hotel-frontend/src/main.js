// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Подключаем глобальные стили
import '@/assets/hotel-styles.css'

// Тема
const myHotelTheme = {
  dark: false,
  colors: {
    background: '#FAFAFA',
    surface: '#FFFFFF',
    primary: '#4A90E2',
    'primary-darken-1': '#357ABD',
    secondary: '#7BDCB5',
    'secondary-darken-1': '#57C09C',
    error: '#D32F2F',
    info: '#2D9CDB',
    success: '#27AE60',
    warning: '#CFCFCF',
  },
  variables: {
    'border-color': '#000000',
    'border-opacity': 0.12,
  }
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'myHotelTheme',
    themes: {
      myHotelTheme
    }
  }
})

createApp(App)
  .use(router)
  .use(vuetify)
  .mount('#app')