<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";

const clients = ref([])
const search = ref("")
let headers = [
          {
            align: 'center',
            key: 'name',
            sortable: false,
            title: '',
          },
          { key: 'first_name', title: 'First Name' },
          { key: 'last_name', title: 'Last Name' },
          { key: 'father_name', title: 'Father/Middle Name' },
          { key: 'passport_number', title: 'Passport Number' },
          { key: 'origin_city', title: 'Origin City' },
        ]

function getClients() {
  instance.get('/hotel/clients/').then(
    response => {
      if (response.status === 200) {
        clients.value = response.data
      }
    }
  ).catch(error => console.log(error))
}

onMounted(() => {
  getClients()
})
</script>

<template>
  <v-card
    title="Sortable Clients List"
    min-height="660"
    min-width="850"
    flat
    flex="true"
    align="center"
  >
    <template v-slot:text>
      <v-text-field
        v-model="search"
        label="Search"
        variant="outlined"
        hide-details
        single-line
      ></v-text-field>
    </template>

    <v-data-table
      :headers="headers"
      :items="clients"
      :search="search"
    ></v-data-table>
  </v-card>
</template>

<style scoped>
.v-data-table-header th {
  text-transform: uppercase;
  text-align: center;
}
</style>
