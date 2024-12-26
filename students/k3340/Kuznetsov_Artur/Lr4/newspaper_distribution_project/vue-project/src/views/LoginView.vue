<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import axiosClient from '@/services/axiosClient'
import {tokenStore} from '@/stores/tokenStore'

const router = useRouter()
const store = tokenStore()

const form = ref({
  username: '',
  password: ''
})

const errorMessage = ref('')

async function loginUser() {
  errorMessage.value = ''
  try {
    const response = await axiosClient.post('/auth/token/login/', {
      username: form.value.username,
      password: form.value.password
    })
    store.setToken(response.data.auth_token)
    router.push('/')
  } catch (error) {
    errorMessage.value = 'Неверные имя пользователя или пароль.'
    console.error(error)
  }
}
</script>

<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card class="pa-6 mx-auto" max-width="600" style="width: 100%; background: white;">
      <v-card-title class="d-flex justify-center">Авторизация</v-card-title>
      <v-card-text>
        <v-text-field
          label="Имя пользователя" v-model="form.username" outlined dense
        ></v-text-field>
        <v-text-field
          label="Пароль" v-model="form.password" type="password" outlined dense
        ></v-text-field>
        <div class="text-danger" v-if="errorMessage">{{ errorMessage }}</div>
      </v-card-text>
      <v-card-actions class="d-flex justify-center">
        <v-btn color="primary" @click="loginUser">Войти</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<style scoped>

</style>
