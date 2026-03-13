<template>
  <v-container class="pa-6">
    <h1 class="text-h4 mb-6">
      <v-icon icon="mdi-book-arrow-right" class="mr-2" />Выдача книг
    </h1>

    <!-- Форма выдачи книги читателю -->
    <v-card class="pa-4 mb-6" elevation="2">
      <v-card-title>Выдать книгу</v-card-title>
      <v-row class="mt-2">

        <!-- Выбор книги из выпадающего списка.
             :items="bookOptions" — список книг загружается с API -->
        <v-col cols="12" md="5">
          <v-select
            v-model="form.book"
            :items="bookOptions"
            label="Книга"
            variant="outlined"
            density="compact"
          />
        </v-col>

        <!-- Выбор читателя -->
        <v-col cols="12" md="5">
          <v-select
            v-model="form.reader"
            :items="readerOptions"
            label="Читатель"
            variant="outlined"
            density="compact"
          />
        </v-col>

        <!-- Кнопка выдачи -->
        <v-col cols="12" md="2" class="d-flex align-center">
          <v-btn color="primary" block @click="borrowBook">
            <v-icon icon="mdi-book-arrow-right" class="mr-1" />Выдать
          </v-btn>
        </v-col>

      </v-row>
    </v-card>

    <!-- Ошибка (например: "Книга отсутствует в читальном зале") -->
    <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

    <!-- Таблица выданных книг -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="borrowings"
        :loading="loading"
        no-data-text="Нет выданных книг"
        loading-text="Загрузка..."
      >

        <!-- Слот для колонки return_date:
             если дата возврата есть — зелёный чип с датой,
             если пустая — оранжевый чип "На руках" -->
        <template #item.return_date="{ item }">
          <v-chip v-if="item.return_date" color="green" size="small">{{ item.return_date }}</v-chip>
          <v-chip v-else color="orange" size="small">На руках</v-chip>
        </template>

        <!-- Слот для колонки actions:
             кнопка "Вернуть" — появляется только если книга ещё не возвращена -->
        <template #item.actions="{ item }">
          <v-btn
            v-if="!item.return_date"
            color="success"
            variant="text"
            size="small"
            @click="returnBook(item)"
          >
            <v-icon icon="mdi-book-arrow-left" />Вернуть
          </v-btn>
        </template>

      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

const API = 'http://127.0.0.1:8000/api/borrowings/'

export default {
  data() {
    return {
      borrowings: [],  // список всех выдач из API
      books: [],       // список книг (для выпадающего списка)
      readers: [],     // список читателей (для выпадающего списка)
      loading: false,
      error: '',

      // Форма выдачи: id книги и id читателя
      form: { book: null, reader: null },

      // Описание столбцов таблицы.
      // book_title и reader_name — дополнительные поля из BorrowingSerializer
      headers: [
        { title: 'Книга',         key: 'book_title' },
        { title: 'Читатель',      key: 'reader_name' },
        { title: 'Дата выдачи',   key: 'borrow_date' },
        { title: 'Дата возврата', key: 'return_date' },
        { title: '',              key: 'actions', sortable: false },
      ],
    }
  },

  computed: {
    authHeaders() {
      return { Authorization: `Token ${localStorage.getItem('token')}` }
    },

    // Преобразуем книги в формат для v-select
    // title — то что видит пользователь, value — что попадает в form.book
    bookOptions() {
      return this.books.map(b => ({ title: `${b.title} (${b.authors})`, value: b.id }))
    },

    // Преобразуем читателей в формат для v-select
    readerOptions() {
      return this.readers.map(r => ({ title: `${r.full_name} (${r.ticket_number})`, value: r.id }))
    },
  },

  // Загружаем все данные параллельно при открытии страницы
  async mounted() {
    await Promise.all([this.loadBorrowings(), this.loadBooks(), this.loadReaders()])
  },

  methods: {
    // Загрузка истории выдач
    async loadBorrowings() {
      this.loading = true
      try {
        const res = await axios.get(API, { headers: this.authHeaders })
        this.borrowings = res.data
      } catch {
        this.error = 'Не удалось загрузить данные'
      } finally {
        this.loading = false
      }
    },

    // Загрузка книг для выпадающего списка
    async loadBooks() {
      const res = await axios.get('http://127.0.0.1:8000/api/books/', { headers: this.authHeaders })
      this.books = res.data
    },

    // Загрузка читателей для выпадающего списка
    async loadReaders() {
      const res = await axios.get('http://127.0.0.1:8000/api/readers/', { headers: this.authHeaders })
      this.readers = res.data
    },

    // Выдать книгу: POST /api/borrowings/ с {book: id, reader: id}
    // BorrowingViewSet.create() проверит наличие экземпляров
    // и уменьшит quantity на 1
    async borrowBook() {
      this.error = ''
      try {
        await axios.post(API, this.form, { headers: this.authHeaders })
        this.form = { book: null, reader: null }  // сброс формы
        await this.loadBorrowings()               // обновляем таблицу
      } catch (err) {
        // Ошибка из views.py: "Книга отсутствует в читальном зале"
        this.error = err.response?.data?.error || 'Ошибка при выдаче книги'
      }
    },

    // Вернуть книгу: PATCH /api/borrowings/{id}/ с {return_date: "дата"}
    // BorrowingViewSet.update() увеличит quantity на 1
    async returnBook(item) {
      const today = new Date().toISOString().split('T')[0]  // формат YYYY-MM-DD
      await axios.patch(`${API}${item.id}/`, { return_date: today }, { headers: this.authHeaders })
      await this.loadBorrowings()
    },
  },
}
</script>
