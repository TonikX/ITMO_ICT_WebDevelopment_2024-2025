<template>
  <div class="container">
    <h2>Enterprise payouts</h2>
    <form @submit.prevent="fetchData">
      <label for="companyId">ID:</label>
      <input type="number" class="form-control" id="companyId" v-model="companyId">

      <button class="btn btn-primary" type="submit">Enter</button>
    </form>

    <div v-if="insurancePayments !== null">
      <h3>Total:</h3>
      <p>{{ insurancePayments.total }}$</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      companyId: '',
      insurancePayments: null,
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/total_payment', {
          params: {
            company_id: this.companyId,
          },
        });

        this.insurancePayments = response.data;
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style>
.container {
    margin: 10px;
}
</style>