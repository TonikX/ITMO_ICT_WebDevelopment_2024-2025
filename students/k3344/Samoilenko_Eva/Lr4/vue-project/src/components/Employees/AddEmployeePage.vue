<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const form = ref({
  first_name: "",
  last_name: "",
  father_name: "",
})

const hotel = 1

function createEmployee() {
  form.value.hotel = hotel
  instance.post('/hotel/employees/', form.value)
    .then(response => {
        if (response.status === 201) {
          router.push('/employees')
        }
      }
    ).catch(error => console.log(error))
}
</script>

<template>
  <div class="container">
    <div class="form-container">
      <h1>Create Hotel Employee</h1>
      <v-text-field label="First Name" v-model="form.first_name"></v-text-field>
      <v-text-field label="Last Name" v-model="form.last_name"></v-text-field>
      <v-text-field label="Father/Middle Name" v-model="form.father_name"></v-text-field>
      <v-btn @click="createEmployee" color="green">Create</v-btn>
    </div>
  </div>
</template>

<style scoped>

</style>
