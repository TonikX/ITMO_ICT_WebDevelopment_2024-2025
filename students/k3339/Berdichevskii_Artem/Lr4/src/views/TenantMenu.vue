<template>
  <h1>🔥 Hot properties in your area are waiting for you! 🏠✨ Don’t miss out on the perfect place—browse now and find your
    dream home today!</h1>
  <div class="row">
    <FlatCard v-for="data in properties" :unit="data" class="col-4"/>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import FlatCard from "@/components/FlatCard.vue";

const properties = ref(null)

onMounted(async () => {
  const presponse = await axiosInstance.get('properties/')
  if (presponse.status === 200) {
    properties.value = presponse.data
  }
})
</script>