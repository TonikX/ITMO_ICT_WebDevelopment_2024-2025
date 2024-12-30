<template>
  <div>
    <button @click="$router.push('/customers')" class="back-button">Назад к клиентам</button>
    <h1>Автомобили клиента</h1>
    <div v-if="cars.length">
      <ul>
        <li v-for="car in cars" :key="car.id">
          {{ car.make }} {{ car.model }} ({{ car.license_plate }})
        </li>
      </ul>
    </div>
    <div v-else>
      <p>У клиента нет автомобилей.</p>
    </div>
    <button @click="addCar" class="add-button">Добавить автомобиль</button>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      cars: [],
    };
  },
  async created() {
    const customerId = this.$route.params.id;
    try {
      const response = await apiClient.get(`/cars/?customer_id=${customerId}`);
      this.cars = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке автомобилей клиента:', error);
    }
  },
  methods: {
    addCar() {
      this.$router.push(`/add-car/${this.$route.params.id}`);
    },
  },
};
</script>

<style scoped>
.back-button,
.add-button {
  margin: 10px 0;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button {
  background-color: #2196f3;
  color: white;
}

.add-button {
  background-color: #4caf50;
  color: white;
}

.back-button:hover {
  background-color: #1976d2;
}

.add-button:hover {
  background-color: #45a049;
}
</style>
