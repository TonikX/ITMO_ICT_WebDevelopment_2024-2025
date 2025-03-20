<template>
  <div class="orders-page">
    <h2 class="page-title">Заявки заказчика за период</h2>

    <div class="filters">
      <label for="client">Выберите клиента:</label>
      <select v-model="selectedClientId" id="client" required>
        <option v-for="client in clients" :key="client.id" :value="client.id">
          {{ client.first_name }} {{ client.last_name }}
        </option>
      </select>

      <label for="start-date">Дата начала:</label>
      <input type="date" v-model="startDate" required />

      <label for="end-date">Дата окончания:</label>
      <input type="date" v-model="endDate" required />

      <button @click="fetchOrders">Показать заявки</button>
    </div>

    <table v-if="orders.length > 0" class="orders-table">
      <thead>
        <tr>
          <th>Номер заявки</th>
          <th>Дата заявки</th>
          <th>Статус заявки</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.order_date }}</td>
          <td>{{ order.status }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Нет заявок за выбранный период.</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '@/api';

export default {
  name: "OrdersByClientAndPeriod",
  setup() {
    const clients = ref([]);
    const selectedClientId = ref(null);
    const startDate = ref('');
    const endDate = ref('');
    const orders = ref([]);

    const fetchClients = async () => {
      try {
        const { data } = await api.get('/clients/');
        clients.value = data;
      } catch (error) {
        console.error('Ошибка при загрузке клиентов:', error.response.data);
      }
    };

    const fetchOrders = async () => {
      if (!selectedClientId.value || !startDate.value || !endDate.value) {
        console.log('Выберите клиента и укажите период');
        return;
      }

      try {
        const { data } = await api.get('/orders-by-client/', {
          params: {
            client_id: selectedClientId.value,
            start_date: startDate.value,
            end_date: endDate.value,
          },
        });
        orders.value = data;
      } catch (error) {
        console.error('Ошибка при загрузке заявок:', error.response.data);
      }
    };

    onMounted(() => {
      fetchClients();
    });

    return { clients, selectedClientId, startDate, endDate, orders, fetchOrders };
  }
};
</script>

<style scoped>
.orders-page {
  background-color: #f9f9f9;
  padding: 20px;
}

.orders-table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.orders-table th, .orders-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.orders-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.filters {
  margin-bottom: 20px;
}

.filters label {
  display: block;
  margin-bottom: 5px;
}

.filters select,
.filters input {
  width: 200px;
  padding: 8px;
  margin-bottom: 15px;
}

.filters button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.filters button:hover {
  background-color: #45a049;
}
</style>
