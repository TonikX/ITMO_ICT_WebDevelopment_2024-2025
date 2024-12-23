<template>
  <v-app>
    <!-- Шапка приложения -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>📚 Библиотека</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Кнопки навигации с атрибутом router -->
      <v-btn text :to="{ name: 'Books' }" router>Книги</v-btn>
      <v-btn text :to="{ name: 'Readers' }" router>Читатели</v-btn>
      <v-btn text :to="{ name: 'ReadingRooms' }" router>Читальные залы</v-btn>
      <v-btn text :to="{ name: 'MonthlyReports' }" router>Отчёты</v-btn>
      <v-btn text :to="{ name: 'Reports' }" router>Сводные отчёты</v-btn>
      <v-btn text :to="{ name: 'Transactions' }" router>Транзакции</v-btn>
      <v-btn text :to="{ name: 'LowStockBooks' }" router>Нехватка книг</v-btn>
      <v-btn text :to="{ name: 'Profile' }" router>Профиль</v-btn>
      <v-btn text :to="{ name: 'Login' }" router>Вход</v-btn>
    </v-app-bar>

    <!-- Основное содержимое -->
    <v-main>
      <v-container fluid>
        <!-- Удаляем тестовый компонент -->
        <!-- <VuetifyTest /> -->
        <!-- Возвращаем маршрутизацию -->
        <router-view />
      </v-container>
    </v-main>

    <!-- Нижний колонтитул -->
    <v-footer app color="primary" dark>
      <v-container>
        <v-row justify="center">
          <v-col cols="12" class="text-center">
            © {{ new Date().getFullYear() }} Библиотечное приложение. Все права защищены.
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
.v-app-bar {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

.v-main {
  background-color: #f9fafc;
  min-height: calc(100vh - 64px - 64px); 
}

.v-footer {
  font-size: 14px;
  padding: 8px 0;
}
</style>
