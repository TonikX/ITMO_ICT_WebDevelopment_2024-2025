<template>
  <div class="container">
    <h2>Contract {{$route.params.contractNumber}}</h2>
    <ul>
      <li v-for="(value, key) in data" :key="key">
        <strong>{{ key }}:</strong> {{ value }}
      </li>
    </ul>

    <router-link class='btn btn-primary' :to="{name: 'edit-contract', params: { contractNumber: $route.params.contractNumber }}">Edit</router-link>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      data: {},
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/contracts/${this.$route.params.contractNumber}/`);

        this.data = response.data;
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