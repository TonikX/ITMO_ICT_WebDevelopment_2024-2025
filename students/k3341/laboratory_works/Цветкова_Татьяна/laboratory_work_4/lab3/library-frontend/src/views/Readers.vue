<template>
  <v-container class="pa-6">
    <h1 class="text-h4 mb-6">
      <v-icon icon="mdi-account-group" class="mr-2" />Читатели
    </h1>

    <!-- Форма добавления читателя -->
    <v-card class="pa-4 mb-6" elevation="2">
      <v-card-title>Добавить читателя</v-card-title>
      <v-row class="mt-2">

        <!-- ФИО -->
        <v-col cols="12" md="4">
          <v-text-field v-model="form.full_name" label="ФИО" variant="outlined" density="compact" />
        </v-col>

        <!-- Номер читательского билета — уникальный для каждого читателя -->
        <v-col cols="12" md="4">
          <v-text-field v-model="form.ticket_number" label="Номер билета" variant="outlined" density="compact" />
        </v-col>

        <!-- Паспортные данные -->
        <v-col cols="12" md="4">
          <v-text-field v-model="form.passport_number" label="Номер паспорта" variant="outlined" density="compact" />
        </v-col>

        <!-- Дата рождения — тип date показывает встроенный датапикер браузера -->
        <v-col cols="12" md="3">
          <v-text-field v-model="form.birth_date" label="Дата рождения" type="date" variant="outlined" density="compact" />
        </v-col>

        <v-col cols="12" md="3">
          <v-text-field v-model="form.phone" label="Телефон" variant="outlined" density="compact" />
        </v-col>

        <v-col cols="12" md="3">
          <v-text-field v-model="form.address" label="Адрес" variant="outlined" density="compact" />
        </v-col>

        <!-- Уровень образования — выпадающий список -->
        <v-col cols="12" md="3">
          <v-select
            v-model="form.education"
            :items="educationOptions"
            label="Образование"
            variant="outlined"
            density="compact"
          />
        </v-col>

        <!-- Привязка к читальному залу.
             clearable — можно очистить выбор (читатель без зала) -->
        <v-col cols="12" md="3">
          <v-select
            v-model="form.reading_room"
            :items="roomOptions"
            label="Читальный зал"
            variant="outlined"
            density="compact"
            clearable
          />
        </v-col>

        <!-- Чекбокс учёной степени -->
        <v-col cols="12" md="3" class="d-flex align-center">
          <v-checkbox v-model="form.has_degree" label="Учёная степень" density="compact" />
        </v-col>

        <!-- Кнопка добавления -->
        <v-col cols="12" md="3" class="d-flex align-center">
          <v-btn color="primary" block @click="addReader">
            <v-icon icon="mdi-plus" class="mr-1" />Добавить
          </v-btn>
        </v-col>

      </v-row>
    </v-card>

    <!-- Сообщение об ошибке -->
    <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

    <!-- Таблица читателей.
         v-data-table — компонент Vuetify с сортировкой и пагинацией.
         :headers — описание столбцов.
         :items   — данные из API (массив объектов Reader).
         :loading — показывает прогрессбар пока данные загружаются. -->
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="readers"
        :loading="loading"
        no-data-text="Читатели не найдены"
        loading-text="Загрузка..."
      >
        <!-- Слот для колонки is_active — показываем цветной чип вместо true/false -->
        <template #item.is_active="{ item }">
          <v-chip :color="item.is_active ? 'green' : 'red'" size="small">
            {{ item.is_active ? 'Активен' : 'Выбыл' }}
          </v-chip>
        </template>

        <!-- Слот для колонки has_degree — иконка галочки или крестика -->
        <template #item.has_degree="{ item }">
          <v-icon
            :icon="item.has_degree ? 'mdi-check' : 'mdi-close'"
            :color="item.has_degree ? 'green' : 'grey'"
          />
        </template>

        <!-- Слот для колонки actions — кнопка удаления -->
        <template #item.actions="{ item }">
          <v-btn icon="mdi-delete" color="error" variant="text" size="small" @click="deleteReader(item.id)" />
        </template>

      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

const API_READERS = 'http://127.0.0.1:8000/api/readers/'
const API_ROOMS   = 'http://127.0.0.1:8000/api/rooms/'

export default {
  data() {
    return {
      readers: [],   // массив читателей из API
      rooms: [],     // массив залов (для выпадающего списка)
      loading: false,
      error: '',

      // Объект формы — v-model полей привязан к этим свойствам
      form: {
        full_name: '',
        ticket_number: '',
        passport_number: '',
        birth_date: '',
        phone: '',
        address: '',
        education: 'secondary',  // значение по умолчанию
        has_degree: false,
        reading_room: null,       // id зала или null
      },

      // Варианты для выпадающего списка образования
      educationOptions: [
        { title: 'Начальное', value: 'primary' },
        { title: 'Среднее',   value: 'secondary' },
        { title: 'Высшее',    value: 'higher' },
      ],

      // Описание столбцов таблицы.
      // key — имя поля в объекте читателя (или вычисляемого поля сериализатора)
      headers: [
        { title: 'ФИО',        key: 'full_name' },
        { title: 'Билет',      key: 'ticket_number' },
        { title: 'Телефон',    key: 'phone' },
        { title: 'Образование',key: 'education' },
        { title: 'Степень',    key: 'has_degree' },
        { title: 'Зал',        key: 'reading_room_name' }, // доп. поле из сериализатора
        { title: 'Статус',     key: 'is_active' },
        { title: '',           key: 'actions', sortable: false },
      ],
    }
  },

  computed: {
    // Заголовок авторизации для всех запросов
    authHeaders() {
      return { Authorization: `Token ${localStorage.getItem('token')}` }
    },

    // Преобразуем массив залов в формат для v-select: [{title, value}, ...]
    roomOptions() {
      return this.rooms.map(r => ({ title: r.name, value: r.id }))
    },
  },

  // При загрузке страницы одновременно загружаем читателей и залы
  async mounted() {
    await Promise.all([this.loadReaders(), this.loadRooms()])
  },

  methods: {
    // Загрузка списка читателей с сервера
    async loadReaders() {
      this.loading = true
      try {
        const res = await axios.get(API_READERS, { headers: this.authHeaders })
        this.readers = res.data  // массив объектов Reader
      } catch {
        this.error = 'Не удалось загрузить читателей'
      } finally {
        this.loading = false
      }
    },

    // Загрузка залов для выпадающего списка
    async loadRooms() {
      const res = await axios.get(API_ROOMS, { headers: this.authHeaders })
      this.rooms = res.data
    },

    // Добавление нового читателя
    async addReader() {
      this.error = ''
      try {
        // POST-запрос с данными формы → Django создаёт объект Reader в БД
        await axios.post(API_READERS, this.form, { headers: this.authHeaders })

        // Сбрасываем форму после успешного добавления
        this.form = {
          full_name: '', ticket_number: '', passport_number: '',
          birth_date: '', phone: '', address: '',
          education: 'secondary', has_degree: false, reading_room: null,
        }

        // Обновляем таблицу
        await this.loadReaders()
      } catch (err) {
        // Показываем ошибку валидации от Django (например: "Билет уже существует")
        this.error = err.response?.data ? JSON.stringify(err.response.data) : 'Ошибка добавления'
      }
    },

    // Удаление читателя по id
    async deleteReader(id) {
      await axios.delete(`${API_READERS}${id}/`, { headers: this.authHeaders })
      await this.loadReaders()
    },
  },
}
</script>
