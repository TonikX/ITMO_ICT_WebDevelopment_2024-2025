<template>
  <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
  <div>
    <button @click="$router.push('/payments/')" class="custom-button">Назад</button>
    <h1>Информация об оплате</h1>
    <div v-if="payment">
      <p>Номер платежа: {{ payment.payment_id }}</p>
      <p>Заказ: {{ payment.order }}</p>
      <p>Дата платежа: {{ formatDate(payment.payment_date) }}</p>
      <p>Метод оплаты: {{ payment.payment_method }}</p>
      <p>Сумма оплаты: {{ payment.payment_amount }} ₽</p>
    </div>
    <p v-else>Загружаем информацию...</p>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      payment: null,
    };
  },
  created() {
    this.fetchPayment();
  },
  methods: {
    async fetchPayment() {
      const paymentId = this.$route.params.id; // Получаем ID платежа из URL
      try {
        const response = await apiClient.get(`/payments/${paymentId}/`);
        this.payment = response.data;
      } catch (error) {
        console.error('Ошибка при получении информации о платеже:', error);
      }
    },
    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
      return new Date(date).toLocaleDateString('ru-RU', options); // Форматируем дату в удобочитаемый формат
    }
  },
};
</script>

<style scoped>

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

/* Header Styles */
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


/* Добавьте стили для кнопки и других элементов, если необходимо */
.back-button {
  background-color: darkslategray;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  text-align: center;
  margin: 20px 0;
}

.back-button:hover {
  background-color: darkslategray;
}
.custom-button {
  background-color: darkslategray !important; /* Зеленый цвет кнопок */
  color: white !important;
  margin-bottom: 10px;
  text-transform: none !important; /* Отключение заглавных букв */
  font-size: 16px;
}
</style>
