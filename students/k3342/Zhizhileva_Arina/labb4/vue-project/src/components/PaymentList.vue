<template>
  <div>
    <button @click="$router.push('/main')" class="back-button">Назад</button>
    <button @click="$router.push('/payments/create')" class="back-button">Создать</button>
    <h1>Список всех платежей</h1>

    <div v-if="payments.length">
      <ul>
        <li v-for="payment in payments" :key="payment.payment_id">
          <div>
            <p>Номер платежа: {{ payment.payment_id }}</p>
            <p>Заказ: {{ payment.order }}</p>
            <p>Метод оплаты: {{ payment.payment_method }}</p>
            <p>Сумма оплаты: {{ payment.payment_amount }} ₽</p>
            <p>
              <button @click="viewPaymentDetails(payment.payment_id)">Просмотр</button>
            </p>
          </div>
        </li>
      </ul>
    </div>

    <p v-else>Платежи не найдены.</p>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      payments: [],
    };
  },
  created() {
    this.fetchPayments();
  },
  methods: {
    async fetchPayments() {
      try {
        const response = await apiClient.get('/payments/');
        this.payments = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке платежей:', error);
      }
    },
    viewPaymentDetails(paymentId) {
      this.$router.push(`/payments/${paymentId}`);
    }
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

button {
  background-color: #2196F3;
  color: white;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0b7dda;
}
</style>
