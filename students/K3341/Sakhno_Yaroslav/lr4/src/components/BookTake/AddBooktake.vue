<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const form = ref({
  book_copy: "",
  reader: "",
  take_date: "",
  return_date : "",

})
function create(){
  instance.post('/library/book-taken/', form.value, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 201){
          router.push('/book-takes')
        }
      }
  ).catch(error => console.log(error))
}

</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Взять книгу</h2>
      <v-text-field label="Экземпляр книги" v-model="form.book_copy"></v-text-field>
      <v-text-field label="Читатель" v-model="form.reader"></v-text-field>
      <v-text-field label="Дата получения" v-model="form.take_date"></v-text-field>
      <v-text-field label="Дата возврата" v-model="form.return_date"></v-text-field>
      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
