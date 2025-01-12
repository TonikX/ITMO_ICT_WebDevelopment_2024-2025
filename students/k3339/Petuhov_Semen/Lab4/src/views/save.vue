<template>
  <div class="manage-flights">
    <!-- Кнопка назад -->
    <button @click="goBack" class="back-button">Назад</button>

    <!-- Фильтрация -->
    <div class="filters">
      <label for="date-filter">Фильтр по дате:</label>
      <input type="date" id="date-filter" v-model="dateFilter" @change="filterFlights" />

      <label for="destination-filter">Фильтр по пункту назначения:</label>
      <input
          type="text"
          id="destination-filter"
          v-model="destinationFilter"
          @input="filterFlights"
          placeholder="Введите пункт назначения"
      />
    </div>

    <!-- Кнопка добавления рейса -->
    <button @click="openAddFlightModal" class="add-flight-btn">Добавить рейс</button>

    <!-- Таблица рейсов -->
    <table>
      <thead>
      <tr>
        <th>Номер рейса</th>
        <th>Пункт назначения</th>
        <th>Пункт вылета</th>
        <th>Дата и время вылета</th>
        <th>Дата и время прилета</th>
        <th>Статус</th>
        <th>Экипаж</th>
        <th>Действия</th> <!-- Добавляем колонку для действий -->
      </tr>
      </thead>
      <tbody>
      <tr v-for="flight in filteredFlights" :key="flight.flight_number">
        <td>{{ flight.flight_number }}</td>
        <td>{{ getTransitAddress(flight) }}</td>
        <td>{{ flight.airport_departure_address }}</td>
        <td>{{ formatDate(flight.departure_date) }}</td>
        <td>{{ formatDate(flight.arrival_date) }}</td>
        <td>{{ flight.status }}</td>
        <td>
          <ul>
            <li v-for="member in flight.crew" :key="member.employee_code">
              Код сотрудника: {{ member.employee_code }}
            </li>
          </ul>
        </td>
        <td>
          <button @click="deleteFlight(flight.flight_number)" class="delete-btn">Удалить</button> <!-- Кнопка удаления -->
        </td>
      </tr>
      </tbody>
    </table>

    <!-- Модальное окно для добавления рейса -->
    <AddFlightModal v-if="isModalOpen" @close="closeAddFlightModal" @save="addFlight" />
  </div>
</template>

<script>
import AddFlightModal from "@/components/AddFlight.vue";
import axios from "axios";

export default {
  components: {
    AddFlightModal,
  },
  data() {
    return {
      flights: [],
      filteredFlights: [],
      dateFilter: "",
      destinationFilter: "",
      isModalOpen: false,
      token: localStorage.getItem("auth_token"),
    };
  },
  created() {
    this.loadFlights();
  },
  methods: {
    async loadFlights() {
      try {
        if (!this.token) {
          console.error("Токен не найден. Вы должны быть авторизованы.");
          return;
        }

        const response = await axios.get("/api/flights/", {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        this.flights = response.data;
        this.filteredFlights = this.flights; // Изначально показываем все рейсы
      } catch (error) {
        console.error("Ошибка при загрузке рейсов:", error);
      }
    },
    filterFlights() {
      if (!this.dateFilter && !this.destinationFilter) {
        this.filteredFlights = this.flights;
        return;
      }

      this.filteredFlights = this.flights.filter((flight) => {
        const matchDate = this.dateFilter
            ? flight.departure_date.startsWith(this.dateFilter)
            : true;
        const matchDestination = this.destinationFilter
            ? this.getTransitAddress(flight)
                .toLowerCase()
                .includes(this.destinationFilter.toLowerCase())
            : true;
        return matchDate && matchDestination;
      });
    },
    formatDate(date) {
      const dateObj = new Date(date);
      return dateObj.toLocaleString();
    },
    getTransitAddress(flight) {
      if (flight.transit_stops && flight.transit_stops.length > 0) {
        return flight.transit_stops[0].airport_arrival_address;
      }
      return "";
    },
    openAddFlightModal() {
      this.isModalOpen = true;
    },
    closeAddFlightModal() {
      this.isModalOpen = false;
    },
    addFlight(newFlightData) {
      this.flights.push(newFlightData);
      this.filterFlights();
      this.closeAddFlightModal();
    },
    goBack() {
      this.$router.push("/dashboard");
    },
    // Метод удаления рейса
    async deleteFlight(flightNumber) {
      const isConfirmed = confirm("Вы уверены, что хотите удалить этот рейс?");
      if (!isConfirmed) return;

      try {
        if (!this.token) {
          console.error("Токен не найден. Вы должны быть авторизованы.");
          return;
        }

        await axios.delete(`/api/flights/${flightNumber}/`, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });

        // Обновление списка рейсов
        this.flights = this.flights.filter(flight => flight.flight_number !== flightNumber);
        this.filteredFlights = this.flights; // Применяем фильтрацию снова
      } catch (error) {
        console.error("Ошибка при удалении рейса:", error);
      }
    },
  },
};
</script>

<style scoped>
.manage-flights {
  padding: 20px;
}

.back-button,
.add-flight-btn,
.delete-btn { /* Стили для кнопок */
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button:hover,
.add-flight-btn:hover,
.delete-btn:hover {
  background-color: #0056b3;
}

.filters {
  margin-bottom: 20px;
}

input[type="date"],
input[type="text"] {
  padding: 10px;
  margin-right: 10px;
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

button.delete-btn {
  background-color: #dc3545; /* Красный для кнопки удаления */
}

button.delete-btn:hover {
  background-color: #c82333;
}
</style>
