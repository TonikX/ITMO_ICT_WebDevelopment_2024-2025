<template>
  <v-container>
    <h2>Contracts</h2>
    <v-row>
      <v-col cols="12" md="6" lg="4" v-for="contract in contracts" :key="contract.id">
        <ContractDetails :contract="contract" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex';
import ContractDetails from '../components/ContractDetails.vue';

export default {
  components: { ContractDetails },
  computed: mapState(['contracts']),
  mounted() {
    this.$store.dispatch('fetchContracts');
  },
};
</script>
