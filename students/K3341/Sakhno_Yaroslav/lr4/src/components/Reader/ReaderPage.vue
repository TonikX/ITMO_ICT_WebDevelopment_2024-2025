<script setup>
import {onMounted, ref} from "vue";
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

function getPaper(){
  instance.get(`/library/reader/${router.currentRoute.value.params.id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          form.value = response.data
        }
      }
  ).catch(error => console.log(error))
}

function savePaper(){
  const {id, ...rest} = form.value
  instance.patch(`/library/reader/${router.currentRoute.value.params.id}/`, rest, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          router.push('/readers')
        }
      }
  ).catch(error => console.log(error))
}

onMounted(() => {
  getPaper()
})

</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Читатель</h2>
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
      <v-btn @click="savePaper">Сохранить</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
