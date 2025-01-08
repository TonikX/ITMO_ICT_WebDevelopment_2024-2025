<script setup>
import { onMounted, ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();

const form = ref({
  flight_number: "",
  crew: "",
  route: "",
  plane: "",
  departure_datetime: "",
  arrival_datetime: "",
});

const flightId = index.currentRoute.value.params.id; // Получаем ID рейса из маршрута

// Функция для получения информации о рейсе
function getFlight() {
  instance.get(`/flights/${flightId}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
    .then(response => {
      if (response.status === 200) {
        form.value = response.data;
      }
    })
    .catch(error => console.log(error));
}

// Функция для сохранения изменений рейса
function saveFlight() {
  const { id, ...rest } = form.value;
  instance.patch(`/flights/${flightId}/`, rest, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
    .then(response => {
      if (response.status === 200) {
        index.push('/flights'); // Перенаправляем на страницу со списком рейсов
      }
    })
    .catch(error => console.log(error));
}

onMounted(() => {
  getFlight();
});
</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Рейс</h2>
      <v-text-field label="Номер рейса" v-model="form.flight_number"></v-text-field>
      <v-select
        label="Экипаж"
        v-model="form.crew"
        :items="form.crew_choices"
        item-text="name"
        item-value="id"
      ></v-select>
      <v-select
        label="Маршрут"
        v-model="form.route"
        :items="form.route_choices"
        item-text="name"
        item-value="id"
      ></v-select>
      <v-select
        label="Самолет"
        v-model="form.plane"
        :items="form.plane_choices"
        item-text="name"
        item-value="id"
      ></v-select>
      <v-text-field
        label="Дата отправления"
        v-model="form.departure_datetime"
        type="datetime-local"
      ></v-text-field>
      <v-text-field
        label="Дата прибытия"
        v-model="form.arrival_datetime"
        type="datetime-local"
      ></v-text-field>
      <v-btn @click="saveFlight">Сохранить</v-btn>
    </div>
  </v-app>
</template>

<style scoped>
</style>
