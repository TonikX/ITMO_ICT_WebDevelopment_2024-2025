<template>
  <div class="container">
    <h2>Edit contract</h2>
    <div class="form-container">
     <form @submit.prevent="submit">
        <label for="signing_date">Signing date:</label>
        <input type="date" id="signing_date" v-model="contractData.signing_date" required class="form-control">

        <label for="start_date">Start date:</label>
        <input type="date" id="start_date" v-model="contractData.start_date" required class="form-control">

        <label for="end_date">End date:</label>
        <input type="date" id="end_date" v-model="contractData.end_date" required class="form-control">

        <label for="agent">Agent:</label>
        <input type="number" id="agent" v-model="contractData.agent" required class="form-control">

        <label for="type">Type:</label>
            <select class="form-select" v-model="contractData.type" id="type" required>
                <option v-for="type in types">{{ type }}</option>
            </select>

        <label for="enterprise">Enterprise:</label>
            <select class="form-select" v-model="contractData.enterprise" id="enterprise">
                <option v-for="enterprise in enterprises" :key="enterprise.id" :value="enterprise.id">{{ enterprise.short_name }}</option>
            </select>

         <label for="available_payouts">Available payouts:</label>
            <select class="form-select" v-model="contractData.available_payouts" id="available_payouts" required multiple>
                <option v-for="payout in payouts" :key="payout.id" :value="payout.id">{{ payout }}</option>
            </select>       

        <label for="participating_persons">Participating persons:</label>
            <select class="form-select" v-model="contractData.participating_persons" id="participating_persons" required multiple>
                <option v-for="client in persons" :key="client.id" :value="client.id">{{ client.name }}</option>
            </select>       
        <br>

      <button class="btn btn-primary" type="submit">Enter</button>
    </form>
  </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
            types: ['col', 'ind'],
      enterprises: [],
      payouts: [],
      persons: [],
      contractData: {
        signing_date: '',
        start_date: '',
        end_date: '',
        type: '',
        agent: null,
        enterprise: null,
        available_payouts: null,
        participating_persons: null
      }

    };
  },
  async mounted() {
    this.fetchInitialData();

    const clients = await axios.get('http://127.0.0.1:8000/clients/')
        this.persons = clients.data
        const enterprises = await axios.get('http://127.0.0.1:8000/enterprises/')
        this.enterprises = enterprises.data
        const payouts = await axios.get('http://127.0.0.1:8000/payouts/')
        this.payouts = payouts.data
  },
  methods: {
    async fetchInitialData() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/contracts/${this.$route.params.contractNumber}/`);
        this.contractData = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async submit() {
      try {
        console.log(this.contractData);
        await axios.put(`http://127.0.0.1:8000/contracts/${this.$route.params.contractNumber}/`,this.contractData);

        this.$router.push({ name: 'contracts' });
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
