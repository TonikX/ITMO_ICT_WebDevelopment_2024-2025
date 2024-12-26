import {createRouter, createWebHistory} from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import UsersListView from '../views/users/UsersListView.vue'
import UserDetailView from '../views/users/UserDetailView.vue'
import NewspapersListView from "@/views/newspapers/NewspapersListView.vue"
import NewspaperDetailView from '../views/newspapers/NewspaperDetailView.vue'
import PrintingHousesListView from "@/views/printinghouses/PrintingHousesListView.vue"
import PostOfficesListView from "@/views/postoffices/PostOfficesListView.vue"
import EditionsListView from "@/views/editions/EditionsListView.vue"
import DistributionsListView from "@/views/distributions/DistributionsListView.vue"
import EditionDetailView from "@/views/editions/EditionDetailView.vue"
import PrintingHouseDetailView from "@/views/printinghouses/PrintingHouseDetailView.vue"
import PostOfficeDetailView from "@/views/postoffices/PostOfficeDetailView.vue"
import DistributionDetailView from "@/views/distributions/DistributionDetailView.vue"
import AnalyticsView from '@/views/analytics/AnalyticsView.vue'
import ReportsView from '@/views/reports/ReportsView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/users',
      name: 'users-list',
      component: UsersListView
    },
    {
      path: '/users/:id',
      name: 'user-detail',
      component: UserDetailView
    },
    {
      path: '/newspapers',
      name: 'newspapers-list',
      component: NewspapersListView
    },
    {
      path: '/newspapers/:id',
      name: 'newspaper-detail',
      component: NewspaperDetailView
    },
    {
      path: '/printinghouses',
      name: 'printinghouses-list',
      component: PrintingHousesListView
    },
    {
      path: '/printinghouses/:id',
      name: 'printinghouse-detail',
      component: PrintingHouseDetailView
    },
    {
      path: '/postoffices',
      name: 'postoffices-list',
      component: PostOfficesListView
    },
    {
      path: '/postoffices/:id',
      name: 'postoffice-detail',
      component: PostOfficeDetailView
    },
    {
      path: '/editions',
      name: 'editions-list',
      component: EditionsListView
    },
    {
      path: '/editions/:id',
      name: 'edition-detail',
      component: EditionDetailView
    },
    {
      path: '/distributions',
      name: 'distributions-list',
      component: DistributionsListView
    },
    {
      path: '/distributions/:id',
      name: 'distribution-detail',
      component: DistributionDetailView
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: AnalyticsView,
    },
    {
      path: '/reports',
      name: 'reports',
      component: ReportsView,
    },
  ],
})

export default router
