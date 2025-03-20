<template>
  <div class="services-page">
    <h2 class="page-title">Рекламные услуги и прайс-лист</h2>

    <div v-if="isStaff" class="admin-actions">
      <button @click="showCreateForm = !showCreateForm" class="btn-create-service">
        {{ showCreateForm ? 'Отмена' : 'Создать услугу' }}
      </button>
    </div>

    <div v-if="showCreateForm && isStaff" class="create-service-form">
      <h3>Создать новую услугу</h3>
      <form @submit.prevent="addService">
        <label for="name">Название услуги:</label>
        <input v-model="newService.name" id="name" type="text" required />

        <label for="price">Цена:</label>
        <input v-model="newService.price" id="price" type="number" required />

        <label for="unit">Единица измерения:</label>
        <input v-model="newService.unit" id="unit" type="text" required />

        <label for="materials">Материалы:</label>
        <textarea v-model="newService.materials" id="materials" required></textarea>

        <label for="end_price">Дата окончания цены:</label>
        <input v-model="newService.end_price" id="end_price" type="date" required />

        <button type="submit">Добавить услугу</button>
      </form>
    </div>

    <div v-if="editServiceData && isStaff" class="create-service-form">
      <h3>Редактировать услугу</h3>
      <form @submit.prevent="updateService">
        <label for="edit-name">Название услуги:</label>
        <input v-model="editServiceData.name" id="edit-name" type="text" required />

        <label for="edit-price">Цена:</label>
        <input v-model="editServiceData.price" id="edit-price" type="number" required />

        <label for="edit-unit">Единица измерения:</label>
        <input v-model="editServiceData.unit" id="edit-unit" type="text" required />

        <label for="edit-materials">Материалы:</label>
        <textarea v-model="editServiceData.materials" id="edit-materials" required></textarea>

        <label for="end_price">Дата окончания цены:</label>
        <input v-model="editServiceData.end_price" id="end_price" type="date" required />

        <button type="submit">Сохранить изменения</button>
      </form>
    </div>

    <table class="services-table" v-if="services.length">
      <thead>
        <tr>
          <th>Название услуги</th>
          <th>Цена</th>
          <th>Единица измерения</th>
          <th>Материалы</th>
          <th v-if="isStaff">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="serviceItem in services" :key="serviceItem.id">
          <td>{{ serviceItem.name }}</td>
          <td>{{ getServicePrice(serviceItem.id) || 'Цена не установлена' }}</td>
          <td>{{ serviceItem.unit }}</td>
          <td>{{ serviceItem.materials }}</td>

          <td v-if="isStaff">
            <button @click="editService(serviceItem)">Редактировать</button>
            <button @click="deleteService(serviceItem.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Нет данных о услугах.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

const services = ref([]);
const priceList = ref([]);
const isStaff = ref(false);
const showCreateForm = ref(false);
const newService = ref({
  name: '',
  price: '',
  unit: '',
  materials: '',
  end_price: ''
});

const editServiceData = ref(null);

const fetchServices = async () => {
  try {
    const { data } = await api.get('price-list/');
    priceList.value = data;
  } catch (error) {
    console.error("Ошибка загрузки прайс-листа:", error);
  }
};

const fetchServiceDetails = async () => {
  try {
    const { data } = await api.get('services/');
    services.value = data;
  } catch (error) {
    console.error("Ошибка загрузки услуг:", error);
  }
};

const checkIfStaff = () => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user && user.is_staff) {
    isStaff.value = true;
  }
};

const getServicePrice = (serviceId) => {
  const price = priceList.value.find(p => p.service.id === serviceId);
  return price ? price.price : null;
};

const addService = async () => {
  try {
    const response = await api.post('services/', newService.value);
    services.value.push(response.data);

    const newPrice = {
      service_id: response.data.id,
      price: newService.value.price,
      start_price: new Date().toISOString(),
      end_price: newService.value.end_price
    };

    await api.post('price-list/', newPrice);

    resetForm();
    showCreateForm.value = false;
  } catch (error) {
    console.error("Ошибка добавления услуги:", error);
  }
};


const editService = (serviceItem) => {
  editServiceData.value = { ...serviceItem };
};

const updateService = async () => {
  try {
    const response = await api.put(`services/${editServiceData.value.id}/`, {
      name: editServiceData.value.name,
      unit: editServiceData.value.unit,
      materials: editServiceData.value.materials
    });

    const index = services.value.findIndex(s => s.id === editServiceData.value.id);
    if (index !== -1) {
      services.value[index] = response.data;
    }

    let priceToUpdate = priceList.value.find(p => p.service.id === editServiceData.value.id);

    if (priceToUpdate) {
      priceToUpdate.price = editServiceData.value.price;
      priceToUpdate.end_price = editServiceData.value.end_price;

      await api.put(`price-list/${priceToUpdate.id}/`, {
        service_id: priceToUpdate.service.id,
        price: editServiceData.value.price,
        start_price: priceToUpdate.start_price,
        end_price: editServiceData.value.end_price
      });
    } else {
      const newPriceData = {
        service_id: editServiceData.value.id,
        price: editServiceData.value.price,
        start_price: new Date().toISOString().split('T')[0],
        end_price: editServiceData.value.end_price
      };

      console.log("Отправляем в API:", newPriceData);

      const { data } = await api.post(`price-list/`, newPriceData);
      priceList.value.push(data);
    }

    editServiceData.value = null;
    showCreateForm.value = false;
  } catch (error) {
    console.error("Ошибка обновления услуги:", error.response ? error.response.data : error);
  }
};


const deleteService = async (id) => {
  try {
    await api.delete(`services/${id}/`);
    services.value = services.value.filter(service => service.id !== id);
  } catch (error) {
    console.error("Ошибка удаления услуги:", error);
  }
};

const resetForm = () => {
  newService.value = {
    name: '',
    price: '',
    unit: '',
    materials: ''
  };
};

onMounted(() => {
  fetchServices();
  fetchServiceDetails();
  checkIfStaff();
});
</script>

<style scoped>
.services-page {
  max-width: 1000px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.services-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
  font-size: 16px;
}

th {
  background-color: #4CAF50;
  color: white;
  font-weight: bold;
}

tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

tbody tr:hover {
  background-color: #e0e0e0;
  cursor: pointer;
}

.admin-actions {
  text-align: center;
  margin-bottom: 20px;
}

.btn-create-service {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
