<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const form = ref({
  employee: "",
  floor_num: 0,
  week_day: ""
})
const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const employee_select = ref([])
const inline = null

function getPage() {
  instance.get(`/hotel/cleanings/${router.currentRoute.value.params.id}/`)
    .then(response => {
        if (response.status === 200) {
          form.value = response.data
          console.log(form)
        }
      }
    ).catch(error => console.log(error))

  instance.get('hotel/employees/').then(response => {
      if (response.status === 200) {
        employee_select.value = response.data
      }
    }
  ).catch(error => console.log(error))
}

function savePage() {
  instance.patch(`/hotel/cleanings/${router.currentRoute.value.params.id}/`,
    {employee: form.value.employee.id, floor_num: form.value.floor_num, week_day:
      form.value.week_day})
    .then(response => {
        if (response.status === 200) {
          router.push('/cleanings')
        }
      }
    ).catch(error => console.log(error))
}

const getCustomEmployeeTitle = (employee) => {
  return `${employee.first_name} ${employee.last_name}`;
};

onMounted(() => {
  getPage()
})

</script>

<template>
  <div v-if="router.currentRoute.value.params.id === 'undefined'">No such cleaning exists.</div>
  <div v-else class="container">
    <div class="form-container">
      <h1>Hotel Cleaning</h1>
      <v-select label="Employee" :items="employee_select"
                :item-title="getCustomEmployeeTitle" item-value="id"
                v-model="form.employee"></v-select>
      <v-select label="Weekday" :items="weekDays" v-model="form.week_day"></v-select>

      <v-radio-group
        v-model="form.floor_num"
        inline
        label="Floor Number"
      >
        <v-radio label="0" :value="0"></v-radio>
        <v-radio label="1" :value="1"></v-radio>
        <v-radio label="2" :value="2"></v-radio>
        <v-radio label="3" :value="3"></v-radio>
        <v-radio label="4" :value="4"></v-radio>
      </v-radio-group>

      <v-btn @click="savePage" color="green">Save</v-btn>
    </div>
  </div>
</template>

<style scoped>

</style>
