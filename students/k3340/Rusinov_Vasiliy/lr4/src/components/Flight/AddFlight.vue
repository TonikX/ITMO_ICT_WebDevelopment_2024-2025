<script setup>
import { ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();

const form = ref({
  flight_number: "",          // Номер рейса
  route: "",                  // Маршрут (ID маршрута)
  plane: "",                  // Самолет (ID самолета)
  crew: "",                   // Экипаж (ID экипажа)
  departure_datetime: "",    // Время отправления
  arrival_datetime: "",      // Время прибытия
});

const routes = ref([]);       // Список доступных маршрутов
const planes = ref([]);       // Список доступных самолетов
const crews = ref([]);        // Список доступных экипажей

// Функция для получения маршрутов
function fetchRoutes() {
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

// Функция для получения самолетов
function fetchPlanes() {
  instance.get('/planes/', {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
    .then(response => {
      if (response.status === 200) {
        planes.value = response.data;
      }
    })
    .catch(error => console.log(error));
}

// Функция для получения экипажей
function fetchCrews() {
  instance.get('/crews/', {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
    .then(response => {
      if (response.status === 200) {
        crews.value = response.data;
      }
    })
    .catch(error => console.log(error));
}

// Функция для создания рейса
function create() {
  instance.post('/flights/', form.value, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
    .then(response => {
      if (response.status === 201) {
        index.push('/flights'); // Перенаправляем на страницу списка рейсов
      }
    })
    .catch(error => console.log(error));
}

// Загружаем маршруты, самолеты и экипажи при монтировании компонента
fetchRoutes();
fetchPlanes();
fetchCrews();
</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Добавить рейс</h2>

      <!-- Номер рейса -->
      <v-text-field
        label="Номер рейса"
        v-model="form.flight_number"
      ></v-text-field>

      <!-- Выбор маршрута -->
      <v-select
        label="Маршрут"
        v-model="form.route"
        :items="routes.map(route => ({ text: route.name, value: route.id }))"
        item-text="text"
        item-value="value"
      ></v-select>

      <!-- Выбор самолета -->
      <v-select
        label="Самолет"
        v-model="form.plane"
        :items="planes.map(plane => ({ text: plane.name, value: plane.id }))"
        item-text="text"
        item-value="value"
      ></v-select>

      <!-- Выбор экипажа -->
      <v-select
        label="Экипаж"
        v-model="form.crew"
        :items="crews.map(crew => ({ text: crew.name, value: crew.id }))"
        item-text="text"
        item-value="value"
      ></v-select>

      <!-- Дата отправления -->
      <v-text-field
        label="Дата отправления"
        v-model="form.departure_datetime"
        type="datetime-local"
      ></v-text-field>

      <!-- Дата прибытия -->
      <v-text-field
        label="Дата прибытия"
        v-model="form.arrival_datetime"
        type="datetime-local"
      ></v-text-field>

      <!-- Кнопка создания рейса -->
      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>
</style>
