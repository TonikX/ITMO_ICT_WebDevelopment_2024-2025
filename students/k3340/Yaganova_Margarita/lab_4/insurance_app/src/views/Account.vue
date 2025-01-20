<template>
  <div class="container">
    <h1>Account</h1>
    <div v-if="user">
      <ul>
        <template v-for="(value, key) in user" :key="key">
            <li v-if="key!=='id'"><strong>{{ key }}:</strong> {{ value }}</li>
        </template>
      </ul>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>

    <router-link class="btn btn-primary" :to="{name: 'edit-user'}">Edit</router-link>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: null, 
    };
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      try {
        const token = localStorage.getItem('token');

        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };

        const response = await axios.get(' http://127.0.0.1:8000/auth/users/me/', config);
        this.user = response.data;
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
