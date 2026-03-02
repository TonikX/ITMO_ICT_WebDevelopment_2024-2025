<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card class="mb-6">
          <v-card-title class="text-h5 primary--text">
            Гости гостиницы
            <v-btn color="primary" to="/guests/create">
              + Новый гость
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-text-field
              v-model="searchCity"
              label="Фильтр по городу"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              class="mb-6"
              clearable
              @input="fetchGuests"
            ></v-text-field>

            <v-alert v-if="loading" type="info" prominent>
              Загрузка гостей...
            </v-alert>

            <v-alert v-else-if="error" type="error" prominent>
              {{ error }}
            </v-alert>

            <v-data-table
              v-else
              :headers="headers"
              :items="guests"
              :items-per-page="10"
              class="elevation-1"
              no-data-text="Гости не найдены"
            >
              <template v-slot:item.actions="{ item }">
                <v-btn small color="primary" @click="viewDetails(item)">
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
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const guests = ref([])
const loading = ref(true)
const error = ref(null)
const searchCity = ref('')
const router = useRouter()
const auth = useAuthStore()

const headers = [
  { text: 'Фамилия', value: 'last_name' },
  { text: 'Имя', value: 'first_name' },
  { text: 'Отчество', value: 'patronymic' },
  { text: 'Паспорт', value: 'passport' },
  { text: 'Город', value: 'city' },
  { text: 'Действия', value: 'actions', sortable: false }
]

async function fetchGuests() {
  loading.value = true
  error.value = null

  try {
    let url = 'http://127.0.0.1:8000/api/guests/'
    if (searchCity.value) {
      url += `?city=${encodeURIComponent(searchCity.value)}`
    }

    const response = await fetch(url, {
      headers: {
        Authorization: `Token ${auth.token}`
      }
    })

    if (!response.ok) {
      throw new Error(`Ошибка загрузки: ${response.status}`)
    }

    const data = await response.json()
    guests.value = data.results || data
  } catch (e) {
    error.value = e.message || 'Не удалось загрузить гостей'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (!auth.isAuthenticated) {
    router.push('/login')
    return
  }
  fetchGuests()
})

// Автоматический поиск при изменении города
watch(searchCity, () => {
  fetchGuests()
})

function viewDetails(guest) {
  alert(`Подробности гостя: ${guest.last_name} ${guest.first_name} (${guest.passport})`)
  // Позже можно сделать /guests/:id
}
</script>

<style scoped>
.v-data-table {
  border-radius: 8px;
  overflow: hidden;
}
</style>
