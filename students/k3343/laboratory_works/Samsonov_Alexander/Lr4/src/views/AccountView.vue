<script setup>
import axiosInstance from "@/services/axios.js";
import {onMounted, ref} from "vue";
import {isAuthenticated} from "@/composables/useAuth.js";
import HorizontalListCard from "@/components/genericInterface/horisontalListCard.vue";

const AccountInfo = ref(null)
const MyRecipes = ref(null)


onMounted(async () => {
  let res = await axiosInstance.get('auth/users/me/')
  AccountInfo.value = await res.data

  res = await axiosInstance.get('recipes/my/')
  MyRecipes.value = await res.data
})
</script>

<template>

  <div v-if="AccountInfo && isAuthenticated" class="container">
    <h1>Hello, {{ AccountInfo.username }}</h1>
    <RouterLink to="recipe/create"><button class="btn btn-primary">Create recipe</button></RouterLink>
    <div v-if="MyRecipes" class="row">
      <h2>Your recipes:</h2>
      <HorizontalListCard :recipe="recipe" v-for="recipe in MyRecipes" class="col-6" />
    </div>
  </div>

</template>

<style scoped>

</style>