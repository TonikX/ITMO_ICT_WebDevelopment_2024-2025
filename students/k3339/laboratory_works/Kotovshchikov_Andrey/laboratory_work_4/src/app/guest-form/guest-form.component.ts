import { NgIf } from '@angular/common';
import { Component, signal } from '@angular/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { HotelService } from '../hotel.service';
import { IAddGuestRequest } from '../types';
import { finalize } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-guest-form',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, NgIf],
  templateUrl: './guest-form.component.html',
  styleUrl: './guest-form.component.css',
})
export class GuestFormComponent {
  form = new FormGroup({
    firstName: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.maxLength(70)],
    }),
    lastName: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.maxLength(70)],
    }),
    patronymic: new FormControl(null, {
      nonNullable: false,
      validators: [Validators.maxLength(70)],
    }),
    passport: new FormControl('', {
      nonNullable: true,
      validators: [],
    }),
    city: new FormControl('', {
      nonNullable: true,
      validators: [],
    }),
  });

  readonly isLoading = signal<boolean>(false);
  readonly errorMessage = signal<string>('');

  constructor(
    private readonly router: Router,
    private readonly hotelService: HotelService
  ) {}

  submit(event: Event) {
    if (this.form.invalid) {
      return;
    }

    const data: IAddGuestRequest = {
      first_name: this.firstNameControl.value,
      last_name: this.lastNameControl.value,
      patronymic: this.patronymicControl.value,
      passport: this.passportControl.value,
      city: this.cityControl.value,
    };

    this.isLoading.set(true);
    this.hotelService
      .addGuest(data)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: () => this.router.navigateByUrl('/guests'),
        error: (err: HttpErrorResponse) => {
          console.log(err.error);
          if ('detail' in err.error) {
            this.errorMessage.set(err.error['detail']);
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

  get patronymicControl() {
    return this.form.controls.patronymic;
  }

  get passportControl() {
    return this.form.controls.passport;
  }

  get cityControl() {
    return this.form.controls.city;
  }
}
