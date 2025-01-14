<template>
  <div id="main">
    <Header />
    <router-view />
    <SectionsList />
  </div>
</template>

<script setup>
import Header from "@/components/layouts/Header.vue";
import SectionsList from "@/components/sections/SectionsList.vue";
</script>
