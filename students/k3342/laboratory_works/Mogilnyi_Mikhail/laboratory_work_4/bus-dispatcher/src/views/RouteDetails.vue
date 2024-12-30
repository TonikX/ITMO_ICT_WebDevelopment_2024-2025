<template>
  <div class="container mt-5">
    <h2>Редактирование маршрута: {{ route.route_number }}</h2>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="route_number">Номер маршрута</label>
        <input
          type="text"
          id="route_number"
          v-model="route.route_number"
          class="form-control"
          disabled
        />
      </div>

      <div class="form-group">
        <label for="start_point">Начальная точка</label>
        <input
          type="text"
          id="start_point"
          v-model="route.start_point"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label for="end_point">Конечная точка</label>
        <input
          type="text"
          id="end_point"
          v-model="route.end_point"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label for="start_time">Время отправления</label>
        <input
          type="time"
          id="start_time"
          v-model="route.start_time"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label for="end_time">Время прибытия</label>
        <input
          type="time"
          id="end_time"
          v-model="route.end_time"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label for="interval_minutes">Интервал (мин.)</label>
        <input
          type="number"
          id="interval_minutes"
          v-model="route.interval_minutes"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label for="duration_minutes">Длительность (мин.)</label>
        <input
          type="number"
          id="duration_minutes"
          v-model="route.duration_minutes"
          class="form-control"
        />
      </div>

      <button type="submit" class="btn btn-primary">Сохранить изменения</button>
      <button type="button" class="btn btn-secondary" @click="cancelEdit">Отмена</button>
    </form>
  </div>
</template>

<script>
import { fetchRoute, updateRoute } from '@/api/route';

export default {
  data() {
    return {
      route: {
        route_number: '',
        start_point: '',
        end_point: '',
        start_time: '',
        end_time: '',
        interval_minutes: null,
        duration_minutes: null,
      },
    };
  },
  methods: {
    async loadRoute() {
      const route_number = this.$route.params.route_number;
      try {
        const routeData = await fetchRoute(route_number);
        this.route = routeData;
      } catch (error) {
        alert('Не удалось загрузить маршрут.');
      }
    },
    async submitForm() {
      try {
        await updateRoute(this.route.route_number, this.route);
        alert('Маршрут успешно обновлен');
        this.$router.push({ name: 'RouteList' });
      } catch (error) {
        alert('Не удалось обновить маршрут.');
      }
    },
    cancelEdit() {
      this.$router.push({ name: 'RouteList' });
    },
  },
  mounted() {
    this.loadRoute();
  },
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}

button {
  margin-top: 1rem;
  margin-right: 1rem;
}
</style>
