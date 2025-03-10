<script setup lang="ts">
import { RouterView } from 'vue-router'
import MyHeader from "@/components/navigation/MyHeader.vue";
import MyFooter from "@/components/navigation/MyFooter.vue";
</script>

<template>
  <MyHeader />
  <RouterView class="container"/>
  <MyFooter />
</template>

<style scoped>
</style>
