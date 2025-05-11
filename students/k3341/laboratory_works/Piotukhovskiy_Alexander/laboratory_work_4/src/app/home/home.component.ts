import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {environment} from '../environment';
import {HttpClient} from '@angular/common/http';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  imports: [CommonModule],
})
export class HomeComponent implements OnInit {
  username: string | null = null;
  appName: string = environment.appName;

  sections = [
    {title: 'Клиенты', route: 'clients'},
    {title: 'Комнаты', route: 'rooms'},
    {title: 'Бронирование', route: 'bookings'},
    {title: 'Расписание уборок', route: 'cleaning-schedule'},
    {title: 'Сотрудники', route: 'employees'},
    {title: 'Отчёты', route: 'reports'},
  ];


  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }

    this.http
      .get<{ username: string }>(`${environment.apiUrl}/auth/users/me/`)
      .subscribe({
        next: (data: any) => {
          this.username = localStorage.getItem('username');
        },
        error: () => {
          localStorage.removeItem('auth_token');
          this.router.navigate(['/login']);
        },
      });
  }

  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('first_name');
    localStorage.removeItem('last_name');
    localStorage.removeItem('username');
    localStorage.removeItem('email');
    this.router.navigate(['/login']);
  }

  navigateTo(route: string) {
    this.router.navigate([`/${route}`]);
  }
}
