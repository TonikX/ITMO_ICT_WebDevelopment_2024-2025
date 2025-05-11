import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Router} from '@angular/router';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {environment} from '../../environment';

@Component({
  selector: 'app-rooms',
  standalone: true,
  templateUrl: './rooms.component.html',
  styleUrls: ['./rooms.component.css'],
  imports: [CommonModule, FormsModule],
})
export class RoomsComponent implements OnInit {
  appName: string = environment.appName;
  username: string | null = null;
  rooms: any[] = [];
  filteredRooms: any[] = [];
  statuses: { value: string; label: string }[] = [
    {value: 'AVAILABLE', label: 'Свободна'},
    {value: 'OCCUPIED', label: 'Занята'},
    {value: 'REQUIRES_CLEANING', label: 'Требует уборки'},
    {value: 'CLEANING_IN_PROGRESS', label: 'Уборка в процессе'},
    {value: 'MAINTENANCE', label: 'На обслуживании'},
  ];
  selectedStatus: string | null = null;
  detailMessage: string | null = null;

  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }
    this.username = localStorage.getItem('username');
    this.loadRooms();
  }

  loadRooms() {
    let params = new HttpParams();
    if (this.selectedStatus && this.selectedStatus != "null") {
      params = params.set('status', this.selectedStatus);
    }

    this.http
      .get(`${environment.apiUrl}/hotel/rooms`, {
        params: params,
      })
      .subscribe({
        next: (data: any) => {
          this.rooms = data.rooms;
          this.filteredRooms = [...this.rooms];
          this.detailMessage = null;
        },
        error: (err) => {
          console.error('Ошибка загрузки комнат:', err);
          this.rooms = [];
          this.filteredRooms = [];
          this.detailMessage = 'Не удалось загрузить список комнат.';
        },
      });
  }

  filterRooms() {
    this.loadRooms();
  }

  createBooking(room: any) {
    this.router.navigate(['/bookings'], {queryParams: {room_number: room.number}});
  }

  checkOut(room: any) {
    this.http
      .patch(`${environment.apiUrl}/hotel/api/rooms/${room.number}/checkout`, {})
      .subscribe({
        next: (updatedRoom: any) => {
          this.rooms = this.rooms.map((r) => (r.number === updatedRoom.number ? updatedRoom : r));
          this.filterRooms();
        },
        error: (err) => {
          console.error('Ошибка при выселении клиента:', err);
        },
      });
  }

  navigateTo(route: string) {
    this.router.navigate([`/${route}`]);
  }

  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('first_name');
    localStorage.removeItem('last_name');
    localStorage.removeItem('username');
    localStorage.removeItem('email');
    this.router.navigate(['/login']);
  }
}
