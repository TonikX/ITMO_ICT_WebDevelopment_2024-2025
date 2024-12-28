<script setup>
import {ref} from "vue";


const props = defineProps(["recipeInfo"])
const recipeInfo = ref(props.recipeInfo)
</script>

<template>
  <div class="row">
    <h1>{{ recipeInfo.header }}</h1>
    <div class="position-relative" style="width: 100%; height: 350px; overflow: hidden">
      <img :src="recipeInfo.thumbnail_link" :alt="recipeInfo.header"
              style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px"></div>
  </div>
</template>

<style scoped>

</style>