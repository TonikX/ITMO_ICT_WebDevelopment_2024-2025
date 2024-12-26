<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="form-container" @click.stop>
      <h1>Добавить новое назначение</h1>
      <form @submit.prevent="submitForm">
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
          <label for="start-date">Дата начала:</label>
          <input id="start-date" type="date" v-model="form.start_date" required />
        </div>

        <div class="form-group">
          <label for="end-date">Дата окончания:</label>
          <input id="end-date" type="date" v-model="form.end_date" />
        </div>

        <div class="form-buttons">
          <button type="submit">Добавить</button>
          <button type="button" @click="closeModal">Отмена</button>
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
        bus: '',
        route: '',
        start_date: "",
        end_date: "",
      },
    };
  },
  props: {
    routes: {
      type: Array,
      default: () => [],
    },
    buses: {
      type: Array,
      default: () => [],
    },
  },
  methods: {

    closeModal() {
      this.$emit("close");
    },

    async submitForm() {
      try {

        const payload = { ...this.form };
        if (!payload.end_date) {
          payload.end_date = null;
        }

        console.log('Отправляемые данные:', payload);


        await apiClient.post('/bus-assignments/create/', payload);
        this.$emit('assignment-added');
        this.closeModal();
      } catch (error) {
        console.error('Ошибка при добавлении автобуса:', error.response?.data || error.message);
        alert('Не удалось добавить автобус. Проверьте введенные данные.');
      }
      },

    handleOverlayClick() {
      this.closeModal();
    },
  },
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
  animation: fadeIn 0.3s ease-in-out;
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
