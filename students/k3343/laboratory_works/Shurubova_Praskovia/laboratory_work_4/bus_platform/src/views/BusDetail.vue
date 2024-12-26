<template>
  <div class="form-container">
    <h1>Информация об автобусе</h1>
    <form @submit.prevent="updateBus">
      <div class="form-group">
        <label for="registration_num">Регистрационный номер:</label>
        <input v-model="bus.registration_num" class="colour" id="registration_num" placeholder="Введите номер автобуса" required />
      </div>

      <div class="form-group">
        <label for="type">Тип автобуса:</label>
        <input v-model="bus.type" class="colour" id="type" placeholder="Введите тип автобуса" required />
      </div>

      <div class="form-group">
        <label for="capacity">Вместимость:</label>
        <input v-model.number="bus.capacity" class="colour" id="capacity" type="number" min="1" placeholder="Введите вместимость" required />
      </div>

      <div class="form-group">
        <label for="status">Статус:</label>
        <select v-model="bus.status" class="colour" id="status" required>
          <option value="AVAILABLE">Свободен</option>
          <option value="IN_REPAIR">В ремонте</option>
          <option value="UNAVAILABLE">Занят</option>
        </select>
      </div>

      <div class="form-buttons">
        <button type="submit">Сохранить</button>
        <router-link to="/buses" class="back-to-list-btn">Вернуться к списку автобусов</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import apiClient from "@/api/axios";
import Header from "@/components/Header.vue";

export default {
  components: {
    Header,
  },
  data() {
    return {
      bus: null,
    };
  },
  async created() {
    try {
      const busId = this.$route.params.id;
      const response = await apiClient.get(`/buses/${busId}/`);
      this.bus = response.data;
    } catch (error) {
      console.error("Ошибка при загрузке данных автобуса:", error);
    }
  },
  methods: {
    async updateBus() {
      try {
        const busId = this.$route.params.id;
        await apiClient.put(`/buses/${busId}/update/`, this.bus);
        alert("Данные автобуса обновлены!");
      } catch (error) {
        console.error("Ошибка при обновлении данных автобуса:", error);
        alert("Не удалось обновить данные автобуса.");
      }
    },
  },
};
</script>

<style scoped>

html, body {
  height: 100%;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}


.form-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-width: 1500px;
  width: 100%;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  text-align: left;
}


h1 {
  font-size: 24px;
  color: #2C3643;
  margin-bottom: 30px;
  text-align: center;
}


.form-group {
  margin-bottom: 20px;
  width: 100%;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 16px;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 2px solid #2C3643;
  font-size: 14px;
  color: #2C3643;
  box-sizing: border-box;
}

.form-group input::placeholder,
.form-group select::placeholder {
  color: #aaa;
}

.form-group input[type="number"],
.form-group input[type="date"] {
  -moz-appearance: textfield;
}

button, .back-to-list-btn {
  padding: 10px 20px;
  border-radius: 6px;
  background-color: #8ABEE5;
  color: black;
  border: none;
  cursor: pointer;
  font-size: 16px;

  max-width: 300px;
  margin-top: 20px;
  text-align: center;
}

button:hover, .back-to-list-btn:hover {
  background-color: #2C3643;
  color: white;
}

.form-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.back-to-list-btn {
  text-decoration: none;
  display: inline-block;
}
</style>
