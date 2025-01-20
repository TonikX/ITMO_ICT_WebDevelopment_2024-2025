import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/views/LoginPage.vue';
import Specializations from '@/views/specializations.vue'
import Enterprises from '@/views/Enterprises.vue'
import Clients from '@/views/Clients.vue'
import Contracts from '@/views/Contracts.vue'
import ContractDetails from '@/views/ContractDetails.vue'
import Account from '@/views/Account.vue'
import EditUser from '@/views/EditUser.vue'
import Registration from '@/views/Registration.vue'
import Main from '@/views/Main.vue'
import EditContract from '@/views/EditContract.vue'
import EnterprisePayouts from '@/views/EnterprisesPayouts.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },

    {
      path: '/payouts',
      name: 'payouts',
      component: EnterprisePayouts,
    },

    {
      path: '/specialization',
      name: 'specialization',
      component: Specializations
    },

    {
      path: '/enterprises',
      name: 'enterprises',
      component: Enterprises
    },

    {
      path: '/clients',
      name: 'clients',
      component: Clients
    },

    {
      path: '/',
      component: Main
    },

    {
      path: '/account',
      name: 'account',
      component: Account
    },

    {
      path: '/reg',
      name: 'reg',
      component: Registration
    },

    {
      path: '/edit-user',
      name: 'edit-user',
      component: EditUser
    },

    {
      path: '/contracts',
      name: 'contracts',
      component: Contracts
    },

    {
      path: '/contract/:contractNumber',
      name: 'contract-details',
      component: ContractDetails,
      props: true,
    },

    {
      path: '/edit-contract/:contractNumber',
      name: 'edit-contract',
      component: EditContract,
      props: true,
    },
  ]
})

export default router
