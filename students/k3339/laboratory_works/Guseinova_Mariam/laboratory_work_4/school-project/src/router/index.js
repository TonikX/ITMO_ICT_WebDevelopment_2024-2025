import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue';
import StudentList from '@/views/StudentList.vue';
import StudentDetail from '@/views/StudentDetail.vue';
import TeachersList from '@/views/TeachersList.vue';
import TeacherDetail from '@/views/TeacherDetail.vue';
import RoomsList from '@/views/RoomsList.vue';
import Lessons from '@/views/Lessons.vue';
import Grades from '@/views/Grades.vue';
import RegistrationView from '@/views/RegistrationView.vue';
import HomeView from '@/views/HomeView.vue';
import Report from '@/views/Report.vue';

const routes = [
  { path: '/home', name: 'Home', component: HomeView },
  { path: '/register', name: 'Registration', component: RegistrationView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/students', name: 'StudentList', component: StudentList, meta: { requiresAuth: true } },
  { path: '/students/:id', name: 'StudentDetail', component: StudentDetail, props: true, meta: { requiresAuth: true } },
  { path: '/teachers', name: 'TeachersList', component: TeachersList, meta: { requiresAuth: true } },
  { path: '/teachers/:id', name: 'TeacherDetail', component: TeacherDetail, props: true, meta: { requiresAuth: true } },
  { path: '/rooms', name: 'RoomsList', component: RoomsList, meta: { requiresAuth: true } },
  { path: '/lessons', name: 'Lessons', component: Lessons, meta: { requiresAuth: true } },
  { path: '/grades', name: 'Grades', component: Grades, meta: { requiresAuth: true } },
  { path: '/report', name: 'Report', component: Report, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('authToken');
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Login' });
    } else {
      next();
    }
  } else {
    next();
  }
});
export default router;
