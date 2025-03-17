<template>
  <div class="employee-orders-page">
    <h2 class="page-title">Сотрудники и выполненные заявки за период</h2>

    <!-- Форма фильтрации по периоду -->
    <div class="filter-form">
      <label for="start_date">Дата начала:</label>
      <input type="date" v-model="startDate" />

      <label for="end_date">Дата окончания:</label>
      <input type="date" v-model="endDate" />

      <button @click="fetchEmployeesOrders">Фильтровать</button>
    </div>

    <!-- Таблица сотрудников -->
    <table class="employees-table" v-if="employees.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Фамилия</th>
          <th>Имя</th>
          <th>Email</th>
          <th>Телефон</th>
          <th>Должность</th>
          <th>Выполнено заявок</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="employee in employees" :key="employee.id">
          <td>{{ employee.id }}</td>
          <td>{{ employee.last_name }}</td>
          <td>{{ employee.first_name }}</td>
          <td>{{ employee.email }}</td>
          <td>{{ employee.phone }}</td>
          <td>{{ employee.position.position_title || employee.position.position_title }}</td>
          <td>{{ employee.order_count }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>Нет данных по сотрудникам за выбранный период.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/api';

const employees = ref([]);
const startDate = ref('');
const endDate = ref('');

// Метод для загрузки сотрудников с количеством выполненных заявок за период
const fetchEmployeesOrders = async () => {
  try {
    // Формируем URL с параметрами, если даты указаны
    let url = '/employee-orders-count/';
    if (startDate.value && endDate.value) {
      url += `?start_date=${startDate.value}&end_date=${endDate.value}`;
    }
    const { data } = await api.get(url);
    employees.value = data;
  } catch (error) {
    console.error("Ошибка загрузки данных сотрудников:", error.response?.data || error.message);
    employees.value = [];
  }
};
</script>

<style scoped>
.employee-orders-page {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f9f9f9;
  font-family: Arial, sans-serif;
}

.page-title {
  font-size: 24px;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.filter-form {
  margin-bottom: 20px;
}

.filter-form label {
  display: block;
  margin-bottom: 5px;
}

.filter-form input {
  padding: 8px;
  margin-bottom: 15px;
  width: 200px;
  border: 1px solid #ddd;
}

.filter-form button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: #fff;
  border: none;
  cursor: pointer;
}

.filter-form button:hover {
  background-color: #45a049;
}

.employees-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  margin-top: 20px;
}

.employees-table th,
.employees-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.employees-table th {
  background-color: #4CAF50;
  color: #fff;
  font-weight: bold;
}

.employees-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.employees-table tr:hover {
  background-color: #f1f1f1;
}
</style>
