import { NgIf } from '@angular/common';
import { Component, effect, input, signal } from '@angular/core';
import { HotelService } from '../hotel.service';
import { finalize } from 'rxjs';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ICreateBookingRequest } from '../types';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'room-booking-modal',
  standalone: true,
  imports: [NgIf, FormsModule, ReactiveFormsModule],
  templateUrl: './room-booking.component.html',
  styleUrl: './room-booking.component.css',
})
export class RoomBookingComponent {
  form = new FormGroup({
    guestPassport: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
    checkOutDate: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
  });

  readonly roomId = input.required<number>();
  readonly isModalOpen = input.required<boolean>();
  readonly isLoading = signal<boolean>(false);
  readonly errorMessage = signal<string>('');
  readonly successMessage = signal<string>('');

  constructor(private readonly hotelService: HotelService) {
    effect(
      () => {
        this.isModalOpen();
        this.clearMessages();
      },
      { allowSignalWrites: true }
    );
  }

  createBooking(event: Event) {
    event.preventDefault();
    if (this.form.invalid) {
      return;
    }

    const data: ICreateBookingRequest = {
      guest_passport: this.form.controls.guestPassport.value,
      check_out_date: this.form.controls.checkOutDate.value,
    };

    this.clearMessages();
    this.isLoading.set(true);
    this.hotelService
      .createBooking(this.roomId(), data)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: () => this.successMessage.set('Клиент заселен'),
        error: (err: HttpErrorResponse) => {
          console.log(err);
          if ('detail' in err.error) {
            this.errorMessage.set(err.error['detail']);
          } else {
            this.errorMessage.set('Что то пошло не так, повторите позже');
          }
        },
      });
  }

  vacateRoom() {
    this.clearMessages();
    this.isLoading.set(true);
    this.hotelService
      .vacateRoom(this.roomId())
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: () => this.successMessage.set('Номер освобожден'),
      });
  }

  private clearMessages() {
    this.successMessage.set('');
    this.errorMessage.set('');
  }
}
