<template>
  <div>
    <Navbar />

    <div class="container mt-5">
      <h1>Список маршрутов</h1>
      <button class="btn btn-primary mb-3" @click="showAddRouteModal">Добавить маршрут</button>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>№</th>
            <th>Номер маршрута</th>
            <th>Начальная точка</th>
            <th>Конечная точка</th>
            <th>Время отправления</th>
            <th>Время прибытия</th>
            <th>Интервал (мин.)</th>
            <th>Длительность (мин.)</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(route, index) in routes" :key="route.route_number">
            <td>{{ index + 1 }}</td>
            <td>
              <a href="#" @click.prevent="viewRouteDetails(route)">
                {{ route.route_number }}
              </a>
            </td>
            <td>{{ route.start_point }}</td>
            <td>{{ route.end_point }}</td>
            <td>{{ route.start_time }}</td>
            <td>{{ route.end_time }}</td>
            <td>{{ route.interval_minutes }}</td>
            <td>{{ route.duration_minutes }}</td>
            <td>
              <div class="button-group">
                <button class="btn btn-warning btn-sm action-button" @click="editRoute(route)">Редактировать</button>
                <button class="btn btn-danger btn-sm action-button" @click="removeRoute(route.route_number)">Удалить</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <AddRouteModal
        v-if="showAddRouteModalFlag"
        :newRoute="newRoute"
        @add-route="addNewRoute"
        @close="closeAddRouteModal"
      />
    </div>

    <Footer />
  </div>
</template>

<script>
import AddRouteModal from '@/components/AddRouteModal.vue';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import { fetchRoutes, addRoute, deleteRoute } from '@/api/route';

export default {
  components: {
    AddRouteModal,
    Navbar,
    Footer,
  },
  data() {
    return {
      routes: [],
      newRoute: {
        route_number: '',
        start_point: '',
        end_point: '',
        start_time: '',
        end_time: '',
        interval_minutes: null,
        duration_minutes: null,
      },
      showAddRouteModalFlag: false,
    };
  },
  methods: {
    async loadRoutes() {
      try {
        this.routes = await fetchRoutes();
      } catch (error) {
        alert('Не удалось загрузить список маршрутов.');
      }
    },
    async addNewRoute(newRoute) {
      try {
        await addRoute(newRoute);
        alert('Маршрут успешно добавлен');
        this.loadRoutes();
        this.newRoute = {
          route_number: '',
          start_point: '',
          end_point: '',
          start_time: '',
          end_time: '',
          interval_minutes: null,
          duration_minutes: null,
        };
        this.closeAddRouteModal();
      } catch (error) {
        alert('Не удалось добавить маршрут.');
      }
    },
    async removeRoute(route_number) {
      try {
        await deleteRoute(route_number);
        alert('Маршрут успешно удален');
        this.loadRoutes();
      } catch (error) {
        alert('Не удалось удалить маршрут.');
      }
    },
    showAddRouteModal() {
      this.showAddRouteModalFlag = true;
    },
    closeAddRouteModal() {
      this.showAddRouteModalFlag = false;
    },
    editRoute(route) {
      this.$router.push({ name: 'RouteDetails', params: { route_number: route.route_number } });
    },
    viewRouteDetails(route) {
      this.$router.push({ name: 'RouteDetails', params: { route_number: route.route_number } });
    },
  },
  mounted() {
    this.loadRoutes();
  },
};
</script>

<style scoped>
h1 {
  margin-bottom: 20px;
}

.table {
  margin-top: 20px;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.button-group button {
  margin-right: 10px;
}
</style>
