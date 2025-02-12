<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">Школьная система</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Переключатель навигации"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li v-for="item in menuItems" :key="item.name" class="nav-item">
            <router-link class="nav-link" :to="item.path">{{ item.name }}</router-link>
          </li>
        </ul>
        <!-- Кнопка Выйти -->
        <router-link class="btn btn-danger ms-auto" to="/login">Выйти</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      menuItems: [
        { name: "Профиль", path: "home-page" },
        { name: "Учителя", path: "/teachers-list" },
        { name: "Ученики", path: "/student-list" },
        { name: "Классы", path: "/classes" },
        { name: "Предметы", path: "/teachersubject" },
        { name: "Оценки", path: "/grades" },
        { name: "Расписание", path: "/schedule" },
        { name: "Отчёты", path: "/class-report" },
      ],
    };
  },
};
</script>

<style scoped>
.nav-item {
  margin-right: 15px;
}

.nav-link:hover {
  background-color: #0D6EFD;
  border: noneж
}

body {
  padding-top: 56px;
}
</style>

