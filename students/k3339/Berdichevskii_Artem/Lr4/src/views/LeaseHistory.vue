<template>
  <h1>Lease History</h1>
  <button class="btn btn-outline-info" @click="tab=!tab">See {{tab ? 'Pending' : 'Confirmed'}}</button>
  <div v-if="tab" class="row">
    <h2>Confirmed leases</h2>
      <LeaseCard :leaseData="leaseData" v-for="leaseData in rentsConfirmed" class="col-6"/>
  </div>
  <div v-if="!tab" class="row">
        <h2>Pending leases</h2>

    <LeaseCard :leaseData="leaseData" v-for="leaseData in rentsPending" class="col-6" />
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import LeaseCard from "@/components/LeaseCard.vue";

const rents = ref(null);
const rentsPending = ref([]);
const rentsConfirmed = ref([]);

const tab = ref(true)

onMounted(async () => {
  const response = await axiosInstance.get('tenant/')
  rents.value = response.data.reverse()
  for (let i = 0; i < rents.value.length; i++) {
    rents.value[i].confirmed
        ? rentsConfirmed.value.push(rents.value[i])
        : rentsPending.value.push(rents.value[i]);
  }
})
</script>