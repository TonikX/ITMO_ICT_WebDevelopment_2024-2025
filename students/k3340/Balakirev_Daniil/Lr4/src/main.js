import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import axios from 'axios'
import VueAxios from 'vue-axios'

const vuetify = createVuetify({
  components,
  directives,
})

const app = createApp(App)

app.use(router)
app.use(vuetify)
app.use(VueAxios, axios)

app.config.globalProperties.$hostname = 'http://127.0.0.1:8000/'
axios.defaults.baseURL = app.config.globalProperties.$hostname;

app.mount('#app')