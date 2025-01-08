<script setup>
import { onMounted, ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();
const airlines = ref([]);

// Получить список авиакомпаний
function getAirlines() {
  instance.get("/airlines/", {
    headers: {
      Authorization: `Token ${Token.token}`,
    },
  })
      .then((response) => {
        if (response.status === 200) {
          airlines.value = response.data;
        }
      })
      .catch((error) => console.log(error));
}

// Удалить авиакомпанию
function deleteAirline(id) {
  instance.delete(`/airlines/${id}/`, {
    headers: {
      Authorization: `Token ${Token.token}`,
    },
  })
      .then((response) => {
        if (response.status === 204) {
          getAirlines();
        }
      })
      .catch((error) => console.log(error));
}

// Выполнить при монтировании компонента
onMounted(() => {
  getAirlines();
});
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Авиакомпании</h2>
    <!-- Отобразить список авиакомпаний -->
    <template v-for="airline in airlines" :key="airline.id">
      <v-card
          width="400"
          :title="airline.name"
          class="mb-4"
      >
        <v-card-text>
          <p>Адрес: {{ airline.address }}</p>
          <p>Контактная информация: {{ airline.contact_info }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="index.push('/airlines/' + airline.id)">Изменить</v-btn>
          <v-btn color="red" @click="deleteAirline(airline.id)">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </template>
    <!-- Кнопка для добавления новой авиакомпании -->
    <v-btn @click="index.push('/add-airline')" class="mt-4">Добавить</v-btn>
  </div>
</template>

<style scoped>
/* Стили для отступов и выравнивания */
</style>
