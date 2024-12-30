<template>
  <div>
    <button @click="$router.push('/main')" class="back-button">Назад на главную страницу</button>
    <button @click="$router.push('/employees/add')" class="add-button">Добавить сотрудника</button>
    <h1>Список сотрудников</h1>
    <ul class="employee-list">
      <li v-for="employee in employees" :key="employee.employee_id">
        <router-link :to="'/employees/' + employee.employee_id">{{ employee.name }}</router-link>
      </li>
    </ul>
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
        const response = await apiClient.get('/employees/');
        this.employees = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка сотрудников:', error);
      }
    },
  },
};
</script>

<style scoped>
.employee-list {
  list-style-type: none;
  padding: 0;
}

.employee-list li {
  margin: 10px 0;
  font-size: 18px;
}

.add-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  margin: 20px 0;
}

.add-button:hover {
  background-color: #45a049;
}

a {
  text-decoration: none;
  color: #333;
}

a:hover {
  color: #4CAF50;
}
</style>
