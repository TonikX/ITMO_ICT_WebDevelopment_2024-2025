<template>
  <div class="page-container">
    <h1>Contracts</h1>
    <div v-for="(item, index) in infoArray" :key="index" class="info-card">
      <contrats-card :dict="item"></contrats-card>
    </div>
  </div>
  <hr>
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
                <option v-for="enterprise in enterprises">{{ enterprise.short_name }}</option>
            </select>

         <label for="available_payouts">Available payouts:</label>
            <select class="form-select" v-model="contractData.available_payouts" id="available_payouts" required multiple>
                <option v-for="payout in payouts">{{ payout }}</option>
            </select>       

        <label for="participating_persons">Participating persons:</label>
            <select class="form-select" v-model="contractData.participating_persons" id="participating_persons" required multiple>
                <option v-for="client in persons">{{ client.name }}</option>
            </select>       
        <br>

      <button class="btn btn-primary" type="submit">Enter</button>
    </form>
  </div>
</template>

<script>
import ContratsCard from '@/components/ContratsCard.vue';
import axios from 'axios';


export default {
  components: {
    ContratsCard,
  },
  data() {
    return {
        infoArray: [],
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
  methods: {
    submit() {
        axios.post('http://127.0.0.1:8000/contracts/', this.contractData)
            .then(response => {window.location.reload()})
    }
  },
  async mounted() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/contracts/')
        this.infoArray = response.data
        const clients = await axios.get('http://127.0.0.1:8000/clients/')
        this.persons = clients.data
        const enterprises = await axios.get('http://127.0.0.1:8000/enterprises/')
        this.enterprises = enterprises.data
        const payouts = await axios.get('http://127.0.0.1:8000/payouts/')
        this.payouts = payouts.data
    } catch (error) {
        console.error(error)
    }
  }
};
</script>

<style>
.form-container {
    margin: 20px;
}

.form-control {
    margin: 7px 0px 7px 0px;
}
.page-container {
  margin: 20px;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.info-card {
  margin-bottom: 20px;
}
</style>