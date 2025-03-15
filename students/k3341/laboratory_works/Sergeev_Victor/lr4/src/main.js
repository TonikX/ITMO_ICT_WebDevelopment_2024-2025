import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const pinia = createPinia();
const app = createApp(App);

const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'dark',
    },
})

app.use(pinia);
app.use(router);
app.use(vuetify);

app.mount('#app');
