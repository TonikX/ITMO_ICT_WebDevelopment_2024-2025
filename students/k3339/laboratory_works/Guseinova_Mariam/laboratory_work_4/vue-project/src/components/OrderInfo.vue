<template>
  <header class="header">
    <h1 class="header-title">Autoservice</h1>
  </header>
  <div class="content">
    <button @click="$router.push('/orders/')" class="custom-button">Назад</button>
    <h2 class="order-title">Информация о заказе</h2>
    <div v-if="order" class="order-details">
      <p><strong>Номер заказа:</strong> {{ order.order_id }}</p>
      <p><strong>Клиент:</strong> {{ order.customer }}</p>
      <p><strong>Автомобиль:</strong> {{ order.car }}</p>
      <p><strong>Сотрудник:</strong> {{ order.employee }}</p>
      <p><strong>Дата заказа:</strong> {{ formatDate(order.order_date) }}</p>
      <p><strong>Статус:</strong> {{ order.status === 'in_progress' ? 'В процессе' : 'Завершен' }}</p>
      <p><strong>Итоговая стоимость:</strong> {{ order.total_cost }} ₽</p>
    </div>
    <p v-else class="loading-text">Загружаем информацию...</p>
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
/* General Styles */
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f7f7f7;
}

/* Header Styles */
.header {
  background-color: #2a3d42; /* Dark teal color */
  color: white;
  padding: 25px;
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
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.order-title {
  font-size: 22px;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.order-details p {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
}

.order-details strong {
  font-weight: bold;
  color: #2a3d42;
}

/* Back Button Style */
.custom-button {
  background-color: #2a3d42;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 20px;
  display: block;
  text-align: center;
  width: 100%;
  transition: background-color 0.3s;
}

.custom-button:hover {
  background-color: #1e2b2f; /* Darker teal on hover */
}

/* Loading Text */
.loading-text {
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: #ff6600;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .content {
    padding: 15px;
  }

  .header-title {
    font-size: 24px;
  }

  .order-title {
    font-size: 20px;
  }

  .custom-button {
    font-size: 14px;
    padding: 10px 15px;
  }
}
</style>
