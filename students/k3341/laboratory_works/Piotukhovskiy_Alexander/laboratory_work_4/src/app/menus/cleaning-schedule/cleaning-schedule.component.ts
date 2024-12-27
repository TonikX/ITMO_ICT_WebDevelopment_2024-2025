import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Router} from '@angular/router';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {environment} from '../../environment';

@Component({
  selector: 'app-cleaning-schedule',
  standalone: true,
  templateUrl: './cleaning-schedule.component.html',
  styleUrls: ['./cleaning-schedule.component.css'],
  imports: [CommonModule, FormsModule],
})
export class CleaningScheduleComponent implements OnInit {
  appName: string = environment.appName;
  username: string | null = null;
  cleaningSchedules: any[] = [];
  filteredSchedules: any[] = [];
  filter: { date: string | null; cleanerId: number | null; roomNumber: number | null } = {
    date: null,
    cleanerId: null,
    roomNumber: null,
  };

  page: number = 1;
  itemsPerPage: number = 5;

  showModal: boolean = false;
  scheduleToDelete: any = null;

  newCleaningDate: string | null = null;
  newRoomId: any | null = null;


  cleaners: any[] = [];
  rooms: any[] = [];
  statuses: { value: string; label: string }[] = [
    {value: 'PENDING', label: 'Ожидается'},
    {value: 'IN_PROGRESS', label: 'В процессе'},
    {value: 'COMPLETED', label: 'Завершена'},
  ];

  showAddForm: boolean = false;
  newSchedule = {
    cleaner_id: null,
    cleaning_dates: [] as string[],
    room_ids: [] as number[],
  };
  selectedRoom: number | null = null;

  toggleAddScheduleForm() {
    this.showAddForm = !this.showAddForm;
    if (!this.showAddForm) {
      this.resetNewScheduleForm();
    }
  }

  resetNewScheduleForm() {
    this.newSchedule = {
      cleaner_id: null,
      cleaning_dates: [],
      room_ids: [],
    };
    this.selectedRoom = null;
  }

  addCleaningDate() {
    if (this.newCleaningDate && !this.newSchedule.cleaning_dates.includes(this.newCleaningDate)) {
      this.newSchedule.cleaning_dates.push(this.newCleaningDate);
      this.newCleaningDate = null;
    } else if (!this.newCleaningDate || this.newCleaningDate == "null") {
      alert('Пожалуйста, выберите дату.');
    } else {
      alert('Эта дата уже добавлена.');
    }
  }


  removeCleaningDate(date: string) {
    this.newSchedule.cleaning_dates = this.newSchedule.cleaning_dates.filter((d) => d !== date);
  }

  addRoom() {
    if (this.newRoomId && !this.newSchedule.room_ids.includes(this.newRoomId)) {
      this.newSchedule.room_ids.push(this.newRoomId);
      this.newRoomId = null;
    } else if (this.newRoomId == null) {
      alert('Пожалуйста, выберите комнату.');
    } else {
      alert('Эта комната уже добавлена.');
    }
  }


  removeRoom(roomId: number) {
    this.newSchedule.room_ids = this.newSchedule.room_ids.filter((id) => id !== roomId);
  }

  saveNewSchedule() {
    if (!this.newSchedule.cleaner_id || this.newSchedule.cleaning_dates.length === 0 || this.newSchedule.room_ids.length === 0) {
      alert('Пожалуйста, заполните все поля формы.');
      return;
    }

    this.http
      .patch(`${environment.apiUrl}/hotel/cleaning-schedules/manage`, this.newSchedule)
      .subscribe({
        next: () => {
          this.loadSchedules();
          this.toggleAddScheduleForm();
        },
        error: (err) => {
          console.error('Ошибка при добавлении расписания:', err);
        },
      });
  }


  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }
    this.username = localStorage.getItem('username');
    this.loadCleaners();
    this.loadRooms();
    this.loadSchedules();
  }

  loadCleaners() {
    this.http
      .get(`${environment.apiUrl}/hotel/api/employees`)
      .subscribe({
        next: (data: any) => {
          this.cleaners = data;
        },
        error: (err) => {
          console.error('Ошибка загрузки списка уборщиков:', err);
        },
      });
  }


  loadRooms() {
    this.http
      .get(`${environment.apiUrl}/hotel/rooms`)
      .subscribe({
        next: (data: any) => {
          this.rooms = data.rooms;
        },
        error: (err) => {
          console.error('Ошибка загрузки списка комнат:', err);
        },
      });
  }


  loadSchedules() {
    let params = new HttpParams();
    if (this.filter.date) params = params.set('date', this.filter.date);
    if (this.filter.cleanerId) params = params.set('cleaner_id', this.filter.cleanerId.toString());
    if (this.filter.roomNumber) params = params.set('room_number', this.filter.roomNumber.toString());

    this.http
      .get(`${environment.apiUrl}/hotel/api/cleaning-schedules`, {
        params: params,
      })
      .subscribe({
        next: (data: any) => {
          this.cleaningSchedules = data;
          this.applyFilter();
        },
        error: (err) => {
          console.error('Ошибка загрузки расписания уборок:', err);
        },
      });
  }

  openDeleteModal(schedule: any) {
    this.scheduleToDelete = schedule;
    this.showModal = true;
  }

  closeDeleteModal() {
    this.scheduleToDelete = null;
    this.showModal = false;
  }

  confirmDelete() {
    if (!this.scheduleToDelete) return;

    this.http
      .delete(`${environment.apiUrl}/hotel/api/cleaning-schedules/${this.scheduleToDelete.id}/`)
      .subscribe({
        next: () => {
          this.loadSchedules();
          this.closeDeleteModal();
        },
        error: (err) => {
          console.error('Ошибка при удалении записи об уборке:', err);
        },
      });
  }

  applyFilter() {
    this.filteredSchedules = this.cleaningSchedules.filter((schedule) => {
      const matchesDate =
        !this.filter.date || schedule.cleaning_date === this.filter.date;

      const matchesCleaner =
        this.filter.cleanerId === null || schedule.cleaner?.id === Number(this.filter.cleanerId);

      const matchesRoom =
        !this.filter.roomNumber || schedule.room?.number === this.filter.roomNumber;

      return matchesDate && matchesCleaner && matchesRoom;
    });

    this.page = 1;
  }

  getPaginatedSchedules(): any[] {
    const startIndex = (this.page - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    return this.filteredSchedules.slice(startIndex, endIndex);
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

  protected readonly Math = Math;
}
