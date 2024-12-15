<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const form = ref({
  reading_room: "",
  full_name: "",
  passport: "",
  birth_date: "",
  phone_number: "",
  education: "",
  registration_date: "",
})
function create(){
  instance.post('/library/reader/', form.value, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 201){
          router.push('/readers')
        }
      }
  ).catch(error => console.log(error))
}

</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Добавить читателя</h2>
      <v-text-field label="Читальный зал" v-model="form.reading_room"></v-text-field>
      <v-text-field label="ФИО" v-model="form.full_name"></v-text-field>
      <v-text-field label="Пасспорт" v-model="form.passport"></v-text-field>
      <v-text-field label="Дата рождения" v-model="form.birth_date"></v-text-field>
      <v-text-field label="Номер телефона" v-model="form.phone_number"></v-text-field>
      <v-select
          label="Образование"
          v-model="form.education"
          :items="['Начальное', 'Среднее', 'Высшее']"
      ></v-select>
      <v-text-field label="Дата регистрации" v-model="form.registration_date"></v-text-field>
      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
