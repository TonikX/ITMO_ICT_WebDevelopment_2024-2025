<template>
  <div>
    <button @click="$router.push('/orders/')" class="back-button">Назад</button>
    <h1>Информация о заказе</h1>
    <div v-if="order">
      <p>Номер заказа: {{ order.order_id }}</p>
      <p>Клиент: {{ order.customer }}</p>
      <p>Автомобиль: {{ order.car }}</p>
      <p>Сотрудник: {{ order.employee }}</p>
      <p>Дата заказа: {{ formatDate(order.order_date) }}</p>
      <p>Статус: {{ order.status === 'in_progress' ? 'В процессе' : 'Завершен' }}</p>
      <p>Итоговая стоимость: {{ order.total_cost }} ₽</p>
    </div>
    <p v-else>Загружаем информацию...</p>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      order: null,
    };
  },
  created() {
    this.fetchOrder();
  },
  methods: {
    async fetchOrder() {
      const orderId = this.$route.params.id;
      try {
        const response = await apiClient.get(`/orders/${orderId}/`);
        this.order = response.data;
      } catch (error) {
        console.error('Ошибка при получении информации о заказе:', error);
      }
    },
    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
      return new Date(date).toLocaleDateString('ru-RU', options);
    }
  },
};
</script>

<style scoped>
.back-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  text-align: center;
  margin: 20px 0;
}

.back-button:hover {
  background-color: #45a049;
}
</style>
