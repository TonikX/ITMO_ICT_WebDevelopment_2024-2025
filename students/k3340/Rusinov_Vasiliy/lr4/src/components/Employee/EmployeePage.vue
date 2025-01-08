<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import {Api} from "@/services/api";

const Token = Api()

const form = ref({
  book : "",
  cipher : "",
  publishing_year: "",

})

function getPaper(){
  instance.get(`/library/book-copy/${index.currentRoute.value.params.id}/`, {
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
  instance.patch(`/library/book-copy/${index.currentRoute.value.params.id}/`, rest, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          index.push('/book-copies')
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
      <h2>Экземпляр книги</h2>
      <v-text-field label="Книга" v-model="form.book"></v-text-field>
      <v-text-field label="Шифр" v-model="form.cipher"></v-text-field>
      <v-text-field label="Год-издания" v-model="form.publishing_year"></v-text-field>
      <v-btn @click="savePaper">Сохранить</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
