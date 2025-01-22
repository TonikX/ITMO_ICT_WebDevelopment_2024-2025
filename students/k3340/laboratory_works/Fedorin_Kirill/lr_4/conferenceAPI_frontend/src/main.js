// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import Base from '@/components/Base.vue'
import router from './router'


const app = createApp(App)
//app.component('base-head', Base)
app.use(router)
app.mount('#app')
