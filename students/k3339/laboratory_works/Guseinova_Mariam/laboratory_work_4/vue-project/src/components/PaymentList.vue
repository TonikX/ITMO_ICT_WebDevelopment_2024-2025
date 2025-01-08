<template>
  <header class="header">
    <h1 class="header-title">Autoservice</h1>
  </header>
  <div class="content">
    <div class="button-group">
      <button @click="$router.push('/main')" class="back-button">Назад</button>
      <button @click="$router.push('/payments/create')" class="create-button">Создать</button>
    </div>
    <h2 class="page-title">Список всех платежей</h2>

    <div v-if="payments.length">
      <ul class="payment-list">
        <li v-for="payment in payments" :key="payment.payment_id" class="payment-item">
          <div class="payment-details">
            <p><strong>Номер платежа:</strong> {{ payment.payment_id }}</p>
            <p><strong>Заказ:</strong> {{ payment.order }}</p>
            <p><strong>Метод оплаты:</strong> {{ payment.payment_method }}</p>
            <p><strong>Сумма оплаты:</strong> {{ payment.payment_amount }} ₽</p>
            <button @click="viewPaymentDetails(payment.payment_id)" class="view-button">Просмотр</button>
          </div>
        </li>
      </ul>
    </div>

    <p v-else class="no-payments">Платежи не найдены.</p>
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
/* General Styles */
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8f8f8;
}

/* Header Styles */
.header {
  background-color: #2a3d42; /* Dark teal color */
  color: white;
  padding: 30px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header-title {
  margin: 0;
  font-size: 28px;
}

/* Content Styles */
.content {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 22px;
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

/* Button Group */
.button-group {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.back-button, .create-button {
  background-color: #2a3d42;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button:hover, .create-button:hover {
  background-color: #1e2b2f; /* Darker teal on hover */
}

/* Payment List Styles */
.payment-list {
  list-style-type: none;
  padding-left: 0;
}

.payment-item {
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.payment-details p {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
}

.payment-details strong {
  color: #2a3d42;
}

/* View Button */
.view-button {
  background-color: #2a3d42;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.view-button:hover {
  background-color: #1e2b2f;
}

/* No Payments Message */
.no-payments {
  text-align: center;
  font-size: 18px;
  color: #ff6600;
  font-weight: bold;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .content {
    padding: 15px;
  }

  .header-title {
    font-size: 24px;
  }

  .page-title {
    font-size: 20px;
  }

  .payment-details p {
    font-size: 14px;
  }

  .back-button, .create-button {
    font-size: 14px;
    padding: 10px 15px;
  }

  .view-button {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>
