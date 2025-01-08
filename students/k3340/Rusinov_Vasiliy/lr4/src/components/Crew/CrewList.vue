<script setup>
import { onMounted, ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();
const crews = ref([]);

// Функция для получения списка экипажей
function getCrews() {
  instance.get('/crews/', {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  }).then(response => {
    if (response.status === 200) {
      crews.value = response.data;
    }
  }).catch(error => console.log(error));
}

// Функция для удаления экипажа
function deleteCrew(id) {
  instance.delete(`/crews/${id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  }).then(response => {
    if (response.status === 204) {
      getCrews();  // Перезагружаем список после удаления
    }
  }).catch(error => console.log(error));
}

onMounted(() => {
  getCrews();  // Загружаем экипажи при монтировании компонента
});
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Список экипажей</h2>

    <template v-for="crew in crews" :key="crew.id">
      <v-card width="400" :title="`Экипаж №${crew.id}`">
        <v-card-text>
          <p><strong>Капитан:</strong> {{ crew.captain.employee }} ({{ crew.captain.role }})</p>
          <p><strong>Помощник капитана:</strong> {{ crew.co_pilot.employee }} ({{ crew.co_pilot.role }})</p>
          <p><strong>Навигатор:</strong> {{ crew.navigator.employee }} ({{ crew.navigator.role }})</p>
          <p><strong>Бортпроводники:</strong>
            <span v-for="(attendant, index) in crew.attendants" :key="attendant.id">
              {{ attendant.employee }} ({{ attendant.role }})
              <span v-if="index < crew.attendants.length - 1">, </span>
            </span>
          </p>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="index.push('/crews/' + crew.id)">
            Изменить
          </v-btn>
          <v-btn @click="deleteCrew(crew.id)">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <v-btn @click="index.push('/add-crew')">Добавить экипаж</v-btn>
  </div>
</template>

<style scoped>
</style>
