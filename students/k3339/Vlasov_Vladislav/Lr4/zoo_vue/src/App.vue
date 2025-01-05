<script setup>
import { RouterView } from 'vue-router'
import HeadBar from './components/HeadBar.vue'
import AccountHeadBar from './components/AccountHeadBar.vue'
</script>

<template>
  <header>
    <AccountHeadBar />
  </header>

  <header>
    <HeadBar />
  </header>
  
  <RouterView />

</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }
}
</style>
