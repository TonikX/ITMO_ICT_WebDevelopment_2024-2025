import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import {isAuthenticated} from "@/composables/useAuth.js";
import {isHR} from "@/stores/globalState.js";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {path: '/', name: 'home', component: HomeView},
        {
            path: "/register", name: "Register", component: () => import('../views/RegisterView.vue'),
            beforeEnter: (to, from, next) => {
                isAuthenticated.value ? next('/') : next();
            },
        },
        {
            path: "/login",
            name: "Login",
            component: () => import('../views/LoginView.vue'),
            beforeEnter: (to, from, next) => {
                isAuthenticated.value && !isHR ? next('/') : next();
            },
        },
        {path: '/vacancies', name: 'vacancies', component: () => import('../views/VacanciesJSView.vue'),},
        {
            path: '/vacancies/:vacancyID',
            name: 'vacancies details',
            component: () => import('../views/VacanciesDetailView.vue'),
        }, {
            path: '/vacancies/:vacancyID/apply',
            name: 'vacancies apply',
            component: () => import('../views/VacanciesApplyView.vue'),
        },
        {
            path: '/cvs', name: 'cvs', component: () => import('../views/CvsView.vue'),
            beforeEnter: (to, from, next) => {
                !isAuthenticated.value ? next('/') : next();
            },
        },
        {
            path: '/cvs/:cvID/edit', name: 'cvs edit', component: () => import('../views/CvsEditView.vue'),
            beforeEnter: (to, from, next) => {
                !isAuthenticated.value ? next('/') : next();
            },
        },
        {
            path: '/cvs/:cvID/delete', name: 'cvs delete', component: () => import('../views/CvsDeleteView.vue'),
            beforeEnter: (to, from, next) => {
                !isAuthenticated.value ? next('/') : next();
            },
        },
        {path: '/applications', name: 'applications', component: () => import('../views/ApplicationsView.vue'),},
        {
            path: '/applications/:applicationId/edit',
            name: 'applications edit',
            component: () => import('../views/ApplicationEditView.vue'),
        },
        {
            path: '/applications/:applicationId/delete',
            name: 'applications delete',
            component: () => import('../views/ApplicationDeleteView.vue'),
        },
        {
            path: '/hr',
            name: 'HR',
            children: [
                {
                    path: "vacancies/create",
                    name: 'Vacancies create',
                    component: () => import('../views/VacancyCreateView.vue'),
                },
                {
                    path: "vacancies/:vacancyID/edit",
                    name: 'Vacancies edit',
                    component: () => import('../views/VacanciesEditHRView.vue'),
                },
                {
                    path: "vacancies/:vacancyID/delete",
                    name: 'Vacancies delete',
                    component: () => import('../views/VacanciesDeleteHRView.vue'),
                }
            ],
        },

        // 404 not found
        {
            path: '/:pathMatch(.*)*', name:
                'NotFound', component:
                () => import('../views/NotFound.vue')
        },
    ],
})

router.beforeEach((to, from, next) => {
    if (to.path.startsWith('/hr') && !isHR.value) {
        next({path: '/'});
    } else {
        next();
    }
});

export default router
