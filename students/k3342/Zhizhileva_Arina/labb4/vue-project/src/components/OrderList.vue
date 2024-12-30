<template>
  <div>
    <button @click="$router.push('/main')" class="back-button">На главную</button>
    <button @click="$router.push('/orders/create')" class="back-button">Создать заказ</button>
    <h1>Список заказов</h1>
    <table v-if="orders.length">
      <thead>
        <tr>
          <th>Номер заказа</th>
          <th>Клиент</th>
          <th>Автомобиль</th>
          <th>Сотрудник</th>
          <th>Дата заказа</th>
          <th>Статус</th>
          <th>Итоговая стоимость</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.order_id">
          <td>{{ order.order_id }}</td>
          <td>{{ order.customer }}</td>
          <td>{{ order.car }}</td>
          <td>{{ order.employee }}</td>
          <td>{{ order.order_date }}</td>
          <td>{{ order.status === 'in_progress' ? 'В процессе' : 'Завершен' }}</td>
          <td>{{ order.total_cost }} ₽</td>
          <td>
            <router-link :to="'/orders/' + order.order_id">Подробнее</router-link>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Нет заказов для отображения.</p>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      orders: [],
    };
  },
  created() {
    this.fetchOrders();
  },
  methods: {
    async fetchOrders() {
      try {
        const response = await apiClient.get('/orders/');
        this.orders = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке заказов:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Добавьте стили для кнопки и других элементов, если необходимо */
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
