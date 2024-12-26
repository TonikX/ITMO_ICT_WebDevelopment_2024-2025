<template>
  <div class="form-container" v-if="schedule && drivers.length && buses.length && routes.length">
    <h1>Редактировать расписание</h1>
    <form @submit.prevent="updateSchedule">

      <div class="form-group">
        <label for="driver">Водитель:</label>
        <select v-model="schedule.driver" class="colour" id="driver" required>
          <option v-for="driver in drivers" :key="driver.id" :value="driver.id">
            {{ driver.name }} {{ driver.surname }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="bus">Автобус:</label>
        <select v-model="schedule.bus" class="colour" id="bus" required>
          <option v-for="bus in buses" :key="bus.id" :value="bus.id">
            {{ bus.registration_num }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="route">Маршрут:</label>
        <select v-model="schedule.route" class="colour" id="route" required>
          <option v-for="route in routes" :key="route.id" :value="route.id">
            {{ route.start_point }} - {{ route.end_point }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="work_date">Дата работы:</label>
        <input v-model="schedule.work_date" class="colour" id="work_date" type="date" required />
      </div>

      <div class="form-group">
        <label for="shift_start">Начало смены:</label>
        <input v-model="schedule.shift_start" class="colour" id="shift_start" type="time" required />
      </div>

      <div class="form-group">
        <label for="shift_end">Конец смены:</label>
        <input v-model="schedule.shift_end" class="colour" id="shift_end" type="time" required />
      </div>

      <div class="form-buttons">
        <button type="submit">Сохранить</button>
        <router-link to="/driver-schedules" class="back-to-list-btn">
          Вернуться к списку расписаний
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import apiClient from "@/api/axios";


export default {
  data() {
    return {
      schedule: null,
      drivers: [],
      buses: [],
      routes: [],
    };
  },
  async created() {
    try {
      const scheduleId = this.$route.params.id;
      const [scheduleResponse, driversResponse, busesResponse, routesResponse] = await Promise.all([
        apiClient.get(`/driver-schedule/${scheduleId}/update/`),
        apiClient.get(`/drivers/`),
        apiClient.get(`/buses/`),
        apiClient.get(`/routes/`),
      ]);

      this.schedule = scheduleResponse.data;
      this.drivers = driversResponse.data;
      this.buses = busesResponse.data;
      this.routes = routesResponse.data;

    } catch (error) {
      console.error("Ошибка при загрузке данных:", error);
    }
  },
  methods: {
    async updateSchedule() {
      try {
        const scheduleId = this.$route.params.id;
        await apiClient.put(`/driver-schedule/${scheduleId}/update/`, this.schedule);
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
  gap: 20px;
  margin-top: 20px;
}

button,
.back-to-list-btn {
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

button:hover,
.back-to-list-btn:hover {
  background-color: #2C3643;
  color: white;
}
</style>
