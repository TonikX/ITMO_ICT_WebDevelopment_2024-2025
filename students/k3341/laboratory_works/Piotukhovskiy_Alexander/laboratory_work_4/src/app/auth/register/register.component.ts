import {Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import {environment} from '../../environment';

@Component({
  selector: 'app-register',
  standalone: true,
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  imports: [FormsModule, CommonModule],
})
export class RegisterComponent {
  user = {username: '', password: '', first_name: '', last_name: '', email: ''};
  isSubmitting = false;
  errors: { [key: string]: string[] } = {};

  constructor(private http: HttpClient, private router: Router) {
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.router.navigate(['/']);
    }
  }

  register() {
    this.isSubmitting = true;
    this.errors = {};

    this.http.post(`${environment.apiUrl}/auth/users/`, this.user).subscribe({
      next: () => {
        this.loginAfterRegister();
      },
      error: (err) => {
        this.isSubmitting = false;
        if (err.status === 400 && err.error) {
          this.errors = err.error;
        } else {
          this.errors = {general: ['Произошла ошибка. Попробуйте ещё раз.']};
        }
      },
    });
  }

  private loginAfterRegister() {
    const credentials = {username: this.user.username, password: this.user.password};
    this.http.post<{ auth_token: string }>(`${environment.apiUrl}/auth/token/login/`, credentials).subscribe({
      next: (response) => {
        localStorage.setItem('auth_token', response.auth_token);
        this.isSubmitting = false;
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.isSubmitting = false;
        this.errors = {general: ['Не удалось выполнить автоматическую авторизацию. Пожалуйста, войдите вручную.']};
        console.error('Ошибка авторизации после регистрации:', err);
      },
    });
  }

  goToLogin() {
    this.router.navigate(['/login']);
  }
}
