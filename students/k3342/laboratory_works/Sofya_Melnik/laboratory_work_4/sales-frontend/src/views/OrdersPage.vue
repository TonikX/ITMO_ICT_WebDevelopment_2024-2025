<template>
  <div class="orders-page">
    <h2>Мои заявки</h2>

    <!-- Кнопка для создания новой заявки -->
    <div class="new-order-btn">
      <router-link to="/orders/new">
        <button class="btn">Создать новую заявку</button>
      </router-link>
    </div>

    <!-- Таблица заявок -->
    <table class="orders-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Услуга</th> <!-- Заменили "Клиент" на "Услуга" -->
          <th>Статус</th>
          <th>Дата</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td>{{ order.id }}</td>
          <!-- Заменили client_id на имя услуги -->
          <td>{{ order.service.name }}</td> <!-- Это будет отображать имя услуги -->
          <td :class="getStatusClass(order.status)">{{ order.status }}</td>
          <td>{{ formatDate(order.order_date) }}</td> <!-- Дата заказа -->
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '@/api';

export default {
  name: "OrdersPage",
  setup() {
    const orders = ref([]);

    const fetchOrders = async () => {
      try {
        const { data } = await api.get("orders/");
        orders.value = data;
      } catch (error) {
        console.error("Ошибка загрузки заявок:", error.response.data);
      }
    };

    const formatDate = (date) => {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return new Date(date).toLocaleDateString('ru-RU', options);
    };

    const getStatusClass = (status) => {
      switch (status) {
        case 'completed':
          return 'status-completed';
        case 'in_progress':
          return 'status-in-progress';
        case 'pending':
          return 'status-pending';
        default:
          return '';
      }
    };

    onMounted(fetchOrders);

    return { orders, formatDate, getStatusClass };
  }
};
</script>

<style scoped>
.orders-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

h2 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.new-order-btn {
  text-align: center;
  margin-bottom: 20px;
}

.new-order-btn .btn {
  padding: 10px 20px;
  font-size: 16px;
  color: white;
  background-color: #4CAF50;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.new-order-btn .btn:hover {
  background-color: #45a049;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
}

.orders-table th,
.orders-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.orders-table th {
  background-color: #f4f4f4;
  color: #333;
}

.orders-table td {
  color: #555;
}

.orders-table .status-completed {
  color: green;
}

.orders-table .status-in-progress {
  color: orange;
}

.orders-table .status-pending {
  color: red;
}
</style>
