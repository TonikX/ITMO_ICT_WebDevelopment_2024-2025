// import './assets/main.css'

// import { createApp } from 'vue'
// import App from './App.vue'
// import router from './router'

// const app = createApp(App)

// app.use(router)

// app.mount('#app')


import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // 引入路由
import "./assets/main.css";

createApp(App).use(router).mount("#app");
