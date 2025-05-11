import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Router} from '@angular/router';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {environment} from '../../environment';

@Component({
  selector: 'app-clients',
  standalone: true,
  templateUrl: './clients.component.html',
  styleUrls: ['./clients.component.css'],
  imports: [CommonModule, FormsModule],
})
export class ClientsComponent implements OnInit {
  appName: string = environment.appName;
  username: string | null = null;
  clients: any[] = [];
  filteredClients: any[] = [];
  searchQuery: string = '';
  room: string | null = null;
  startDate: string | null = null;
  endDate: string | null = null;
  city: string | null = null;
  page: number = 1;
  itemsPerPage: number = 4;
  detailMessage: string | null = null;

  showModal: boolean = false;
  clientToDelete: any = null;

  showEditModal: boolean = false;
  clientToEdit: any = null;

  fields: (keyof typeof this.editForm)[] = ['passport_number', 'first_name', 'last_name', 'middle_name', 'city_from'];

  fieldLabels: { [key: string]: string } = {
    passport_number: 'Номер паспорта',
    last_name: 'Фамилия',
    first_name: 'Имя',
    middle_name: 'Отчество',
    city_from: 'Город',
  };


  editForm: {
    passport_number: string;
    first_name: string;
    last_name: string;
    middle_name: string | null;
    city_from: string;
  } = {
    passport_number: '',
    first_name: '',
    last_name: '',
    middle_name: '',
    city_from: '',
  };
  isEditMode: boolean = false;
  errors: Partial<Record<keyof typeof this.editForm, string[]>> = {};

  showOverlapModal: boolean = false;
  overlapResults: any[] = [];
  overlapClient: any = null;
  overlapFilters: { start_date: string | null; end_date: string | null } = {
    start_date: null,
    end_date: null,
  };

  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      this.router.navigate(['/login']);
      return;
    }
    this.username = localStorage.getItem('username');
    this.loadClients();
  }

  loadClients() {
    let params = new HttpParams();
    if (this.room) params = params.append('room', this.room);
    if (this.startDate) params = params.append('start_date', this.startDate);
    if (this.endDate) params = params.append('end_date', this.endDate);
    if (this.city) params = params.append('city', this.city);

    this.http
      .get(`${environment.apiUrl}/hotel/clients`, {
        params: params,
      })
      .subscribe({
        next: (data: any) => {
          this.clients = data.clients;
          this.filteredClients = [...this.clients];
          this.detailMessage = null;
        },
        error: (err) => {
          if (err.status === 404 && err.error?.detail) {
            this.clients = [];
            this.filteredClients = [];
            this.detailMessage = err.error.detail;
          } else {
            console.error('Ошибка загрузки клиентов:', err);
          }
        },
      });
  }

  searchClients() {
    this.filteredClients = this.clients.filter((client) =>
      `${client.first_name} ${client.last_name} ${client.middle_name} ${client.passport_number}`
        .toLowerCase()
        .includes(this.searchQuery.toLowerCase())
    );
  }

  openOverlapModal(clientId: number) {
    const client = this.clients.find((c) => c.id === clientId);
    if (!client) {
      console.error('Некорректный клиент для поиска пересечений');
      return;
    }
    this.overlapClient = client;
    this.showOverlapModal = true;
    this.overlapResults = [];
    this.overlapFilters = {start_date: null, end_date: null};
    this.findOverlaps()
  }

  closeOverlapModal() {
    this.overlapClient = null;
    this.showOverlapModal = false;
    this.overlapResults = [];
  }

  findOverlaps() {
    if (!this.overlapClient || !this.overlapClient.id) {
      console.error('client_id отсутствует или некорректен');
      return;
    }

    let params = new HttpParams().set('client_id', this.overlapClient.id.toString());
    if (this.overlapFilters.start_date) {
      params = params.set('start_date', this.overlapFilters.start_date);
    }
    if (this.overlapFilters.end_date) {
      params = params.set('end_date', this.overlapFilters.end_date);
    }

    this.http
      .get(`${environment.apiUrl}/hotel/clients/stay-overlap`, {params})
      .subscribe({
        next: (data: any) => {
          this.overlapResults = data.clients || [];
        },
        error: (err) => {
          console.error('Ошибка при поиске пересечений:', err);
          this.overlapResults = [];
        },
      });
  }


  editClient(clientId: number) {
    const client = this.clients.find((c) => c.id === clientId);
    if (client) {
      this.openEditModal(client);
    }
  }

  applyFilters() {
    this.page = 1;
    this.loadClients();
  }

  openEditModal(client: any = null) {
    this.isEditMode = !!client;
    this.clientToEdit = client;
    this.editForm = client
      ? {...client}
      : {
        passport_number: '',
        first_name: '',
        last_name: '',
        middle_name: '',
        city_from: '',
      };
    this.errors = {};
    this.showEditModal = true;
  }

  closeEditModal() {
    this.clientToEdit = null;
    this.showEditModal = false;
    this.errors = {};
  }

  validateForm(): boolean {
    this.errors = {};
    if (!this.editForm.passport_number || this.editForm.passport_number.length > 10) {
      this.errors.passport_number = ['Номер паспорта обязателен и должен быть не длиннее 10 символов.'];
    }
    if (!this.editForm.first_name || this.editForm.first_name.length > 50) {
      this.errors.first_name = ['Имя обязательно и должно быть не длиннее 50 символов.'];
    }
    if (!this.editForm.last_name || this.editForm.last_name.length > 50) {
      this.errors.last_name = ['Фамилия обязательна и должна быть не длиннее 50 символов.'];
    }
    if (this.editForm.middle_name && this.editForm.middle_name.length > 50) {
      this.errors.middle_name = ['Отчество должно быть не длиннее 50 символов.'];
    }
    if (!this.editForm.city_from || this.editForm.city_from.length > 50) {
      this.errors.city_from = ['Город обязателен и должен быть не длиннее 50 символов.'];
    }
    return Object.keys(this.errors).length === 0;
  }

  saveClient() {
    if (!this.validateForm()) return;

    const url = this.isEditMode
      ? `${environment.apiUrl}/hotel/api/clients/${this.clientToEdit.id}/`
      : `${environment.apiUrl}/hotel/api/clients/`;

    const method = this.isEditMode ? 'patch' : 'post';

    this.http[method](url, this.editForm).subscribe({
      next: (savedClient: any) => {
        if (this.isEditMode) {
          this.clients = this.clients.map((client) =>
            client.id === savedClient.id ? savedClient : client
          );
        } else {
          this.clients.push(savedClient);
          this.filteredClients.push(savedClient);
        }
        this.closeEditModal();
        this.loadClients();
      },
      error: (err) => {
        console.error('Ошибка при сохранении клиента:', err);
        if (err.error) {
          this.errors = err.error;
        }
      },
    });
  }

  deleteClient(clientId: number) {
    const client = this.clients.find((c) => c.id === clientId);
    if (client) {
      this.clientToDelete = client;
      this.showModal = true;
    }
  }

  closeDeleteModal() {
    this.clientToDelete = null;
    this.showModal = false;
  }

  confirmDelete() {
    if (this.clientToDelete) {
      const clientId = this.clientToDelete.id;
      this.http
        .delete(`${environment.apiUrl}/hotel/api/clients/${clientId}/`)
        .subscribe({
          next: () => {
            this.clients = this.clients.filter((client) => client.id !== clientId);
            this.filteredClients = this.filteredClients.filter((client) => client.id !== clientId);
            this.closeDeleteModal();
          },
          error: (err) => {
            console.error('Ошибка при удалении клиента:', err);
          },
        });
    }
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
