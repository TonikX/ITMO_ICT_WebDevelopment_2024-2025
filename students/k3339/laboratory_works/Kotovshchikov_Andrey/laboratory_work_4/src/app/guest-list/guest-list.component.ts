import { Component, OnInit, signal } from '@angular/core';
import { IGuest } from '../types';
import { HotelService } from '../hotel.service';
import { finalize } from 'rxjs';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-guest-list',
  standalone: true,
  imports: [NgIf],
  templateUrl: './guest-list.component.html',
  styleUrl: './guest-list.component.css',
})
export class GuestListComponent implements OnInit {
  guests: IGuest[] = [];

  readonly isLoading = signal<boolean>(false);
  readonly errorMessage = signal<string>('');

  constructor(private readonly hotelService: HotelService) {}

  ngOnInit(): void {
    this.loadGuests();
  }

  filterGuestsByCity(city: string) {
    this.isLoading.set(true);
    this.hotelService
      .filterGuestsByCity(city)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (data) => {
          this.guests = data.guests;
        },
      });
  }

  private loadGuests() {
    this.isLoading.set(true);
    this.hotelService
      .getGuests()
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (data) => {
          this.guests = data.guests;
        },
      });
  }
}
