<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <UnderFilledRoutes />
      </v-col>

      <v-col cols="12" md="6">
        <MostFrequentPlane />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import UnderFilledRoutes from '@/components/reports/UnderFilledRoutes.vue';
import MostFrequentPlane from '@/components/reports/FrequentPlaneOnRoute.vue';

export default {
  components: {
    UnderFilledRoutes,
    MostFrequentPlane,
  },
};
</script>

<style scoped>
</style>
