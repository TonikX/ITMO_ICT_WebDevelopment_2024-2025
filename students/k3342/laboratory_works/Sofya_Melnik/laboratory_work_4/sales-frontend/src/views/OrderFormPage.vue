<template>
  <div class="order-form">
    <h2>{{ isEdit ? 'Редактировать заявку' : 'Создать заявку' }}</h2>

    <form @submit.prevent="handleSubmit">
      <!-- Услуга -->
      <div class="form-group">
        <label for="service">Услуга:</label>
        <select v-model="form.service" required @change="updateTotalCost">
          <option value="" disabled>Выберите услугу</option>
          <option v-for="service in services" :key="service.id" :value="service.id">
            {{ service.name }} - {{ service.unit }}
          </option>
        </select>
      </div>

      <!-- Количество -->
      <div class="form-group">
        <label for="quantity">Количество:</label>
        <input id="quantity" type="number" v-model.number="form.quantity" required min="1" @input="updateTotalCost" />
      </div>

      <!-- Стоимость -->
      <div class="form-group">
        <label for="total_cost">Общая стоимость:</label>
        <input id="total_cost" type="text" v-model="form.total_cost" readonly />
      </div>

      <!-- Сотрудник -->
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
        {{ isEdit ? 'Обновить заявку' : 'Создать заявку' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const isEdit = ref(false);
const isSubmitting = ref(false);
const form = ref({
  service: '',
  quantity: 1,
  employee: '',
  total_cost: 0,
});

const services = ref([]);
const employees = ref([]);
const clientData = ref(null);
const priceList = ref([]);

// Получение списка услуг
const fetchServices = async () => {
  try {
    const { data } = await api.get('/service-list/');
    services.value = data;
  } catch (error) {
    console.error("Ошибка загрузки услуг:", error);
  }
};

// Получение цен из прайс-листа
const fetchPriceList = async () => {
  try {
    const { data } = await api.get('/price-list/');
    priceList.value = data;
  } catch (error) {
    console.error("Ошибка загрузки цен:", error);
  }
};

// Получение данных клиента
const fetchClientData = async () => {
  try {
    const { data } = await api.get('/client-info/');
    clientData.value = data;
    console.log("Данные клиента:", clientData.value);
    if (!clientData.value || !clientData.value.id) {
      alert("Ошибка: клиент не привязан.");
    }
  } catch (error) {
    console.error("Ошибка загрузки данных клиента:", error);
    alert("Ошибка при получении данных клиента.");
  }
};

// Получение списка сотрудников
const fetchEmployees = async () => {
  try {
    const { data } = await api.get('/employees/');
    employees.value = data;
  } catch (error) {
    console.error("Ошибка загрузки сотрудников:", error);
  }
};

// Обновление стоимости заявки
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

// Получение заявки для редактирования
const fetchOrder = async (id) => {
  try {
    const { data } = await api.get(`orders/${id}/`);
    form.value = {
      service: data.service.id,
      quantity: data.quantity,
      employee: data.employee.id,
      total_cost: data.total_cost,
    };
  } catch (error) {
    console.error("Ошибка загрузки заявки:", error);
  }
};

// Валидация данных перед отправкой
const validateOrderData = () => {
  if (!form.value.service || !form.value.quantity || !form.value.employee) {
    alert("Ошибка: все поля обязательны для заполнения.");
    return false;
  }
  return true;
};

// Отправка заявки
const handleSubmit = async () => {
  if (!validateOrderData()) return;

  // if (!clientData.value) {
  //   await fetchClientData(); // Повторная загрузка клиента, если не загружен
  // }

  // if (!clientData.value || !clientData.value.id) {
  //   alert("Ошибка: данные клиента не загружены.");
  //   return;
  // }

  const orderData = {
    client_id: clientData.value.id,
    service_id: form.value.service,
    quantity: form.value.quantity,
    employee_id: form.value.employee,
    order_date: new Date().toISOString(),
    completion_date: new Date().toISOString(),
    total_cost: form.value.total_cost || 0,
    status: "pending",
  };

  console.log("Отправляем заявку:", orderData);

  isSubmitting.value = true;

  try {
    if (isEdit.value) {
      await api.put(`orders/${route.params.id}/`, orderData);
      alert("Заявка обновлена успешно!");
    } else {
      await api.post('orders/', orderData);
      alert("Заявка создана успешно!");
    }

    router.push('/orders');
  } catch (error) {
    console.error("Ошибка при отправке заявки:", error.response?.data || error.message);
    alert("Ошибка при отправке заявки: " + JSON.stringify(error.response?.data || error.message));
  } finally {
    isSubmitting.value = false;
  }
};

// Загрузка данных при монтировании
onMounted(() => {
  fetchServices();
  fetchPriceList();
  fetchClientData();
  fetchEmployees();

  if (route.params.id) {
    isEdit.value = true;
    fetchOrder(route.params.id);
  }
});
</script>

<style scoped>
.order-form {
  max-width: 600px;
  margin: auto;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-size: 16px;
  color: #555;
  margin-bottom: 8px;
  display: block;
}

input, select {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

input:focus, select:focus {
  border-color: #007bff;
  outline: none;
}

button {
  padding: 12px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  width: 100%;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}
</style>
