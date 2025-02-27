<template>

  <div class="container">
    <h1>Your applications</h1>
    <div v-if="data">
      <application-card :application="application" v-for="application in data">
        <strong>Job title: </strong>{{ application.vacancy.title }}<br>
        <strong>At </strong>{{ application.vacancy.company }}
        <p>For {{ application.vacancy.salary }}$</p>
        <router-link :to="`/vacancies/${application.vacancy.id}`" class="btn btn-primary">Check the vacancy
        </router-link>
        <hr>
        <router-link :to="`/applications/${application.id}/edit`" class="btn btn-warning">Edit</router-link>
        <router-link :to="`/applications/${application.id}/delete`" class="btn btn-danger">Delete</router-link>
      </application-card>
    </div>
  </div>
</template>


<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import ApplicationCard from "@/components/applicationCard.vue";


const loading = ref(true);
const errors = ref(null);
const data = ref(null);

onMounted(async () => {
  const result = await axiosInstance.get('/applications');

  if (result.status === 200) {
    console.log(result);
    loading.value = false;
    data.value = result.data;
  }
})
</script>