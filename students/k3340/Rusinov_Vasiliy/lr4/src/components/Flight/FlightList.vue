<script setup>
import { onMounted, ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();
const flights = ref([]); // Для хранения списка рейсов

// Функция для получения списка рейсов
function getFlights() {
  instance.get('/flights/', {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
    .then(response => {
      if (response.status === 200) {
        flights.value = response.data;
      }
    })
    .catch(error => console.log(error));
}

// Функция для удаления рейса
function deleteFlight(id) {
  instance.delete(`/flights/${id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
    .then(response => {
      if (response.status === 204) {
        getFlights(); // Перезагружаем список рейсов после удаления
      }
    })
    .catch(error => console.log(error));
}

onMounted(() => {
  getFlights(); // Загружаем рейсы при монтировании компонента
});
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Рейсы</h2>
    <template v-for="flight in flights" :key="flight.id">
      <v-card width="400" :title="flight.flight_number">
        <v-card-subtitle>
          Маршрут: {{ flight.route.name }} - Самолет: {{ flight.plane.name }}
        </v-card-subtitle>
        <v-card-actions>
          <v-btn @click="index.push('/flights/' + flight.id)">
            Изменить
          </v-btn>
          <v-btn @click="deleteFlight(flight.id)">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
    <v-btn @click="index.push('/add-flight')">Добавить рейс</v-btn>
  </div>
</template>

<style scoped>
</style>
