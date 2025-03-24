<template>
  <div class="container">
    <h1 class="text-center mb-4">Отчет о состоянии автопарка</h1>

    <div class="report-section mb-4">
      <h3>Количество автобусов по категориям</h3>
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>Тип автобуса</th>
            <th>Количество автобусов</th>
            <th>Количество маршрутов</th>
            <th>Количество водителей</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="busType in report.bus_types" :key="busType.driver_class">
            <td>{{ busType.category__name }}</td>
            <td>{{ busType.bus_count }}</td>
            <td>{{ busType.route_count }}</td>
            <td>{{ busType.driver_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="report-section mb-4">
      <h3>Статистика по водителям</h3>
      <p><strong>Средний стаж водителей:</strong> {{ report.driver_stats.avg_experience }} лет</p>
      <p><strong>Общее количество водителей:</strong> {{ report.driver_stats.total_count }}</p>
    </div>

    <div class="report-section mb-4">
      <h3>Детали по маршрутам</h3>
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>Номер маршрута</th>
            <th>Точка отправления</th>
            <th>Точка назначения</th>
            <th>Количество автобусов</th>
            <th>Количество водителей</th>
            <th>Продолжительность маршрута (минуты)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="route in report.route_details" :key="route.route_number">
            <td>{{ route.route_number }}</td>
            <td>{{ route.start_point }}</td>
            <td>{{ route.end_point }}</td>
            <td>{{ route.bus_count }}</td>
            <td>{{ route.driver_count }}</td>
            <td>{{ route.duration_minutes }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="report-summary mb-4">
      <p><strong>Общая длительность всех маршрутов:</strong> {{ report.total_route_duration }} минут</p>
    </div>
  </div>
</template>

<script>
import { getParkStatusReport } from '@/api/api';

export default {
  data() {
    return {
      report: {
        bus_types: [],
        total_route_duration: 0,
        driver_stats: {
          avg_experience: 0,
          total_count: 0
        },
        route_details: []
      }
    };
  },
  mounted() {
    this.loadParkStatusReport(); // Загружаем отчет при монтировании компонента
  },
  methods: {
    loadParkStatusReport() {
      getParkStatusReport()
        .then(response => {
          this.report = response.data; // Сохраняем данные отчета в состояние компонента
        })
        .catch(error => {
          console.error('Ошибка при загрузке отчета:', error);
        });
    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

.report-section {
  margin-bottom: 30px;
}

table {
  margin-bottom: 20px;
}

.report-summary {
  font-size: 18px;
}

</style>
