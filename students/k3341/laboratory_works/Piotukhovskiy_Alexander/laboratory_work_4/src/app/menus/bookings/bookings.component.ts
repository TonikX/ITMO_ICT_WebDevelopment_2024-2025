import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { environment } from '../../environment';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-bookings',
  standalone: true,
  templateUrl: './bookings.component.html',
  styleUrls: ['./bookings.component.css'],
  imports: [CommonModule, FormsModule],
})
export class BookingsComponent implements OnInit {


  appName: string = environment.appName;
  username: string | null = null;

  bookings: any[] = [];
  filteredBookings: any[] = [];
  filters: {
    roomType: string | null;
    arrivalDate: string | null;
    departureDate: string | null;
  } = {
    roomType: null,
    arrivalDate: null,
    departureDate: null,
  };

  searchQuery: string = ''; // Для поиска
  roomTypes: string[] = [];

  page: number = 1;
  itemsPerPage: number = 3;

  showEditBookingForm: boolean = false;
  currentBooking: any = {}; // Для редактирования брони
  originalBooking: any = {}; // Исходные данные брони для сравнения

  showAddBookingForm: boolean = false;
  newBooking: any = {
    passport_number: '',
    first_name: '',
    last_name: '',
    middle_name: '',
    city_from: '',
    room_number: null,
    arrival_date: '',
    departure_date: '',
    status: 'BOOKED',
    payment_status: 'UNPAID',
  };
  validationErrors: { [key: string]: string[] } = {}; // Для отображения ошибок валидации



  constructor(private http: HttpClient, private router: Router, private route: ActivatedRoute) {}




  ngOnInit() {
    this.username = localStorage.getItem('username');
    if (!localStorage.getItem('auth_token')) {
      this.router.navigate(['/login']);
    } else {
      this.loadBookings();
      this.route.queryParams.subscribe((params) => {
        if (params['room_number']) {
          this.openAddBookingForm(parseInt(params['room_number']));
        }
      });
    }
  }

  loadBookings() {
    this.http.get(`${environment.apiUrl}/hotel/api/reservations`).subscribe({
      next: (data: any) => {
        if (data) {
          this.bookings = data;
          this.filteredBookings = [...this.bookings];
          const uniqueTypes = new Set(this.bookings.map((booking: any) => booking.room.type_name));
          this.roomTypes = Array.from(uniqueTypes);
        } else {
          this.bookings = [];
          this.filteredBookings = [];
        }
      },
      error: (err) => console.error('Ошибка загрузки броней:', err),
    });
  }

  formatDate(dateString: string | null): string {
    if (!dateString) {
      return '—';
    }
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
  }



  applyFiltersAndSearch() {
    const query = this.searchQuery.toLowerCase();

    this.filteredBookings = this.bookings.filter((booking) => {
      // Поиск
      const matchesSearch = [
        booking.client.first_name,
        booking.client.last_name,
        booking.client.middle_name,
        booking.client.passport_number,
        booking.status,
        booking.payment_status,
        booking.room.number.toString(),
      ]
        .some((field) => field && field.toLowerCase().includes(query));

      // Фильтр по типу комнаты
      const matchesRoomType = this.filters.roomType
        ? booking.room.type_name === this.filters.roomType
        : true;

      // Фильтр по дате заезда
      const matchesArrivalDate = this.filters.arrivalDate
        ? booking.arrival_date === this.filters.arrivalDate
        : true;

      // Фильтр по дате выезда
      const matchesDepartureDate = this.filters.departureDate
        ? booking.departure_date === this.filters.departureDate
        : true;

      return matchesSearch && matchesRoomType && matchesArrivalDate && matchesDepartureDate;
    });
  }


  openAddBookingForm(roomNumber: number | null = null) {
    this.showAddBookingForm = true;
    this.newBooking = {
      passport_number: '',
      first_name: '',
      last_name: '',
      middle_name: '',
      city_from: '',
      room_number: roomNumber || null,
      arrival_date: '',
      departure_date: '',
      status: 'BOOKED',
      payment_status: 'UNPAID',
    };
    this.validationErrors = {};
  }

  closeAddBookingForm() {
    this.showAddBookingForm = false;
    this.newBooking = {};
    this.validationErrors = {};
  }




  addBooking() {
    this.http.post(`${environment.apiUrl}/hotel/reservation`, this.newBooking).subscribe({
      next: () => {
        this.loadBookings(); // Перезагружаем список бронирований
        this.closeAddBookingForm(); // Закрываем форму
      },
      error: (err) => {
        console.error('Ошибка при добавлении бронирования:', err);
        if (err.error) {
          this.validationErrors = err.error;
        }
      },
    });
  }


  openEditBookingForm(booking: any) {
    this.showEditBookingForm = true;
    this.currentBooking = { ...booking }; // Копируем текущую бронь
    this.originalBooking = { ...booking }; // Сохраняем оригинальные данные для сравнения
  }

  closeEditBookingForm() {
    this.showEditBookingForm = false;
    this.currentBooking = {};
    this.originalBooking = {};
  }

  saveBooking() {
    const body: any = {};

    // Проверяем изменения и добавляем в тело запроса только изменённые поля
    if (this.currentBooking.arrival_date !== this.originalBooking.arrival_date) {
      body.arrival_date = this.currentBooking.arrival_date;
    }
    if (this.currentBooking.departure_date !== this.originalBooking.departure_date) {
      body.departure_date = this.currentBooking.departure_date;
    }
    if (this.currentBooking.status !== this.originalBooking.status) {
      body.status = this.currentBooking.status;
    }
    if (this.currentBooking.payment_status !== this.originalBooking.payment_status) {
      body.payment_status = this.currentBooking.payment_status;
    }
    if (this.currentBooking.room.number !== this.originalBooking.room.number) {
      body.room_number = this.currentBooking.room.number;
    }

    if (Object.keys(body).length === 0) {
      alert('Нет изменений для сохранения.');
      return;
    }

    // Отправляем PATCH-запрос
    this.http.patch(`${environment.apiUrl}/hotel/reservation/${this.originalBooking.id}`, body).subscribe({
      next: () => {
        this.loadBookings(); // Обновляем список бронирований
        this.closeEditBookingForm(); // Закрываем форму
      },
      error: (err) => {
        console.error('Ошибка при редактировании бронирования:', err);
      },
    });
  }



  editBooking(booking: any) {
    console.log('Редактировать бронирование:', booking);
    // Реализуйте функционал редактирования здесь
  }

  navigateTo(route: string) {
    this.router.navigate([`/${route}`]);
  }

  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('username');
    this.router.navigate(['/login']);
  }

  protected readonly Math = Math;
}
