<script setup>
import { ref } from "vue";
import axiosInstance from "@/services/axios.js";
import {useRoute} from "vue-router";
import router from "@/router/index.js";

const rentId = useRoute().params.landId;

defineProps({
  instanceId: {
    type: Number,
    required: true,
  },
});

const isConfirming = ref(false);
const message = ref("");

const deleteInstance = async () => {
  try {
    message.value = "";
    await axiosInstance.delete(`/properties/${rentId}/`);
    message.value = "Instance successfully deleted.";
    alert(message.value);
    router.push({path: '/landlord/me', force: true});
  } catch (error) {
    message.value = "Failed to delete the instance. Please try again.";
  } finally {
    isConfirming.value = false;
  }
};
</script>

<template>
  <div>
    <button class="btn btn-danger" @click="isConfirming = true">
      Delete Instance
    </button>

    <div v-if="isConfirming" class="modal d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Deletion</h5>
            <button
              type="button"
              class="btn-close"
              aria-label="Close"
              @click="isConfirming = false"
            ></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this instance? This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="isConfirming = false">
              Cancel
            </button>
            <button class="btn btn-danger" @click="deleteInstance">
              Confirm Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="message" class="alert mt-3" :class="message.includes('success') ? 'alert-success' : 'alert-danger'">
      {{ message }}
    </div>
  </div>
</template>

<style scoped>
.modal.d-block {
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
