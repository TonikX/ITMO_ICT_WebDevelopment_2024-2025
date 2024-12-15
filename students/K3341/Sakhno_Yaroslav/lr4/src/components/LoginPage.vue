<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const form = ref({
  username: '',
  password: ''
})

function login(){
  instance.post('/auth/token/login', form.value).then(response => {
    if (response.status === 200){
      Token.setToken(response.data.auth_token)
      console.log(Token.token)
      router.push('/categories')
    }
  }
  ).catch(error => console.log(error))
}

</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Вход</h2>
    <v-text-field label="Логин" v-model="form.username"></v-text-field>
    <v-text-field label="Пароль" v-model="form.password"></v-text-field>
    <v-btn @click="login">Войти</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
