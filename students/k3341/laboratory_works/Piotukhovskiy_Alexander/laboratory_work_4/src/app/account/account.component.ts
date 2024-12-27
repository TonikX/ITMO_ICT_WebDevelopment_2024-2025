import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {environment} from '../environment';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-account',
  standalone: true,
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.css'],
  imports: [CommonModule],
})
export class AccountComponent implements OnInit {
  user: any;

  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }

    this.http
      .get(`${environment.apiUrl}/auth/users/me/`)
      .subscribe({
        next: (data: any) => {
          this.user = data;
          localStorage.setItem('first_name', data.first_name);
          localStorage.setItem('last_name', data.last_name);
          localStorage.setItem('username', data.username);
          localStorage.setItem('email', data.email);
        },
        error: (err) => {
          console.error('Ошибка при загрузке профиля:', err);
        },
      });
  }

  goToHome() {
    this.router.navigate(['/']);
  }

  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('first_name');
    localStorage.removeItem('last_name');
    localStorage.removeItem('username');
    localStorage.removeItem('email');
    this.router.navigate(['/login']);
  }
}
