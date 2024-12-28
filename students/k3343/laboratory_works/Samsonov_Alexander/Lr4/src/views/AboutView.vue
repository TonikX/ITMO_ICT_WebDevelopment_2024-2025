<script setup>
import Carousel from "@/components/genericInterface/Carousel.vue";
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";

const collection = ref(null)

const fetchLists = async () => {
  return await (await axiosInstance.get(`/lists/4`)).data;
}


onMounted(async () => {
  collection.value = await fetchLists();
})
</script>


<template>
  <div v-if="collection">
    <carousel :carousel-data="collection" />
  </div>
</template>

<style>
</style>
