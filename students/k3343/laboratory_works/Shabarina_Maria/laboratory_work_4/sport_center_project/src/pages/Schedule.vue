<template>
  <div id="main">
    <Header />
    <router-view />
    <ScheduleTable />
  </div>
</template>

<script setup>
import ScheduleTable from "@/components/schedule/ScheduleTable.vue";
import Header from "@/components/layouts/Header.vue";
</script>
