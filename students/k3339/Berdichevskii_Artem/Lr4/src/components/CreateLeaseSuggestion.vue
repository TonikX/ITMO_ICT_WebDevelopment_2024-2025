<script setup>
import {ref} from 'vue';
import axiosInstance from "@/services/axios.js";

const dateFrom = ref('');
const dateTo = ref('');
const message = ref('');

const status = ref(null)

const props = defineProps(['id'])
const pathId = props.id


const bookProperty = async () => {
  try {
    const response = await axiosInstance.post(`/properties/${pathId}/book/`, {
      dt_start: dateFrom.value,
      dt_end: dateTo.value,
    });
    message.value = response.data
    status.value = true
  } catch (error) {
    message.value = error
    status.value = false
  }
};
</script>

<template>
  <div class="container mt-4">
    <h5>Book Property</h5>
    <form @submit.prevent="bookProperty" class="row g-3">
      <div class="col-md-6">
        <label for="dateFrom" class="form-label">From:</label>
        <input
            type="date"
            id="dateFrom"
            class="form-control"
            v-model="dateFrom"
            required
        />
      </div>

      <div class="col-md-6">
        <label for="dateTo" class="form-label">To:</label>
        <input
            type="date"
            id="dateTo"
            class="form-control"
            v-model="dateTo"
            required
        />
      </div>

      <div class="col-12">
        <button type="submit" class="btn btn-primary">Book</button>
      </div>
    </form>
    <div v-if="message" class="mt-3 alert" :class="status ? 'alert-success' : 'alert-danger'">
      <p v-if="status">
        Booking creates successfully.
      </p>
      <p v-else>
        Booking failed: {{ message.response.data.detail }}
      </p>
    </div>
  </div>
</template>
