<template>
  <div class="container" v-if="data">
    <h1>Welcome back</h1>
    <router-link to="/landlord/archive/" class="btn btn-primary h2">To manage your applications click here</router-link>
    <hr>
    <h2>Your property</h2>
    <router-link to="/landlord/register/" class="btn btn-primary my-2">Register new one</router-link>
    <div class="row">
      <FlatCard v-for="unit in data" :unit="unit" class="col-4"><div class="row">
        <router-link :to="`/landlord/me/${unit.id}/edit`" class="btn btn-outline-warning my-3">Edit</router-link>
        <router-link :to="`/landlord/me/${unit.id}/delete`" class="btn btn-outline-danger">Delete</router-link>
      </div></FlatCard>
    </div>
    <h2 class="my-3">Your reviews</h2>
    <div class="row">
      <CommentCard :review="review" v-for="review in reviews" class="col-4"/>
    </div>
    <hr>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import FlatCard from "@/components/FlatCard.vue";
import CommentCard from "@/components/CommentCard.vue";

const data = ref()
const reviews = ref()

onMounted(async () => {
  data.value =  (await axiosInstance.get(`landlord/me/`)).data
  reviews.value =  (await axiosInstance.get(`landlord/me/reviews`)).data

})
</script>