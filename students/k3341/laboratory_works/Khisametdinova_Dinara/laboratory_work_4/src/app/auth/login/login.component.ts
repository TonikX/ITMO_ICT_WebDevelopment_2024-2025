import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  standalone: true,
  imports: [FormsModule, CommonModule],
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  currentUser: any = null;
  errorMessage: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  login(): void {
    this.authService.login(this.username, this.password).subscribe({
      next: (response) => {
        localStorage.setItem('auth_token', response.auth_token);
        this.authService.getCurrentUserDetails().subscribe({
          next: (user) => {
            this.currentUser = user;
            localStorage.setItem('current_user', JSON.stringify(user));
            this.router.navigate(['/home']);
          },
          error: () => {
            this.errorMessage = 'Failed to fetch user details.';
          },
        });
      },
      error: () => {
        this.errorMessage = 'Invalid username or password.';
      },
    });
  }

  navigateToHome(): void {
    this.router.navigate(['/home']);
  }
}
