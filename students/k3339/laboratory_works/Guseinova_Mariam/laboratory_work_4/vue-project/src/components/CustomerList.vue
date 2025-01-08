<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <div class="actions">
      <button @click="$router.push('/main')" class="custom-button">Назад на главную страницу</button>
      <button @click="$router.push('/add-customer')" class="custom-button">Добавить клиента</button>
    </div>
    <h1>Список клиентов</h1>
    <div class="customer-list">
      <!-- Обернули v-if в отдельный контейнер -->
      <div v-if="customers.length">
        <div class="customer-card" v-for="customer in customers" :key="customer.customer_id">
          <h3>{{ customer.name }}</h3>
          <p><strong>Телефон:</strong> {{ customer.phone }}</p>
          <p><strong>Email:</strong> {{ customer.email }}</p>
          <router-link :to="`/customer/${customer.customer_id}`" class="view-details">Посмотреть детали</router-link>
        </div>
      </div>
      <p v-else>Клиенты не найдены.</p>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      customers: [],
    };
  },
  async created() {
    try {
      const response = await apiClient.get('/clients/');
      this.customers = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке списка клиентов:', error);
    }
  },
};
</script>

<style scoped>
/* Общие стили страницы */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

/* Header */
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

/* Кнопки действий */
.actions {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.custom-button {
  background-color: darkslategray;
  color: white;
  margin: 0 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  text-transform: none;
}

.custom-button:hover {
  background-color: #555;
}

/* Список клиентов */
.customer-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
  margin: 0 auto;
  max-width: 1200px;
}

/* Карточки клиентов */
.customer-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
}

.customer-card h3 {
  margin: 0 0 10px;
  color: darkslategray;
}

.customer-card p {
  margin: 5px 0;
  color: #555;
}

.view-details {
  display: inline-block;
  margin-top: 10px;
  color: darkslategray;
  text-decoration: none;
  font-weight: bold;
}

.view-details:hover {
  text-decoration: underline;
}
</style>
