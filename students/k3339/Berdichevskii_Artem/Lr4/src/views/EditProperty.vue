<script setup>
import {onMounted, reactive, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import {useRoute} from "vue-router";

const rentId = useRoute().params.landId;

const formData = reactive({
  description: "",
  address: "",
  area_sq_m: null,
  cost: null,
});

const message = ref("");
const isSubmitting = ref(false);

const EditInstance = async () => {
  try {
    isSubmitting.value = true;
    message.value = "";

    await axiosInstance.patch(`/properties/${rentId}/`, formData);

    message.value = "Property edited successfully.";
    alert(message.value);
  } catch (error) {
    message.value = "Failed to edit instance. Please try again.";
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(async () => {
  const response = (await axiosInstance.get(`/properties/${rentId}/`)).data;
  formData.description = response.description
  formData.address = response.address
  formData.per_period = response.per_period
  formData.area_sq_m = response.area_sq_m
  formData.cost = response.cost
})
</script>

<template>
  <div class="container mt-4">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Edut property</h5>
        <form @submit.prevent="EditInstance" class="needs-validation" novalidate>
          <div class="mb-3">
            <label for="address" class="form-label">Address</label>
            <input
                type="text"
                id="address"
                class="form-control"
                v-model="formData.address"
                placeholder="Enter address"
                required
            />
          </div>

          <div class="mb-3">
            <label for="address" class="form-label">Per period</label>
            <select
                id="per_period"
                class="form-control"
                v-model="formData.per_period"
                required
            >
              <option value="st">day</option>
              <option value="lt">month</option>
            </select>
          </div>

          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea
                id="description"
                class="form-control"
                v-model="formData.description"
                placeholder="Enter description"
                required
            ></textarea>
          </div>
          <div class="mb-3">
            <label for="area" class="form-label">Area (sq.m)</label>
            <input
                type="number"
                id="area"
                class="form-control"
                v-model="formData.area_sq_m"
                placeholder="Enter area in square meters"
                required
                min="1"
            />
          </div>

          <div class="mb-3">
            <label for="cost" class="form-label">Cost</label>
            <input
                type="number"
                id="cost"
                class="form-control"
                v-model="formData.cost"
                placeholder="Enter cost"
                required
                min="1"
            />
          </div>

          <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
            {{ isSubmitting ? "Submitting..." : "Edit" }}
          </button>
        </form>

        <div v-if="message" class="alert mt-3" :class="message.includes('success') ? 'alert-success' : 'alert-danger'">
          {{ message }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
