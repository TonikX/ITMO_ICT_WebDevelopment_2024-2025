<script setup>
import { onMounted, ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();
const planes = ref([]);

// Функция для получения списка самолетов
function getPlanes() {
  instance.get('/planes/', {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  }).then(response => {
    if (response.status === 200) {
      planes.value = response.data; // Присваиваем полученные данные в переменную planes
    }
  }).catch(error => console.log(error));
}

// Функция для удаления самолета
function deletePlane(id) {
  instance.delete(`/planes/${id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  }).then(response => {
    if (response.status === 204) {
      getPlanes(); // Перезагружаем список самолетов
    }
  }).catch(error => console.log(error));
}

onMounted(() => {
  getPlanes(); // Загружаем список самолетов при монтировании компонента
});
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Самолеты</h2>

    <!-- Перебираем все самолеты и отображаем информацию о каждом -->
    <template v-for="plane in planes" :key="plane.id">
      <v-card width="400" :title="plane.number" :subtitle="plane.model">
        <v-card-text>
          Вместимость: {{ plane.seats_capacity }} мест<br/>
          Скорость: {{ plane.speed }} км/ч<br/>
          Авиакомпания: {{ plane.airline }}
        </v-card-text>
        <v-card-actions>
          <v-btn @click="index.push('/planes/' + plane.id)">
            Изменить
          </v-btn>
          <v-btn @click="deletePlane(plane.id)">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <v-btn @click="index.push('/add-plane')">Добавить</v-btn> <!-- Кнопка для добавления нового самолета -->
  </div>
</template>

<style scoped>
</style>
