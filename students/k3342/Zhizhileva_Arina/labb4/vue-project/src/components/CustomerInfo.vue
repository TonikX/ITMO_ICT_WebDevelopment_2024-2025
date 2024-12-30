<template>
  <div>
    <button @click="$router.push('/customers')" class="back-button">Назад к списку клиентов</button>
    <h1>Информация о клиенте</h1>
    <div v-if="customer">
      <p><strong>Имя:</strong> {{ customer.name }}</p>
      <p><strong>Телефон:</strong> {{ customer.phone }}</p>
      <p><strong>Email:</strong> {{ customer.email }}</p>
      <p><strong>Адрес:</strong> {{ customer.address }}</p>
      <button @click="$router.push(`/customer-cars/${this.$route.params.id}`)" class="back-button">Автомобили клиента</button>
    </div>
    <div v-else>
      <p>Загрузка информации...</p>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  props: ['id'],
  data() {
    return {
      customer: null,
    };
  },
  async created() {
    const customerId = this.$route.params.id; // Получаем ID клиента из URL
    try {
      const response = await apiClient.get(`/customers/${customerId}/`);
      this.customer = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке данных клиента:', error);
    }
  },
};
</script>

<style scoped>
.back-button {
  background-color: #2196f3;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #1976d2;
}

h1 {
  text-align: center;
}
</style>
