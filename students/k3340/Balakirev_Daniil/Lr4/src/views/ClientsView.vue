<template>
  <v-main>
    <v-container fluid>
      <h1>Клиенты</h1>

      <v-row align="center">
        <v-col cols="12" md="4">
          <v-text-field
            v-model="search"
            label="Искать клиентов"
            append-icon="mdi-magnify"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="4" class="text-right">
          <v-btn color="primary" @click="openAddClientDialog">Добавить клиента</v-btn>
        </v-col>
      </v-row>

      <v-row>
        <v-col
          v-for="client in filteredClients"
          :key="client.passport_number"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card @click="openClientDetails(client)" class="client-card">
            <v-card-title>{{ client.last_name }} {{ client.first_name }}</v-card-title>
            <v-card-subtitle>Паспорт: {{ client.passport_number }}</v-card-subtitle>
            <v-card-text>Город: {{ client.city }}</v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-dialog v-model="dialog" max-width="600px">
        <client-details
          v-if="selectedClient"
          :client="selectedClient"
          @client-updated="getClients"
          @client-deleted="getClients"
          @close="closeDialog"
        />
      </v-dialog>

      <v-dialog v-model="addDialog" max-width="500px">
        <v-card>
          <v-card-title>Добавить нового клиента</v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field v-model="newClient.last_name" label="Фамилия" required></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="newClient.first_name" label="Имя" required></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="newClient.middle_name" label="Отчество"></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="newClient.passport_number" label="Паспорт" required></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="newClient.city" label="Город" required></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue-grey lighten-1" text @click="closeAddClientDialog">Оменить</v-btn>
            <v-btn color="primary" @click="addClient">Сохранить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
        {{ snackbarText }}
        <template v-slot:action="{ attrs }">
          <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-container>
  </v-main>
</template>

<script>
import ClientDetails from '@/components/ClientDetails.vue';

export default {
  name: 'ClientsView',
  components: {
    ClientDetails
  },
  data() {
    return {
      clients: [],
      dialog: false,
      addDialog: false,
      selectedClient: null,
      search: '',
      filterCity: null,
      newClient: {
        last_name: '',
        first_name: '',
        middle_name: '',
        passport_number: '',
        city: ''
      },
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'error'
    };
  },
  computed: {
    filteredClients() {
      let filtered = this.clients;

      if (this.search) {
        const searchTerm = this.search.toLowerCase();
        filtered = filtered.filter(client => {
          return (
            client.last_name.toLowerCase().includes(searchTerm) ||
            client.first_name.toLowerCase().includes(searchTerm) ||
            client.passport_number.toLowerCase().includes(searchTerm) ||
            client.city.toLowerCase().includes(searchTerm)
          );
        });
      }

      if (this.filterCity) {
        filtered = filtered.filter(client => client.city === this.filterCity);
      }

      return filtered;
    },
    availableCities() {
      return [...new Set(this.clients.map(client => client.city))];
    }
  },
  methods: {
    async getClients() {
      try {
        const response = await this.axios.get(this.$hostname + 'clients/', {
          headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
        });
        this.clients = response.data;
      } catch (error) {
        console.error(error);
        this.showSnackbar('Error loading clients: ' + error.message, 'error');
      }
    },
    openClientDetails(client) {
      this.selectedClient = client;
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
      this.selectedClient = null;
    },
    openAddClientDialog() {
      this.addDialog = true;
    },
    closeAddClientDialog() {
      this.addDialog = false;
      this.newClient = {
        last_name: '',
        first_name: '',
        middle_name: '',
        passport_number: '',
        city: ''
      };
    },
    async addClient() {
      try {
        const response = await this.axios.post(this.$hostname + 'clients/', this.newClient, {
          headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
        });

        if (response.status === 201) {
          this.showSnackbar('Client added successfully', 'success');
          this.closeAddClientDialog();
          this.getClients();
        } else {
          this.showSnackbar('Error adding client', 'error');
        }
      } catch (error) {
        console.error(error);
        this.showSnackbar('Error adding client: ' + error.message, 'error');
      }
    },
    showSnackbar(text, color = 'error') {
      this.snackbarText = text;
      this.snackbarColor = color;
      this.snackbar = true;
    }
  },
  created() {
    this.$hostname = 'http://localhost:8000/api/';
    this.getClients();
  }
};
</script>

<style scoped>
.client-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.client-card:hover {
  transform: scale(1.05);
}
</style>