<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <button @click="$router.push('/payments/')" class="back-button">Назад</button>
    <h1>Создание записи об оплате</h1>
    <form @submit.prevent="createPayment">

      <!-- Выбор существующего заказа -->
      <div class="form-group">
        <label for="order_id">Выберите заказ:</label>
        <select v-model="form.order_id" @change="fetchOrder" required>
          <option value="">Выберите заказ</option>
          <option v-for="order in orders" :key="order.order_id" :value="order.order_id">
            Заказ №{{ order.order_id }} - Статус: {{ order.status }}
          </option>
        </select>
      </div>

      <div v-if="order">
        <p>Заказ найден: {{ order.order_id }} - Статус: {{ order.status }}</p>
      </div>
      <div v-else>
        <p v-if="form.order_id">Заказ с таким номером не найден.</p>
      </div>

      <!-- Ввод метода оплаты -->
      <div class="form-group">
        <label for="payment_method">Метод оплаты:</label>
        <input type="text" v-model="form.payment_method" required />
      </div>

      <!-- Ввод суммы оплаты -->
      <div class="form-group">
        <label for="payment_amount">Сумма оплаты:</label>
        <input type="number" v-model="form.payment_amount" required />
      </div>

      <button type="submit" class="submit-button">Создать запись об оплате</button>
    </form>

    <p v-if="message" :class="{'message': true, 'error': message.includes('Ошибка') }">{{ message }}</p>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      form: {
        order_id: '',
        payment_method: '',
        payment_amount: 0.0,
      },
      order: null,
      orders: [], // Список заказов для выбора
      message: '',
    };
  },
  created() {
    this.fetchOrders();
  },
  watch: {
    'form.order_id': 'fetchOrder',
  },
  methods: {
    // Получение всех заказов для выбора
    async fetchOrders() {
      try {
        const response = await apiClient.get('/orders/');
        this.orders = response.data; // Заполняем список заказов
      } catch (error) {
        console.error('Ошибка при получении списка заказов:', error);
      }
    },
    // Получение информации по выбранному заказу
    async fetchOrder() {
      if (this.form.order_id) {
        try {
          const response = await apiClient.get(`/orders/${this.form.order_id}/`);
          this.order = response.data;
        } catch (error) {
          console.error('Ошибка при получении заказа:', error);
          this.order = null;
        }
      } else {
        this.order = null;
      }
    },
    // Создание записи об оплате
    async createPayment() {
      if (!this.order) {
        this.message = 'Невозможно создать запись об оплате. Заказ не найден.';
        return;
      }

      try {
        const response = await apiClient.post('/payments/', {
          order: this.order.order_id,
          payment_method: this.form.payment_method,
          payment_amount: this.form.payment_amount,
        });
        if (response.status === 201) {
          this.message = 'Запись об оплате успешно создана!';
          this.form = { order_id: '', payment_method: '', payment_amount: 0.0 }; // Очистка формы
        }
      } catch (error) {
        console.error('Ошибка при создании записи об оплате:', error);
        this.message = 'Ошибка при создании записи об оплате.';
      }
    },
  },
};
</script>

<style scoped>
/* General Styles */
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f9f9f9;
}

/* Header Styles */
.header {
  background-color: #2a3d42; /* Dark teal color */
  color: white;
  padding: 20px;
  text-align: center;
}

.header-title {
  margin: 0;
  font-size: 28px;
}

/* Form Styles */
form {
  margin: 20px auto;
  max-width: 600px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.form-group select {
  background-color: #fff;
}

/* Buttons */
.back-button,
.submit-button {
  background-color: #2a3d42;
  color: white;
  padding: 12px 20px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 20px;
  font-size: 16px;
}

.back-button:hover,
.submit-button:hover {
  background-color: #1e2b2f; /* Darker teal */
}

/* Message Styles */
.message {
  margin-top: 20px;
  font-weight: bold;
  font-size: 16px;
}

.message.error {
  color: red;
}

.message.success {
  color: green;
}
</style>
