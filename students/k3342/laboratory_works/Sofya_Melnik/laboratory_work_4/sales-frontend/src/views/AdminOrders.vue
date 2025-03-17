<template>
  <div class="orders-page">
    <h2>Заявки</h2>

    <!-- Кнопка для создания новой заявки -->
    <div class="new-order-btn">
      <router-link to="/admin-orders/new">
        <button class="btn">Создать новую заявку</button>
      </router-link>
    </div>

    <!-- Таблица заявок -->
    <table class="orders-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Клиент</th>
          <th>Услуга</th>
          <th>Статус</th>
          <th>Дата</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.client.first_name }} {{ order.client.last_name }}</td> <!-- Отображение имени клиента -->
          <td>{{ order.service.name }}</td>
          <td :class="getStatusClass(order.status)">{{ order.status }}</td>
          <td>{{ formatDate(order.order_date) }}</td>
          <td class="actions">
            <router-link :to="`/admin-orders/edit/${order.id}`" class="edit-btn">✏️</router-link>
            <button @click="deleteOrder(order.id)" class="delete-btn">🗑️</button>
          </td>
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
        console.error("Ошибка загрузки заявок:", error.response?.data || error.message);
      }
    };

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ru-RU', { year: 'numeric', month: '2-digit', day: '2-digit' });
    };

    const getStatusClass = (status) => {
      return {
        completed: "status-completed",
        in_progress: "status-in-progress",
        pending: "status-pending",
      }[status] || '';
    };

    // Метод удаления заявки
    const deleteOrder = async (orderId) => {
      if (!confirm("Вы уверены, что хотите удалить заявку?")) return;

      try {
        await api.delete(`orders/${orderId}/`);
        orders.value = orders.value.filter(order => order.id !== orderId);
      } catch (error) {
        console.error("Ошибка при удалении заявки:", error.response?.data || error.message);
      }
    };

    onMounted(fetchOrders);

    return { orders, formatDate, getStatusClass, deleteOrder };
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

.status-completed {
  color: green;
}

.status-in-progress {
  color: orange;
}

.status-pending {
  color: red;
}

.actions {
  display: flex;
  gap: 10px;
}

.edit-btn {
  color: #1e88e5;
  text-decoration: none;
  font-size: 18px;
}

.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: red;
  font-size: 18px;
}
</style>
