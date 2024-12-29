<template>
  <div id="app">
    <AppHeader />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import AppHeader from '@/views/AppHeader.vue';

export default {
  components: {
    AppHeader,
  },
};
</script>

<style>
body {
  font-family: 'Inter', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f7f6;
}
main {
  padding: 30px;
}
</style>
