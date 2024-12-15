<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const form = ref({
  book : "",
  cipher : "",
  publishing_year: "",

})

function create(){
  instance.post('/library/book-copy/', form.value, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 201){
          router.push('/book-copies')
        }
      }
  ).catch(error => console.log(error))
}

</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Добавить экземпляр книги</h2>
      <v-text-field label="Книга" v-model="form.book"></v-text-field>
      <v-text-field label="Шифр" v-model="form.cipher"></v-text-field>
      <v-text-field label="Год-издания" v-model="form.publishing_year"></v-text-field>
      <div v-if="error" class="text-red">
        Возникла ошибка
      </div>
      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
