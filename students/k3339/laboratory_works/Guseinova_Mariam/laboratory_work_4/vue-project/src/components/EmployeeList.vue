<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <div class="button-container">
      <button @click="$router.push('/main')" class="custom-button">Назад на главную страницу</button>
      <button @click="$router.push('/employees/add')" class="custom-button">Добавить сотрудника</button>
    </div>
    <h1 class="page-title">Список сотрудников</h1>
    <div class="employee-list-container">
      <ul class="employee-list">
        <li v-for="employee in employees" :key="employee.employee_id" class="employee-item">
          <router-link :to="'/employees/' + employee.employee_id" class="employee-link">{{ employee.name }}</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      employees: [],
    };
  },
  created() {
    this.fetchEmployees();
  },
  methods: {
    async fetchEmployees() {
      try {
        const response = await apiClient.get('/workers/');
        this.employees = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка сотрудников:', error);
      }
    },
  },
};
</script>

<style scoped>
/* General Styles */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

/* Header Styles */
.header {
  background-color: darkslategray;
  color: white;
  padding: 20px;
  text-align: center;
}

.header-title {
  margin: 0;
  font-size: 24px;
}

/* Page Title */
.page-title {
  text-align: center;
  margin-top: 20px;
  font-size: 28px;
  color: darkslategray;
}

/* Button container */
.button-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

/* Employee List Styles */
.employee-list-container {
  background-color: white;
  padding: 20px;
  margin: 20px auto;
  max-width: 600px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.employee-list {
  list-style-type: none;
  padding: 0;
}

.employee-item {
  margin-bottom: 15px;
  font-size: 18px;
}

.employee-link {
  text-decoration: none;
  color: #333;
  font-weight: bold;
  display: block;
}

.employee-link:hover {
  color: darkslategray;
}

/* Buttons */
.custom-button {
  background-color: darkslategray !important;
  color: white !important;
  padding: 10px 20px;
  font-size: 16px;
  text-transform: none !important;
  border-radius: 5px;
  cursor: pointer;
  display: inline-block;
  margin-top: 15px;
}

.custom-button:hover {
  background-color: #2f4f4f;
}
</style>
