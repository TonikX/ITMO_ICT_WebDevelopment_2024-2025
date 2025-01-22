import {createRouter, createWebHistory} from "vue-router";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import HomeView from "@/views/HomeView.vue";
import AgentView from "@/views/agent/AgentView.vue";
import AgentDetail from "@/views/agent/AgentDetail.vue";
import ClientView from "@/views/client/ClientView.vue";
import ClientDetail from "@/views/client/ClientDetail.vue";
import OrganizationView from "@/views/organization/OrganizationView.vue";
import OrganizationDetail from "@/views/organization/OrganizationDetail.vue";
import ReportView from "@/views/ReportView.vue";
import {tokenStore} from "@/stores/token.js";

const routes = [
    {
        name: 'Login',
        path: '/login',
        component: LoginView
    },
    {
        name: 'Register',
        path: '/register',
        component: RegisterView
    },
    {
          name: 'home',
          path: '/home',
          component: HomeView
    },
    {
          name: 'agents',
          path: '/agents',
          component: AgentView
    },
    {
          name: 'agentDetails',
          path: '/agents/:id',
          component: AgentDetail
    },
    {
          name: 'clients',
          path: '/clients',
          component: ClientView
    },
    {
          name: 'clientDetails',
          path: '/clients/:id',
          component: ClientDetail
    },
    {
          name: 'organization',
          path: '/organizations',
          component: OrganizationView
    },
    {
          name: 'organizationDetails',
          path: '/organizations/:id',
          component: OrganizationDetail
    },
    {
          name: 'report',
          path: '/report',
          component: ReportView
    },
]

const router = createRouter({
    history: createWebHistory(), routes
})

export default router

router.beforeEach((to, from, next) => {
    const token = tokenStore().token;

    if (to.name !== 'Login' && to.name !== 'Register' && !token) {
        next({name: 'Login'});
    } else {
        next();
    }
});
