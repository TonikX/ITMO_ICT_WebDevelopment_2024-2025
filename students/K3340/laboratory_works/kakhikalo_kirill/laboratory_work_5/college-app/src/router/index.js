import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TeachersView from '@/views/TeachersView.vue'
import TeacherDetail from '@/views/TeacherDetail.vue'
import AcademicDisciplines from '@/views/AcademicDisciplines.vue'
import ClassroomsView from '@/views/ClassroomsView.vue'
import GroupsView from '@/views/GroupsView.vue'
import ScheduleView from '@/views/ScheduleView.vue'
import GradeReport from '@/views/GradeReport.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    { path: '/teachers', name: 'TeachersView', component: TeachersView },
    { path: '/teachers/:id', name: 'TeacherDetail', component: TeacherDetail, props: true },
    { path: '/disciplines', name: 'AcademicDisciplines', component: AcademicDisciplines },
    { path: '/classrooms', name: 'ClassroomsView', component: ClassroomsView },
    { path: '/groups', name: 'GroupsView', component: GroupsView },
    { path: '/schedule', name: 'ScheduleView', component: ScheduleView },
    { path: '/grade-report', name: 'GradeReport', component: GradeReport },
    { path: '/login', name: 'LoginView', component: LoginView },
    { path: '/register', name: 'RegisterView', component: RegisterView },
  ],
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login']  // pages that don't require auth
  const authRequired = !publicPages.includes(to.path)
  const token = localStorage.getItem('authToken')

  if (authRequired && !token) {
    return next('/login')
  }
  next()
})

export default router
