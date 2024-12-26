<template>
  <div>

    <h1>Управление назначениями автобусов</h1>

    <div class="filter-actions-container">
      <div class="filter-container">
        <label for="busFilter">Выберите автобус:</label>
        <select v-model="selectedBusId" id="busFilter" class="filter-select">
          <option value="">Все автобусы</option>
          <option v-for="bus in buses" :key="bus.id" :value="bus.id">
            {{ bus.registration_num }}
          </option>
        </select>
      </div>

      <button @click="showModal = true" class="add">Добавить назначение</button>
    </div>

    <table v-if="filteredAssignments.length > 0">
      <thead>
        <tr>
          <th>Автобус</th>
          <th>Маршрут</th>
          <th>Дата начала</th>
          <th>Дата окончания</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="assignment in filteredAssignments" :key="assignment.id">
          <td>{{ assignment.bus.registration_num }}</td>
          <td>№{{ assignment.route.route_num }}: {{ assignment.route.start_point }} - {{ assignment.route.end_point }}</td>
          <td>{{ assignment.start_date }}</td>
          <td>{{ assignment.end_date || "Не указана" }}</td>
          <td>
            <router-link :to="`/assignment/${assignment.id}/`" class="edit-btn">Редактировать</router-link>
            <button @click="deleteAssignment(assignment.id)" class="delete-btn">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Нет доступных назначений</p>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <button class="modal-close" @click="showModal = false">×</button>
        <AssignmentModal
          :buses="buses"
          :routes="routes"
          @close="showModal = false"
          @submit="fetchAssignments"
        />
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api/axios";
import Header from "@/components/Header.vue";
import AssignmentModal from "@/components/AssignmentModal.vue";

export default {
  components: {
    Header,
    AssignmentModal,
  },
  data() {
    return {
      assignments: [],
      buses: [],
      routes: [],
      selectedBusId: "",
      showModal: false,
    };
  },
  computed: {

    filteredAssignments() {
      if (this.selectedBusId) {
        return this.assignments.filter(
          assignment => assignment.bus.id === parseInt(this.selectedBusId)
        );
      }
      return this.assignments;
    },
  },
  methods: {
    async fetchAssignments() {
      try {
        const response = await apiClient.get("/bus-assignments/");
        this.assignments = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке назначений:", error);
      }
    },
    async fetchBuses() {
      try {
        const response = await apiClient.get("/buses/");
        this.buses = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке автобусов:", error);
      }
    },
    async fetchRoutes() {
      try {
        const response = await apiClient.get("/routes/");
        this.routes = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке маршрутов:", error);
      }
    },
    async deleteAssignment(assignmentId) {
      if (confirm("Вы уверены, что хотите удалить назначение?")) {
        try {
          await apiClient.delete(`/bus-assignments/${assignmentId}/delete/`);
          this.fetchAssignments();
        } catch (error) {
          console.error("Ошибка при удалении назначения:", error);
        }
      }
    },
    handleAssignmentAdded() {
      this.fetchAssignments();
    },
  },
  created() {
    this.fetchAssignments();
    this.fetchBuses();
    this.fetchRoutes();
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}

.filter-actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-container {
  display: flex;
  align-items: center;
  flex-direction: row;
  white-space: nowrap;
  gap: 20px;
}

button {
  padding: 10px;
  background-color: #2c3643;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #1f2c3d;
}

.add {
  padding: 5px 10px;
  margin-bottom: 20px;
  border-radius: 6px;
  border: 2px solid #2C3643;
  background-color: transparent;
  color: black;
  cursor: pointer;
}

.add:hover {
  background-color: #2C3643;
  color: white;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table th, table td {
  padding: 8px;
  border: 1px solid #ddd;
  text-align: left;
}

table th {
  background-color: #f4f4f4;
}

.delete-btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  color: red;
  font-weight: bold;
  font-size: 14px;
  transition: color 0.2s ease;
}

.delete-btn:hover {
  color: darkred;
  background: white;
}

/* Ссылка "Редактировать" */
.edit-btn {
  margin-left: 10px;
  color: #2c3643;
  text-decoration: none;
  font-weight: bold;
  font-size: 14px;
  border: 1px solid #2c3643;
  border-radius: 4px;
  padding: 4px 8px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.edit-btn:hover {
  background-color: #2c3643;
  color: white;
}


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

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  max-width: 50px;
  width: 100%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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

.filter-select {
  appearance: none;
  width: 100%;
  max-width: 400px;
  padding: 5px 35px 5px 10px;
  border-radius: 6px;
  border: 2px solid #2C3643;
  background-color: white;
  font-size: 16px;
  color: #333;
  cursor: pointer;
  position: relative;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath fill='%232C3643' d='M5.5 7l4.5 4.5L14.5 7H5.5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px 16px;
}

.filter-select:hover {
  border-color: #2C3643;
}
</style>
