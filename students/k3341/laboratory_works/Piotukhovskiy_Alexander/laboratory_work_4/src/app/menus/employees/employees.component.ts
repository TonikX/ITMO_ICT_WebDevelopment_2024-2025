import {environment} from '../../environment';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';


@Component({
  selector: 'app-employees',
  standalone: true,
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css'],
  imports: [CommonModule, FormsModule],
})
export class EmployeesComponent implements OnInit {
  originalEmployee: any = {};
  validationErrors: { [key: string]: string[] } = {};
  employmentContracts: any[] = [];
  appName: string = environment.appName;
  username: string | null = null;
  employees: any[] = [];
  positions: any[] = [];
  showEmployeeForm: boolean = false;
  isEditMode: boolean = false;
  currentEmployee: any = {};
  showModal: boolean = false;
  selectedEmployee: any = null;
  page: number = 1;
  itemsPerPage: number = 8;


  newEmployee: any = {
    passport_number: '',
    first_name: '',
    last_name: '',
    middle_name: '',
    position_id: null,
    contract_type: 'PERMANENT',
    start_date: '',
    end_date: null,
  };


  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit() {
    this.username = localStorage.getItem('username');
    this.loadEmployees();
    this.loadPositions();
    this.loadContracts();
  }

  loadEmployees() {
    this.http.get(`${environment.apiUrl}/hotel/api/employees`).subscribe({
      next: (data: any) => {
        console.log('Сотрудники:', data);
        this.employees = data;
      },
      error: (err) => console.error('Ошибка загрузки сотрудников:', err),
    });
  }

  loadPositions() {
    this.http.get(`${environment.apiUrl}/hotel/api/positions`).subscribe({
      next: (data: any) => {
        console.log('Должности:', data);
        this.positions = data;
      },
      error: (err) => console.error('Ошибка загрузки должностей:', err),
    });
  }

  loadContracts() {
    this.http.get(`${environment.apiUrl}/hotel/api/employment-contracts`).subscribe({
      next: (data: any) => {
        console.log('Контракты:', data);
        this.employmentContracts = data;
        this.mapContractsToEmployees();
      },
      error: (err) => console.error('Ошибка загрузки контрактов:', err),
    });
  }


  mapContractsToEmployees() {
    if (!this.employees || !this.employmentContracts) return;

    this.employees.forEach((employee) => {
      const contract = this.employmentContracts.find(
        (c) => c.employee_id === employee.id
      );

      employee.contract = contract || null;
    });
  }


  openAddEmployeeForm() {
    this.isEditMode = false;
    this.originalEmployee = {}
    this.newEmployee = {
      passport_number: '',
      first_name: '',
      last_name: '',
      middle_name: '',
      position_id: null,
      contract_type: 'PERMANENT',
      start_date: '',
      end_date: null,
    };
    this.showEmployeeForm = true;
  }


  openEditEmployeeForm(employee: any) {
    this.isEditMode = true;
    this.currentEmployee = {
      id: employee.id,
      first_name: employee.first_name || '',
      last_name: employee.last_name || '',
      middle_name: employee.middle_name || '',
      passport_number: employee.passport_number || '',
      position_id: employee.position?.id || null,
      contract_type: employee.contract?.contract_type || null,
      start_date: employee.contract?.start_date || '',
      end_date: employee.contract?.end_date || '',
    };

    this.originalEmployee = {...this.currentEmployee};

    this.showEmployeeForm = true;
  }


  closeEmployeeForm() {
    this.showEmployeeForm = false;
    this.currentEmployee = {};
  }


  saveEmployee() {
    this.validationErrors = {};

    if (!this.currentEmployee.passport_number || !this.currentEmployee.first_name || !this.currentEmployee.last_name) {
      alert('Пожалуйста, заполните обязательные поля.');
      return;
    }

    const body: any = {
      employee_id: this.currentEmployee.id,
    };

    if (!this.originalEmployee.first_name || this.currentEmployee.first_name !== this.originalEmployee.first_name) {
      body.first_name = this.currentEmployee.first_name;
    }

    if (!this.originalEmployee.last_name || this.currentEmployee.last_name !== this.originalEmployee.last_name) {
      body.last_name = this.currentEmployee.last_name;
    }

    if (!this.originalEmployee.middle_name || this.currentEmployee.middle_name !== this.originalEmployee.middle_name) {
      body.middle_name = this.currentEmployee.middle_name;
    }

    if (!this.originalEmployee.passport_number || this.currentEmployee.passport_number !== this.originalEmployee.passport_number) {
      body.passport_number = this.currentEmployee.passport_number;
    }

    if (!this.originalEmployee.position_id || this.currentEmployee.position_id !== this.originalEmployee.position_id) {
      body.position_id = this.currentEmployee.position_id;
    }

    if (!this.originalEmployee.contract_type || this.currentEmployee.contract_type !== this.originalEmployee.contract_type) {
      body.contract_type = this.currentEmployee.contract_type;
    }

    if (!this.originalEmployee.start_date || this.currentEmployee.start_date !== this.originalEmployee.start_date) {
      body.start_date = this.currentEmployee.start_date;
    }

    if ((!this.originalEmployee.start_date || this.currentEmployee.end_date) && this.currentEmployee.end_date !== this.originalEmployee.end_date) {
      body.end_date = this.currentEmployee.end_date;
    }

    const url = `${environment.apiUrl}/hotel/employees/manage`;

    const method = this.isEditMode ? 'patch' : 'post';

    this.http[method](url, this.isEditMode ? {...body, employee_id: this.currentEmployee.id} : body).subscribe({
      next: () => {
        this.loadEmployees();
        this.loadPositions();
        this.loadContracts();
        this.closeEmployeeForm();
      },
      error: (err) => {
        if (err.status === 422 && err.error) {
          console.error('Ошибка валидации:', err.error);
          this.validationErrors = err.error;
        } else {
          console.error('Ошибка сохранения сотрудника:', err);
        }
      },
    });
  }


  confirmTermination(employee: any) {
    this.selectedEmployee = employee;
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
    this.selectedEmployee = null;
  }

  terminateEmployee() {
    if (!this.selectedEmployee) return;

    const body: any = {
      employee_id: this.selectedEmployee.id,
    };

    if (this.selectedEmployee.termination_date) {
      body.termination_date = this.selectedEmployee.termination_date;
    }

    this.http
      .delete(`${environment.apiUrl}/hotel/employees/manage`, {
        body: body,
      })
      .subscribe({
        next: () => {
          this.loadEmployees();
          this.loadPositions();
          this.loadContracts();
          this.closeModal();
        },
        error: (err) => console.error('Ошибка увольнения сотрудника:', err),
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

  protected readonly Math = Math;
}
