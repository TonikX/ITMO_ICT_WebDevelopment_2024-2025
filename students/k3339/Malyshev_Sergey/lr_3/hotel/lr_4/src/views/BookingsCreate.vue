<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card elevation="10" class="pa-6">
          <v-card-title class="text-h5 text-center mb-6">Новая бронь</v-card-title>

          <v-card-text>
            <v-alert v-if="error" type="error" class="mb-6" dismissible>
              {{ error }}
            </v-alert>

            <v-alert v-if="success" type="success" class="mb-6" dismissible>
              Бронь успешно создана! ID: {{ success.id }}
            </v-alert>

            <v-form @submit.prevent="createBooking">
              <v-select
                v-model="form.guest_id"
                :items="guests"
                item-title="full_name"
                item-value="id"
                label="Гость"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                required
                class="mb-4"
              ></v-select>

              <v-select
                v-model="form.room_id"
                :items="rooms"
                item-title="number"
                item-value="id"
                label="Номер"
                prepend-inner-icon="mdi-bed"
                variant="outlined"
                required
                class="mb-4"
              ></v-select>

              <v-text-field
                v-model="form.check_in"
                label="Дата заезда"
                type="date"
                variant="outlined"
                required
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="form.check_out"
                label="Дата выезда (необязательно)"
                type="date"
                variant="outlined"
                class="mb-6"
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
                Создать бронь
              </v-btn>
            </v-form>

            <div class="text-center">
              <v-btn text color="primary" to="/bookings">
                Назад к бронированиям
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const form = ref({
  guest_id: null,
  room_id: null,
  check_in: '',
  check_out: ''
})

const guests = ref([])
const rooms = ref([])
const loading = ref(false)
const error = ref(null)
const success = ref(null)
const router = useRouter()
const auth = useAuthStore()

onMounted(async () => {
  if (!auth.isAuthenticated) {
    router.push('/login')
    return
  }

  await loadGuests()
  await loadRooms()
})

async function loadGuests() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/guests/', {
      headers: {
        Authorization: `Token ${auth.token}`
      }
    })
    if (response.ok) {
      const data = await response.json()
      guests.value = (data.results || data).map(g => ({
        id: g.id,
        full_name: `${g.last_name} ${g.first_name} (${g.passport})`
      }))
    }
  } catch (e) {
    console.error('Ошибка загрузки гостей:', e)
  }
}

async function loadRooms() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/rooms/', {
      headers: {
        Authorization: `Token ${auth.token}`
      }
    })
    if (response.ok) {
      const data = await response.json()
      rooms.value = (data.results || data).map(r => ({
        id: r.id,
        number: r.number
      }))
    }
  } catch (e) {
    console.error('Ошибка загрузки номеров:', e)
  }
}

async function createBooking() {
  error.value = null
  success.value = null
  loading.value = true

  try {
    const response = await fetch('http://127.0.0.1:8000/api/bookings/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${auth.token}`
      },
      body: JSON.stringify(form.value)
    })

    if (!response.ok) {
      const errData = await response.json()
      error.value = Object.values(errData).flat().join(', ') || 'Ошибка создания брони'
      throw new Error(error.value)
    }

    success.value = await response.json()
    form.value = { guest_id: null, room_id: null, check_in: '', check_out: '' }
  } catch (e) {
    console.error(e)
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
