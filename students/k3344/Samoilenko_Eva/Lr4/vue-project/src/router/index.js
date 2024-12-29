import Register from "@/components/Register.vue";
import Login from "@/components/Login.vue";
import RoomsList from "@/components/Rooms/RoomsList.vue"
import OneRoom from "@/components/Rooms/OneRoomPage.vue";
import ClientsList from "@/components/Clients/ClientsList.vue"
import OneClient from "@/components/Clients/OneClientPage.vue"
import AddClient from "@/components/Clients/AddClientPage.vue"
import ClientsSortable from "@/components/Clients/ClientsFromCity.vue"
import EmployeesList from "@/components/Employees/EmployeesList.vue"
import OneEmployee from "@/components/Employees/OneEmployeePage.vue"
import AddEmployee from "@/components/Employees/AddEmployeePage.vue"
import BookingsList from "@/components/Bookings/BookingsList.vue"
import OneBooking from "@/components/Bookings/OneBookingPage.vue"
import BookingsSortable from "@/components/Bookings/SortBookings.vue"
import AddBooking from "@/components/Bookings/AddBookingPage.vue"
import CleaningsList from "@/components/Cleanings/CleaningsList.vue"
import OneCleaning from "@/components/Cleanings/OneCleaningPage.vue"
import AddCleaning from "@/components/Cleanings/AddCleaningPage.vue"
import QuarterReport from "@/components/Reports/QuarterReport.vue"
import {createRouter, createWebHistory} from "vue-router";
import {TokenDB} from "@/tokens/TokenDB";

const routes = [
  {path: '/register', component: Register, name: "Register"},
  {path: '/login', component: Login, name: "Login"},

  {path: '/rooms', component: RoomsList, name: "Home", meta: { requiresAuth: true }},
  {path: '/rooms/:id', component: OneRoom, meta: { requiresAuth: true }},

  {path: '/clients', component: ClientsList},
  {path: '/clients/:id', component: OneClient},
  {path: '/clients/add', component: AddClient},
  {path: '/clients/sort', component: ClientsSortable},

  {path: '/employees', component: EmployeesList},
  {path: '/employees/:id', component: OneEmployee},
  {path: '/employees/add', component: AddEmployee},

  {path: '/bookings', component: BookingsList},
  {path: '/bookings/:id', component: OneBooking},
  {path: '/bookings/add', component: AddBooking},
  {path: '/bookings/sort', component: BookingsSortable},

  {path: '/cleanings', component: CleaningsList},
  {path: '/cleanings/:id', component: OneCleaning},
  {path: '/cleanings/add', component: AddCleaning},

  {path: '/report', component: QuarterReport},


]

const router = createRouter({
  history: createWebHistory(), routes
})

// const Token = TokenDB()
//
// router.beforeEach((to, from, next) => {
//   if (to.meta.requiresAuth && !Token.token) {
//     next({ name: "Login" });
//   } else if ((to.name === "Login" || to.name === "Register") && Token.token) {
//     next({ name: "Home" });
//   } else {
//     next(); // Proceed to the route
//   }
// });

export default router
