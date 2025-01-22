import {createRouter, createWebHistory} from "vue-router";
import ConferencesList from "@/components/ConferenceList.vue"
import Login from "@/components/Login.vue";
import Main from "@/components/Main.vue";
import Logout from "@/components/Logout.vue";
import Register from "@/components/Register.vue";
import ParticipationList from "@/components/ParticipationList.vue";

const routes = [  
   { path: '/conferences', component: ConferencesList },
   { path: '/login', component: Login },
   { path: '/register', component: Register },
   { path: '/', component: Main },
   { path: '/logout', component: Logout },
   { path: '/participation', component: ParticipationList },

]

const router = createRouter({
   history: createWebHistory(), routes
})

export default router