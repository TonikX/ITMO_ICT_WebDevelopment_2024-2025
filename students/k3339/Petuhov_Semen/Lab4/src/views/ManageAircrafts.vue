<template>
  <div class="aircraft-list">
    <!-- Кнопка назад -->
    <button @click="goBack" class="back-button">Назад</button>

    <!-- Фильтрация -->
    <div class="filters">
      <label for="onboard-filter">Фильтр по бортовому номеру:</label>
      <input
          type="text"
          id="onboard-filter"
          v-model="onBoardFilter"
          @input="filterAircraft"
          placeholder="Введите бортовой номер"
      />

      <label for="company-filter">Фильтр по названию компании:</label>
      <input
          type="text"
          id="company-filter"
          v-model="companyFilter"
          @input="filterAircraft"
          placeholder="Введите название компании"
      />
    </div>
    <button @click="openAddAircraftModal" class="add-aircraft-btn">Добавить самолёт</button>
    <!-- Таблица самолётов -->
    <table>
      <thead>
      <tr>
        <th>Бортовой номер</th>
        <th>Название компании</th>
        <th>Налет часов</th>
        <th>Дата последнего обслуживания</th>
        <th>Дата выпуска</th>
        <th>Производитель</th>
        <th>Номер модели</th>
        <th>Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="aircraft in filteredAircraftList" :key="aircraft.onBoard_number">
        <td>{{ aircraft.onBoard_number }}</td>
        <td>{{ aircraft.company_name.company_name }}</td>
        <td>{{ aircraft.flight_hours }}</td>
        <td>{{ aircraft.last_maintenance_date || 'Не указана' }}</td>
        <td>{{ aircraft.manufacture_date || 'Не указана' }}</td>
        <td>{{ getManufacturer(aircraft) }}</td>
        <td>{{ getModelNumber(aircraft) }}</td>
        <td>
          <button @click="openEditAircraftModal(aircraft)" class="edit-btn">Редактировать</button>
          <button @click="deleteAircraft(aircraft.onBoard_number)" class="delete-btn">Удалить</button>
        </td>
      </tr>
      </tbody>
    </table>

    <AddAircraftModal v-if="isAddModalOpen" @close="closeAddAircraftModal" @save="addAircraft" />
    <EditAircraftModal v-if="isEditModalOpen" :aircraft="selectedAircraft" @close="closeEditAircraftModal" @save="updateAircraft"/>
  </div>
</template>

<script>
import axios from "axios";
import AddAircraftModal from "@/components/AddAircraft.vue";
import EditAircraftModal from "@/components/EditAircraft.vue";
export default {
  components: {EditAircraftModal, AddAircraftModal},
  data() {
    return {
      aircraftList: [], // Исходный список самолётов
      filteredAircraftList: [], // Отфильтрованный список самолётов
      onBoardFilter: "",
      companyFilter: "",
      isAddModalOpen: false,
      isEditModalOpen: false,
      selectedAircraft: null,
      token: localStorage.getItem("auth_token"), // Токен для авторизации
    };
  },
  created() {
    this.loadAircraftList();
  },
  methods: {
    goBack() {
      this.$router.push("/dashboard");
    },
    // Загрузка списка самолётов с сервера
    async loadAircraftList() {
      try {
        if (!this.token) {
          console.error("Токен не найден. Вы должны быть авторизованы.");
          return;
        }
        const response = await axios.get("/api/aircrafts/", {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        this.aircraftList = response.data;
        this.filteredAircraftList = this.aircraftList; // Изначально показываем всех самолётов
      } catch (error) {
        console.error("Ошибка при загрузке самолётов:", error);
      }
    },
    // Фильтрация списка самолётов
    filterAircraft() {
      this.filteredAircraftList = this.aircraftList.filter((aircraft) => {
        const matchOnBoard = this.onBoardFilter
            ? aircraft.onBoard_number
                .toLowerCase()
                .includes(this.onBoardFilter.toLowerCase())
            : true;
        const matchCompany = this.companyFilter
            ? aircraft.company_name.company_name
                .toLowerCase()
                .includes(this.companyFilter.toLowerCase())
            : true;
        return matchOnBoard && matchCompany;
      });
    },
    getManufacturer(aircraft) {
      if (aircraft.model_details) {
        return (aircraft.model_details.manufacturer);
      }
      return "";
    },
    getModelNumber(aircraft) {
      if (aircraft.model_details) {
        return (aircraft.model_details.model_number);
      }
      return "";
    },
    openAddAircraftModal() {
      this.isAddModalOpen = true;
    },
    closeAddAircraftModal() {
      this.isAddModalOpen = false;
    },
    addAircraft(newAircraftData) {
      this.aircraftList.push(newAircraftData);
      this.filterAircraft();
      this.closeAddAircraftModal();
    },
    async deleteAircraft(onBoard_number) {
      const isConfirmed = confirm("Вы уверены, что хотите удалить этот рейс?");
      if (!isConfirmed) return;
      try {
        if (!this.token) {
          console.error("Токен не найден. Вы должны быть авторизованы.");
          return;
        }
        await axios.delete(`/api/aircraft/${onBoard_number}/`, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        // Обновление списка рейсов
        this.aircraftList = this.aircraftList.filter(aircraft => aircraft.onBoard_number !== onBoard_number);
        this.filteredAircraftList = this.aircraftList; // Применяем фильтрацию снова
      } catch (error) {
        console.error("Ошибка при удалении рейса:", error);
      }
    },
    openEditAircraftModal(aircraft) {
      this.selectedAircraft = aircraft;
      this.isEditModalOpen = true;
    },
    closeEditAircraftModal() {
      this.selectedAircraft = null;
      this.isEditModalOpen = false;
    },
    async updateAircraft(updatedAircraft) {
      const index = this.aircraftList.findIndex(aircraft => aircraft.onBoard_number === updatedAircraft.onBoard_number);
      if (index !== -1) {
        this.aircraftList.splice(index, 1, updatedAircraft);
      }
      this.filterAircraft();
      this.closeEditAircraftModal();
    },
  },
};
</script>

<style scoped>
.aircraft-list {
  padding: 20px;
}

/* Стили для кнопки назад */
.back-button {
  margin-bottom: 20px;
}

.back-button,
.add-aircraft-btn,
.delete-btn,
.edit-btn,
.back-btn{
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-btn:hover,
.back-button:hover,
.add-aircraft-btn:hover,
.delete-btn:hover,
.edit-btn:hover{
  background-color: #0056b3;
}

.filters {
  margin-bottom: 20px;
}

.filters label {
  font-weight: bold;
  margin-right: 10px;
}

.filters input[type="text"] {
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
}

.filters input[type="text"]:focus {
  border-color: #007bff;
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
