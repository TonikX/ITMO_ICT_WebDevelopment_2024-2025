<template>
  <div id="main">
    <Header />
    <router-view />
    <CoachesList />
  </div>
</template>

<script setup>
import CoachesList from "@/components/coaches/CoachesList.vue";
import Header from "@/components/layouts/Header.vue";
</script>

