<template>
  <div class="crew-list">
    <!-- Кнопка назад -->
    <button @click="goBack" class="back-btn">Назад</button>

    <!-- Фильтрация -->
    <div class="filters">
      <label for="position-filter">Фильтр по позиции:</label>
      <input type="text" id="position-filter" v-model="positionFilter" @input="filterCrew" placeholder="Введите должность" />

      <label for="employee-filter">Фильтр по сотруднику:</label>
      <input type="text" id="employee-filter" v-model="employeeFilter" @input="filterCrew" placeholder="Введите код сотрудника" />
    </div>

    <!-- Кнопка добавления экипажа -->
    <button @click="openAddCrewModal" class="add-crew-btn">Добавить экипаж</button>

    <!-- Таблица экипажей -->
    <table>
      <thead>
      <tr>
        <th>Номер экипажа</th>
        <th>Код сотрудника</th>
        <th>ФИО</th>
        <th>Номер рейса</th>
        <th>Должность</th>
        <th>Дата медосмотра</th>
        <th>Статус проверки</th>
        <th>Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="crew in filteredCrewList" :key="crew.crew_number">
        <td>{{ crew.crew_number }}</td>
        <td>{{ crew.employee_code.employee_code }}</td>
        <td>{{ crew.employee_code.full_name }}</td>
        <td>{{ crew.flight_number }}</td>
        <td>{{ crew.flight_position }}</td>
        <td>{{ crew.medical_check_date }}</td>
        <td>{{ crew.clearance_status }}</td>
        <td>
          <button @click="openEditCrewModal(crew)" class="edit-btn">Редактировать</button>
          <button @click="deleteCrew(crew.crew_number)" class="delete-btn">Удалить</button>
        </td>
      </tr>
      </tbody>
    </table>

    <!-- Модальное окно для добавления экипажа -->
    <CrewForm v-if="isModalOpen" @close="closeAddCrewModal" @save="addCrew" />
    <EditCrewModal v-if="isEditModalOpen" :crew="selectedCrew" @close="closeEditCrewModal" @save="updateCrew"/>
  </div>
</template>

<script>
import axios from 'axios';
import CrewForm from '@/components/AddCrew.vue';
import EditCrewModal from "@/components/EditCrew.vue"; // Импортируем компонент для добавления экипажа

export default {
  components: {EditCrewModal, CrewForm },
  data() {
    return {
      crewList: [],
      filteredCrewList: [],
      positionFilter: '',
      employeeFilter: '',
      isModalOpen: false,
      isEditModalOpen: false,
      selectedCrew: null,
      token: localStorage.getItem('auth_token'),
    };
  },
  created() {
    this.loadCrewList();
  },
  methods: {
    async loadCrewList() {
      try {
        if (!this.token) {
          console.error('Токен не найден. Вы должны быть авторизованы.');
          return;
        }
        const response = await axios.get('/api/crews/', {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        this.crewList = response.data;
        this.filteredCrewList = this.crewList;
      } catch (error) {
        console.error('Ошибка при загрузке экипажей:', error);
      }
    },
    filterCrew() {
      this.filteredCrewList = this.crewList.filter((crew) => {
        const matchPosition = this.positionFilter
            ? crew.flight_position.toLowerCase().includes(this.positionFilter.toLowerCase())
            : true;
        const matchEmployee = this.employeeFilter
            ? crew.employee_code.toString().includes(this.employeeFilter)
            : true;
        return matchPosition && matchEmployee;
      });
    },
    openAddCrewModal() {
      this.isModalOpen = true;
    },
    closeAddCrewModal() {
      this.isModalOpen = false;
    },
    addCrew(newCrew) {
      this.crewList.push(newCrew);
      this.filterCrew();
      this.closeAddCrewModal();
    },
    goBack() {
      this.$router.push("/dashboard");
    },
    async deleteCrew(crewNumber) {
      const isConfirmed = confirm("Вы уверены, что хотите удалить этот рейс?");
      if (!isConfirmed) return;
      try {
        if (!this.token) {
          console.error("Токен не найден. Вы должны быть авторизованы.");
          return;
        }
        await axios.delete(`/api/crew/${crewNumber}/`, {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        // Обновление списка рейсов
        this.crewList = this.crewList.filter(crew => crew.crew_number !== crewNumber);
        this.filteredCrewList = this.crewList; // Применяем фильтрацию снова
      } catch (error) {
        console.error("Ошибка при удалении члена экипажа:", error);
      }
    },
    openEditCrewModal(crew) {
      this.selectedCrew = crew;
      this.isEditModalOpen = true;
    },
    closeEditCrewModal() {
      this.selectedCrew = null; // Очищаем выбранный рейс
      this.isEditModalOpen = false;
    },
    async updateCrew(updatedCrew) {
      const index = this.crewList.findIndex(crew => crew.crew_number === updatedCrew.crew_number);
      if (index !== -1) {
        this.crewList.splice(index, 1, updatedCrew);
      }
      this.filterCrew();
      this.closeEditCrewModal();
    },
  },
};
</script>

<style scoped>
.crew-list {
  padding: 20px;
}

.filters {
  margin-bottom: 20px;
}

input[type='text'] {
  padding: 10px;
  margin-right: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button.add-crew-btn,
.back-btn,
.edit-btn,
.delete-btn{
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
}

button.add-crew-btn:hover,
back-btn:hover,
.edit-btn:hover,
.delete-btn:hover,{
  background-color: #0056b3;
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

.filters input[type='text'] {
  padding: 8px;
  font-size: 1rem;
  border-radius: 5px;
}

.filters input[type='text']:focus {
  border-color: #007bff;
}
button.delete-btn {
  background-color: #dc3545;
}
button.delete-btn:hover {
  background-color: #c82333;
}
</style>
