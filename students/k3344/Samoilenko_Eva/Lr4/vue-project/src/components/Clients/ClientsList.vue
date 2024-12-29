<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const clients = ref([])

function getClients() {
  instance.get('/hotel/clients/').then(
    response => {
      if (response.status === 200) {
        clients.value = response.data
      }
    }
  ).catch(error => console.log(error))
}

function deleteClient(id) {
  if (confirm("Are you sure you want to delete this client?")) {
    instance.delete(`/hotel/clients/${id}/`)
      .then(response => {
        if (response.status === 204) {
          getClients();
        }
      })
      .catch(error => console.log(error));
  } else {
    console.log("Client deletion cancelled.");
  }
}

onMounted(() => {
  getClients()
})
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <div align="center">
      <h1>Hotel Clients</h1>
      <div class="button-group">
        <v-btn
          class="styled-btn"
          color="green"
          block
          @click="router.push('/clients/add')"
        >
          ADD
        </v-btn>
        <v-btn
          class="styled-btn"
          color="blue"
          block
          @click="router.push('/clients/sort')"
        >
          SORT
        </v-btn>
      </div>
    </div>

    <div v-if="clients.length === 0">Loading clients...</div>

    <v-container min-width="1000">
      <v-row>
        <v-col
          v-for="client in clients"
          :key="client.id"
          cols="12"
          md="6"
        >
          <v-card width="100%">
            <v-card-title>Client {{ client.first_name }} {{ client.last_name }}</v-card-title>
            <v-card-item v-if="client.father_name">
              Father/Middle Name: {{ client.father_name }}
            </v-card-item>
            <v-card-item> Passport: {{ client.passport_number }}</v-card-item>
            <v-card-item> Origin City: {{ client.origin_city }}</v-card-item>
            <v-card-actions>
              <v-btn color="blue" @click="router.push('/clients/' + client.id)">
                Edit
              </v-btn>
              <v-btn color="red" @click="deleteClient(client.id)">
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style scoped>
.button-group {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 10px;
}

.styled-btn {
  width: 50px;
  height: 50px;
  font-size: 15px;
  font-weight: bold;
  border-radius: 8px;
  text-transform: uppercase;
}
h1{
  margin-top: 50px;
}
</style>
