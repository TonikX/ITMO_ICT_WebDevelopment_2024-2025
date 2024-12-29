<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const form = ref({
  employee: "",
  floor_num: "",
  week_day: ""
})

const defaultForm = {employee: null, floor_num: null, week_day: null}
const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const employee_select = ref([])

function createForm() {
  instance.get('hotel/employees/').then(response => {
      if (response.status === 200) {
        employee_select.value = response.data
      }
    }
  ).catch(error => console.log(error))
  form.value = defaultForm
}

function createCleaning() {
  instance.post('/hotel/cleanings/', form.value)
    .then(response => {
        if (response.status === 201) {
          router.push('/cleanings')
        }
      }
    ).catch(error => console.log(error))
}

const getCustomEmployeeTitle = (employee) => {
  return `${employee.first_name} ${employee.last_name}`;
};

onMounted(() => {
  createForm()
})

</script>

<template>
  <div class="container">
    <div class="form-container">
      <h1>Create Hotel Booking</h1>
      <v-select label="Employee" :items="employee_select"
                :item-title="getCustomEmployeeTitle" item-value="id"
                v-model="form.employee"></v-select>
      <v-select label="Weekday" :items="weekDays" v-model="form.week_day"></v-select>

      <v-radio-group
        v-model="form.floor_num"
        inline
        label="Floor Number"
      >
        <v-radio label="0" value="0"></v-radio>
        <v-radio label="1" value="1"></v-radio>
        <v-radio label="2" value="2"></v-radio>
        <v-radio label="3" value="3"></v-radio>
        <v-radio label="4" value="4"></v-radio>

      </v-radio-group>

      <v-btn @click="createCleaning" color="green">Create</v-btn>
    </div>
  </div>
</template>

<style scoped>

</style>
