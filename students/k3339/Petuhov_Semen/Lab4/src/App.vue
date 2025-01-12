<template>
  <div id="app">
    <router-view></router-view> <!-- Здесь будет отображаться компоненты согласно маршрутам -->
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Простой стиль */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
