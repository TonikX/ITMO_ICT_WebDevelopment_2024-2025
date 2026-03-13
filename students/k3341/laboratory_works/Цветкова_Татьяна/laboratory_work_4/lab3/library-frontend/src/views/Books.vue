<template>
  <v-container class="pa-6">
    <h1 class="text-h4 mb-6">
      <v-icon icon="mdi-book-open" class="mr-2" />Книги библиотеки
    </h1>

    <!-- Форма добавления книги -->
    <v-card class="pa-4 mb-6" elevation="2">
      <v-card-title class="text-h6 mb-2">Добавить книгу</v-card-title>
      <v-row dense>
        <v-col cols="12" md="4">
          <v-text-field v-model="form.title" label="Название *" variant="outlined" density="compact" />
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field v-model="form.authors" label="Автор(ы) *" variant="outlined" density="compact" />
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field v-model="form.publisher" label="Издательство" variant="outlined" density="compact" />
        </v-col>
        <v-col cols="12" md="2">
          <v-text-field v-model="form.publication_year" label="Год издания" type="number" variant="outlined" density="compact" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field v-model="form.section" label="Раздел" variant="outlined" density="compact" />
        </v-col>
        <v-col cols="12" md="2">
          <v-text-field v-model="form.cipher" label="Шифр" variant="outlined" density="compact" />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="form.room"
            :items="roomOptions"
            label="Зал (сразу разместить)"
            variant="outlined"
            density="compact"
            clearable
          />
        </v-col>
        <v-col cols="12" md="1">
          <v-text-field
            v-model="form.quantity"
            label="Кол-во"
            type="number"
            variant="outlined"
            density="compact"
            min="1"
            :disabled="!form.room"
          />
        </v-col>
        <v-col cols="12" md="1" class="d-flex align-center">
          <v-btn color="primary" block @click="addBook" :loading="saving">
            <v-icon icon="mdi-plus" />
          </v-btn>
        </v-col>
      </v-row>
    </v-card>

    <v-alert v-if="error" type="error" variant="tonal" class="mb-4" closable @click:close="error=''">{{ error }}</v-alert>
    <v-alert v-if="success" type="success" variant="tonal" class="mb-4" closable @click:close="success=''">{{ success }}</v-alert>

    <!-- Таблица книг -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="books"
        :loading="loading"
        no-data-text="Книги не найдены"
        loading-text="Загрузка..."
        item-value="id"
      >
        <!-- Экземпляры по залам -->
        <template #item.copies="{ item }">
          <span v-if="item.copies && item.copies.length">
            <v-chip
              v-for="copy in item.copies"
              :key="copy.id"
              :color="copy.quantity > 0 ? 'green' : 'red'"
              size="small"
              class="mr-1"
              variant="tonal"
            >
              {{ copy.room_name }}: {{ copy.quantity }} экз.
            </v-chip>
          </span>
          <v-chip v-else color="warning" size="small" variant="tonal">Нет в залах</v-chip>
        </template>

        <!-- Действия -->
        <template #item.actions="{ item }">
          <v-btn
            icon="mdi-plus-box"
            color="primary"
            variant="text"
            size="small"
            @click="openCopyDialog(item)"
            title="Добавить экземпляры в зал"
          />
          <v-btn
            icon="mdi-pencil"
            color="secondary"
            variant="text"
            size="small"
            @click="openEditDialog(item)"
            title="Редактировать книгу"
          />
          <v-btn
            icon="mdi-delete"
            color="error"
            variant="text"
            size="small"
            @click="deleteBook(item.id)"
            title="Удалить книгу"
          />
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог: добавить экземпляры в зал -->
    <v-dialog v-model="copyDialog" max-width="480">
      <v-card>
        <v-card-title class="text-h6 pa-4">
          <v-icon icon="mdi-plus-box" class="mr-2" />Экземпляры: {{ selectedBook?.title }}
        </v-card-title>
        <v-card-text>
          <!-- Текущие экземпляры -->
          <div v-if="selectedBook?.copies?.length" class="mb-4">
            <div class="text-subtitle-2 mb-2">Сейчас в залах:</div>
            <v-list density="compact">
              <v-list-item
                v-for="copy in selectedBook.copies"
                :key="copy.id"
                :subtitle="`${copy.quantity} экз.`"
                :title="copy.room_name"
              >
                <template #append>
                  <div class="d-flex align-center gap-2">
                    <v-btn icon="mdi-minus" size="x-small" variant="text" @click="changeCopyQty(copy, -1)" :disabled="copy.quantity <= 0" />
                    <span class="text-body-2 font-weight-bold" style="min-width:20px;text-align:center">{{ copy.quantity }}</span>
                    <v-btn icon="mdi-plus" size="x-small" variant="text" @click="changeCopyQty(copy, 1)" />
                    <v-btn icon="mdi-delete" size="x-small" color="error" variant="text" @click="deleteCopy(copy.id)" />
                  </div>
                </template>
              </v-list-item>
            </v-list>
          </div>

          <v-divider class="mb-4" />
          <div class="text-subtitle-2 mb-2">Добавить в зал:</div>
          <v-row dense>
            <v-col cols="7">
              <v-select
                v-model="copyForm.room"
                :items="availableRooms"
                label="Зал"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="copyForm.quantity"
                label="Кол-во"
                type="number"
                variant="outlined"
                density="compact"
                min="1"
              />
            </v-col>
            <v-col cols="2" class="d-flex align-center">
              <v-btn color="primary" block size="small" @click="addCopy" :loading="copySaving">
                <v-icon icon="mdi-plus" />
              </v-btn>
            </v-col>
          </v-row>
          <v-alert v-if="copyError" type="error" variant="tonal" density="compact" class="mt-2">{{ copyError }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="copyDialog = false">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог: редактировать книгу -->
    <v-dialog v-model="editDialog" max-width="600">
      <v-card v-if="editForm">
        <v-card-title class="text-h6 pa-4">
          <v-icon icon="mdi-pencil" class="mr-2" />Редактировать книгу
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="editForm.title" label="Название" variant="outlined" density="compact" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="editForm.authors" label="Автор(ы)" variant="outlined" density="compact" />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="editForm.publisher" label="Издательство" variant="outlined" density="compact" />
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field v-model="editForm.publication_year" label="Год" type="number" variant="outlined" density="compact" />
            </v-col>
            <v-col cols="12" md="3">
              <v-text-field v-model="editForm.cipher" label="Шифр" variant="outlined" density="compact" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="editForm.section" label="Раздел" variant="outlined" density="compact" />
            </v-col>
          </v-row>
          <v-alert v-if="editError" type="error" variant="tonal" density="compact" class="mt-2">{{ editError }}</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="editDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveEdit" :loading="editSaving">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

const API_BOOKS = 'http://127.0.0.1:8000/api/books/'
const API_COPIES = 'http://127.0.0.1:8000/api/bookcopies/'
const API_ROOMS = 'http://127.0.0.1:8000/api/rooms/'

export default {
  data() {
    return {
      books: [],
      rooms: [],
      copies: [],
      loading: false,
      saving: false,
      error: '',
      success: '',
      form: {
        title: '', authors: '', publisher: '',
        publication_year: new Date().getFullYear(),
        section: '', cipher: '', room: null, quantity: 1,
      },
      headers: [
        { title: 'Название', key: 'title', width: '22%' },
        { title: 'Автор(ы)', key: 'authors', width: '18%' },
        { title: 'Издательство', key: 'publisher', width: '14%' },
        { title: 'Год', key: 'publication_year', width: '6%' },
        { title: 'Раздел', key: 'section', width: '12%' },
        { title: 'Шифр', key: 'cipher', width: '8%' },
        { title: 'Экземпляры по залам', key: 'copies', sortable: false, width: '15%' },
        { title: '', key: 'actions', sortable: false, width: '5%' },
      ],
      // copy dialog
      copyDialog: false,
      selectedBook: null,
      copyForm: { room: null, quantity: 1 },
      copyError: '',
      copySaving: false,
      // edit dialog
      editDialog: false,
      editForm: null,
      editError: '',
      editSaving: false,
    }
  },
  computed: {
    authHeaders() {
      return { Authorization: `Token ${localStorage.getItem('token')}` }
    },
    roomOptions() {
      return this.rooms.map(r => ({ title: `${r.name} (зал №${r.number})`, value: r.id }))
    },
    availableRooms() {
      if (!this.selectedBook) return this.roomOptions
      const usedRoomIds = (this.selectedBook.copies || []).map(c => c.reading_room)
      return this.roomOptions.filter(r => !usedRoomIds.includes(r.value))
    },
  },
  async mounted() {
    await Promise.all([this.loadBooks(), this.loadRooms(), this.loadCopies()])
  },
  methods: {
    async loadRooms() {
      const res = await axios.get(API_ROOMS, { headers: this.authHeaders })
      this.rooms = res.data
    },
    async loadCopies() {
      const res = await axios.get(API_COPIES, { headers: this.authHeaders })
      this.copies = res.data
    },
    async loadBooks() {
      this.loading = true
      try {
        const res = await axios.get(API_BOOKS, { headers: this.authHeaders })
        const copiesRes = await axios.get(API_COPIES, { headers: this.authHeaders })
        this.copies = copiesRes.data
        this.books = res.data.map(book => ({
          ...book,
          copies: copiesRes.data.filter(c => c.book === book.id),
        }))
      } catch {
        this.error = 'Не удалось загрузить книги'
      } finally {
        this.loading = false
      }
    },
    async addBook() {
      if (!this.form.title || !this.form.authors) {
        this.error = 'Заполните название и автора'
        return
      }
      this.saving = true
      this.error = ''
      try {
        const bookData = {
          title: this.form.title,
          authors: this.form.authors,
          publisher: this.form.publisher || '',
          publication_year: this.form.publication_year || new Date().getFullYear(),
          section: this.form.section || '',
          cipher: this.form.cipher || '',
        }
        const res = await axios.post(API_BOOKS, bookData, { headers: this.authHeaders })
        // Если указан зал — сразу создаём BookCopy
        if (this.form.room) {
          await axios.post(API_COPIES, {
            book: res.data.id,
            reading_room: this.form.room,
            quantity: parseInt(this.form.quantity) || 1,
          }, { headers: this.authHeaders })
        }
        this.success = `Книга «${res.data.title}» добавлена!`
        this.form = {
          title: '', authors: '', publisher: '',
          publication_year: new Date().getFullYear(),
          section: '', cipher: '', room: null, quantity: 1,
        }
        await this.loadBooks()
      } catch (err) {
        this.error = err.response?.data ? JSON.stringify(err.response.data) : 'Ошибка добавления'
      } finally {
        this.saving = false
      }
    },
    async deleteBook(id) {
      if (!confirm('Удалить книгу?')) return
      try {
        await axios.delete(`${API_BOOKS}${id}/`, { headers: this.authHeaders })
        await this.loadBooks()
      } catch {
        this.error = 'Не удалось удалить книгу (возможно, есть активные выдачи)'
      }
    },
    // --- Copy dialog ---
    openCopyDialog(book) {
      this.selectedBook = { ...book }
      this.copyForm = { room: null, quantity: 1 }
      this.copyError = ''
      this.copyDialog = true
    },
    async addCopy() {
      if (!this.copyForm.room) {
        this.copyError = 'Выберите зал'
        return
      }
      this.copySaving = true
      this.copyError = ''
      try {
        await axios.post(API_COPIES, {
          book: this.selectedBook.id,
          reading_room: this.copyForm.room,
          quantity: parseInt(this.copyForm.quantity) || 1,
        }, { headers: this.authHeaders })
        await this.loadBooks()
        // Refresh selected book copies
        const updated = this.books.find(b => b.id === this.selectedBook.id)
        if (updated) this.selectedBook = { ...updated }
        this.copyForm = { room: null, quantity: 1 }
      } catch (err) {
        this.copyError = err.response?.data ? JSON.stringify(err.response.data) : 'Ошибка'
      } finally {
        this.copySaving = false
      }
    },
    async changeCopyQty(copy, delta) {
      const newQty = copy.quantity + delta
      if (newQty < 0) return
      try {
        await axios.patch(`${API_COPIES}${copy.id}/`, { quantity: newQty }, { headers: this.authHeaders })
        await this.loadBooks()
        const updated = this.books.find(b => b.id === this.selectedBook.id)
        if (updated) this.selectedBook = { ...updated }
      } catch {
        this.copyError = 'Ошибка обновления'
      }
    },
    async deleteCopy(copyId) {
      try {
        await axios.delete(`${API_COPIES}${copyId}/`, { headers: this.authHeaders })
        await this.loadBooks()
        const updated = this.books.find(b => b.id === this.selectedBook.id)
        if (updated) this.selectedBook = { ...updated }
      } catch {
        this.copyError = 'Ошибка удаления'
      }
    },
    // --- Edit dialog ---
    openEditDialog(book) {
      this.editForm = { ...book }
      this.editError = ''
      this.editDialog = true
    },
    async saveEdit() {
      this.editSaving = true
      this.editError = ''
      try {
        await axios.put(`${API_BOOKS}${this.editForm.id}/`, {
          title: this.editForm.title,
          authors: this.editForm.authors,
          publisher: this.editForm.publisher,
          publication_year: this.editForm.publication_year,
          section: this.editForm.section,
          cipher: this.editForm.cipher,
        }, { headers: this.authHeaders })
        this.editDialog = false
        this.success = 'Книга обновлена!'
        await this.loadBooks()
      } catch (err) {
        this.editError = err.response?.data ? JSON.stringify(err.response.data) : 'Ошибка'
      } finally {
        this.editSaving = false
      }
    },
  },
}
</script>
