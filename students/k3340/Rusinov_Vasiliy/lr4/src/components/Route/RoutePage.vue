<script setup>
import { onMounted, ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();

const form = ref({
  name: "",
  departure_airport: "",
  destination_airport: "",
  stops: [],
  distance: "",
});

const airports = ref([]); // Список аэропортов для выбора
const stopOptions = ref([]); // Возможные промежуточные остановки

// Получение данных маршрута
function getRoute() {
  instance.get(`/routes/${index.currentRoute.value.params.id}/`, {
    headers: {
      Authorization: `Token ${Token.token}`,
    },
  })
      .then((response) => {
        if (response.status === 200) {
          form.value = response.data;
        }
      })
      .catch((error) => console.log(error));
}

// Сохранение изменений маршрута
function saveRoute() {
  const {id, ...rest} = form.value;
  instance.patch(`/routes/${index.currentRoute.value.params.id}/`, rest, {
    headers: {
      Authorization: `Token ${Token.token}`,
    },
  })
      .then((response) => {
        if (response.status === 200) {
          index.push("/routes");
        }
      })
      .catch((error) => console.log(error));
}

// Загрузка аэропортов
function getAirports() {
  instance.get("/airports/", {
    headers: {
      Authorization: `Token ${Token.token}`,
    },
  })
      .then((response) => {
        if (response.status === 200) {
          airports.value = response.data.map((airport) => ({
            text: airport.name,
            value: airport.id,
          }));
        }
      })
      .catch((error) => console.log(error));
}

// Загрузка промежуточных остановок
function getStops() {
  instance.get("/airports/", {
    headers: {
      Authorization: `Token ${Token.token}`,
    },
  })
      .then((response) => {
        if (response.status === 200) {
          stopOptions.value = response.data.map((airport) => ({
            text: airport.name,
            value: airport.id,
          }));
        }
      })
      .catch((error) => console.log(error));
}

onMounted(() => {
  getRoute();
  getAirports();
  getStops();
});
</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Маршрут</h2>
      <v-text-field label="Название маршрута" v-model="form.name"></v-text-field>
      <v-select
          label="Аэропорт вылета"
          v-model="form.departure_airport"
          :items="airports"
          item-text="text"
          item-value="value"
      ></v-select>
      <v-select
          label="Аэропорт назначения"
          v-model="form.destination_airport"
          :items="airports"
          item-text="text"
          item-value="value"
      ></v-select>
      <v-select
          label="Промежуточные остановки"
          v-model="form.stops"
          :items="stopOptions"
          item-text="text"
          item-value="value"
          multiple
      ></v-select>
      <v-text-field label="Расстояние (км)" v-model="form.distance"></v-text-field>
      <v-btn @click="saveRoute" color="primary">Сохранить</v-btn>
    </div>
  </v-app>
</template>

<style scoped>
</style>
