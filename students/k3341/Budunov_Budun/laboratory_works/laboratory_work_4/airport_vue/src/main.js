import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify'; // Import vuetify from plugins
import store from './store'; // Import Vuex store

Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  store, // Use store here
  render: (h) => h(App),
}).$mount('#app');
