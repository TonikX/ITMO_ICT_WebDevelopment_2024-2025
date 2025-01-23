import {createApp} from 'vue'
import {createPinia} from 'pinia'
import App from './App.vue'
import '@mdi/font/css/materialdesignicons.css'
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

import 'vuetify/styles'
import {createVuetify} from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import router from "@/utils/router.js";
import axios from "axios";

const pinia = createPinia()
pinia.use(piniaPluginPersistedState)

const myCustomLightTheme = {
    dark: false,
    colors: {
      background: '#dad7cd',
      surface: '#a3b18a',
      primary: '#588157',
      'primary-darken-1': '#3a5a40',
      secondary: '#4f772d',
      'secondary-darken-1': '#31572c',
      error: '#bc4749',
      info: '#2196F3',
      success: '#4CAF50',
      warning: '#FB8C00',
    },
  }
  
const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'myCustomLightTheme',
    themes: {
      myCustomLightTheme,
    },
    },
})

axios.defaults.baseURL = 'http://localhost:8000'

createApp(App).use(pinia).use(router).use(vuetify).mount('#app')

