<template>
  <v-container class="pa-6">
    <h1 class="text-h4 mb-6">
      <v-icon icon="mdi-view-dashboard" class="mr-2" />Система управления библиотекой
    </h1>

    <!-- Сетка карточек со статистикой.
         v-for — перебирает массив stats и рисует карточку для каждого элемента.
         :key — уникальный ключ для Vue (оптимизация перерисовки) -->
    <v-row>
      <v-col cols="12" sm="6" md="3" v-for="card in stats" :key="card.label">

        <!-- Карточка-ссылка.
             :color  — цвет берётся из объекта card (blue, green, orange, purple)
             :to     — маршрут для перехода при клике (как router-link)
             hover   — подсвечивает карточку при наведении -->
        <v-card
          :color="card.color"
          variant="tonal"
          class="pa-4 text-center"
          :to="card.route"
          hover
          style="cursor: pointer;"
        >
          <!-- Иконка раздела -->
          <v-icon :icon="card.icon" size="40" class="mb-2" />

          <!-- Числовое значение (загружается с API) -->
          <div class="text-h4 font-weight-bold">{{ card.value }}</div>

          <!-- Название раздела -->
          <div class="text-subtitle-1">{{ card.label }}</div>

          <!-- Подсказка для пользователя -->
          <div class="text-caption mt-1 text-medium-emphasis">Нажмите для перехода →</div>
        </v-card>

      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      // Массив карточек статистики.
      // value изначально 0 — заполнится в mounted() после запросов к API.
      stats: [
        { label: 'Книги',         value: 0, icon: 'mdi-book-open',        color: 'blue',   route: '/books' },
        { label: 'Читатели',      value: 0, icon: 'mdi-account-group',    color: 'green',  route: '/readers' },
        { label: 'Выдано книг',   value: 0, icon: 'mdi-book-arrow-right', color: 'orange', route: '/borrowings' },
        { label: 'Читальные залы',value: 0, icon: 'mdi-door',             color: 'purple', route: '/rooms' },
      ],
    }
  },

  // mounted() — вызывается когда компонент добавлен в DOM.
  // Здесь загружаем данные с сервера.
  async mounted() {
    const token = localStorage.getItem('token')

    // Заголовок Authorization нужен для всех защищённых эндпоинтов Django REST
    const headers = { Authorization: `Token ${token}` }

    // Promise.all — отправляем все 4 запроса одновременно (параллельно),
    // а не последовательно. Это быстрее.
    const [books, readers, borrowings, rooms] = await Promise.all([
      axios.get('http://127.0.0.1:8000/api/books/',     { headers }),
      axios.get('http://127.0.0.1:8000/api/readers/',   { headers }),
      axios.get('http://127.0.0.1:8000/api/borrowings/',{ headers }),
      axios.get('http://127.0.0.1:8000/api/rooms/',     { headers }),
    ])

    // Обновляем значения в карточках — .length даёт количество записей
    this.stats[0].value = books.data.length
    this.stats[1].value = readers.data.length
    this.stats[2].value = borrowings.data.length
    this.stats[3].value = rooms.data.length
  },
}
</script>
