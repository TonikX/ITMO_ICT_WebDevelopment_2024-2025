<template>
  <div>
    <h1>Редактирование инцидента</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="incident_date">Дата инцидента</label>
        <input
          type="date"
          id="incident_date"
          class="form-control"
          v-model="localIncident.incident_date"
          required
        />
      </div>
      <div class="form-group">
        <label for="reason">Причина</label>
        <textarea
          id="reason"
          class="form-control"
          v-model="localIncident.reason"
          required
        ></textarea>
      </div>
      <div class="form-group">
        <label for="schedule">Расписание</label>
        <select
          id="schedule"
          class="form-control"
          v-model="localIncident.schedule"
          required
        >
          <option v-for="schedule in schedules" :key="schedule.id" :value="schedule.id">
            {{ schedule.driver }} - {{ schedule.bus }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary">Сохранить</button>
    </form>
  </div>
</template>

<script>
import { getSchedules } from '@/api/schedule.js';
import { updateIncident } from '@/api/incident.js';

export default {
  props: {
    incident: Object,
  },
  data() {
    return {
      localIncident: { ...this.incident },
      schedules: [],
    };
  },
  async created() {
    await this.loadSchedules();
  },
  methods: {
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
    async handleSubmit() {
      try {
        await updateIncident(this.localIncident.id, this.localIncident);
        alert('Инцидент успешно обновлен');
        this.$router.push('/incidents');
      } catch (error) {
        alert('Не удалось обновить инцидент.');
      }
    },
  },
};
</script>
