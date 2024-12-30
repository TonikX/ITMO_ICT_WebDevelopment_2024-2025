<template>
  <div class="modal fade show" tabindex="-1" style="display: block; background: rgba(0, 0, 0, 0.5);" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Добавить расписание</h5>
          <button type="button" class="btn-close" aria-label="Close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="driver" class="form-label">Водитель</label>
              <select id="driver" class="form-control" v-model="newSchedule.driver" required>
                <option v-for="driver in drivers" :key="driver.id" :value="driver.id">{{ driver.name }}</option>
              </select>
            </div>

            <div class="mb-3">
              <label for="bus" class="form-label">Автобус</label>
              <select id="bus" class="form-control" v-model="newSchedule.bus" required>
                <option v-for="bus in buses" :key="bus.id" :value="bus.id">{{ bus.registration_number }}</option>
              </select>
            </div>

            <div class="mb-3">
              <label for="route" class="form-label">Маршрут</label>
              <select id="route" class="form-control" v-model="newSchedule.route" required>
                <option v-for="route in routes" :key="route.id" :value="route.id">{{ route.route_number }}</option>
              </select>
            </div>

            <div class="mb-3">
              <label for="work_date" class="form-label">Дата работы</label>
              <input type="date" id="work_date" class="form-control" v-model="newSchedule.work_date" required />
            </div>

            <div class="mb-3">
              <label for="shift_start" class="form-label">Начало смены</label>
              <input type="time" id="shift_start" class="form-control" v-model="newSchedule.shift_start" required />
            </div>

            <div class="mb-3">
              <label for="shift_end" class="form-label">Конец смены</label>
              <input type="time" id="shift_end" class="form-control" v-model="newSchedule.shift_end" required />
            </div>

            <div class="mb-3">
              <label for="status" class="form-label">Статус</label>
              <select id="status" class="form-control" v-model="newSchedule.status" required>
                <option value="0">Активно</option>
                <option value="1">Завершено</option>
                <option value="2">Отменено</option>
              </select>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Закрыть</button>
              <button type="submit" class="btn btn-primary">Добавить</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getDrivers, getBuses, getRoutes } from '@/api/schedule';

export default {
  props: {},
  data() {
    return {
      newSchedule: {
        driver: '',
        bus: '',
        route: '',
        work_date: '',
        shift_start: '',
        shift_end: '',
        status: '0',
      },
      drivers: [],
      buses: [],
      routes: [],
    };
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    async submitForm() {
      try {
        const scheduleData = {
          driver: this.newSchedule.driver,
          bus: this.newSchedule.bus,
          route: this.newSchedule.route,
          work_date: this.newSchedule.work_date,
          shift_start: this.newSchedule.shift_start,
          shift_end: this.newSchedule.shift_end,
          status: this.newSchedule.status,
        };

        this.$emit('add-schedule', scheduleData);
        this.newSchedule = { driver: '', bus: '', route: '', work_date: '', shift_start: '', shift_end: '', status: '0' }; // Reset form
      } catch (error) {
        alert('Не удалось добавить расписание.');
      }
    },
    async loadOptions() {
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
        alert('Не удалось загрузить данные для водителей, автобусов и маршрутов.');
      }
    },
  },
  mounted() {
    this.loadOptions();
  },
};
</script>

<style scoped>
.modal-dialog {
  max-width: 500px;
}
</style>
