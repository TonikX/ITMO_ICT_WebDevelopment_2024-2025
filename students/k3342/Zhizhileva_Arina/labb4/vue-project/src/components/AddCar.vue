<template>
  <div class="add-car-container">
    <button @click="$router.push(`/customer-cars/${this.$route.params.id}`)" class="back-button">Автомобили клиента</button>
    <h2>Добавить машину для клиента</h2>
    <form @submit.prevent="addCar">
      <div class="form-group">
        <label for="license_plate">Номерной знак:</label>
        <input v-model="car.license_plate" type="text" id="license_plate" required class="form-input" />
      </div>
      <div class="form-group">
        <label for="make">Марка:</label>
        <input v-model="car.make" type="text" id="make" required class="form-input" />
      </div>
      <div class="form-group">
        <label for="model">Модель:</label>
        <input v-model="car.model" type="text" id="model" required class="form-input" />
      </div>
      <div class="form-group">
        <label for="year">Год:</label>
        <input v-model="car.year" type="number" id="year" required class="form-input" />
      </div>
      <button type="submit" class="submit-button">Добавить машину</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      car: {
        license_plate: '',
        make: '',
        model: '',
        year: ''
      }
    };
  },
  methods: {
    async addCar() {
      try {
        await axios.post(`http://localhost:8000/api/cars/`, { ...this.car, customer: this.$route.params.id }, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        alert('Машина успешно добавлена');
        this.$router.push(`/customer-cars/${this.$route.params.id}`);
      } catch (error) {
        console.error('Ошибка при добавлении машины:', error);
        alert('Произошла ошибка при добавлении машины');
      }
    },
  },
};
</script>

<style scoped>
.add-car-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-size: 16px;
  color: #333;
  display: block;
}

.form-input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
}

.form-input:focus {
  border-color: #2196f3;
  outline: none;
}

button {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #fff;
  background-color: #4caf50;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}

.back-button {
  background-color: #2196f3;
  margin-bottom: 20px;
}

.back-button:hover {
  background-color: #1976d2;
}
</style>
