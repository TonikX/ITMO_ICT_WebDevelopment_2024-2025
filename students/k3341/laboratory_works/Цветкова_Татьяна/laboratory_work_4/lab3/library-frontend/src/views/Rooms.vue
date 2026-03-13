<template>
  <v-container class="pa-6">
    <h1 class="text-h4 mb-6">
      <v-icon icon="mdi-door" class="mr-2" />Читальные залы
    </h1>

    <!-- Форма добавления -->
    <v-card class="pa-4 mb-6" elevation="2">
      <v-card-title class="text-h6 mb-2">Добавить зал</v-card-title>
      <v-row dense>
        <v-col cols="12" md="2">
          <v-text-field v-model="form.number" label="Номер зала" type="number" variant="outlined" density="compact" />
        </v-col>
        <v-col cols="12" md="5">
          <v-text-field v-model="form.name" label="Название" variant="outlined" density="compact" />
        </v-col>
        <v-col cols="12" md="2">
          <v-text-field v-model="form.capacity" label="Вместимость (чел.)" type="number" variant="outlined" density="compact" />
        </v-col>
        <v-col cols="12" md="3" class="d-flex align-center">
          <v-btn color="primary" block @click="addRoom" :loading="saving">
            <v-icon icon="mdi-plus" class="mr-1" />Добавить зал
          </v-btn>
        </v-col>
      </v-row>
    </v-card>

    <v-alert v-if="error" type="error" variant="tonal" class="mb-4" closable @click:close="error=''">{{ error }}</v-alert>
    <v-alert v-if="!loading && rooms.length === 0" type="info" variant="tonal" class="mt-4">
      Читальные залы не добавлены. Добавьте первый зал выше.
    </v-alert>

    <!-- Карточки залов -->
    <v-row>
      <v-col cols="12" md="6" v-for="room in rooms" :key="room.id">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="bg-primary text-white pa-3 d-flex align-center justify-space-between">
            <span>
              <v-icon icon="mdi-door" class="mr-2" />Зал №{{ room.number }} — {{ room.name }}
            </span>
            <v-btn
              icon="mdi-delete"
              color="white"
              variant="text"
              size="small"
              @click="deleteRoom(room.id)"
            />
          </v-card-title>
          <v-card-text class="pa-4">
            <div class="d-flex gap-4 mb-4">
              <v-chip color="blue" variant="tonal" size="small">
                <v-icon icon="mdi-account-group" class="mr-1" size="16" />
                Вместимость: {{ room.capacity }} чел.
              </v-chip>
              <v-chip color="green" variant="tonal" size="small">
                <v-icon icon="mdi-book" class="mr-1" size="16" />
                Книг: {{ roomBookCount(room.id) }}
              </v-chip>
              <v-chip color="orange" variant="tonal" size="small">
                <v-icon icon="mdi-account" class="mr-1" size="16" />
                Читателей: {{ roomReaderCount(room.id) }}
              </v-chip>
            </div>

            <!-- Книги в зале -->
            <div class="text-subtitle-2 mb-1">
              <v-icon icon="mdi-book-open" size="16" class="mr-1" />Книги в зале:
            </div>
            <div v-if="getCopiesForRoom(room.id).length" class="mb-3">
              <v-list density="compact" class="pa-0">
                <v-list-item
                  v-for="copy in getCopiesForRoom(room.id)"
                  :key="copy.id"
                  :title="copy.book_title"
                  density="compact"
                  class="pa-0"
                >
                  <template #append>
                    <v-chip
                      :color="copy.quantity > 0 ? 'green' : 'red'"
                      size="x-small"
                      variant="tonal"
                    >
                      {{ copy.quantity }} экз.
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </div>
            <div v-else class="text-caption text-medium-emphasis mb-3">Книг нет</div>

            <!-- Читатели зала -->
            <div class="text-subtitle-2 mb-1">
              <v-icon icon="mdi-account-group" size="16" class="mr-1" />Читатели зала:
            </div>
            <div v-if="getReadersForRoom(room.id).length">
              <v-chip
                v-for="reader in getReadersForRoom(room.id)"
                :key="reader.id"
                size="x-small"
                class="mr-1 mb-1"
                color="primary"
                variant="tonal"
              >
                {{ reader.full_name }}
              </v-chip>
            </div>
            <div v-else class="text-caption text-medium-emphasis">Нет закреплённых читателей</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

const API_ROOMS = 'http://127.0.0.1:8000/api/rooms/'
const API_COPIES = 'http://127.0.0.1:8000/api/bookcopies/'
const API_READERS = 'http://127.0.0.1:8000/api/readers/'

export default {
  data() {
    return {
      rooms: [],
      copies: [],
      readers: [],
      loading: false,
      saving: false,
      error: '',
      form: { number: '', name: '', capacity: '' },
    }
  },
  computed: {
    authHeaders() {
      return { Authorization: `Token ${localStorage.getItem('token')}` }
    },
  },
  async mounted() {
    await Promise.all([this.loadRooms(), this.loadCopies(), this.loadReaders()])
  },
  methods: {
    getCopiesForRoom(roomId) {
      return this.copies.filter(c => c.reading_room === roomId)
    },
    getReadersForRoom(roomId) {
      return this.readers.filter(r => r.reading_room === roomId)
    },
    roomBookCount(roomId) {
      return this.getCopiesForRoom(roomId).reduce((sum, c) => sum + c.quantity, 0)
    },
    roomReaderCount(roomId) {
      return this.getReadersForRoom(roomId).length
    },
    async loadRooms() {
      this.loading = true
      try {
        const res = await axios.get(API_ROOMS, { headers: this.authHeaders })
        this.rooms = res.data
      } catch {
        this.error = 'Не удалось загрузить залы'
      } finally {
        this.loading = false
      }
    },
    async loadCopies() {
      const res = await axios.get(API_COPIES, { headers: this.authHeaders })
      this.copies = res.data
    },
    async loadReaders() {
      const res = await axios.get(API_READERS, { headers: this.authHeaders })
      this.readers = res.data
    },
    async addRoom() {
      if (!this.form.number || !this.form.name || !this.form.capacity) {
        this.error = 'Заполните номер, название и вместимость зала'
        return
      }
      this.saving = true
      this.error = ''
      try {
        await axios.post(API_ROOMS, this.form, { headers: this.authHeaders })
        this.form = { number: '', name: '', capacity: '' }
        await this.loadRooms()
      } catch (err) {
        this.error = err.response?.data ? JSON.stringify(err.response.data) : 'Ошибка добавления'
      } finally {
        this.saving = false
      }
    },
    async deleteRoom(id) {
      if (!confirm('Удалить зал? Все книги и читатели зала будут откреплены.')) return
      try {
        await axios.delete(`${API_ROOMS}${id}/`, { headers: this.authHeaders })
        await Promise.all([this.loadRooms(), this.loadCopies(), this.loadReaders()])
      } catch {
        this.error = 'Не удалось удалить зал'
      }
    },
  },
}
</script>
