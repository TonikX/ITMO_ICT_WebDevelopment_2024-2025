<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import {Api} from "@/services/api";

const Token = Api();

const form = ref({
  number: "",
  model: "",
  seats_capacity: "",
  speed: "",
  airline: "", // Assuming you might want to display the airline as well
});

// Функция для получения данных о самолете
function getPlane() {
  instance.get(`/planes/${index.currentRoute.value.params.id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  }).then(response => {
    if (response.status === 200) {
      form.value = response.data; // Присваиваем полученные данные в форму
    }
  }).catch(error => console.log(error));
}

// Функция для сохранения изменений
function savePlane() {
  const {id, ...rest} = form.value;
  instance.patch(`/planes/${index.currentRoute.value.params.id}/`, rest, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  }).then(response => {
    if (response.status === 200) {
      index.push('/planes');  // Переходим на страницу списка самолетов
    }
  }).catch(error => console.log(error));
}

onMounted(() => {
  getPlane(); // Загружаем данные о самолете при монтировании компонента
});
</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Самолет</h2>
      <v-text-field label="Номер" v-model="form.number"></v-text-field>
      <v-text-field label="Модель" v-model="form.model"></v-text-field>
      <v-text-field label="Вместимость" v-model="form.seats_capacity"></v-text-field>
      <v-text-field label="Скорость" v-model="form.speed"></v-text-field>
      <v-text-field label="Авиакомпания" v-model="form.airline" disabled></v-text-field>
      <!-- Здесь отображаем авиакомпанию, но не редактируем -->
      <v-btn @click="savePlane">Сохранить</v-btn>
    </div>
  </v-app>
</template>

<style scoped>
</style>
