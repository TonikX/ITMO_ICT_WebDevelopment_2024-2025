<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const form = ref({
  name: "",
  publisher: "",
  category: "",
  authors: "",
})

function getPaper(){
  instance.get(`/library/book/${router.currentRoute.value.params.id}/`, {
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
  instance.patch(`/library/book/${router.currentRoute.value.params.id}/`, rest, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          router.push('/books')
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
      <h2>Книга</h2>
      <v-text-field label="Название" v-model="form.name"></v-text-field>
      <v-text-field label="Издатель" v-model="form.publisher"></v-text-field>
      <v-text-field label="Категории" v-model="form.category"></v-text-field>
      <v-text-field label="Авторы" v-model="form.authors"></v-text-field>
      <v-btn @click="savePaper">Сохранить</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
