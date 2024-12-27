import {createRouter, createWebHistory} from 'vue-router';
import LoginForm from '@/components/LoginForm.vue';
import RegisterForm from '@/components/RegisterForm.vue';
import Dashboard from '@/views/Dashboard.vue';
import EmployeeDashboard from '@/views/EmployeeDashboard.vue';
import DirectorDashboard from '@/views/DirectorDashboard.vue';
import AgentDashboard from '@/views/AgentDashboard.vue';
import AuthService from '@/services/AuthService';
import UserService from '@/services/UserService';
import ChangePassword from '@/views/ChangePassword.vue';
import EditProfile from '@/views/EditProfile.vue';
import EditEmployee from "@/views/EditEmployee.vue";
import EmployeeList from '@/views/EmployeeList.vue';
import InsuranceCases from '@/views/InsuranceCases.vue';
import ProcessInsuranceCase from '@/views/ProcessInsuranceCase.vue';
import ContractList from '@/views/ContractList.vue';

const routes = [
    {path: '/login', component: LoginForm},
    {path: '/register', component: RegisterForm},
    {
        path: '/profile/edit',
        component: EditProfile,
        meta: {requiresAuth: true},
    },
    {
        path: '/dashboard',
        component: Dashboard,
        meta: {requiresAuth: true},
    },
    {
        path: '/employee-dashboard',
        component: EmployeeDashboard,
        meta: {requiresAuth: true, roles: ['employee']},
    },
    {
        path: '/director-dashboard',
        component: DirectorDashboard,
        meta: {requiresAuth: true, roles: ['org_admin']},
    },
    {
        path: '/agent-dashboard',
        component: AgentDashboard,
        meta: {requiresAuth: true, roles: ['agent']},
    },
    {
        path: '/profile/change-password',
        component: ChangePassword,
        meta: {requiresAuth: true},

    },
    {path: '/employees', component: EmployeeList},
    {path: '/employees/:id/edit', component: EditEmployee, props: true},
    {path: '/insurance-cases', component: InsuranceCases, meta: {requiresAuth: true}},
    {path: '/insurance-cases/:id/process', component: ProcessInsuranceCase, meta: {requiresAuth: true}},
    {path: '/contracts', component: ContractList, meta: {requiresAuth: true}},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    const token = localStorage.getItem('token');

    // Если маршрут требует авторизации
    if (to.meta.requiresAuth) {
        if (!token) {
            // Если токена нет, отправляем на страницу логина
            next('/login');
        } else {
            try {
                // Проверяем роль пользователя
                const user = await UserService.getProfile();
                const allowedRoles = to.meta.roles || [];

                // Если для маршрута указаны роли, проверяем их
                if (allowedRoles.length && !allowedRoles.includes(user.role)) {
                    alert('У вас нет доступа к этой странице');
                    next('/dashboard'); // Перенаправляем на общий дэшборд
                } else {
                    next(); // Если роль подходит, продолжаем
                }
            } catch (error) {
                console.error('Ошибка при проверке пользователя:', error);
                AuthService.logout();
                next('/login');
            }
        }
    } else {
        next();  // Если маршрут не требует авторизации, продолжаем
    }
});

export default router;
