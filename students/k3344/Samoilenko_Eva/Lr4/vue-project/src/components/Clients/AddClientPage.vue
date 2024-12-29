<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const form = ref({
  first_name: "",
  last_name: "",
  father_name: "",
  passport_number: "",
  origin_city: ""
})

function createClient(){
  instance.post('/hotel/clients/', form.value)
    .then(response => {
        if (response.status === 201){
          router.push('/clients')
        }
      }
  ).catch(error => console.log(error))
}
</script>

<template>
  <div class="container">
  <form class="form-container" >
    <h1>Create Hotel Client</h1>
    <v-text-field label="First Name" v-model="form.first_name"></v-text-field>
    <v-text-field label="Last Name" v-model="form.last_name"></v-text-field>
    <v-text-field label="Father/Middle Name" v-model="form.father_name"></v-text-field>
    <v-text-field label="Passport Number" v-model="form.passport_number"></v-text-field>
    <v-text-field label="Origin City" v-model="form.origin_city"></v-text-field>
    <v-btn @click="createClient" color="green">Create</v-btn>
  </form>
    </div>
</template>

<style>
.container {
  display: flex;
  justify-content: center;  /* Center horizontally */
  align-items: center;      /* Center vertically */
  min-height: 100vh;         /* Make sure the container takes full viewport height */
}

.form-container {
  position: absolute;
  width: 100%;               /* Optional: Set width of your form */
  max-width: 500px;          /* Optional: Set maximum width of your form */
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
}
</style>
