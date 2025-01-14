<template>
  <header class="navbar navbar-expand-lg">
    <router-link to="/">Главная</router-link>
    <nav>
      <router-link to="/schedule">Расписание</router-link>
      <router-link to="/sections">Секции</router-link>
      <router-link to="/sportsmen">Ученики</router-link>
      <router-link to="/coaches">Тренеры</router-link>
      <router-link to="/reports">Отчет</router-link>
    </nav>
  </header>
</template>

<script>

</script>

<style scoped>
.navbar {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 0.5% 3% 0.5% 3%;
  background: #596dff;
}

nav {
  display: flex;
  flex-direction: row;
}

a, button {
  align-items: center;
  justify-content: center;
  color: black;
  margin: 0.5%;
  text-decoration: none;
  text-align: center;
  background-color: #ffa44b;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  cursor: pointer;
}

a:hover {
  background-color: #c5813b;
}

button:hover {
  background-color: #c5813b;
}
</style>
