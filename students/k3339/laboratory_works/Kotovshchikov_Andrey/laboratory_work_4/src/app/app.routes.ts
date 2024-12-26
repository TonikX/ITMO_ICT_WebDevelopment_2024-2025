import { Routes } from '@angular/router';
import { SignInComponent } from './sign-in/sign-in.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { ReportComponent } from './report/report.component';
import { EmployeeListComponent } from './employee-list/employee-list.component';
import { RoomListComponent } from './room-list/room-list.component';
import { GuestListComponent } from './guest-list/guest-list.component';
import { EmployeeDetailComponent } from './employee-detail/employee-detail.component';
import { GuestFormComponent } from './guest-form/guest-form.component';
import { EmployeeFormComponent } from './employee-form/employee-form.component';
import { isAuthGuard } from './auth.guard';

export const routes: Routes = [
  { path: 'sign-up', component: SignUpComponent },
  { path: 'sign-in', component: SignInComponent },
  { path: 'reports', component: ReportComponent, canActivate: [isAuthGuard] },
  {
    path: 'employees',
    canActivate: [isAuthGuard],
    children: [
      { path: '', component: EmployeeListComponent },
      { path: 'add', component: EmployeeFormComponent },
    ],
  },
  { path: 'rooms', component: RoomListComponent, canActivate: [isAuthGuard] },
  {
    path: 'guests',
    canActivate: [isAuthGuard],
    children: [
      { path: '', component: GuestListComponent },
      { path: 'add', component: GuestFormComponent },
    ],
  },
  {
    path: 'employees/:id',
    component: EmployeeDetailComponent,
    canActivate: [isAuthGuard],
  },
  { path: '**', redirectTo: 'reports' },
];
