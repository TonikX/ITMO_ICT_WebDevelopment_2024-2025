import {Routes} from '@angular/router';
import {LoginComponent} from './auth/login/login.component';
import {RegisterComponent} from './auth/register/register.component';
import {AccountComponent} from './account/account.component';
import {HomeComponent} from './home/home.component';
import {NotFoundComponent} from './not-found/not-found.component';
import {ClientsComponent} from './menus/clients/clients.component';
import {RoomsComponent} from './menus/rooms/rooms.component';
import {CleaningScheduleComponent} from './menus/cleaning-schedule/cleaning-schedule.component';
import {EmployeesComponent} from './menus/employees/employees.component';
import {ReportsComponent} from './menus/reports/reports.component';
import {BookingsComponent} from './menus/bookings/bookings.component';

export const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'account', component: AccountComponent},

  {path: 'clients', component: ClientsComponent},
  {path: 'rooms', component: RoomsComponent},
  {path: 'bookings', component: BookingsComponent},
  {path: 'cleaning-schedule', component: CleaningScheduleComponent},
  {path: 'employees', component: EmployeesComponent},
  {path: 'reports', component: ReportsComponent},

  {path: '**', component: NotFoundComponent},
];
