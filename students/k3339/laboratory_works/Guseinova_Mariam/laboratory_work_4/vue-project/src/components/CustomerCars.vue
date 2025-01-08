<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <button @click="$router.push('/customers')" class="custom-button">Назад к клиентам</button>
    <h1 class="page-title">Автомобили клиента</h1>

    <div v-if="cars.length" class="cars-list">
      <ul>
        <li v-for="car in cars" :key="car.id" class="car-item">
          <div class="car-info">
            <strong>{{ car.make }} {{ car.model }}</strong>
            <span class="license-plate">({{ car.license_plate }})</span>
          </div>
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
/* General Styles */
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

/* Page Title */
.page-title {
  text-align: center;
  margin-top: 20px;
  font-size: 28px;
  color: darkslategray;
}

/* Cars List Styles */
.cars-list {
  background-color: white;
  padding: 20px;
  margin: 20px auto;
  max-width: 600px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.car-item {
  margin-bottom: 15px;
  font-size: 18px;
}

.car-info {
  display: flex;
  justify-content: space-between;
}

.license-plate {
  color: #666;
}

/* Buttons */
.custom-button,
.add-button {
  background-color: darkslategray !important;
  color: white !important;
  padding: 10px 20px;
  font-size: 16px;
  text-transform: none !important;
  border-radius: 5px;
  cursor: pointer;
  display: block;
  width: 100%;
  margin-top: 15px;
}

.custom-button:hover,
.add-button:hover {
  background-color: #2f4f4f;
}

</style>
