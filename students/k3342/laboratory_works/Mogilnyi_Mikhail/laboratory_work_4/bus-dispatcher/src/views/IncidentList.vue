<template>
  <div>
    <Navbar />

    <div class="container mt-5">
      <h1>Список инцидентов</h1>
      <button class="btn btn-primary mb-3" @click="showAddIncidentModal">Добавить инцидент</button>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>№</th>
            <th>Дата</th>
            <th>Причина</th>
            <th>Водитель</th>
            <th>Автобус</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(incident, index) in incidents" :key="incident.id">
            <td>{{ index + 1 }}</td>
            <td>{{ incident.incident_date }}</td>
            <td>{{ incident.reason }}</td>
            <td>{{ incident.schedule_details.driver }}</td>
            <td>{{ incident.schedule_details.bus }}</td>
            <td>
              <div class="button-group">
                <button class="btn btn-warning btn-sm action-button" @click="editIncident(incident)">Редактировать</button>
                <button class="btn btn-danger btn-sm action-button" @click="removeIncident(incident.id)">Удалить</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <AddEditIncidentModal
      v-if="showIncidentModalFlag"
      :incident="selectedIncident"
      :schedules="schedules"
      @close="closeIncidentModal"
      @save="saveIncident"
    />

    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import AddEditIncidentModal from '@/components/AddIncidentModal.vue';
import { getIncidents, deleteIncident, createIncident, updateIncident } from '@/api/incident.js';
import { getSchedules } from '@/api/schedule.js';

export default {
  components: {
    Navbar,
    Footer,
    AddEditIncidentModal,
  },
  data() {
    return {
      incidents: [],
      schedules: [],
      showIncidentModalFlag: false,
      selectedIncident: null,
    };
  },
  methods: {
    async loadIncidents() {
      try {
        const response = await getIncidents();
        this.incidents = response.data;
      } catch (error) {
        alert('Не удалось загрузить список инцидентов.');
      }
    },
    async loadSchedules() {
      try {
        const response = await getSchedules();
        this.schedules = response.data.map(schedule => ({
          id: schedule.id,
          driver: schedule.driver.name,
          bus: schedule.bus.registration_number,
        }));
      } catch (error) {
        alert('Не удалось загрузить расписания.');
      }
    },
    showAddIncidentModal() {
      this.selectedIncident = null;
      this.showIncidentModalFlag = true;
    },
    editIncident(incident) {
      this.$router.push({ name: 'IncidentDetails', params: { id: incident.id } });
    },
    closeIncidentModal() {
      this.showIncidentModalFlag = false;
    },
    async removeIncident(id) {
      try {
        await deleteIncident(id);
        alert('Инцидент успешно удален');
        this.loadIncidents();
      } catch (error) {
        alert('Не удалось удалить инцидент.');
      }
    },
    async saveIncident(incidentData) {
  try {
    if (this.selectedIncident) {
      await updateIncident(this.selectedIncident.id, incidentData);
    } else {
      const response = await createIncident(incidentData);
      this.incidents.push(response.data);
    }
    alert('Инцидент успешно сохранен');
    this.loadIncidents();
  } catch (error) {
    console.error(error.response?.data || error.message);
    alert('Не удалось сохранить инцидент.');
  }
  this.closeIncidentModal();
}
  },
  mounted() {
    this.loadIncidents();
    this.loadSchedules();
  },
};
</script>

<style scoped>
h1 {
  margin-bottom: 20px;
}

.button-group button {
  margin-right: 10px;
}
</style>
