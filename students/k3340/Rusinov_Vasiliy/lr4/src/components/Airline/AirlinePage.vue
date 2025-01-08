<script setup>
import { onMounted, ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();

const form = ref({
  name: "",
  address: "",
  contact_info: "",
});

function getAirline() {
  instance.get(`/airlines/${index.currentRoute.value.params.id}/`, {
    headers: {
      Authorization: `Token ${Token.token}`,
    },
  })
  .then((response) => {
    if (response.status === 200) {
      form.value = response.data;
    }
  })
  .catch((error) => console.error("Ошибка при получении авиакомпании:", error));
}

function saveAirline() {
  const { id, ...rest } = form.value;
  instance.patch(`/airlines/${index.currentRoute.value.params.id}/`, rest, {
    headers: {
      Authorization: `Token ${Token.token}`,
    },
  })
  .then((response) => {
    if (response.status === 200) {
      index.push("/airlines");
    }
  })
  .catch((error) => {
    console.error("Ошибка при сохранении авиакомпании:", error.response?.data || error);
    alert("Ошибка: " + JSON.stringify(error.response?.data));
  });
}

onMounted(() => {
  getAirline();
});
</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Редактирование авиакомпании</h2>
      <v-text-field label="Название" v-model="form.name"></v-text-field>
      <v-text-field label="Адрес" v-model="form.address"></v-text-field>
      <v-text-field label="Контактная информация" v-model="form.contact_info"></v-text-field>
      <v-btn @click="saveAirline">Сохранить</v-btn>
    </div>
  </v-app>
</template>

<style scoped>
/* Стили можно оставить пустыми или добавить свои */
</style>
