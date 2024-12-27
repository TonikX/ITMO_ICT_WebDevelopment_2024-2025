<template>
  <div class="employee-dashboard-container">
    <div class="dashboard-card">
      <h1>Личный кабинет сотрудника</h1>

      <div class="employee-info">
        <h2>Информация о сотруднике</h2>
        <p><strong>Email:</strong> {{ user.email || 'Не указан' }}</p>
        <p><strong>Организация:</strong> {{ user.organization || 'Не указана' }}</p>
        <p><strong>Должность:</strong> {{ user.position?.name || 'Не указана' }}</p>
        <p><strong>Роль:</strong> {{ user.role || 'Сотрудник' }}</p>
        <button class="primary-btn" @click="$router.push('/profile/edit')">
          Редактировать профиль
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return {
      contracts: [],
      user: {},  // Данные пользователя
    };
  },
  async created() {
    await this.fetchContracts();
    await this.fetchUserProfile();
  },
  methods: {
    async fetchContracts() {
      try {
        const response = await apiClient.get('/insurance/contracts/');
        const userId = localStorage.getItem('userId');
        this.contracts = response.data.filter(contract =>
            contract.employees.some(emp => emp.user_id == userId)
        );
        console.log('Контракты сотрудника:', this.contracts);
      } catch (error) {
        console.error('Ошибка загрузки контрактов:', error);
      }
    },

    async fetchUserProfile() {
      try {
        const response = await apiClient.get('/insurance/user/profile/');
        this.user = response.data;
        console.log('Профиль сотрудника:', this.user);
      } catch (error) {
        console.error('Ошибка загрузки профиля сотрудника:', error);
      }
    },
  },
};
</script>



<style scoped>
.dashboard {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
}
.company-info {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}
.primary-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
}
.primary-btn:hover {
  background-color: #0056b3;
}

textarea,
select,
input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
</style>