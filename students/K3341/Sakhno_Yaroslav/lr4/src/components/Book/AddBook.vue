<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const form = ref({
  name : "",
  publisher : "",
  category : "",
  authors : "",
})

function create(){
  instance.post('/library/book/', form.value, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 201){
          router.push('/books')
        }
      }
  ).catch(error => console.log(error))
}

</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Добавить книгу</h2>
      <v-text-field label="Название" v-model="form.name"></v-text-field>
      <v-text-field label="Издатель" v-model="form.publisher"></v-text-field>
      <v-text-field label="Категории" v-model="form.category"></v-text-field>
      <v-text-field label="Авторы" v-model="form.authors"></v-text-field>
      <div v-if="error" class="text-red">
        Возникла ошибка
      </div>
      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
