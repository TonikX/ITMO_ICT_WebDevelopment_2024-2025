import { createRouter, createWebHistory } from 'vue-router'
import RegistrationView from '../views/RegistrationView.vue'
import BooksView from '../views/BooksView.vue'
import NewBookComponent from '../components/NewBook.vue'
import LoginComponent from '../components/Login.vue'
import LogoutComponent from '../components/Logout.vue'
import ReadersComponent from '../components/AllReaders.vue'
import NewReaderComponent from '../components/NewReader.vue'
import AssignmentsComponent from '../components/AllAssignments.vue'
import AssignmentDetailsComponent from '../components/AssignmentDetails.vue'
import EditAssignmentComponent from '../components/EditAssignment.vue'
import NewAssignmentComponent from '../components/NewAssignment.vue'
import HallsComponent from '../components/AllHalls.vue'
import NewHallComponent from '../components/NewHall.vue'
import CopiesComponent from '../components/AllCopies.vue'
import NewCopyComponent from '../components/NewCopy.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/registration',
      name: 'registration',
      component: RegistrationView
    },
    {
      path: '/books',
      name: 'books',
      component: BooksView
    },
    {
      path: '/books/new',
      name: 'newBook',
      component: NewBookComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginComponent,
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutComponent,
    },
    {
      path: '/readers',
      name: 'readers',
      component: ReadersComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/readers/new',
      name: 'newReader',
      component: NewReaderComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/assignments',
      name: 'Assignments',
      component: AssignmentsComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/assignments/:assignmentId',
      name: 'AssignmentDetails',
      component: AssignmentDetailsComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/assignments/:assignmentId/edit',
      name: 'EditAssignment',
      component: EditAssignmentComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/halls',
      name: 'Halls',
      component: HallsComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/copies',
      name: 'Copies',
      component: CopiesComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/assignments/new',
      name: 'newAssignment',
      component: NewAssignmentComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/halls/new',
      name: 'newHall',
      component: NewHallComponent,
      meta: { requiredAuth: true },
    },
    {
      path: '/copies/new',
      name: 'newCopy',
      component: NewCopyComponent,
      meta: { requiredAuth: true },
    },
  ]
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiredAuth && !localStorage.getItem('token')) {
    next('/login');
  }
  else {
    next();
  }
})

export default router
