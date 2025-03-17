<template>
  <div class="admin-order-form">
    <h2>Создать заявку</h2>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="client">Клиент:</label>
        <select v-model="form.client" required>
          <option value="" disabled>Выберите клиента</option>
          <option v-for="client in clients" :key="client.id" :value="client.id">
            {{ client.first_name }} {{ client.last_name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="service">Услуга:</label>
        <select v-model="form.service" required @change="updateTotalCost">
          <option value="" disabled>Выберите услугу</option>
          <option v-for="service in services" :key="service.id" :value="service.id">
            {{ service.name }} - {{ service.unit }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="quantity">Количество:</label>
        <input id="quantity" type="number" v-model.number="form.quantity" required min="1" @input="updateTotalCost" />
      </div>

      <div class="form-group">
        <label for="total_cost">Общая стоимость:</label>
        <input id="total_cost" type="text" v-model="form.total_cost" readonly />
      </div>

      <div class="form-group">
        <label for="employee">Сотрудник:</label>
        <select v-model="form.employee" required>
          <option value="" disabled>Выберите сотрудника</option>
          <option v-for="employee in employees" :key="employee.id" :value="employee.id">
            {{ employee.first_name }} {{ employee.last_name }}
          </option>
        </select>
      </div>

      <button type="submit" class="btn-submit" :disabled="isSubmitting">
        Создать заявку
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import { useRouter } from 'vue-router';

const router = useRouter();

const isSubmitting = ref(false);
const form = ref({
  client: '',
  service: '',
  quantity: 1,
  employee: '',
  total_cost: 0,
});

const services = ref([]);
const employees = ref([]);
const clients = ref([]);
const priceList = ref([]);

const fetchClients = async () => {
  try {
    const { data } = await api.get('/clients/');
    clients.value = data;
  } catch (error) {
    console.error("Ошибка загрузки клиентов:", error);
  }
};

const fetchServices = async () => {
  try {
    const { data } = await api.get('/service-list/');
    services.value = data;
  } catch (error) {
    console.error("Ошибка загрузки услуг:", error);
  }
};

const fetchEmployees = async () => {
  try {
    const { data } = await api.get('/employees/');
    employees.value = data;
  } catch (error) {
    console.error("Ошибка загрузки сотрудников:", error);
  }
};

const fetchPriceList = async () => {
  try {
    const { data } = await api.get('/price-list/');
    priceList.value = data;
  } catch (error) {
    console.error("Ошибка загрузки цен:", error);
  }
};

const updateTotalCost = () => {
  if (!form.value.service) {
    form.value.total_cost = 0;
    return;
  }
  const servicePrice = priceList.value.find(p => p.service.id === form.value.service);
  if (servicePrice) {
    form.value.total_cost = parseFloat(servicePrice.price) * (form.value.quantity || 1);
  } else {
    form.value.total_cost = 0;
  }
};

const handleSubmit = async () => {
  if (!form.value.service || !form.value.quantity || !form.value.employee) {
    alert("Все поля обязательны для заполнения.");
    return;
  }

  const orderData = {
    client_id: form.value.client,
    service_id: form.value.service,
    quantity: form.value.quantity,
    employee_id: form.value.employee,
    order_date: new Date().toISOString(),
    completion_date: new Date().toISOString(),
    total_cost: form.value.total_cost || 0,
    status: "pending",  // По умолчанию статус "Ожидает"
  };

  isSubmitting.value = true;
  try {
    await api.post('orders/', orderData);
    alert("Заявка создана успешно!");
    router.push('/admin-orders');
  } catch (error) {
    console.error("Ошибка при отправке заявки:", error.response?.data || error.message);
    alert("Ошибка при отправке заявки: " + JSON.stringify(error.response?.data || error.message));
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(() => {
  fetchClients();
  fetchServices();
  fetchPriceList();
  fetchEmployees();
});
</script>

<style scoped>
.admin-order-form {
  max-width: 600px;
  margin: auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 16px;
  color: #555;
}

input, select {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

button {
  width: 100%;
  padding: 12px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background: #0056b3;
}
</style>
