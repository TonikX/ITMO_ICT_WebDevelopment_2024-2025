<template>
  <div class="container" v-if="data">
    <h1>Landlord number {{ data.id }}: <strong>{{ data.username }}</strong></h1>

    <div class="row">
      <FlatCard v-for="unit in data.rent_units" :unit="unit" class="col-4"/>
    </div>
    <hr>
    <div class="row">
      <CommentCard :review="review" v-for="review in data.reviews" class="col-4"/>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import FlatCard from "@/components/FlatCard.vue";
import {useRoute} from "vue-router";
import CommentCard from "@/components/CommentCard.vue";

const pathId = useRoute().params.landId;
const data = ref()

onMounted(async () => {
  const response = await axiosInstance.get(`landlord/${pathId}/`)
  if (pathId === 'me') {
    data.value =
    {
      id: 0,
      username: 'You',
      rent_units: response.data
    }
  } else {
    data.value = response.data
  }
})
</script>