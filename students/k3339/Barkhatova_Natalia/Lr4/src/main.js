import {createApp} from "vue";
import App from "./App.vue";
import {createPinia} from 'pinia';
import router from "./router";
import 'core-js/stable';
import 'regenerator-runtime/runtime';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.mount("#app");
