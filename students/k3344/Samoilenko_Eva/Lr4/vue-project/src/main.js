import './assets/main.css'
import router from "./router/index.js";
import { createApp } from 'vue'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { createPinia } from 'pinia'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css';
import App from './App.vue'
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
  },
  icons: {
    defaultSet: 'mdi',
  },
})

const pinia = createPinia()
pinia.use(piniaPluginPersistedState)

createApp(App).use(vuetify).use(pinia).use(router).mount('#app')
