<template>
  <div>
    <Navbar />

    <div class="container mt-5">
      <h1>Список расписаний</h1>
      <button class="btn btn-primary mb-3" @click="showAddScheduleModal">Добавить расписание</button>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>№</th>
            <th>Водитель</th>
            <th>Автобус</th>
            <th>Маршрут</th>
            <th>Статус</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(schedule, index) in schedules" :key="schedule.id">
            <td>{{ index + 1 }}</td>
            <td>{{ schedule.driver.name }}</td>
            <td>{{ schedule.bus.registration_number }}</td>
            <td>{{ schedule.route.route_number }}</td>
            <td>{{ getStatusText(schedule.status) }}</td>
            <td>
              <div class="button-group">
                <button class="btn btn-warning btn-sm action-button" @click="editSchedule(schedule.id)">Редактировать</button>
                <button class="btn btn-danger btn-sm action-button" @click="removeSchedule(schedule.id)">Удалить</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <AddScheduleModal v-if="showAddScheduleModalFlag" @close="closeAddScheduleModal" @add-schedule="addNewSchedule" />

    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import AddScheduleModal from '@/components/AddScheduleModal.vue';
import { getSchedules, createSchedule, deleteSchedule } from '@/api/schedule.js';

export default {
  components: {
    Navbar,
    Footer,
    AddScheduleModal,
  },
  data() {
    return {
      schedules: [],
      showAddScheduleModalFlag: false,
    };
  },
  methods: {
    async loadSchedules() {
      try {
        const response = await getSchedules();
        this.schedules = response.data;
      } catch (error) {
        alert('Не удалось загрузить список расписаний.');
      }
    },

    async addNewSchedule(newSchedule) {
      try {
        await createSchedule(newSchedule);
        alert('Расписание успешно добавлено');
        this.loadSchedules();
        this.closeAddScheduleModal();
      } catch (error) {
        alert('Не удалось добавить расписание.');
      }
    },

    async removeSchedule(id) {
      try {
        await deleteSchedule(id);
        alert('Расписание успешно удалено');
        this.loadSchedules();
      } catch (error) {
        alert('Не удалось удалить расписание.');
      }
    },

    showAddScheduleModal() {
      this.showAddScheduleModalFlag = true;
    },

    closeAddScheduleModal() {
      this.showAddScheduleModalFlag = false;
    },


    getStatusText(status) {
      switch (status) {
        case 'Completed':
          return 'Завершено';
        case 'Active':
          return 'Активно';
        case 'Canceled':
          return 'Отменено';
        default:
          return 'Неизвестно';
      }
    }
  },
  mounted() {
    this.loadSchedules();
  }
};
</script>
