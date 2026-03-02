<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6" lg="5">
        <v-card elevation="10" class="pa-8 rounded-lg">
          <v-card-title class="text-h5 text-center mb-6 primary--text">
            Новый гость
          </v-card-title>

          <v-card-text>
            <!-- Сообщения об успехе / ошибке -->
            <v-alert
              v-if="success"
              type="success"
              prominent
              dismissible
              class="mb-6"
            >
              Гость успешно создан! ID: {{ success.id }}
            </v-alert>

            <v-alert
              v-if="error"
              type="error"
              prominent
              dismissible
              class="mb-6"
            >
              {{ error }}
            </v-alert>

            <!-- Форма -->
            <v-form ref="form" @submit.prevent="createGuest" lazy-validation>
              <v-text-field
                v-model="form.passport"
                label="Паспорт (серия и номер)"
                prepend-inner-icon="mdi-card-account-details-outline"
                variant="outlined"
                :rules="[rules.required, rules.passportFormat]"
                class="mb-4"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.last_name"
                label="Фамилия"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                :rules="[rules.required]"
                class="mb-4"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.first_name"
                label="Имя"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                :rules="[rules.required]"
                class="mb-4"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.patronymic"
                label="Отчество"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="form.city"
                label="Город прибытия"
                prepend-inner-icon="mdi-city"
                variant="outlined"
                :rules="[rules.required]"
                class="mb-6"
                required
              ></v-text-field>

              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                class="mb-4"
                :loading="loading"
                :disabled="loading"
              >
                Создать гостя
              </v-btn>
            </v-form>

            <div class="text-center mt-4">
              <v-btn variant="text" color="primary" to="/guests">
                Назад к списку гостей
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = ref({
  passport: '',
  last_name: '',
  first_name: '',
  patronymic: '',
  city: ''
})

const loading = ref(false)
const error = ref(null)
const success = ref(null)

const rules = {
  required: value => !!value || 'Обязательное поле',
  passportFormat: value => {
    if (!value) return true
    return /^[0-9]{4}\s?[0-9]{6}$/.test(value) || 'Формат: 1234 567890'
  }
}

async function createGuest() {
  error.value = null
  success.value = null
  loading.value = true

  try {
    const response = await fetch('http://127.0.0.1:8000/api/guests/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${auth.token}`
      },
      body: JSON.stringify({
        passport: form.value.passport,
        last_name: form.value.last_name,
        first_name: form.value.first_name,
        patronymic: form.value.patronymic,
        city: form.value.city
      })  // ← отправляем чистый объект без ref и циклических ссылок
    })

    if (!response.ok) {
      const errData = await response.json()
      error.value = Object.entries(errData)
        .map(([field, msgs]) => `${field}: ${msgs.join(', ')}`)
        .join('; ') || 'Ошибка создания гостя'
      throw new Error(error.value)
    }

    success.value = await response.json()
    // Очищаем форму после успеха
    form.value = {
      passport: '',
      last_name: '',
      first_name: '',
      patronymic: '',
      city: ''
    }
  } catch (e) {
    error.value = e.message || 'Неизвестная ошибка'
    console.error('Ошибка создания гостя:', e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}
</style>
