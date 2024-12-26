import { Component, OnInit, signal } from '@angular/core';
import { IEmployeeDetail, ISchedule, Weekdays } from '../types';
import { FormsModule } from '@angular/forms';
import { HotelService } from '../hotel.service';
import { ActivatedRoute } from '@angular/router';
import { finalize } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-employee-detail',
  standalone: true,
  imports: [FormsModule, NgIf],
  templateUrl: './employee-detail.component.html',
  styleUrl: './employee-detail.component.css',
})
export class EmployeeDetailComponent implements OnInit {
  employee: IEmployeeDetail;
  readonly floor: number;
  readonly weekDay: Weekdays = 'пн';

  readonly isLoading = signal<boolean>(false);
  readonly errorMessage = signal<string>('');

  constructor(
    private readonly router: ActivatedRoute,
    private readonly hotelService: HotelService
  ) {}

  ngOnInit(): void {
    const employeeId = Number.parseInt(
      <string>this.router.snapshot.paramMap.get('id')
    );

    this.loadEmployee(employeeId);
  }

  createEmployeeSchedule(event: Event) {
    event.preventDefault();
    if (!this.floor || !this.weekDay) {
      return;
    }

    const data: ISchedule = {
      week_day: this.weekDay,
      floor: this.floor,
    };

    this.errorMessage.set('');
    this.isLoading.set(true);
    this.hotelService.createEmployeeSchedule(this.employee.id, data).subscribe({
      next: () => this.loadEmployee(this.employee.id),
      error: (err: HttpErrorResponse) => {
        console.log(err.error);
        if ('detail' in err.error) {
          this.errorMessage.set(err.error['detail']);
        } else {
          this.errorMessage.set('Что то пошло не так, повторите позже');
        }

        this.isLoading.set(false);
      },
    });
  }

  resetEmployeeSchedule() {
    this.errorMessage.set('');
    this.isLoading.set(true);
    this.hotelService.resetEmployeeSchedule(this.employee.id).subscribe({
      next: () => this.loadEmployee(this.employee.id),
      error: (err: HttpErrorResponse) => {
        console.log(err.error);
        this.errorMessage.set('Что то пошло не так, повторите позже');
        this.isLoading.set(false);
      },
    });
  }

  dismissEmployee(event: Event) {
    event.preventDefault();
    if (!this.employee.dismissal_date) {
      return;
    }

    this.errorMessage.set('');
    this.isLoading.set(true);
    this.hotelService
      .updateEmployee(this.employee.id, this.employee)
      .subscribe({
        next: () => this.loadEmployee(this.employee.id),
      });
  }

  private loadEmployee(employeeId: number) {
    this.isLoading.set(true);
    this.hotelService
      .getEmployeeDetail(employeeId)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (data) => {
          this.employee = data;
          console.log(this.employee);
        },
      });
  }
}
