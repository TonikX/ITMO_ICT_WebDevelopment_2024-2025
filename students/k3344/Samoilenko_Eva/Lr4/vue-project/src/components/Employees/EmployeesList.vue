<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const employees = ref([])

function getEmployees() {
  instance.get('/hotel/employees/').then(
    response => {
      if (response.status === 200) {
        employees.value = response.data
      }
    }
  ).catch(error => console.log(error))
}

function deleteEmployee(id) {
  if (confirm("Are you sure you want to fire this employee?")) {
    instance.delete(`/hotel/employees/${id}/`).then(response => {
        if (response.status === 204) {
          getEmployees()
        }
      }
    ).catch(error => console.log(error))
  } else {
    console.log("Employee deletion cancelled.")
  }
}

onMounted(() => {
  getEmployees()
})
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <div align="center">
      <h1>Hotel Employees</h1>
      <div class="button-group">
        <v-btn
          class="styled-btn"
          color="green"
          block
          @click="router.push('/employees/add')"
        >
          ADD
        </v-btn>
      </div>
    </div>
    <div v-if="employees.length === 0">Loading employees...</div>
    <v-container class="card-container" min-width="1000">
      <template v-for="employee in employees" :key="employee.id">
        <v-card class="card">
          <v-card-title>
            Employee {{ employee.first_name }} {{ employee.last_name }}
          </v-card-title>
          <v-card-item v-if="employee.father_name">
            Father/Middle Name: {{ employee.father_name }}
          </v-card-item>
          <v-card-item>
            <p style="color: green">Is currently employed</p>
          </v-card-item>
          <v-card-actions>
            <v-btn color="blue" @click="router.push('/employees/' + employee.id)">
              Edit
            </v-btn>
            <v-btn color="red" @click="deleteEmployee(employee.id)">
              Fire
            </v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-container>
  </div>
</template>

<style scoped>
h1{
 margin-top: 0;
 font-weight: bold;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.styled-btn {
  width: 50px; /* Adjust width */
  height: 50px; /* Adjust height */
  font-size: 15px;
  font-weight: bold;
  border-radius: 8px;
  text-transform: uppercase;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* Adjust columns */
  gap: 20px;
  margin-top: 20px;
  width: 100%; /* Ensure cards span the available space */
  justify-items: center; /* Center items in their grid cells */
}

.card {
  max-width: 400px; /* Ensure consistent card width */
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
