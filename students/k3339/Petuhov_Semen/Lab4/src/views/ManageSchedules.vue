<template>
  <div class="schedule-list">
    <!-- Кнопка назад -->
    <button @click="goBack" class="back-button">Назад</button>

    <!-- Фильтрация -->
    <div class="filters">
      <label for="schedule-filter">Фильтр по номеру расписания:</label>
      <input
          type="text"
          id="schedule-filter"
          v-model="scheduleFilter"
          @input="filterSchedules"
          placeholder="Введите номер расписания"
      />

      <label for="departure-filter">Фильтр по адресу отправления:</label>
      <input
          type="text"
          id="departure-filter"
          v-model="departureFilter"
          @input="filterSchedules"
          placeholder="Введите адрес отправления"
      />

      <label for="arrival-filter">Фильтр по адресу прибытия:</label>
      <input
          type="text"
          id="arrival-filter"
          v-model="arrivalFilter"
          @input="filterSchedules"
          placeholder="Введите адрес прибытия"
      />
    </div>

    <!-- Таблица расписаний -->
    <table>
      <thead>
      <tr>
        <th>Номер расписания</th>
        <th>Время отправления</th>
        <th>Время прибытия</th>
        <th>Адрес отправления</th>
        <th>Адрес прибытия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="schedule in filteredSchedules" :key="schedule.schedule_number">
        <td>{{ schedule.schedule_number }}</td>
        <td>{{ schedule.departure_time || "Не указано" }}</td>
        <td>{{ schedule.arrival_time || "Не указано" }}</td>
        <td>{{ schedule.airport.address }}</td>
        <td>{{ schedule.transit_stops[0]?.airport_arrival_address || "Не указано" }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      schedules: [], // Исходный список расписаний
      filteredSchedules: [], // Отфильтрованный список расписаний
      scheduleFilter: "", // Фильтр по номеру расписания
      departureFilter: "", // Фильтр по адресу отправления
      arrivalFilter: "", // Фильтр по адресу прибытия
      token: localStorage.getItem("auth_token"), // Токен для авторизации
    };
  },
  created() {
    this.loadSchedules();
  },
  methods: {
    // Загрузка расписаний с сервера
    async loadSchedules() {
      try {
        if (!this.token) {
          console.error("Токен не найден. Вы должны быть авторизованы.");
          return;
        }
        const response = await axios.get("/api/schedules/", {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        this.schedules = response.data;
        this.filteredSchedules = this.schedules; // Изначально показываем все расписания
      } catch (error) {
        console.error("Ошибка при загрузке расписаний:", error);
      }
    },
    // Фильтрация списка расписаний
    filterSchedules() {
      this.filteredSchedules = this.schedules.filter((schedule) => {
        const matchSchedule = this.scheduleFilter
            ? schedule.schedule_number.toString().includes(this.scheduleFilter)
            : true;
        const matchDeparture = this.departureFilter
            ? schedule.airport.address
                .toLowerCase()
                .includes(this.departureFilter.toLowerCase())
            : true;
        const matchArrival = this.arrivalFilter
            ? schedule.transit_stops[0]?.airport_arrival_address
                .toLowerCase()
                .includes(this.arrivalFilter.toLowerCase())
            : true;
        return matchSchedule && matchDeparture && matchArrival;
      });
    },
    // Возврат на страницу /dashboard
    goBack() {
      this.$router.push("/dashboard");
    },
  },
};
</script>

<style scoped>
.schedule-list {
  padding: 20px;
}

.back-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
}

.back-button:hover {
  background-color: #0056b3;
}

.filters {
  margin-bottom: 20px;
}

input[type="text"] {
  padding: 10px;
  margin-right: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ccc;
}

th {
  background-color: #f4f4f4;
}

.filters label {
  font-weight: bold;
  margin-right: 5px;
}

.filters input[type="text"]:focus {
  border-color: #007bff;
}
</style>
