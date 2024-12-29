<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const form = ref({
  first_name: "",
  last_name: "",
  father_name: "",
})

function getPage() {
  instance.get(`/hotel/employees/${router.currentRoute.value.params.id}/`)
    .then(response => {
        if (response.status === 200) {
          form.value = response.data
        }
      }
    ).catch(error => console.log(error))
}

function savePage() {
  const {id, ...rest} = form.value
  instance.patch(`/hotel/employees/${router.currentRoute.value.params.id}/`, rest)
    .then(response => {
        if (response.status === 200) {
          router.push('/employees')
        }
      }
    ).catch(error => console.log(error))
}

onMounted(() => {
  getPage()
})

</script>

<template>
  <div v-if="router.currentRoute.value.params.id ==='undefined'">No such employee exists.</div>
  <div v-else class="container">
    <div class="form-container">
      <h1>Hotel Employee</h1>
      <v-text-field label="First Name" v-model="form.first_name"></v-text-field>
      <v-text-field label="Last Name" v-model="form.last_name"></v-text-field>
      <v-text-field label="Father/Middle Name" v-model="form.father_name"></v-text-field>
      <v-btn @click="savePage" color="green">Save</v-btn>
    </div>
  </div>
</template>

<style scoped>

</style>
