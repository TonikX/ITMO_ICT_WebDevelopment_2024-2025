<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card class="mb-6">
          <v-card-title class="text-h5 primary--text">
            Бронирования и заселения
            <v-spacer></v-spacer>
            <v-btn color="primary" to="/bookings/create">
              + Новая бронь
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-alert v-if="loading" type="info" prominent>
              Загрузка бронирований...
            </v-alert>

            <v-alert v-else-if="error" type="error" prominent>
              {{ error }}
            </v-alert>

            <v-data-table
              v-else
              :headers="headers"
              :items="bookings"
              :items-per-page="10"
              class="elevation-1"
              no-data-text="Бронирования не найдены"
              loading-text="Загрузка данных..."
            >
              <template v-slot:item.guest="{ item }">
                {{ item.guest.last_name }} {{ item.guest.first_name }}
                <br>
                <small>{{ item.guest.passport }}</small>
              </template>

              <template v-slot:item.room="{ item }">
                №{{ item.room.number }} (этаж {{ item.room.floor }})
              </template>

              <template v-slot:item.period="{ item }">
                {{ item.check_in }} — {{ item.check_out || 'по настоящее время' }}
              </template>

              <template v-slot:item.status="{ item }">
                <v-chip
                  :color="item.is_active ? 'success' : 'grey'"
                  small
                >
                  {{ item.is_active ? 'Активно' : 'Завершено' }}
                </v-chip>
              </template>

              <template v-slot:item.actions="{ item }">
                <v-btn
                  v-if="item.is_active"
                  small
                  color="warning"
                  @click="checkout(item)"
                >
                  Выселить
                </v-btn>
                <v-btn
                  small
                  color="primary"
                  @click="viewDetails(item)"
                  class="ml-2"
                >
                  Подробнее
                </v-btn>
              </template>
            </v-data-table>
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

const bookings = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()
const auth = useAuthStore()

const headers = [
  { text: 'Гость', value: 'guest' },
  { text: 'Номер', value: 'room' },
  { text: 'Период', value: 'period' },
  { text: 'Статус', value: 'status' },
  { text: 'Действия', value: 'actions', sortable: false }
]

onMounted(async () => {
  if (!auth.isAuthenticated) {
    router.push('/login')
    return
  }

  await fetchBookings()
})

async function fetchBookings() {
  loading.value = true
  error.value = null

  try {
    const response = await fetch('http://127.0.0.1:8000/api/bookings/', {
      headers: {
        Authorization: `Token ${auth.token}`
      }
    })

    if (!response.ok) {
      throw new Error(`Ошибка загрузки: ${response.status} - ${response.statusText}`)
    }

    const data = await response.json()
    bookings.value = data.results || data
  } catch (e) {
    error.value = e.message || 'Не удалось загрузить бронирования'
    console.error('Ошибка загрузки бронирований:', e)
  } finally {
    loading.value = false
  }
}

function viewDetails(booking) {
  alert(`Подробности бронирования ID: ${booking.id}\nГость: ${booking.guest.last_name} ${booking.guest.first_name}\nНомер: ${booking.room.number}`)
}

async function checkout(booking) {
  if (!confirm(`Выселить гостя из номера ${booking.room.number}?`)) return

  try {
    const today = new Date().toISOString().split('T')[0]
    const response = await fetch(`http://127.0.0.1:8000/api/bookings/${booking.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${auth.token}`
      },
      body: JSON.stringify({ check_out: today })
    })

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.detail || 'Не удалось выселить')
    }

    await fetchBookings()
    alert('Гость успешно выселен')
  } catch (e) {
    alert('Ошибка выселения: ' + e.message)
  }
}
</script>

<style scoped>
.v-data-table {
  border-radius: 8px;
  overflow: hidden;
}
</style>
