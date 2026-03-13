<template>
  <!-- v-app — обязательный корневой контейнер Vuetify,
       оборачивает всё приложение -->
  <v-app>

    <!-- НАВИГАЦИОННАЯ ПАНЕЛЬ (шапка)
         color="primary" — синий цвет из темы Vuetify
         elevation="2"   — тень под панелью -->
    <v-app-bar color="primary" elevation="2">

      <!-- Логотип и название системы слева -->
      <v-app-bar-title>
        <v-icon icon="mdi-library" class="mr-2" />
        Библиотека
      </v-app-bar-title>

      <!-- Меню для авторизованного пользователя
           v-if="isLoggedIn" — показывается только если есть токен -->
      <template v-if="isLoggedIn">
        <v-btn variant="text" color="white" to="/dashboard">Главная</v-btn>
        <v-btn variant="text" color="white" to="/books">Книги</v-btn>
        <v-btn variant="text" color="white" to="/readers">Читатели</v-btn>
        <v-btn variant="text" color="white" to="/borrowings">Выдача книг</v-btn>
        <v-btn variant="text" color="white" to="/rooms">Залы</v-btn>
        <!-- Кнопка выхода — вызывает метод logout() -->
        <v-btn variant="text" color="white" @click="logout">
          <v-icon icon="mdi-logout" class="mr-1" />Выход
        </v-btn>
      </template>

      <!-- Меню для неавторизованного пользователя
           v-else — показывается когда токена нет -->
      <template v-else>
        <v-btn variant="text" color="white" to="/login">Вход</v-btn>
        <v-btn variant="text" color="white" to="/register">Регистрация</v-btn>
      </template>

    </v-app-bar>

    <!-- Основная область страницы -->
    <v-main>
      <!-- router-view — сюда Vue Router вставляет компонент
           текущей страницы (Books, Readers, Dashboard и т.д.) -->
      <router-view />
    </v-main>

  </v-app>
</template>

<script>
export default {
  data() {
    return {
      // Токен авторизации из localStorage.
      // Если токен есть — пользователь вошёл в систему.
      // Djoser выдаёт токен при POST /auth/token/login/
      token: localStorage.getItem('token'),
    }
  },

  computed: {
    // isLoggedIn — вычисляемое свойство (обновляется когда меняется token).
    // !! преобразует любое значение в boolean:
    //   'abc123' → true  (пользователь авторизован)
    //   null     → false (не авторизован)
    isLoggedIn() {
      return !!this.token
    },
  },

  watch: {
    // $route — слежение за сменой страницы (маршрута).
    // При каждой навигации перечитываем localStorage.
    // Это нужно потому что localStorage не реактивен в Vue:
    // computed-свойство не обновится само при Login.vue вызове
    // localStorage.setItem('token', ...) — только через watch.
    $route() {
      this.token = localStorage.getItem('token')
    },
  },

  methods: {
    // Выход из системы
    logout() {
      localStorage.removeItem('token')   // удаляем токен из браузера
      this.token = null                  // обнуляем реактивное поле → шапка обновится
      this.$router.push('/login')        // перенаправляем на страницу входа
    },
  },
}
</script>
