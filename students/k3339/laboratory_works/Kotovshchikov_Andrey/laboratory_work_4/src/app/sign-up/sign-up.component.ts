import { NgIf } from '@angular/common';
import { Component, signal } from '@angular/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { AuthService } from '../auth.service';
import { finalize } from 'rxjs';
import { Router, RouterLink } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { ISignUpRequest } from '../types';

@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, NgIf, RouterLink],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.css',
  providers: [AuthService],
})
export class SignUpComponent {
  form = new FormGroup({
    firstName: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.maxLength(70)],
    }),
    lastName: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.maxLength(70)],
    }),
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

    const data: ISignUpRequest = {
      first_name: this.firstNameControl.value,
      last_name: this.lastNameControl.value,
      email: this.emailControl.value,
      password: this.passwordControl.value,
    };

    this.isLoading.set(true);
    this.authService
      .signUp(data)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: () => this.router.navigateByUrl('/sign-in'),
        error: (err: HttpErrorResponse) => {
          if ('email' in err.error) {
            this.errorMessage.set('Администратор с таким email уже существует');
          } else {
            this.errorMessage.set('Что то пошло не так, повторите позже');
          }
        },
      });
  }

  get firstNameControl() {
    return this.form.controls.firstName;
  }

  get lastNameControl() {
    return this.form.controls.lastName;
  }

  get emailControl() {
    return this.form.controls.email;
  }

  get passwordControl() {
    return this.form.controls.password;
  }
}
