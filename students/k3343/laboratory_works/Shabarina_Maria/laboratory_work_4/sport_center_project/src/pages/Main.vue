<template>
  <div id="main">
    <Header />
    <router-view />
    <MainBanner />
    <MainTodayTrainings />
  </div>
</template>

<script setup>
import Header from '../components/layouts/Header.vue';
import MainTodayTrainings from "@/components/main/MainTodayTrainingsTable.vue";
import MainBanner from "@/components/main/MainBanner.vue";

</script>
