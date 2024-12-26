import { Component, OnInit, signal } from '@angular/core';
import { IEmployee } from '../types';
import { Router } from '@angular/router';
import { NgIf } from '@angular/common';
import { HotelService } from '../hotel.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-employee-list',
  standalone: true,
  imports: [NgIf],
  templateUrl: './employee-list.component.html',
  styleUrl: './employee-list.component.css',
})
export class EmployeeListComponent implements OnInit {
  employees: IEmployee[] = [];
  readonly isLoading = signal<boolean>(false);

  constructor(
    private readonly router: Router,
    private readonly hotelService: HotelService
  ) {}

  ngOnInit(): void {
    this.loadEmployees();
  }

  navigateToDetail(employeeId: number) {
    this.router.navigateByUrl(`/employees/${employeeId}`);
  }

  private loadEmployees() {
    this.isLoading.set(true);
    this.hotelService
      .getEmployees()
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (data) => {
          this.employees = data.employees;
        },
      });
  }
}
