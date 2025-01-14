import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { ReviewListComponent } from './pages/review-list/review-list.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { SubmissionListComponent } from './pages/submission-list/submission-list.component';
import { ReportComponent } from './pages/reports/reports.component';
import { TaskListComponent } from './pages/task-list/task-list.component';
import { UserListComponent } from './users/user-list/user-list.component';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'home', component: HomeComponent },
  { path: 'reviews', component: ReviewListComponent },
  { path: 'tasks', component: TaskListComponent },
  { path: 'submissions', component: SubmissionListComponent },
  { path: 'reports', component: ReportComponent },
  { path: 'users', component: UserListComponent},
];