<template>
  <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
  <div class="container">
    <div class="content">
      <button @click="$router.push('/orders/')" class="custom-button">Назад</button>
      <h2 class="form-title">Создание нового заказа</h2>
      <form @submit.prevent="createOrder" class="order-form">
        <div class="form-group">
          <label for="customer">Клиент:</label>
          <select v-model="form.customer" required class="form-control">
            <option v-for="client in clients" :key="client.customer_id" :value="client.customer_id">
              {{ client.name }} ({{ client.phone }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="car">Автомобиль:</label>
          <select v-model="form.car" required class="form-control">
            <option v-for="car in cars" :key="car.car_id" :value="car.car_id">
              {{ car.make }} {{ car.model }} ({{ car.license_plate }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="employee">Сотрудник:</label>
          <select v-model="form.employee" required class="form-control">
            <option v-for="employee in employees" :key="employee.employee_id" :value="employee.employee_id">
              {{ employee.name }} ({{ employee.position }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="status">Статус:</label>
          <select v-model="form.status" required class="form-control">
            <option value="in_progress">В процессе</option>
            <option value="completed">Завершен</option>
          </select>
        </div>

        <div class="form-group">
          <label for="total_cost">Итоговая стоимость:</label>
          <input type="number" v-model="form.total_cost" required placeholder="Введите итоговую стоимость" class="form-control" />
        </div>

        <div class="form-group">
          <label for="order_date">Дата заказа:</label>
          <input type="datetime-local" v-model="form.order_date" required class="form-control" />
        </div>

        <button type="submit" class="submit-button">Создать заказ</button>
      </form>
      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      form: {
        customer: '',
        car: '',
        employee: '',
        status: 'in_progress',
        total_cost: 0.0,
        order_date: '',
      },
      clients: [],
      cars: [],
      employees: [],
      message: '',
    };
  },
  created() {
    this.fetchClients();
    this.fetchCars();
    this.fetchEmployees();
  },
  methods: {
    async fetchClients() {
      try {
        const response = await apiClient.get('/clients/');
        this.clients = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка клиентов:', error);
      }
    },
    async fetchCars() {
      try {
        const response = await apiClient.get('/cars/');
        this.cars = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка автомобилей:', error);
      }
    },
    async fetchEmployees() {
      try {
        const response = await apiClient.get('/workers/');
        this.employees = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка сотрудников:', error);
      }
    },
    async createOrder() {
      try {
        this.form.order_date = new Date(this.form.order_date).toISOString().slice(0, 16);
        const response = await apiClient.post('/orders/', this.form);

        if (response.status === 201) {
          this.message = 'Заказ успешно создан!';
          this.form = { customer: '', car: '', employee: '', status: 'in_progress', total_cost: 0.0, order_date: '' };
        }
      } catch (error) {
        console.error('Ошибка при создании заказа:', error);
        this.message = 'Ошибка при создании заказа.';
      }
    },
  },
};
</script>

<style scoped>
/* General Styles */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
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
  font-size: 28px;
}

/* Content Styles */
.content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-title {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
}

.form-group .form-control {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 10px;
}

.form-group select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.form-group input[type="number"] {
  -moz-appearance: textfield;
}

.submit-button {
  background-color: darkslategray;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: darkslategray;
}

/* Message Styles */
.message {
  margin-top: 20px;
  font-weight: bold;
  text-align: center;
  color: #28a745; /* Green for success */
}

.message.error {
  color: #dc3545; /* Red for error */
}

/* Responsive Styles */
@media (max-width: 768px) {
  .container {
    padding: 10px;
  }

  .header-title {
    font-size: 22px;
  }

  .form-title {
    font-size: 20px;
  }

  .submit-button {
    font-size: 14px;
  }
}
</style>
