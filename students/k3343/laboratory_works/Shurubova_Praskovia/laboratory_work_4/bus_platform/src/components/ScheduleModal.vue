<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="form-container" @click.stop>
      <h1>Добавить новое расписание</h1>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="driver">Выберите водителя:</label>
          <select v-model="form.driver" id="driver" required>
            <option v-for="driver in drivers" :key="driver.id" :value="driver.id">
              {{ driver.name }} {{ driver.surname }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="bus">Выберите автобус:</label>
          <select v-model="form.bus" id="bus" required>
            <option v-for="bus in buses" :key="bus.id" :value="bus.id">
              {{ bus.registration_num }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="route">Выберите маршрут:</label>
          <select v-model="form.route" id="route" required>
            <option v-for="route in routes" :key="route.id" :value="route.id">
              {{ route.start_point }} - {{ route.end_point }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="work_date">Дата работы:</label>
          <input type="date" v-model="form.work_date" id="work_date" required />
        </div>

        <div class="form-group">
          <label for="shift_start">Начало смены:</label>
          <input type="time" v-model="form.shift_start" id="shift_start" required />
        </div>

        <div class="form-group">
          <label for="shift_end">Конец смены:</label>
          <input type="time" v-model="form.shift_end" id="shift_end" required />
        </div>

        <div class="form-buttons">
          <button type="submit">Сохранить</button>
          <button type="button" @click="closeModal">Закрыть</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import apiClient from '@/api/axios';

export default {
  data() {
    return {
      form: {
        driver: '',
        bus: '',
        route: '',
        work_date: '',
        shift_start: '',
        shift_end: ''
      },
      drivers: [],
      buses: [],
      routes: []
    };
  },
  methods: {

    closeModal() {
      this.$emit('close');
    },

    async submitForm() {
      try {
        await apiClient.post('/driver-schedule/create/', this.form);
        this.$emit('schedule-added');
        this.closeModal();
      } catch (error) {
        console.error('Ошибка при добавлении расписания:', error);
        alert('Не удалось добавить расписание. Попробуйте позже.');
      }
    },


    async fetchOptions() {
      try {
        const [drivers, buses, routes] = await Promise.all([
          apiClient.get('/drivers/'),
          apiClient.get('/buses/'),
          apiClient.get('/routes/')
        ]);
        this.drivers = drivers.data;
        this.buses = buses.data;
        this.routes = routes.data;
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
      }
    }
  },

    created() {
      this.fetchOptions();
    },

    handleOverlayClick() {
        this.closeModal();
    }
};
</script>

<style scoped>

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.form-container {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  max-width: 550px;
  width: 100%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  animation: none;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

label {
  font-size: 16px;
  margin-bottom: 5px;
}

input, select {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.form-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

button {
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid #2C3643;
}

button[type="submit"] {
  background-color: #2C3643;
  color: white;
}

button[type="submit"]:hover {
  background-color: #1d2a35;
}

button[type="button"] {
  background-color: transparent;
  color: #2C3643;
  border: 1px solid #2C3643;
}

button[type="button"]:hover {
  background-color: #f1f1f1;
}
</style>
