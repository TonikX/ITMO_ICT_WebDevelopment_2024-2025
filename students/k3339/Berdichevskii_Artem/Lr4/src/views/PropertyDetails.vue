<template>
  <div class="container mt-4" v-if="!PLoading">
    <div class="card">
      <div class="card-header">
        <h5>Property Details</h5>
      </div>
      <div class="card-body">
        <router-link class="none" :to="`/landlord/${PropertyData.owner.id}`"><p><strong>Owner:</strong> {{ PropertyData.owner.username }}</p></router-link>

        <p><strong>Description:</strong> {{ PropertyData.description }}</p>

        <p><strong>Address:</strong> {{ PropertyData.address }}</p>

        <p><strong>Area (sq.m):</strong> {{ PropertyData.area_sq_m }}</p>

        <p><strong>Cost:</strong> ${{ PropertyData.cost }}/{{ PropertyData.per_period }}</p>
        <p>
          <strong>Created At:</strong>
          {{ new Date(PropertyData.created_at).toLocaleString() }}
        </p>
      </div>
    </div>
  </div>
  <div v-if="!DLoading" class="row">
    <h6>Available Dates</h6>
    <div class="d-flex flex-wrap gap-2 col-8">
      <span v-for="date in DatesData" :key="date" class="badge bg-primary">
        {{ new Date(date).toLocaleDateString() }}
      </span>
    </div>
    <form class="col-4" @submit.prevent="getDates">
      <div class="col-auto">
        <label for="dateFrom" class="form-label">From:</label>
        <input type="date" id="dateFrom" class="form-control" v-model="dateFrom" required/>
      </div>

      <div class="col-auto">
        <label for="dateTo" class="form-label">To:</label>
        <input type="date" id="dateTo" class="form-control" v-model="dateTo" required/>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
  <CreateLeaseSuggestion :id="pathId" v-if="IsAuthenticated"/>
  <router-link to="/tenant/history" class="btn btn-primary my-3" v-if="IsAuthenticated">Check your active booking here</router-link>

</template>

<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import {useRoute} from "vue-router";
import CreateLeaseSuggestion from "@/components/CreateLeaseSuggestion.vue";
import {IsAuthenticated} from "@/composables/token.js";

const pathId = useRoute().params.propId;

const PropertyData = ref(null);
const PLoading = ref(true);

const DatesData = ref(null);
const DLoading = ref(true);

const dateFrom = ref(new Date());
const dateTo = ref(new Date());

async function getDates() {
  const response = await axiosInstance.get(`properties/${pathId}/free_dates/?start_date=${dateFrom.value}&end_date=${dateTo.value}`)
  DatesData.value = response.data
  DLoading.value = false
}

onMounted(async () => {
  let response = await axiosInstance.get(`properties/${pathId}/`)
  PropertyData.value = response.data
  PLoading.value = false
  response = await axiosInstance.get(`properties/${pathId}/free_dates/`)
  DatesData.value = response.data
  DLoading.value = false
})
</script>
<style>
.none {
  text-decoration: none;
}
</style>