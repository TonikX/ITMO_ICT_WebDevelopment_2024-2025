<template>
  <div>
    <Navbar />

    <section class="mt-5 p-4 rounded shadow">
      <h2 class="fw-bold mb-4">Главная информация</h2>
      <div v-if="dashboardData">
        <div class="row">
          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Количество автобусов</h5>
                <p class="card-text">{{ dashboardData.total_buses }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Количество маршрутов</h5>
                <p class="card-text">{{ dashboardData.total_routes }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Общая протяженность маршрутов</h5>
                <p class="card-text">{{ dashboardData.total_distance }} мин.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>Загрузка данных...</p>
      </div>
    </section>

    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';

export default {
  name: 'Dashboard',
  components: {
    Navbar,
    Footer,
  },
  data() {
    return {
      dashboardData: null,
    };
  },
  mounted() {
    this.fetchDashboardData();
  },
  methods: {
    async fetchDashboardData() {
      try {
        const routesResponse = await fetch('http://localhost:8000/manage/routes', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          },
        });
        const routesData = await routesResponse.json();

        const busesResponse = await fetch('http://localhost:8000/manage/buses', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          },
        });
        const busesData = await busesResponse.json();

        const distanceResponse = await fetch('http://localhost:8000/manage/total-route-distance/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
          },
        });
        const distanceData = await distanceResponse.json();

        this.dashboardData = {
          total_buses: busesData.length,
          total_routes: routesData.length,
          total_distance: distanceData.total_distance,
        };
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
      }
    },
  },
};
</script>

<style scoped>
</style>
