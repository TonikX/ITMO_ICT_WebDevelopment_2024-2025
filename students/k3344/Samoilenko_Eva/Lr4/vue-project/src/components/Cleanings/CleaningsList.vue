<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const headers = [
  {
    align: 'center', key: 'name',
    title: '',
  },
  {
    title: 'Employee', align: "center", children: [
      {key: 'employee.first_name', title: 'First Name'},
      {key: 'employee.last_name', title: 'Last Name'}]
  },
  {key: 'week_day', title: 'Weekday'},
  {key: 'floor_num', title: 'Floor'},
  {title: 'Actions', align: "center", value: 'actions', sortable: false}]

const search = ref("")
const cleanings = ref([])
const employees = ref([])

function getCleanings() {
  instance.get('/hotel/cleanings/').then(
    response => {
      if (response.status === 200) {
        cleanings.value = response.data
      }
    }
  ).catch(error => console.log(error))

  instance.get('hotel/employees/').then(response => {
      if (response.status === 200) {
        employees.value = response.data
      }
    }
  ).catch(error => console.log(error))
}

function deleteCleaning(id) {
  if (confirm("Are you sure you want to delete this cleaning?")) {
    instance.delete(`/hotel/cleanings/${id}/`).then(response => {
        if (response.status === 204) {
          getCleanings()
        }
      }
    ).catch(error => console.log(error))
  } else {
    console.log("Cleaning deletion cancelled.")
  }
}

onMounted(() => {
  getCleanings()
})

</script>

<template>
  <div class="table-container">
    <v-data-table
      :headers="headers"
      :items="cleanings"
      :search="search"
      class="elevation-2 styled-table"
      items-per-page="6"
      height="450"
    >
      <template v-slot:top>
        <v-toolbar flat class="table-toolbar">
          <v-toolbar-title class="v-toolbar_title">Hotel Cleanings</v-toolbar-title>
          <v-text-field
            v-model="search"
            label="Search"
            variant="outlined"
            hide-details
            single-line
          ></v-text-field>
          <v-btn class="add-btn" color="green" @click="router.push('/cleanings/add')">
            Add Cleaning
          </v-btn>
        </v-toolbar>
      </template>

      <template v-slot:item.actions="{ item }">
        <div class="d-flex align-center justify-center action-buttons">
          <v-btn variant="text" color="blue" @click="router.push('/cleanings/' + item.id)">
            Edit
          </v-btn>
          <v-btn variant="text" color="red" @click="deleteCleaning(item.id)">
            Delete
          </v-btn>
        </div>
      </template>
    </v-data-table>
  </div>
</template>

<style scoped>
.v-toolbar_title {
  font-weight: bold !important;
}

.table-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 50px;
  width: 1000px;
}

.styled-table {
  max-width: 1000px;
  min-height: 600px;
  border-radius: 8px;
  overflow: hidden;
}

.table-toolbar {
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
  padding: 10px 16px;
}

.add-btn {
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
}

.action-buttons v-btn {
  margin: 0 8px;
  text-transform: uppercase;
  font-size: 12px;
  font-weight: bold;
}
</style>
