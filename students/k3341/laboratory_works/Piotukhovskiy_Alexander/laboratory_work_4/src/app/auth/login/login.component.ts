import {Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {environment} from '../../environment';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  imports: [FormsModule, CommonModule],
})
export class LoginComponent {
  credentials = {username: '', password: ''};
  errorMessage: string | null = null;
  isSubmitting = false;

  constructor(private http: HttpClient, private router: Router) {
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.router.navigate(['/']);
    }
  }


  login() {
    this.errorMessage = null;
    this.isSubmitting = true;

    this.http.post<{ auth_token: string }>(`${environment.apiUrl}/auth/token/login/`, this.credentials).subscribe({
      next: (response) => {
        localStorage.setItem('auth_token', response.auth_token);

        this.http
          .get(`${environment.apiUrl}/auth/users/me/`)
          .subscribe((userData: any) => {
            localStorage.setItem('first_name', userData.first_name);
            localStorage.setItem('last_name', userData.last_name);
            localStorage.setItem('username', userData.username);
            localStorage.setItem('email', userData.email);
          });
        this.isSubmitting = false;
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.isSubmitting = false;
        if (err.status === 400 && err.error?.non_field_errors) {
          this.errorMessage = err.error.non_field_errors[0];
        } else {
          this.errorMessage = 'Произошла ошибка. Попробуйте ещё раз.';
        }
      },
    });
  }

  goToRegister() {
    this.router.navigate(['/register']);
  }
}
