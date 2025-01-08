<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import {Api} from "@/services/api";

const Token = Api()

const form = ref({
  name : "",
  capacity: "",
})

function create(){
  instance.post('/library/reading-room/', form.value, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 201){
          index.push('/readingrooms')
        }
      }
  ).catch(error => console.log(error))
}

</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Добавить комнату</h2>
      <v-text-field label="Название" v-model="form.name"></v-text-field>
      <v-text-field label="Вместимость" v-model="form.capacity"></v-text-field>
      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
