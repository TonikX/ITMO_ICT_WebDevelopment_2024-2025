<script setup>
import {computed, onMounted, reactive, ref} from "vue";

import {useRoute} from "vue-router";
import axiosInstance from "@/services/axios.js";
import router from "@/router/index.js";

const rentId = useRoute().params.rentId;
const data = ref(null)

const isEditing = ref(false);
const message = ref("");

const isCommenting = ref(false);
const comment = reactive({
  description: '',
  rating: null
})
const commentWas = ref(false)

onMounted(async () => {
  let response = await axiosInstance.get(`tenant/${rentId}/`)
  data.value = response.data
  response = await axiosInstance.get(`tenant/${rentId}/review/`)
  comment.description = response.data.description
  comment.rating = response.data.rating
  comment.rating = response.data.rating
  commentWas.value = !response.data.rating === null
})


const isValidRating = computed(() => comment.rating >= 1 && comment.rating <= 10);
const submitComment = () => {
  console.log(comment)
  if (isValidRating.value && comment.description !== '' && comment.rating !== null) {
    console.log('comment in progress')
    if (commentWas.value) {
      console.log('comment in patch')
      axiosInstance.patch(`tenant/${rentId}/review/`, comment)
    } else {
      console.log('comment in post')
      axiosInstance.post(`tenant/${rentId}/review/`, comment)
    }
  }
  console.log("Comment submitted:", comment);
};


const saveChanges = async () => {
  try {
    const response = await axiosInstance.patch(`tenant/${rentId}/`, {
      dt_start: data.dt_start,
      dt_end: data.dt_end,
    });
    Object.assign(data, response.data);
    isEditing.value = false;
    message.value = "Changes saved successfully.";
  } catch (error) {
    message.value = "Failed to save changes.";
  }
};

const deleteLease = async () => {
  if (confirm("Are you sure you want to delete this lease?")) {
    try {
      await axiosInstance.delete(`tenant/${rentId}/`);
      message.value = "Lease deleted successfully.";
      await router.push('/tenant/history')
    } catch (error) {
      message.value = "Failed to delete lease.";
    }
  }
};

const showCommentForm = () => {
  isCommenting.value = !isCommenting.value;
}
</script>

<template>
  <div class="container mt-4">
    <div class="card" v-if="data">
      <div class="card-body">
        <!-- Property Address -->
        <h5 class="card-title">{{ data.rent_unit.address }}</h5>

        <!-- Cost and Period -->
        <p class="card-text">
          <strong>Cost:</strong> ${{ data.rent_unit.cost }} / {{ data.rent_unit.per_period }}
        </p>

        <!-- Area -->
        <p class="card-text">
          <strong>Area:</strong> {{ data.rent_unit.area_sq_m }} sq.m
        </p>

        <!-- Lease Dates -->
        <div v-if="!isEditing">
          <p class="card-text">
            <strong>Lease Period:</strong> {{ new Date(data.dt_start).toLocaleDateString() }}
            to {{ new Date(data.dt_end).toLocaleDateString() }}
          </p>
          <button class="btn btn-secondary me-2" @click="isEditing = true">
            Edit Dates
          </button>
        </div>

        <div v-else>
          <div class="mb-2">
            <label for="dtStart" class="form-label">Start Date:</label>
            <input
                type="date"
                id="dtStart"
                class="form-control"
                v-model="data.dt_start"
            />
          </div>
          <div class="mb-3">
            <label for="dtEnd" class="form-label">End Date:</label>
            <input
                type="date"
                id="dtEnd"
                class="form-control"
                v-model="data.dt_end"
            />
          </div>
          <button class="btn btn-primary me-2" @click="saveChanges">Save</button>
          <button class="btn btn-secondary" @click="isEditing = false">
            Cancel
          </button>
        </div>

        <!-- Confirmation Status -->
        <p class="card-text mt-3">
          <strong>Status:</strong>
          <span
              class="badge"
              :class="data.confirmed ? 'bg-success' : 'bg-warning text-dark'"
          >
            {{ data.confirmed ? "Confirmed" : "Pending" }}
          </span>
        </p>

        <div class="row">
          <button class="btn btn-danger mt-3 col" @click="deleteLease" v-if="!data.confirmed">Delete Lease</button>
          <button class="btn btn-outline-info mt-3 col" @click="showCommentForm" v-if="data.confirmed">Comment lease
          </button>
        </div>
      </div>
    </div>

    <!-- Message -->
    <div v-if="message" class="alert mt-3" :class="message.includes('success') ? 'alert-success' : 'alert-danger'">
      {{ message }}
    </div>

    <div v-if="isCommenting">
      <h5>Leave/edit your Comment</h5>
      <form @submit.prevent="submitComment" class="p-3 border rounded shadow-sm">
        <!-- Comment Description -->
        <div class="mb-3">
          <label for="description" class="form-label">Comment</label>
          <textarea
              id="description"
              class="form-control"
              v-model="comment.description"
              placeholder="Write your comment here..."
              rows="3"
              required
          ></textarea>
        </div>

        <!-- Rating -->
        <div class="mb-3">
          <label for="rating" class="form-label">Rating (1-10)</label>
          <input
              type="number"
              id="rating"
              class="form-control"
              v-model="comment.rating"
              :class="{'is-invalid': !isValidRating}"
              placeholder="Enter a rating between 1 and 10"
              required
          />
          <div class="invalid-feedback">
            Please enter a valid rating between 1 and 10.
          </div>
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-primary" :disabled="!isValidRating">
          Submit
        </button>
        <button type="button" class="btn btn-secondary ms-2" @click="cancelComment">
          Cancel
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.card {
  max-width: 600px;
  margin: 0 auto;
}
</style>
