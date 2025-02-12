<template>
  <div id="app">
    <!-- Header будет отображаться только на страницах, где это нужно -->
    <Header v-if="showHeader" />
    <router-view />
  </div>
</template>

<script>
import Header from "@/components/Header.vue"; // Проверьте путь до компонента

export default {
  name: "App",
  components: {
    Header,
  },
  computed: {
    // Проверяем текущий маршрут и решаем, показывать ли Header
    showHeader() {
      const noHeaderRoutes = ["/login", "/register"]; // Пути, где header не нужен
      return !noHeaderRoutes.includes(this.$route.path);
    },
  },
};
</script>
