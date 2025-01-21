<template>
    <v-container class="employee-details" v-if="employee">
      <v-row>
        <v-col cols="12" class="text-center">
          <h1>Детали работника: {{ employee.full_name }}</h1>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" md="6">
          <v-card outlined class="mb-4">
            <v-card-title>Основная информация</v-card-title>
            <v-card-text>
              <p><strong>Имя:</strong> {{ employee.full_name }}</p>
              <p><strong>Телефон:</strong> {{ employee.phone }}</p>
              <p><strong>Email:</strong> {{ employee.email || "Нет информации" }}</p>
              <p><strong>Должность:</strong> {{ employee.job_position ? employee.job_position.name : "Не указана" }}</p>
              <p><strong>Мастерская:</strong> {{ employee.car_workshop ? `${employee.car_workshop.city}, ${employee.car_workshop.address}` : "Не указана" }}</p>
              <p><strong>Ранг:</strong> {{ employee.rank }}</p>
              <p><strong>Бонус:</strong> {{ employee.bonus || "Не указан" }}</p>
            </v-card-text>
          </v-card>
        </v-col>
  
        <v-col cols="12" md="6">
          <v-card outlined class="mb-4">
            <v-card-title>Зарплата и штрафы</v-card-title>
            <v-card-text>
              <p><strong>Зарплата:</strong> {{ employee.salary || "Не указано" }}</p>
              <p><strong>Штрафы:</strong> {{ employee.fines || "Нет штрафов" }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" class="d-flex justify-center">
          <v-btn color="primary" @click="navigateToEdit">Редактировать</v-btn>
          <v-btn color="secondary" @click="navigateBack">Назад</v-btn>
          <v-btn color="red" @click="deleteEmployee">Удалить</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import apiClient from "@/services/api";
  
  export default {
    name: "EmployeeDetails",
    data() {
      return {
        employee: null,
      };
    },
    methods: {
      async fetchEmployeeDetails() {
        const employeeId = this.$route.params.id;
        try {
          const response = await apiClient.get(`/employees/${employeeId}/`);
          this.employee = response.data;
          if (this.employee.job_position) {
            this.employee.job_position.name = this.employee.job_position.name || "Не указана";
          }
          if (this.employee.car_workshop) {
            this.employee.car_workshop.city = this.employee.car_workshop.city || "Не указана";
            this.employee.car_workshop.address = this.employee.car_workshop.address || "Не указана";
          }
        } catch (error) {
          console.error("Ошибка загрузки данных работника:", error.response?.data || error.message);
        }
      },
      navigateToEdit() {
        this.$router.push(`/employees/edit/${this.employee.id}`);
      },
      navigateBack() {
        this.$router.push("/employees");
      },
      async deleteEmployee() {
        const confirmDelete = confirm("Вы уверены, что хотите удалить этого работника?");
        if (confirmDelete) {
          try {
            await apiClient.delete(`/employees/${this.employee.id}/`);
            this.$router.push("/employees");
          } catch (error) {
            console.error("Ошибка удаления работника:", error.response?.data || error.message);
          }
        }
      }
    },
    mounted() {
      this.fetchEmployeeDetails();
    },
  };
  </script>
  
  <style scoped>
  .employee-details {
    margin-top: 50px;
  }
  .mb-4 {
    margin-bottom: 20px;
  }
  .text-center {
    text-align: center;
  }
  </style>
  