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
import { IHireEmployeeRequest } from '../types';
import { finalize } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-employee-form',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, NgIf],
  templateUrl: './employee-form.component.html',
  styleUrl: './employee-form.component.css',
})
export class EmployeeFormComponent {
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
    hireDate: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
  });

  readonly isLoading = signal<boolean>(false);
  readonly successMessage = signal<string>('');
  readonly errorMessage = signal<string>('');

  constructor(
    private readonly router: Router,
    private readonly hotelService: HotelService
  ) {}

  submit(event: Event) {
    event.preventDefault();
    if (this.form.invalid) {
      return;
    }

    const data: IHireEmployeeRequest = {
      first_name: this.firstNameControl.value,
      last_name: this.lastNameControl.value,
      patronymic: this.patronymicControl.value,
      hire_date: this.hireDateControl.value,
    };

    this.isLoading.set(true);
    this.hotelService
      .hireEmployee(data)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: () => this.successMessage.set('Работник успешно нанят'),
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

  get hireDateControl() {
    return this.form.controls.hireDate;
  }
}
