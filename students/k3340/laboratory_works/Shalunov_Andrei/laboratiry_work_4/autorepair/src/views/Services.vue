<template>
  <v-container>
    <h2>Services</h2>
    <v-row>
      <v-col cols="12" md="6" lg="4" v-for="service in services" :key="service.id">
        <ServiceCard :service="service" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex';
import ServiceCard from '../components/ServiceCard.vue';

export default {
  components: { ServiceCard },
  computed: mapState(['services']),
  mounted() {
    this.$store.dispatch('fetchServices');
  },
};
</script>
