<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import axiosClient from '@/services/axiosClient'
import {tokenStore} from "@/stores/tokenStore.js";

const router = useRouter()
const store = tokenStore()

const usernameRegex = /^[A-Za-z0-9+_.-]+$/
const nameRegex = /^[a-zA-Zа-яА-ЯёЁ]+([ -][a-zA-Zа-яА-ЯёЁ]+)?$/
const emailRegex = /^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$/

const form = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  patronymic: '',
  password: '',
  role: 'user',
})

const errorMessage = ref('')
const isFormValid = ref(false)
const formRef = ref(null)

async function submitForm() {
  if (formRef.value && formRef.value.validate()) {
    errorMessage.value = ''
    try {
      await axiosClient.post('/auth/users/', {
        ...form.value
      })

      const response = await axiosClient.post('/auth/token/login/', {
        username: form.value.username,
        password: form.value.password,
      })

      store.setToken(response.data.auth_token)
      router.push('/')
    } catch (error) {
      errorMessage.value = 'Произошла ошибка при регистрации. Пожалуйста, проверьте введённые данные.'
      console.error(error)
    }
  } else {
    errorMessage.value = 'Пожалуйста, заполните форму корректно.'
  }
}
</script>

<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card class="pa-6 mx-auto" max-width="600" style="width: 100%; background: white;">
      <v-card-title class="d-flex justify-center">Регистрация</v-card-title>
      <v-card-text>
        <v-form ref="formRef" v-model="isFormValid">
          <v-text-field
            label="Имя пользователя" v-model="form.username" outlined dense
            :rules="[v => !!v || 'Имя пользователя обязательно', v => usernameRegex.test(v) || 'Неверный формат имени пользователя']"
          ></v-text-field>
          <v-text-field
            label="Email" v-model="form.email" outlined dense
            :rules="[v => !!v || 'Email обязателен', v => emailRegex.test(v) || 'Неверный формат email']"
          ></v-text-field>
          <v-text-field
            label="Имя" v-model="form.first_name" outlined dense
            :rules="[v => !!v || 'Имя обязательно', v => nameRegex.test(v) || 'Неверный формат имени']"
          ></v-text-field>
          <v-text-field
            label="Фамилия" v-model="form.last_name" outlined dense
            :rules="[v => !!v || 'Фамилия обязательна', v => nameRegex.test(v) || 'Неверный формат фамилии']"
          ></v-text-field>
          <v-text-field
            label="Отчество" v-model="form.patronymic" outlined dense
            :rules="[v => !!v || 'Отчество обязательно', v => nameRegex.test(v) || 'Неверный формат отчества']"
          ></v-text-field>
          <v-text-field
            label="Пароль" type="password" v-model="form.password" outlined dense
            :rules="[v => !!v || 'Пароль обязателен']"
          ></v-text-field>
        </v-form>
        <div class="text-danger" v-if="errorMessage">{{ errorMessage }}</div>
      </v-card-text>
      <v-card-actions class="d-flex justify-center">
        <v-btn color="primary" :disabled="!isFormValid" @click="submitForm">Зарегистрироваться</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<style scoped>
.text-danger {
  color: red;
}
</style>
