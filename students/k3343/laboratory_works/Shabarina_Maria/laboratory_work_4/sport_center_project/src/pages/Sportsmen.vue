<template>
  <div id="main">
    <Header />
    <router-view />
    <SportsmenTable />
  </div>
</template>

<script setup>
import Header from '../components/layouts/Header.vue';
import SportsmenTable from "@/components/sportsmen/SportsmenTable.vue";

</script>
