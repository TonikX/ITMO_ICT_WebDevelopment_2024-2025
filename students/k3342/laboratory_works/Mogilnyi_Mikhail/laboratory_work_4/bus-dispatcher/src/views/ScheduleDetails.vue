<template>
  <div>
    <Navbar />

    <div class="container mt-5">
      <h1>Редактировать расписание</h1>
      <div v-if="schedule && drivers.length && buses.length && routes.length">
        <div class="form-group">
          <label for="driver">Водитель</label>
          <select v-model="schedule.driver" id="driver" class="form-control">
            <option v-for="driver in drivers" :key="driver.id" :value="driver.id">
              {{ driver.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="bus">Автобус</label>
          <select v-model="schedule.bus" id="bus" class="form-control">
            <option v-for="bus in buses" :key="bus.id" :value="bus.id">
              {{ bus.registration_number }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="route">Маршрут</label>
          <select v-model="schedule.route" id="route" class="form-control">
            <option v-for="route in routes" :key="route.id" :value="route.id">
              {{ route.route_number }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="work_date">Дата работы</label>
          <input v-model="schedule.work_date" id="work_date" class="form-control" type="date" />
        </div>
        <div class="form-group">
          <label for="shift_start">Начало смены</label>
          <input v-model="schedule.shift_start" id="shift_start" class="form-control" type="time" />
        </div>
        <div class="form-group">
          <label for="shift_end">Конец смены</label>
          <input v-model="schedule.shift_end" id="shift_end" class="form-control" type="time" />
        </div>
        <div class="form-group">
          <label for="status">Статус</label>
          <select v-model="schedule.status" id="status" class="form-control">
            <option value="0">Активно</option>
            <option value="1">Завершено</option>
            <option value="2">Отменено</option>
          </select>
        </div>
        <div class="button-group mt-3">
          <button class="btn btn-success" @click="saveChanges">Сохранить изменения</button>
          <button class="btn btn-danger" @click="deleteSchedule">Удалить расписание</button>
        </div>
      </div>
      <div v-else>
        <p>Загрузка...</p>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import { getScheduleById, updateSchedule, deleteSchedule, getDrivers, getBuses, getRoutes } from '@/api/schedule.js';

export default {
  components: {
    Navbar,
    Footer,
  },
  data() {
    return {
      schedule: null,
      drivers: [],
      buses: [],
      routes: [],
    };
  },
  methods: {
    async loadSchedule() {
      const scheduleId = this.$route.params.id;
      try {
        const response = await getScheduleById(scheduleId);
        this.schedule = response.data;
      } catch (error) {
        alert('Не удалось загрузить расписание.');
      }
    },
    async loadDependencies() {
      try {
        const [driversResponse, busesResponse, routesResponse] = await Promise.all([
          getDrivers(),
          getBuses(),
          getRoutes(),
        ]);
        this.drivers = driversResponse.data;
        this.buses = busesResponse.data;
        this.routes = routesResponse.data;
      } catch (error) {
        alert('Не удалось загрузить списки зависимостей.');
      }
    },
    async saveChanges() {
      const scheduleId = this.$route.params.id;
      try {
        await updateSchedule(scheduleId, this.schedule);
        alert('Изменения успешно сохранены');
        this.$router.push({ name: 'ScheduleList' });
      } catch (error) {
        alert('Не удалось сохранить изменения.');
      }
    },
    async deleteSchedule() {
      const scheduleId = this.$route.params.id;
      try {
        await deleteSchedule(scheduleId);
        alert('Расписание успешно удалено');
        this.$router.push({ name: 'ScheduleList' });
      } catch (error) {
        alert('Не удалось удалить расписание.');
      }
    },
  },
  async mounted() {
    await Promise.all([this.loadSchedule(), this.loadDependencies()]);
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
