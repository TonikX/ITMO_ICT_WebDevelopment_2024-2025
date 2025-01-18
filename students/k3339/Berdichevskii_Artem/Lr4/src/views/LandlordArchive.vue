<template>
  <h1>Incoming requests</h1>
  <button class="btn btn-outline-info" @click="toggle=!toggle">See {{ toggle ? 'Pending' : 'Confirmed' }}</button>
  <div v-if="applicantsConfirmed" class="row">
    <LeaseCard :leaseData="leaseData" v-for="leaseData in applicantsConfirmed" class="col-6" v-if="toggle"/>
    <LeaseCard :leaseData="leaseData" v-for="leaseData in applicantsPending" class="col-6" v-else>
      <div class="col">
        <button class="btn btn-success btn-sm" @click="confirmLease(leaseData.id)">Confirm</button>
      </div>
    </LeaseCard>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import LeaseCard from "@/components/LeaseCard.vue";

const applicantsConfirmed = ref()
const applicantsPending = ref()
const toggle = ref(false)

const fetchData = async () => {
  applicantsConfirmed.value = (await axiosInstance.get("/landlord/me/archive")).data
  applicantsPending.value = (await axiosInstance.get("/landlord/me/bookings")).data
}

onMounted(fetchData)

async function confirmLease(leaseId) {
  const response = await axiosInstance.put(`/landlord/me/bookings/${leaseId}/`, {confirmed: true})
  if (response.status === 200) {
    alert('Successfully confirmed')
    fetchData()
  }
}
</script>