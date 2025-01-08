<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <div class="button-container">
      <button @click="$router.push('/employees')" class="custom-button">Назад к списку сотрудников</button>
    </div>
    <h1 class="page-title">Информация о сотруднике</h1>
    <div v-if="employee" class="employee-info">
      <p><strong>Имя:</strong> {{ employee.name }}</p>
      <p><strong>Должность:</strong> {{ employee.position }}</p>
      <p><strong>Телефон:</strong> {{ employee.phone }}</p>
      <p><strong>Email:</strong> {{ employee.email }}</p>
    </div>
    <p v-else class="loading-text">Загружаем информацию...</p>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      employee: null,
    };
  },
  created() {
    this.fetchEmployee();
  },
  methods: {
    async fetchEmployee() {
      const employeeId = this.$route.params.id; // Получаем ID сотрудника из URL
      try {
        const response = await apiClient.get(`/workers/${employeeId}/`);
        this.employee = response.data;
      } catch (error) {
        console.error('Ошибка при получении информации о сотруднике:', error);
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
  margin-top: 20px;
}

/* Employee Info Styles */
.employee-info {
  background-color: white;
  padding: 20px;
  max-width: 600px;
  margin: 20px auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-size: 18px;
}

.employee-info p {
  margin: 10px 0;
}

strong {
  font-weight: bold;
}

/* Loading Text */
.loading-text {
  text-align: center;
  font-size: 18px;
  color: #888;
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
