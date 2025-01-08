<script setup>
import { ref } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();

const form = ref({
  name: "",
  address: "",
  contact_info: "",
});

function createAirline() {
  instance.post("/airlines/", form.value, {
    headers: {
      Authorization: `Token ${Token.token}`,
    },
  })
  .then((response) => {
    if (response.status === 201) {
      index.push("/airlines"); // Переход на страницу со списком авиакомпаний
    }
  })
  .catch((error) => console.log(error));
}
</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Добавить авиакомпанию</h2>
      <v-text-field label="Название" v-model="form.name" class="mb-4"></v-text-field>
      <v-text-field label="Адрес" v-model="form.address" class="mb-4"></v-text-field>
      <v-text-field label="Контактная информация" v-model="form.contact_info" class="mb-4"></v-text-field>
      <v-btn @click="createAirline" color="primary">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>
/* Стили для формы */
</style>
