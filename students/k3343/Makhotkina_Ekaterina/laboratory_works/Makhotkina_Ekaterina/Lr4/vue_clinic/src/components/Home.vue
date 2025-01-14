<template>
  <v-app>
    <Header />
    <v-main class="content-container">
      <v-container>
        <h1>Добро пожаловать на главную страницу!</h1>
        <p>Выберите раздел из меню выше.</p>
      </v-container>
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import Header from "@/components/Visual/Header.vue";
import Footer from "@/components/Visual/Footer.vue";

export default {
  components: {
    Header,
    Footer,
  },
};
</script>

<style scoped>
.content-container {
  min-height: calc(100vh - 128px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
