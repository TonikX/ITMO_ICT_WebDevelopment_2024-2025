<template>
  <v-container>
    <h1>Отчеты</h1>
    <MostFrequentPlane />
    <UnderFilledRoutes />
    <PlaneStats />
  </v-container>
</template>

<script>
import MostFrequentPlane from '@/components/reports/FrequentPlaneOnRoute.vue';
import UnderFilledRoutes from '@/components/reports/UnderFilledRoutes.vue';
import PlaneStats from '@/components/reports/PlaneStats.vue';

export default {
  components: {
    MostFrequentPlane,
    UnderFilledRoutes,
    PlaneStats,
  },
};
</script>

<style scoped>
</style>
