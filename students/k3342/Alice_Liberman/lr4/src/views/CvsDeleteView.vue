<template>
  <!-- Delete Confirmation Modal -->
  <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h5 class="modal-title" id="deleteModalLabel">Confirm Deletion</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <!-- Modal Body -->
        <div class="modal-body">
          <p>Are you sure you want to delete this vacancy? This action cannot be undone.</p>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-danger" @click="handleDelete">Delete</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Trigger Button for Modal -->
  <div class="container">
    <button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal">Delete CV</button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axiosInstance from "@/services/axios.js";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const cvID = route.params.cvID;

const dLoading = ref(false);

const handleDelete = async () => {
  dLoading.value = true;

  try {
    const response = await axiosInstance.delete(`/cvs/${cvID}/`);
    if (response.status === 204) {
      alert("CV deleted successfully!");
      router.push("/");
    }
  } catch (error) {
    console.error("Error deleting CV:", error);
    alert("Failed to delete the CV.");
  } finally {
    dLoading.value = false;
  }
};
</script>
<style>

.modal-content {
  border-radius: 8px;
}

.modal-header {
  background-color: #f8d7da;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
}
</style>
