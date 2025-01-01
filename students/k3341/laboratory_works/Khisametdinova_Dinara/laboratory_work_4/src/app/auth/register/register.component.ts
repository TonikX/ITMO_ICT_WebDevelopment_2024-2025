import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { trigger, transition, style, animate } from '@angular/animations';
import { CommonModule } from '@angular/common'
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  standalone: true,
  imports: [FormsModule, CommonModule],
  styleUrls: ['./register.component.css'],
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'scale(0.9)' }),
        animate('300ms ease-out', style({ opacity: 1, transform: 'scale(1)' })),
      ]),
    ]),
  ],
})
export class RegisterComponent {
  user = {
    username: '',
    email: '',
    password: '',
    re_password: '',
    role: 'student',
    first_name: '',
    last_name: '',
  };
  submitted = false;
  errorMessage: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  register() {  
    this.submitted = true;
    if (this.user.password !== this.user.re_password) {
      this.errorMessage = 'Passwords do not match!';
      return;
    }

    const userPayload = {
      username: this.user.username,
      email: this.user.email,
      password: this.user.password,
      re_password: this.user.re_password,
      role: this.user.role,
      first_name: this.user.first_name,
      last_name: this.user.last_name,
    };

    this.authService.register(userPayload).subscribe({
      next: () => {
        alert('You have successfully registered!');
        this.errorMessage = null;
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = 'Registration failed. Please try again.';
      },
    });
  }
}
