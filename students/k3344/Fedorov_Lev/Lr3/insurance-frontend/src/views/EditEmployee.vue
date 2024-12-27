<template>
  <div class="edit-employee-container">
    <div class="form-card">
      <h1>Редактирование сотрудника</h1>
      <form @submit.prevent="updateEmployee">
        <div class="form-group">
          <label for="first_name">Имя</label>
          <input
            v-model="employee.first_name"
            id="first_name"
            type="text"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="last_name">Фамилия</label>
          <input
            v-model="employee.last_name"
            id="last_name"
            type="text"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="age">Возраст</label>
          <input
            v-model="employee.age"
            id="age"
            type="number"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="passport_data">Паспортные данные</label>
          <input
            v-model="employee.passport_data"
            id="passport_data"
            type="text"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="organization">Организация</label>
          <select
            v-model="employee.organization"
            id="organization"
            required
            class="form-control"
          >
            <option
              v-for="org in organizations"
              :key="org.id"
              :value="org.id"
            >
              {{ org.full_name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="risk_category">Категория риска</label>
          <input
            v-model="employee.risk_category"
            id="risk_category"
            type="text"
            required
            class="form-control"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="primary-btn">Сохранить</button>
          <button @click.prevent="fireEmployee" class="danger-btn">Уволить</button>
          <button
            @click.prevent="$router.push('/employees')"
            class="secondary-btn"
          >
            Отмена
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import EmployeeService from '@/services/EmployeeService';

export default {
  props: ['id'],
  data() {
    return {
      employee: {
        first_name: '',
        last_name: '',
        age: '',
        passport_data: '',
        organization: '',
        risk_category: '',
      },
      organizations: [],
    };
  },
  async mounted() {
    try {
      this.employee = await EmployeeService.getEmployeeById(this.id);
      this.organizations = await EmployeeService.getOrganizations();
    } catch (error) {
      console.error('Ошибка загрузки данных сотрудника:', error);
    }
  },
  methods: {
    async updateEmployee() {
      try {
        await EmployeeService.updateEmployee(this.id, this.employee);
        alert('Данные сотрудника успешно обновлены');
        this.$router.push('/employees');
      } catch (error) {
        console.error('Ошибка обновления данных:', error);
      }
    },
    async fireEmployee() {
      try {
        await EmployeeService.fireEmployee(this.id);
        alert('Сотрудник успешно уволен');
        this.$router.push('/employees');
      } catch (error) {
        console.error('Ошибка при увольнении сотрудника:', error);
      }
    },
  },
};
</script>

<style scoped>
.edit-employee-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
  background-color: #f4f7f6;
}

.form-card {
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 600px;
  width: 100%;
}

.form-card h1 {
  margin-bottom: 25px;
  font-size: 2rem;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: space-between;
}

.primary-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 30px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.primary-btn:hover {
  background-color: #0056b3;
}

.danger-btn {
  background-color: #dc3545;
  color: white;
  padding: 12px 30px;
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
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.secondary-btn:hover {
  background-color: #5a6268;
}
</style>
