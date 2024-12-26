<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="form-container" @click.stop>
      <h1>Добавить новый автобус</h1>
      <form @submit.prevent="submitBus">
        <div class="form-group">
          <label for="registration_num">Регистрационный номер:</label>
          <input v-model="newBus.registration_num" id="registration_num" type="text" placeholder="Введите номер автобуса" required />
        </div>

        <div class="form-group">
          <label for="type">Тип автобуса:</label>
          <input v-model="newBus.type" id="type" type="text" placeholder="Введите тип автобуса" required />
        </div>

        <div class="form-group">
          <label for="capacity">Вместимость:</label>
          <input v-model.number="newBus.capacity" id="capacity" type="number" placeholder="Введите вместимость" required />
        </div>

        <div class="form-group">
          <label for="status">Статус:</label>
          <select v-model="newBus.status" id="status" required>
            <option value="AVAILABLE">Свободен</option>
            <option value="IN_REPAIR">В ремонте</option>
            <option value="UNAVAILABLE">Занят</option>
          </select>
        </div>

        <div class="form-buttons">
          <button type="submit">Добавить автобус</button>
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
      newBus: {
        registration_num: '',
        type: '',
        capacity: null,
        status: '',
      },
    };
  },
  methods: {

    closeModal() {
      this.$emit('close');
    },

    async submitBus() {
      try {
        await apiClient.post('/buses/create/', this.newBus);
        this.$emit('bus-added');
        this.closeModal();
      } catch (error) {
        console.error('Ошибка при добавлении автобуса:', error);
        alert('Не удалось добавить автобус. Попробуйте позже.');
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
