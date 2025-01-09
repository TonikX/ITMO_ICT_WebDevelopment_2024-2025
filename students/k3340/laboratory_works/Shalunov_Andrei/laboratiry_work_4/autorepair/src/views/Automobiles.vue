<template>
  <v-container>
    <h2>Automobiles</h2>
    <CarList :cars="automobiles" />
  </v-container>
</template>

<script>
import { mapState } from 'vuex';
import CarList from '../components/CarList.vue';

export default {
  components: { CarList },
  computed: mapState(['automobiles']),
  mounted() {
    this.$store.dispatch('fetchAutomobiles');
  },
};
</script>
