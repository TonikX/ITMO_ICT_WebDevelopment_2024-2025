<template>
  <v-app>
    <v-app-bar app>
      <Navbar />
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>

    <v-footer app>
      <v-container>
        <p>© 2024 Компания Авиаперевозок. Все права защищены.</p>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
import Navbar from './components/tools/Navbar.vue';

export default {
  components: {
    Navbar,
  },
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin: 0;
}
</style>
