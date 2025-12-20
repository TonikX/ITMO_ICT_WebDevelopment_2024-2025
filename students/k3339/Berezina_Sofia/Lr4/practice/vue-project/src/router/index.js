import Hello from "@/components/Hello.vue";
import Warriors from "@/views/Warriors.vue";
import {createRouter, createWebHistory} from "vue-router";

const routes = [  // массив с роутами
   // отдельный роут:
   {
       path: '/hi', // конкретный url-адрес
       component: Hello // Ссылка на компонент
   },
    {
       path: '/warriors',
       component: Warriors
    }
]

const router = createRouter({
   history: createWebHistory(), routes
})

export default router // экспортируем сконфигурированный роутер