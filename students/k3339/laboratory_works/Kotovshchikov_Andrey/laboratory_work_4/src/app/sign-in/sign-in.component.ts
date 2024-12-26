import { NgIf } from '@angular/common';
import { Component, signal } from '@angular/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../auth.service';
import { finalize } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { ISignInRequest } from '../types';

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, NgIf, RouterLink],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css',
})
export class SignInComponent {
  form = new FormGroup({
    email: new FormControl('', {
      nonNullable: true,
      validators: [
        Validators.required,
        Validators.email,
        Validators.maxLength(70),
      ],
    }),
    password: new FormControl('', {
      nonNullable: true,
      validators: [
        Validators.required,
        Validators.minLength(8),
        Validators.maxLength(100),
      ],
    }),
  });

  readonly isLoading = signal<boolean>(false);
  readonly errorMessage = signal<string>('');

  constructor(
    private readonly router: Router,
    private readonly authService: AuthService
  ) {}

  submit(event: Event) {
    event.preventDefault();
    if (this.form.invalid) {
      return;
    }

    const data: ISignInRequest = {
      email: this.emailControl.value,
      password: this.passwordControl.value,
    };

    this.isLoading.set(true);
    this.authService
      .signIn(data)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: () => this.router.navigateByUrl('/'),
        error: (err: HttpErrorResponse) => {
          console.log(err.error);
          if (err.status === 400) {
            this.errorMessage.set('Неверный логин или пароль');
          } else {
            this.errorMessage.set('Что то пошло не так, повторите позже');
          }
        },
      });
  }

  get emailControl() {
    return this.form.controls.email;
  }

  get passwordControl() {
    return this.form.controls.password;
  }
}
