<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card class="v-card pa-6 mx-auto">
      <v-card-title class="text-center text-h5 font-weight-bold">Регистрация</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleRegister">
          <v-text-field v-model="user.username" label="Имя пользователя" required></v-text-field>
          <v-text-field v-model="user.email" label="Email" required></v-text-field>
          <v-text-field v-model="user.password" label="Пароль" type="password"
                        required></v-text-field>
          <v-text-field v-model="user.re_password" label="Подтвердите пароль" type="password"
                        required></v-text-field>
          <v-btn type="submit" color="primary" class="mt-4" :loading="loading">Зарегистрироваться
          </v-btn>
        </v-form>

        <v-alert v-if="errors.length" type="error" class="mt-2">
          <ul>
            <li v-for="(err, index) in errors" :key="index">{{ err }}</li>
          </ul>
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {api} from '@/utils/api'
import {useAuthStore} from '@/stores/auth'

export default {
  setup() {
    const user = ref({
      username: '',
      email: '',
      password: '',
      re_password: ''
    })
    const errors = ref([])
    const loading = ref(false)
    const router = useRouter()
    const authStore = useAuthStore()

    const handleRegister = async () => {
      errors.value = []
      loading.value = true

      try {
        await api.post('/auth/users/', user.value)

        await authStore.login({
          username: user.value.username,
          password: user.value.password
        })
        router.push('/')
      } catch (error) {
        loading.value = false

        if (!error.response) {
          errors.value.push('Некорректные введенные данные')
        }
      } finally {
        loading.value = false
      }
    }
    return {user, errors, loading, handleRegister}
  }
}
</script>

<style scoped>
.fill-height {
  height: 100vh;
}

.v-card {
  max-width: 500px;
  width: 100%;
}

.v-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80vh;
}
</style>
