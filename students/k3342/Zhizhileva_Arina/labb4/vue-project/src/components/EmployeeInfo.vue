<template>
  <div>
    <button @click="$router.push('/employees')" class="back-button">Назад к списку сотрудников</button>
    <h1>Информация о сотруднике</h1>
    <div v-if="employee" class="employee-info">
      <p><strong>Имя:</strong> {{ employee.name }}</p>
      <p><strong>Должность:</strong> {{ employee.position }}</p>
      <p><strong>Телефон:</strong> {{ employee.phone }}</p>
      <p><strong>Email:</strong> {{ employee.email }}</p>
    </div>
    <p v-else>Загружаем информацию...</p>
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
        const response = await apiClient.get(`/employees/${employeeId}/`);
        this.employee = response.data;
      } catch (error) {
        console.error('Ошибка при получении информации о сотруднике:', error);
      }
    },
  },
};
</script>

<style scoped>
.employee-info {
  max-width: 600px;
  margin: 0 auto;
  font-size: 18px;
}

.employee-info p {
  margin: 10px 0;
}

strong {
  font-weight: bold;
}
</style>
