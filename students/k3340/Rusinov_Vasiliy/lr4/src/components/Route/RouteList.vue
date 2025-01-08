<script setup>
import { onMounted, ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();
const routes = ref([]);
const stats = ref({});

function getRoutes() {
  instance.get('/routes/', {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
  .then(response => {
    if (response.status === 200) {
      routes.value = response.data;
    }
  })
  .catch(error => console.log(error));
}

function deleteRoute(id) {
  instance.delete(`/routes/${id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
  .then(response => {
    if (response.status === 204) {
      getRoutes();
    }
  })
  .catch(error => console.log(error));
}

function getStats() {
  instance.get('/routes/stats/', {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
  .then(response => {
    if (response.status === 200) {
      stats.value = response.data;
    }
  })
  .catch(error => console.log(error));
}

function initialize() {
  getRoutes();
  getStats();
}

onMounted(() => {
  initialize();
});
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Маршруты</h2>
    <v-card
      width="400"
      :title="`Всего маршрутов: ${stats.total || 0}`"
      :text="`С прямым рейсом: ${stats.direct || 0}, с пересадками: ${stats.indirect || 0}`"
    >
    </v-card>
    <template v-for="route in routes" :key="route.id">
      <v-card
        width="400"
        :title="route.name"
        :subtitle="`${route.departure_airport} → ${route.destination_airport}`"
        :text="`Расстояние: ${route.distance} км,
        Промежуточные остановки: ${(route.stops || []).join(', ') || 'нет'}`"
      >
        <v-card-actions>
          <v-btn @click="index.push('/routes/' + route.id)">
            Изменить
          </v-btn>
          <v-btn @click="deleteRoute(route.id)">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
    <v-btn @click="index.push('/add-route')">Добавить маршрут</v-btn>
  </div>
</template>

<style scoped>
</style>
