<template>
  <div id="main">
    <Header />
    <router-view />
    <ReportsGenerate />
  </div>
</template>

<script setup>
import Header from '../components/layouts/Header.vue';
import ReportsGenerate from "@/components/reports/ReportsGenerate.vue";

</script>
