<template>
  <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
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

/* Content Styles */
.content {
  margin: 20px auto;
  max-width: 600px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Buttons */
.back-button,
.submit-button {
  background-color: darkslategray;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
}

.back-button:hover,
.submit-button:hover {
  background-color: darkslategray;
}

/* Form Styles */
.form-container {
  display: flex;
  flex-direction: column;
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
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

/* Message Styles */
.message {
  margin-top: 15px;
  color: green;
  font-weight: bold;
}

.message.error {
  color: red;
}
</style>