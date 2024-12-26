<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="form-container" @click.stop>
      <h1>Добавить новый маршрут</h1>
      <form @submit.prevent="submitRoute">
        <div class="form-group">
          <label for="route_num">Номер маршрута:</label>
          <input v-model.number="newRoute.route_num" id="route_num" type="number" placeholder="Введите номер маршрута" required />
        </div>

        <div class="form-group">
          <label for="start_point">Начальный пункт:</label>
          <input v-model="newRoute.start_point" id="start_point" type="text" placeholder="Введите начальный пункт" required />
        </div>

        <div class="form-group">
          <label for="end_point">Конечный пункт:</label>
          <input v-model="newRoute.end_point" id="end_point" type="text" placeholder="Введите конечный пункт" required />
        </div>

        <div class="form-group">
          <label for="start_time">Время начала:</label>
          <input v-model="newRoute.start_time" id="start_time" type="time" required />
        </div>

        <div class="form-group">
          <label for="end_time">Время окончания:</label>
          <input v-model="newRoute.end_time" id="end_time" type="time" required />
        </div>

        <div class="form-group">
          <label for="interval">Интервал (мин.):</label>
          <input v-model.number="newRoute.interval" id="interval" type="number" placeholder="Введите интервал" required />
        </div>

        <div class="form-group">
          <label for="duration">Длительность (мин.):</label>
          <input v-model.number="newRoute.duration" id="duration" type="number" placeholder="Введите длительность" required />
        </div>

        <div class="form-buttons">
          <button type="submit">Добавить маршрут</button>
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
      newRoute: {
        route_num: null,
        start_point: "",
        end_point: "",
        start_time: "",
        end_time: "",
        interval: null,
        duration: null,
      },
    };
  },
  methods: {

    closeModal() {
      this.$emit("close");
    },

    async submitRoute() {
      try {
        await apiClient.post('/routes/create/', this.newRoute);
        this.$emit("route-added");
        this.closeModal();
      } catch (error) {
        console.error("Ошибка при добавлении маршрута:", error);
        alert("Не удалось добавить маршрут. Попробуйте позже.");
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
  max-width: 500px;
  width: 100%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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

input {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.modal-actions {
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

.form-buttons {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}
</style>
