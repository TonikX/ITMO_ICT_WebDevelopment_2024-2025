import { createApp } from 'vue'
import App from './App.vue'

import { createPinia } from "pinia"
import router from "./router"

import { createVuetify } from 'vuetify'
import 'vuetify/styles'

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#FF8C00',   // основной оранжевый
          secondary: '#FFA726', // светлый оранжевый
        },
      },
    },
  },
})

createApp(App)
  .use(createPinia())
  .use(router)
  .use(vuetify)
  .mount('#app')


