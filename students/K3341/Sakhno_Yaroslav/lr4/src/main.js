import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/router';
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const pinia = createPinia()
pinia.use(piniaPluginPersistedState)

const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'dark',
    },
})

createApp(App).use(vuetify).use(pinia).use(router).mount('#app')
