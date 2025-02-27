// import Vue from 'vue'
import App from './App.vue'
import 'vuetify/styles'
// import { createVuetify } from 'vuetify'
import { createApp } from 'vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'

// const vuetify = createVuetify()

// Vue.config.productionTip = false

// new Vue({
//   vuetify,
//   router,
//   store,
//   render: h => h(App)
// }).$mount('#app')
const app = createApp(App)
app.use(vuetify)
app.use(router)
app.use(store)
app.mount('#app')

// export default vuetify
