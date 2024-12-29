<template>
  <div class="employee-list-container">
    <div class="employee-list-card">
      <h1>Список сотрудников</h1>

      <!-- Информация о текущем пользователе -->
      <div class="user-info">
        <p><strong>Организация:</strong> {{ currentUser.organization }}</p>
        <p><strong>ID пользователя:</strong> {{ currentUser.id }}</p>
        <p><strong>Имя пользователя:</strong> {{ currentUser.username }} </p>
        <p><strong>Должность:</strong> {{ currentUser.position.name }}</p>
      </div>

      <!-- Фильтры и поиск -->
      <div class="filters">
        <input
          v-model="searchQuery"
          placeholder="Поиск по имени"
          class="form-control"
        />
      </div>

      <!-- Таблица сотрудников -->
      <table class="styled-table">
        <thead>
          <tr>
            <th>ФИО</th>
            <th>Возраст</th>
            <th>Должность</th>
            <th>Организация</th>
            <th v-if="currentUser.position.is_staff">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in filteredEmployees" :key="employee.id">
            <td>{{ employee.first_name }} {{ employee.last_name }}</td>
            <td>{{ employee.age }}</td>
            <td>{{ employee.position.name }}</td>
            <td>{{ getOrganizationName(employee.organization) }}</td>
            <td v-if="currentUser.position.is_staff">
              <button
                @click="editEmployee(employee.id)"
                class="primary-btn"
                v-if="canEdit(employee)"
              >
                Редактировать
              </button>
              <button
                @click="fireEmployee(employee.id)"
                class="danger-btn"
                v-if="canEdit(employee)"
              >
                Уволить
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Пагинация -->
      <div class="pagination">
        <button
          @click="loadPage(pagination.prev)"
          :disabled="!pagination.prev"
          class="secondary-btn"
        >
          Назад
        </button>
        <button
          @click="loadPage(pagination.next)"
          :disabled="!pagination.next"
          class="primary-btn"
        >
          Вперед
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import EmployeeService from '@/services/EmployeeService';
import UserService from '@/services/UserService';

export default {
  data() {
    return {
      employees: [],
      organizations: [],
      searchQuery: '',
      pagination: {
        next: null,
        prev: null,
      },
      currentUser: {
        organization: '',
        id: '',
        position: {
          is_staff: false,
        },
      },
    };
  },
  async mounted() {
    this.currentUser = await UserService.getProfile();
    this.organizations = await EmployeeService.getOrganizations();
    await this.loadEmployees();
  },
  computed: {
    filteredEmployees() {
      if (!this.employees) return [];
      return this.employees.filter(employee => {
        const fullName = `${employee.first_name} ${employee.last_name}`.toLowerCase();
        const passportData = employee.passport_data?.toLowerCase() || '';
        const searchQuery = this.searchQuery.toLowerCase();
        return (
          fullName.includes(searchQuery) ||
          passportData.includes(searchQuery)
        );
      });
    },
  },
  methods: {
    async loadEmployees() {
      const params = {
        search: this.searchQuery,
        organization: this.currentUser.organization_id,
      };
      const response = await EmployeeService.getEmployees(params);
      this.employees = Array.isArray(response) ? [...response] : [];
      this.pagination.next = response.next;
      this.pagination.prev = response.previous;
    },
    async loadPage(url) {
      if (url) {
        const response = await EmployeeService.getEmployees({ url });
        this.employees = response.results ? response.results.slice() : [];
        this.pagination.next = response.next;
        this.pagination.prev = response.previous;
      }
    },
    editEmployee(id) {
      this.$router.push(`/employees/${id}/edit`);
    },
    async fireEmployee(id) {
      if (confirm('Вы уверены, что хотите уволить сотрудника?')) {
        await EmployeeService.fireEmployee(id);
        alert('Сотрудник уволен');
        this.loadEmployees();
      }
    },
    canEdit(employee) {
      return (
        this.currentUser.position.is_staff &&
        employee.organization === this.currentUser.organization_id
      );
    },
    getOrganizationName(orgId) {
      const org = this.organizations.find(org => org.id === orgId);
      return org ? org.full_name : 'Неизвестно';
    },
  },
  watch: {
    searchQuery() {
      this.loadEmployees();
    },
  },
};
</script>

<style scoped>
.employee-list-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  background-color: #f4f7f6;
  height: 100vh;
}
.employee-list-card {
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 1100px;
  width: 100%;
}
.user-info {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #ddd;
}
.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.styled-table th,
.styled-table td {
  padding: 15px;
  border: 1px solid #ddd;
  text-align: left;
}
.styled-table th {
  background-color: #f4f4f4;
}
.filters input {
  padding: 12px;
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
}
.primary-btn {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.primary-btn:hover {
  background-color: #0056b3;
}
.danger-btn {
  background-color: #dc3545;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.danger-btn:hover {
  background-color: #c82333;
}
.secondary-btn {
  background-color: #6c757d;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 15px;
}
</style>
