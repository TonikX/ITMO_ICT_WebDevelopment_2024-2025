// import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     {
//       path: '/',
//       name: 'home',
//       component: HomeView,
//     },
//     {
//       path: '/about',
//       name: 'about',
//       // route level code-splitting
//       // this generates a separate chunk (About.[hash].js) for this route
//       // which is lazy-loaded when the route is visited.
//       component: () => import('../views/AboutView.vue'),
//     },
//   ],
// })

// export default router


// import Hello from "@/components/Hello.vue";
// import { createRouter, createWebHistory } from "vue-router";

// const routes = [
//   {
//     path: '/hi', // 定义路径为 /hi
//     component: Hello, // 对应组件为 Hello
//   },
// ];

// const router = createRouter({
//   history: createWebHistory(),
//   routes,
// });

// export default router;


import { createRouter, createWebHistory } from "vue-router";
import Warriors from "@/views/Warriors.vue"; // 导入新的 Warriors 视图

const routes = [
  {
    path: "/warriors",
    component: Warriors // 访问 "/warriors" 路径时加载 Warriors 视图
  },
  // 其他路由配置
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
