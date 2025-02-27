<script setup>
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import axiosInstance from "@/services/axios.js";
import router from "@/router/index.js";

const route = useRoute();
const CV_id = route.params.cvID;

const initialData = ref(null);
const dErrors = ref(null);
const dLoading = ref(true);

const formData = ref("");

async function handleSubmit() {
  const response = await axiosInstance.put(`/cvs/${CV_id}/`, {content_blob: formData.value});
  if (response.status === 200) {
    alert('Successfully applied!');
    router.push({path: '/cvs', force: true});
  }
}

onMounted(async () => {
  try {
    const response = await axiosInstance.get(`cvs/${CV_id}`);
    if (response.status === 200) {
      initialData.value = response.data;
      formData.value = response.data.content_blob;
      dLoading.value = false;
    } else {
      dErrors.value = true;
    }
  } catch (error) {
    console.error("Error fetching CV:", error);
    dErrors.value = true;
    dLoading.value = false;
  }
});
</script>

<template>
  <div class="card shadow-sm p-4">
    <div v-if="dLoading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else>
      <h5 class="card-title">Edit Vacancy</h5>
      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="title" class="form-label">Title</label>
          <textarea
            ref="largeTextField"
            v-model="formData"
            rows="10"
            cols="50"
            placeholder="Type something..."
            class="col-7"
        ></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </div>

</template>