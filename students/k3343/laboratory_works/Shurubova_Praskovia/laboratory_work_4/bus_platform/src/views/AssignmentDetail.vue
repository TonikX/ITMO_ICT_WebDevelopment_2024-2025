<template>
  <div class="form-container">
    <h1>Редактировать назначение автобуса</h1>
    <form @submit.prevent="updateAssignment">
      <div class="form-group">
        <label for="bus">Автобус:</label>
        <select v-model="assignment.bus" class="colour" id="bus" required>
          <option v-for="bus in buses" :key="bus.id" :value="bus.id">
            {{ bus.registration_num }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="route">Маршрут:</label>
        <select v-model="assignment.route" class="colour" id="route" required>
          <option v-for="route in routes" :key="route.id" :value="route.id">
            {{ route.route_num }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="start_date">Дата начала:</label>
        <input v-model="assignment.start_date" class="colour" id="start_date" type="date" required />
      </div>

      <div class="form-group">
        <label for="end_date">Дата окончания:</label>
        <input v-model="assignment.end_date" class="colour" id="end_date" type="date" />
      </div>

      <div class="form-buttons">
        <button type="submit">Сохранить</button>
        <router-link to="/assignment" class="back-to-list-btn">
          Вернуться к списку
        </router-link>
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
      assignment: null,
      buses: [],
      routes: [],
    };
  },
  async created() {
    try {
      const assignmentId = this.$route.params.id;

      const response = await apiClient.get(`/bus-assignments/${assignmentId}/update/`);  // без /update
      this.assignment = response.data;

      const busesResponse = await apiClient.get('/buses/');
      this.buses = busesResponse.data;

      const routesResponse = await apiClient.get('/routes/');
      this.routes = routesResponse.data;
    } catch (error) {
      console.error("Ошибка при загрузке данных:", error);
    }
  },
  methods: {
    async updateAssignment() {
      try {
        const assignmentId = this.$route.params.id;
        await apiClient.put(`/bus-assignments/${assignmentId}/update/`, this.assignment);
        alert("Данные обновлены!");
      } catch (error) {
        console.error("Ошибка при обновлении данных:", error);
      }
    },
  },
};
</script>

<style scoped>
.form-container {
  max-width: 500px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  margin: auto;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-size: 16px;
}

input,
select {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.form-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  text-decoration: none;
}

button:hover, .back-to-list-btn:hover {
  background-color: #2C3643;
  color: white;
}
</style>
