<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const form = ref({
  full_name : "",
})

function create(){
  instance.post('/library/author/', form.value, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 201){
          router.push('/authors')
        }
      }
  ).catch(error => console.log(error))
}

</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Добавить автора</h2>
      <v-text-field label="Имя" v-model="form.full_name"></v-text-field>
      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
