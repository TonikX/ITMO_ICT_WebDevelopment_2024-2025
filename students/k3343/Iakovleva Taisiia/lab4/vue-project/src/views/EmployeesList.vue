<template>
    <div class="page-container">
      <Header />
      <h3 class="table-header">Список сотрудников</h3>
      <div class="table-container">
      <div class="table-controls">
        <button @click="showAddForm = true" class="btn btn-primary">Добавить сотрудника</button>
      </div>
  
      <div class="table-container">
        <table class="styled-table">
          <thead>
            <tr>
              <th>Имя</th>
              <th>Фамилия</th>
              <th>Отчество</th>
              <th>Паспорт</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="employee in employees" :key="employee.id">
              <td>{{ employee.first_name }}</td>
              <td>{{ employee.second_name }}</td>
              <td>{{ employee.patronymic }}</td>
              <td>{{ employee.passport }}</td>
              <td>
                <button @click="deleteEmployee(employee.id)" class="btn btn-danger">Удалить</button>
              </td>
            </tr>
            <tr v-if="!employees.length">
              <td colspan="5">Нет доступных сотрудников.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  
      <div v-if="showAddForm || selectedEmployee" class="form-modal">
        <div class="modal-overlay">
          <div class="modal-content">
            <h2>{{ selectedEmployee ? 'Редактировать сотрудника' : 'Добавить сотрудника' }}</h2>
            <form @submit.prevent="saveEmployee">
              <div class="form-group">
                <label for="first_name" class="form-label">Имя:</label>
                <input v-model="formData.first_name" type="text" id="first_name" class="form-control" required />
              </div>
              <div class="form-group">
                <label for="second_name" class="form-label">Фамилия:</label>
                <input v-model="formData.second_name" type="text" id="second_name" class="form-control" required />
              </div>
              <div class="form-group">
                <label for="patronymic" class="form-label">Отчество:</label>
                <input v-model="formData.patronymic" type="text" id="patronymic" class="form-control" required />
              </div>
              <div class="form-group">
                <label for="passport" class="form-label">Паспорт:</label>
                <input v-model="formData.passport" type="text" id="passport" class="form-control" required />
              </div>
              <div class="form-group">
                <label for="position" class="form-label">Должность:</label>
                <input v-model="formData.position" type="text" id="position" class="form-control" required />
              </div>
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">Сохранить</button>
                <button type="button" @click="cancelEdit" class="btn btn-secondary">Отмена</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Header from "@/components/Header.vue";
  import apiClient from "@/api/axios";
  
  export default {
    components: {
      Header,
    },
    data() {
      return {
        employees: [],
        workshops: [],
        showAddForm: false,
        selectedEmployee: null,
        formData: {
          name: "",
          position: "",
          workshop: null,
        },
      };
    },
    async created() {
      await this.loadEmployees();
      await this.loadWorkshops();
    },
    methods: {
      async loadEmployees() {
        try {
          const response = await apiClient.get("/manufactory/employees/");
          this.employees = response.data;
        } catch (error) {
          console.error("Ошибка при загрузке сотрудников:", error);
          alert("Не удалось загрузить сотрудников.");
        }
      },
      async loadWorkshops() {
        try {
          const response = await apiClient.get("/manufactory/workshops/");
          this.workshops = response.data;
        } catch (error) {
          console.error("Ошибка при загрузке цехов:", error);
          alert("Не удалось загрузить цехи.");
        }
      },
      async saveEmployee() {
        try {
          if (this.selectedEmployee) {
            await apiClient.put(
              `/manufactory/employees/${this.selectedEmployee.id}/`,
              this.formData
            );
            alert("Изменения сохранены.");
          } else {
            await apiClient.post("/manufactory/employees/", this.formData);
            alert("Сотрудник добавлен.");
          }
          await this.loadEmployees();
          this.cancelEdit();
        } catch (error) {
          console.error("Ошибка при сохранении сотрудника:", error);
          alert("Не удалось сохранить изменения.");
        }
      },
      async deleteEmployee(id) {
        try {
          if (confirm("Вы уверены, что хотите удалить этого сотрудника?")) {
            await apiClient.delete(`/manufactory/employees/${id}/`);
            this.employees = this.employees.filter(
              (employee) => employee.id !== id
            );
          }
        } catch (error) {
          console.error("Ошибка при удалении сотрудника:", error);
          alert("Не удалось удалить сотрудника.");
        }
      },
      editEmployee(employee) {
        this.selectedEmployee = employee;
        this.formData = { ...employee, workshop: employee.workshop.id };
      },
      cancelEdit() {
        this.selectedEmployee = null;
        this.showAddForm = false;
        this.formData = {
          name: "",
          position: "",
          workshop: null,
        };
      },
    },
  };
  </script>
  
  <style scoped>
  .table-header {
  text-align: center;
  font-size: 26px;
  font-weight: bold;
  margin: 30px 0;
  color: #4a4a4a;
}

.table-controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.table-container {
  overflow-x: auto;
  margin: 0 auto;
  max-width: 1200px;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;
  background-color: #ffffff;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.styled-table th, .styled-table td {
  padding: 12px 20px;
  border: 1px solid #e0e0e0;
  text-align: center;
}

.styled-table th {
  background-color: #086f99;
  color: #ffffff;
  font-weight: bold;
}

.styled-table tr:nth-child(even) {
  background-color: #f8f8f8;
}

.styled-table tr:hover {
  background-color: #eef7fc;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #28a745;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #218838;
}

.btn-warning {
  background-color: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background-color: #e0a800;
}

.btn-danger {
  background-color: #dc3545;
  color: #ffffff;
}

.btn-danger:hover {
  background-color: #c82333;
}

.form-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.modal-content {
  background-color: #ffffff;
  padding: 25px 30px;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  max-width: 600px;
  width: 100%;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333333;
}

.form-group input, .form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group input:focus, .form-group select:focus {
  outline: none;
  border-color: #086f99;
  box-shadow: 0 0 4px rgba(8, 111, 153, 0.5);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .styled-table th, .styled-table td {
    padding: 10px;
    font-size: 14px;
  }

  .btn {
    font-size: 14px;
    padding: 8px 16px;
  }

  .modal-content {
    padding: 20px;
  }

  .form-group input, .form-group select {
    padding: 8px;
    font-size: 14px;
  }
}
  </style>
  