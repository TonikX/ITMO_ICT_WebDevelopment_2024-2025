<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";

const bookings = ref([])
const search = ref("")
let headers = [
  {
    key: 'name',
    sortable: false,
    title: '',
  },
  {
    title: 'Client', align: "center", children: [
      {key: 'client.first_name', title: 'Name'},
      {key: 'client.last_name', title: 'Surname'}]
  },
  {
    title: 'Room', align: "center", children: [
      {key: 'room.room_type', title: 'Type'},
      {key: 'room.floor_num', title: 'Floor'}]
  },

  {
    title: 'Dates', align: "center", children: [
      {key: 'start_date', title: 'Start', align: "center"},
      {key: 'end_date', title: 'End', align: "center"}]
  },

  {key: 'is_verified', title: 'Status', align: "center"},
]

function getBookings() {
  instance.get('/hotel/bookings/').then(
    response => {
      if (response.status === 200) {
        bookings.value = response.data
      }
    }
  ).catch(error => console.log(error))
}

onMounted(() => {
  getBookings()
})
</script>

<template>
  <v-card
    title="Sortable Bookings List"
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
      :items="bookings"
      :search="search"
      width="1000"
    ></v-data-table>
  </v-card>
</template>

<style scoped>
.v-data-table-header th {
  text-transform: uppercase;
  text-align: center;
}
</style>
