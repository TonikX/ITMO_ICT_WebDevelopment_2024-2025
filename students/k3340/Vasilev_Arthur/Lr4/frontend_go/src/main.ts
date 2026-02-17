console.log('MAIN_TS_LOADED')

import { createApp } from 'vue'
console.log('STEP1_VUE_IMPORTED')

import { createPinia } from 'pinia'
console.log('STEP2_PINIA_IMPORTED')

import App from './App.vue'
console.log('STEP3_APP_IMPORTED')

import router from './router'
console.log('STEP4_ROUTER_IMPORTED')

import vuetify from './plugins/vuetify'
console.log('STEP5_VUETIFY_IMPORTED')

const app = createApp(App)
console.log('STEP6_APP_CREATED')

const pinia = createPinia()

app.use(pinia)
console.log('STEP7_PINIA_LOADED')

app.use(router)
console.log('STEP8_ROUTER_LOADED')

app.use(vuetify)
console.log('STEP9_VUETIFY_LOADED')

app.config.errorHandler = (err, instance, info) => {
  console.error('VUE_ERROR:', err)
  console.error('ERROR_INFO:', info)
}

app.mount('#app')
console.log('STEP10_APP_MOUNTED')
