<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="text-h4 mb-6">Номера гостиницы</h1>

        <v-alert v-if="loading" type="info" class="mb-6">
          Загрузка...
        </v-alert>

        <v-alert v-else-if="error" type="error" class="mb-6">
          {{ error }}
        </v-alert>

        <v-card v-else>
          <v-data-table
            :headers="headers"
            :items="rooms"
            :items-per-page="10"
            class="elevation-1"
          >
            <template v-slot:item.room_type="{ item }">
              {{ item.room_type.name }} ({{ item.room_type.capacity }} мест, {{ item.room_type.price_per_day }} ₽/сутки)
            </template>

            <template v-slot:item.actions="{ item }">
              <v-btn small color="primary" @click="viewDetails(item)">
                Подробнее
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const rooms = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()
const auth = useAuthStore()

const headers = [
  { text: 'Номер', value: 'number' },
  { text: 'Этаж', value: 'floor' },
  { text: 'Тип номера', value: 'room_type' },
  { text: 'Телефон', value: 'phone' },
  { text: 'Действия', value: 'actions', sortable: false }
]

onMounted(async () => {
  if (!auth.isAuthenticated) {
    router.push('/login')
    return
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/rooms/', {
      headers: {
        Authorization: `Token ${auth.token}`
      }
    })

    if (!response.ok) {
      throw new Error('Не удалось загрузить номера')
    }

    const data = await response.json()
    rooms.value = data.results || data  // поддержка как с пагинацией, так и без
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

function viewDetails(room) {
  alert(`Подробности номера ${room.number} — пока просто заглушка`)
  // Позже можно сделать переход на /rooms/:id
}
</script>
