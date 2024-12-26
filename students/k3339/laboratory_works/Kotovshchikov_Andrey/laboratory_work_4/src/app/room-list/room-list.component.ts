import { Component, OnInit, signal } from '@angular/core';
import { IRoom } from '../types';
import { HotelService } from '../hotel.service';
import { finalize } from 'rxjs';
import { NgIf } from '@angular/common';
import { RoomBookingComponent } from '../room-booking/room-booking.component';

@Component({
  selector: 'app-room-list',
  standalone: true,
  imports: [NgIf, RoomBookingComponent],
  templateUrl: './room-list.component.html',
  styleUrl: './room-list.component.css',
})
export class RoomListComponent implements OnInit {
  rooms: IRoom[] = [];
  total: number = 0;

  readonly isLoading = signal<boolean>(false);
  readonly isOnlyAvailable = signal<boolean>(false);
  readonly selectedRoomId = signal<number | null>(null);

  constructor(private readonly hotelService: HotelService) {}

  ngOnInit(): void {
    this.loadRooms();
  }

  openModal(roomId: number) {
    this.selectedRoomId.set(roomId);
  }

  closeModal(event: Event) {
    const target = event.target as HTMLElement;
    if (target.classList.contains('modal')) {
      this.selectedRoomId.set(null);
    }
  }

  changeIsOnlyAvailable() {
    this.isOnlyAvailable.set(!this.isOnlyAvailable());
    if (this.isOnlyAvailable()) {
      this.loadOnlyAvailableRooms();
    } else {
      this.loadRooms();
    }
  }

  private loadRooms() {
    this.isLoading.set(true);
    this.hotelService
      .getRooms()
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe((data) => {
        this.total = data.total;
        this.rooms = data.rooms;
      });
  }

  private loadOnlyAvailableRooms() {
    this.isLoading.set(true);
    this.hotelService
      .getAvailableRooms()
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe((data) => {
        this.total = data.total;
        this.rooms = data.rooms;
      });
  }
}
