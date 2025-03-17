<template>
  <div class="payments-page">
    <h2 class="page-title">Список платежных поручений за период</h2>

    <!-- Форма для выбора периода -->
    <div class="date-range-form">
      <label for="start_date">Дата начала:</label>
      <input type="date" v-model="startDate" />

      <label for="end_date">Дата окончания:</label>
      <input type="date" v-model="endDate" />

      <button @click="fetchPaymentsByPeriod">Показать платежи</button>
    </div>

    <!-- Таблица платежей -->
    <table class="payments-table" v-if="payments.length">
      <thead>
        <tr>
          <th>ID поручения</th>
          <th>Статус поручения</th>
          <th>ID заявки</th>
          <th>Дата поручения</th>
          <th>Дата оплаты</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="payment in payments" :key="payment.id">
          <td>{{ payment.id }}</td>
          <td>{{ payment.payment_status }}</td>
          <td>{{ payment.order }}</td>
          <td>{{ payment.payment_order_date }}</td>
          <td>{{ payment.payment_date }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>Нет платежей за указанный период.</p>
  </div>
</template>

<script>
import { ref } from 'vue';
import api from '@/api';

export default {
  name: "PaymentsByPeriodPage",
  setup() {
    const payments = ref([]);
    const startDate = ref('');
    const endDate = ref('');

    // Метод для получения платежей за указанный период
    const fetchPaymentsByPeriod = async () => {
      try {
        // Проверка на пустые поля дат
        if (!startDate.value || !endDate.value) {
          alert("Пожалуйста, выберите обе даты.");
          return;
        }

        const url = `payment-orders-by-period/?start_date=${startDate.value}&end_date=${endDate.value}`;
        const { data } = await api.get(url);
        payments.value = data;
      } catch (error) {
        console.error("Ошибка загрузки платежей за период:", error.response.data);
        alert("Ошибка при загрузке данных.");
      }
    };

    return { payments, startDate, endDate, fetchPaymentsByPeriod };
  }
};
</script>

<style scoped>
/* Добавляем стили для страницы */
.payments-page {
  background-color: #f4f6f9;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.page-title {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
}

.date-range-form {
  margin-bottom: 20px;
}

.date-range-form label {
  margin-right: 10px;
}

.date-range-form input {
  padding: 8px;
  margin-right: 10px;
  border: 1px solid #ddd;
}

.date-range-form button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.date-range-form button:hover {
  background-color: #45a049;
}

/* Стили для таблицы */
.payments-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.payments-table th,
.payments-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.payments-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.payments-table th {
  background-color: #4CAF50;
  color: white;
  font-weight: bold;
}

.payments-table tr:hover {
  background-color: #f1f1f1;
}

@media (max-width: 768px) {
  .payments-table th, .payments-table td {
    font-size: 14px;
    padding: 8px;
  }
}
</style>
