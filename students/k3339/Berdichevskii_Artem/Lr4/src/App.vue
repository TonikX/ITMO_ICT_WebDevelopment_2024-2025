<script setup>
import MyHeader from "@/components/MyHeader.vue";
import MyFooter from "@/components/MyFooter.vue";
</script>

<template>
  <MyHeader />
  <main class="container py-4">
    <RouterView/>
  </main>
  <MyFooter />
</template>

<style scoped>
</style>
