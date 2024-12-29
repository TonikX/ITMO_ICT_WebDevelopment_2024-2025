import {createRouter, createWebHistory} from 'vue-router'
import Main from '@/views/Main.vue'
import Students from '@/views/Students.vue'
import Teachers from '@/views/Teachers.vue'
import Grades from '@/views/Grades.vue'
import Schedule from '@/views/Schedule.vue'
import Subjects from '@/views/Subjects.vue'
import Marks from '@/views/Marks.vue'
import Report from '@/views/Report.vue'
import LogIn from '@/views/LogIn.vue'
import SignUp from '@/views/SignUp.vue'

const routes = [
  {
    path: '/',
    component: Main
  },
  {
    path: '/students',
    component: Students,
    meta: { requiresAuth: true }
  },
  {
    path: '/teachers',
    component: Teachers,
    meta: { requiresAuth: true }
  },
  {
    path: '/grades',
    component: Grades,
    meta: { requiresAuth: true }
  },
  {
    path: '/schedule',
    component: Schedule,
    meta: { requiresAuth: true }
  },
  {
    path: '/subjects',
    component: Subjects,
    meta: { requiresAuth: true }
  },
  {
    path: '/marks',
    component: Marks,
    meta: { requiresAuth: true }
  },
  {
    path: '/report/:id',
    component: Report,
    meta: { requiresAuth: true }
  },
  {
    path: '/log-in',
    component: LogIn,
    name: 'Login'
  },
  {
    path: '/sign-up',
    component: SignUp
  }
]

const router = createRouter({routes, history: createWebHistory()})

export default router