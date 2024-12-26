import { Component, signal } from '@angular/core';
import { IReport } from '../types';
import { HotelService } from '../hotel.service';
import { finalize } from 'rxjs';
import { NgFor, NgIf } from '@angular/common';

@Component({
  selector: 'app-report',
  standalone: true,
  imports: [NgIf],
  templateUrl: './report.component.html',
  styleUrl: './report.component.css',
})
export class ReportComponent {
  private report: IReport;
  readonly quarter = signal<number>(1);
  readonly isLoading = signal<boolean>(false);
  readonly isReportGenerated = signal<boolean>(false);

  constructor(private readonly hotelService: HotelService) {}

  generateReport(event: Event) {
    event.preventDefault();

    this.isReportGenerated.set(false);
    this.isLoading.set(true);
    this.hotelService
      .generateReport(this.quarter())
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (data) => {
          console.log(data);
          this.report = data;
          this.isReportGenerated.set(true);
        },
      });
  }

  onQuarterChange(event: Event) {
    const selectQuarter = event.target as HTMLSelectElement;
    this.quarter.set(parseInt(selectQuarter.value, 10));
  }

  get guestsPerRoom() {
    return Object.entries(this.report.guests_per_room);
  }

  get roomsPerFloor() {
    return Object.entries(this.report.rooms_per_floor);
  }

  get profitPerRoom() {
    return Object.entries(this.report.profit_per_room);
  }

  get totalProfit() {
    return this.report.total_profit;
  }
}
