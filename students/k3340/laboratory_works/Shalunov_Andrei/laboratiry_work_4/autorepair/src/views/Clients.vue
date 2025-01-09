<template>
  <v-container>
    <h2>Clients</h2>
    <v-row>
      <v-col cols="12" md="6" lg="4" v-for="client in clients" :key="client.id">
        <ClientCard :client="client" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex';
import axios from 'axios';
import ClientCard from '../components/ClientCard.vue';

export default {
  components: { ClientCard },
  data() {
    return {
      clients: [],
    };
  },
  computed: mapState(['token']),
  async mounted() {
    try {
      const response = await axios.get('/clients/'); // Токен автоматически добавляется через Axios
      this.clients = response.data;
    } catch (error) {
      console.error('Failed to fetch clients:', error);
    }
  },
};
</script>
