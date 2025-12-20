import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Views
import LoginView from '@/views/Login.vue'
import DashboardView from '@/views/Dashboard.vue'
import GroupsView from '@/views/GroupList.vue'
import GroupStudentsView from '@/views/GroupStudents.vue'
import ScheduleView from '@/views/GroupSchedule.vue'
import StudentsView from '@/views/Students.vue'
import StudentGradesView from '@/views/Grades.vue'
import StudentStatsView from '@/views/StudentsStats.vue'

import ClassroomsView from '@/views/Classrooms.vue'
import TeachersView from '@/views/Teachers.vue'
import SubjectsView from '@/views/Subjects.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },

  // Группы
  {
    path: '/groups',
    name: 'Groups',
    component: GroupsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/groups/:groupId/students',
    name: 'GroupStudents',
    component: GroupStudentsView,
    meta: { requiresAuth: true }
  },

  // Студенты
  {
    path: '/students',
    name: 'Students',
    component: StudentsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/students/:id/grades',
    name: 'StudentGrades',
    component: StudentGradesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/students/:id/stats',
    name: 'StudentStats',
    component: StudentStatsView,
    meta: { requiresAuth: true }
  },

  // Расписание
  {
    path: '/schedule/group/:group_id',
    name: 'Schedule',
    component: ScheduleView,
    meta: { requiresAuth: true }
  },
  {
    path: '/groups/:groupId/schedule',
    name: 'GroupSchedule',
    component: ScheduleView,
    meta: { requiresAuth: true }
  },

  // Оценки
  {
    path: '/grades',
    name: 'Grades',
    component: StudentGradesView,
    meta: { requiresAuth: true }
  },

  // Кабинеты
  {
    path: '/classrooms',
    name: 'Classrooms',
    component: ClassroomsView,
    meta: { requiresAuth: true }
  },

  // Преподаватели
  {
    path: '/teachers',
    name: 'Teachers',
    component: TeachersView,
    meta: { requiresAuth: true }
  },

  // Дисциплины
  {
    path: '/subjects',
    name: 'Subjects',
    component: SubjectsView,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Навигационные хуки
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router