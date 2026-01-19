<template>
  <v-container>
    <v-card>
      <v-card-title>Мой профиль</v-card-title>
      <v-card-text>
        <v-alert v-if="message.show" :type="message.type" class="mb-4">
          {{ message.text }}
        </v-alert>

        <div v-if="auth.user" class="mb-6">
          <v-list>
            <v-list-item>
              <v-list-item-title class="text-subtitle-1">Логин</v-list-item-title>
              <v-list-item-subtitle>{{ auth.user.username }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="text-subtitle-1">Имя</v-list-item-title>
              <v-list-item-subtitle>{{ auth.user.first_name }} {{ auth.user.last_name }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="text-subtitle-1">Email</v-list-item-title>
              <v-list-item-subtitle>{{ auth.user.email }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title class="text-subtitle-1">Статус</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip :color="auth.user.is_staff ? 'primary' : 'secondary'" size="small">
                  {{ auth.user.is_staff ? 'Администратор' : 'Пользователь' }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </div>

        <v-form @submit.prevent="updateProfile">
          <v-text-field
            v-model="form.first_name"
            label="Имя"
            required
          />
          <v-text-field
            v-model="form.last_name"
            label="Фамилия"
            required
          />
          <v-text-field
            v-model="form.email"
            label="Email"
            type="email"
            required
          />
          <v-text-field
            v-model="form.password"
            label="Новый пароль"
            type="password"
            hint="Оставьте пустым, если не хотите менять"
            persistent-hint
          />
          <v-btn 
            type="submit" 
            color="primary" 
            :loading="loading"
            :disabled="!form.first_name || !form.last_name || !form.email"
          >
            Сохранить изменения
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { authAPI } from '@/api/endpoints'

const auth = useAuth()
const loading = ref(false)
const message = reactive({
  show: false,
  text: '',
  type: 'info'
})

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: ''
})

const showMessage = (text, type = 'info') => {
  message.text = text
  message.type = type
  message.show = true
  setTimeout(() => {
    message.show = false
  }, 3000)
}

onMounted(async () => {
  // Загружаем данные текущего пользователя
  await auth.fetchCurrentUser()
  
  if (auth.user) {
    form.value = {
      first_name: auth.user.first_name || '',
      last_name: auth.user.last_name || '',
      email: auth.user.email || '',
      password: ''
    }
  }
})

const updateProfile = async () => {
  loading.value = true
  try {
    // Убираем пустые поля
    const dataToSend = { ...form.value }
    if (!dataToSend.password) {
      delete dataToSend.password
    }

    const response = await authAPI.updateUser(auth.user.id, dataToSend)
    
    // Обновляем данные пользователя
    auth.user = response.data
    
    showMessage('Профиль успешно обновлен', 'success')
  } catch (error) {
    console.error('Ошибка обновления профиля:', error)
    showMessage(error.response?.data?.detail || 'Ошибка обновления профиля', 'error')
  } finally {
    loading.value = false
  }
}
</script>