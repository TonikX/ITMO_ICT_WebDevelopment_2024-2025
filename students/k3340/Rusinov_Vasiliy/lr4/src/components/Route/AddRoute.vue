<script setup>
import { ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();

// Форма для создания маршрута
const form = ref({
  name: "",
  departure_airport: "", // Ожидаем ID аэропорта
  destination_airport: "", // Ожидаем ID аэропорта
  stops: "", // Ввод остановок через запятую
  distance: null, // Расстояние маршрута
});

function create() {
  // Подготовка данных для отправки на сервер
  const updatedForm = {
    ...form.value,
    stops: form.value.stops
        ? form.value.stops.split(",").map(stop => stop.trim()).filter(stop => stop)
        : [], // Преобразуем строку остановок в массив строк
  };

  console.log("Отправляемые данные:", updatedForm);

  instance
      .post("/routes/", updatedForm, {
        headers: {
          Authorization: `Token ${Token.token}`,
        },
      })
      .then(response => {
        if (response.status === 201) {
          index.push("/routes"); // Переход на страницу маршрутов
        }
      })
      .catch(error => {
        console.error("Ошибка при создании маршрута:", error.response?.data || error.message);
        alert("Ошибка при создании маршрута. Проверьте данные и попробуйте снова.");
      });
}
</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Добавить маршрут</h2>
      <v-text-field
          label="Название маршрута"
          v-model="form.name"
      ></v-text-field>
      <v-text-field
          label="ID аэропорта отправления"
          v-model="form.departure_airport"
          type="number"
      ></v-text-field>
      <v-text-field
          label="ID аэропорта назначения"
          v-model="form.destination_airport"
          type="number"
      ></v-text-field>
      <v-text-field
          label="Промежуточные остановки (через запятую)"
          v-model="form.stops"
      ></v-text-field>
      <v-text-field
          label="Расстояние (км)"
          v-model="form.distance"
          type="number"
      ></v-text-field>
      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>
</style>
