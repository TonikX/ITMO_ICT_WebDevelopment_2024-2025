<template>
  <v-container>
    <h2>Employees</h2>
    <v-row>
      <v-col cols="12" md="6" lg="4" v-for="employee in employees" :key="employee.id">
        <EmployeeCard :employee="employee" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex';
import EmployeeCard from '../components/EmployeeCard.vue';

export default {
  components: { EmployeeCard },
  computed: mapState(['employees']),
  mounted() {
    this.$store.dispatch('fetchEmployees');
  },
};
</script>
