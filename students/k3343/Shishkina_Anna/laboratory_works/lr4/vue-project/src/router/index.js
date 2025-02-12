import { createRouter, createWebHistory } from 'vue-router'
import Register from "@/views/Register.vue";
import Login from "@/views/Login.vue";
import HomePage from "@/views/HomePage.vue";
import TeacherList from "@/views/TeacherList.vue";
import StudentList from "@/views/StudentList.vue";
import Schedule from "@/views/Schedule.vue";
import ClassReport from "@/views/ClassReport.vue";
import Grades from "@/views/Grades.vue";
import TeacherSubject from "@/views/TeacherSubject.vue";
import StudentClasses from "@/views/StudentClasses.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/home-page',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/teachers-list',
      name: 'TeacherList',
      component: TeacherList,
    },
    {
      path: '/student-list',
      name: 'StudentList',
      component: StudentList,
    },
    {
      path: '/schedule',
      name: 'Schedule',
      component: Schedule,
    },
    {
      path: '/class-report',
      name: 'ClassReport',
      component: ClassReport,
    },
    {
      path: '/grades',
      name: 'Grades',
      component: Grades,
    },
    {
      path: '/teachersubject',
      name: 'TeacherSubject',
      component: TeacherSubject,
    },
    {
      path: '/classes',
      name: 'StudentClasses',
      component: StudentClasses,
    }
  ],
})

export default router
