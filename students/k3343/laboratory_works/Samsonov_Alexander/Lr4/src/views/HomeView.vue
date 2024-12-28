<script async setup>

import BigCard from "@/components/genericInterface/BigCard.vue";
import axiosInstance from "@/services/axios.js";
import {onMounted, ref} from "vue";
import Carousel from "@/components/genericInterface/Carousel.vue";


const recipeData = ref(null)
const collection = ref(null)

const fetchRecipe = async (id) => {
  return await (await axiosInstance.get(`recipes/${id}`)).data;
}

const fetchLists = async () => {
  return await (await axiosInstance.get(`/lists`)).data;
}

onMounted(async () => {
  recipeData.value = await fetchRecipe(1);
  collection.value = await fetchLists();
})
</script>
<template>


  <BigCard v-if="recipeData" :recipe="recipeData"/>
  <hr>

  <div v-for="item in collection" class="my-3">
    <Carousel v-if="collection" :carouselData="item" :key="item.id"/>
  </div>


</template>

