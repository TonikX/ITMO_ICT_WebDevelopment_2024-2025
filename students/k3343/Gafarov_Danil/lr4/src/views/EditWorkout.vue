<script setup>
import {onMounted, reactive, ref} from "vue";
import {useRoute} from "vue-router";
import router from "@/router/index.js";
import axiosInstance from "@/services/axios.js";
import {isAuthenticated} from "@/composables/tokenActions.js";
import {fetchWithLoading} from "@/composables/serverActions.js";


const workoutPath = useRoute().params.workoutId;
const workoutData = ref(null)
const wLoading = ref(true);
const wError = ref(null);

onMounted(async () => {
  if (! isAuthenticated.value || !(await axiosInstance.get(`workouts/${workoutPath}/canEdit/`)).data) {
    router.push('/');
  }
  await fetchWithLoading(`workouts/${workoutPath}`, workoutData, wLoading, wError);
  fetchData()
})

const form = reactive({
  tags: [],
  steps: [],
  time_takes: 0,
  title: '',
  description: '',
  video_link: '',
});

const newTag = ref('');

const addTag = () => {
  if (newTag.value.trim()) {
    form.tags.push(newTag.value.trim());
    newTag.value = '';
  }
};

const removeTag = (index) => {
  form.tags.splice(index, 1);
};

const addStep = () => {
  form.steps.push('');
};

const removeStep = (index) => {
  form.steps.splice(index, 1);
};

const submitForm = async () => {
  try {
    const response = await axiosInstance.patch(`/workouts/${workoutPath}/`, { ...form });
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};

async function fetchData() {
  form.description = workoutData.value.description;
  form.video_link = workoutData.value.video_link;
  form.time_takes = workoutData.value.time_takes;
  form.title = workoutData.value.title;
  form.steps = workoutData.value.steps_display;
  form.tags = workoutData.value.tags_display;
}
</script>
<template>
  <div class="container my-5">
    <h2 class="mb-4">Edit Resource</h2>

    <form @submit.prevent="submitForm">
      <!-- Title -->
      <div class="mb-3">
        <label for="title" class="form-label">Title</label>
        <input
          type="text"
          id="title"
          class="form-control"
          v-model="form.title"
          placeholder="Enter the title"
          required
        />
      </div>

      <!-- Description -->
      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          id="description"
          class="form-control"
          v-model="form.description"
          rows="3"
          placeholder="Enter a description"
        ></textarea>
      </div>

      <!-- Video Link -->
      <div class="mb-3">
        <label for="video_link" class="form-label">Video Link</label>
        <input
          type="url"
          id="video_link"
          class="form-control"
          v-model="form.video_link"
          placeholder="Enter the video link"
        />
      </div>

      <!-- Time Takes -->
      <div class="mb-3">
        <label for="time_takes" class="form-label">Time Takes (minutes)</label>
        <input
          type="number"
          id="time_takes"
          class="form-control"
          v-model.number="form.time_takes"
          placeholder="Enter the time in minutes"
        />
      </div>

      <!-- Tags -->
      <div class="mb-3">
        <label for="tags" class="form-label">Tags</label>
        <input
          type="text"
          id="tags"
          class="form-control"
          v-model="newTag"
          placeholder="Add a tag and press Enter"
          @keyup.enter="addTag"
        />
        <div class="mt-2">
          <span
            v-for="(tag, index) in form.tags"
            :key="index"
            class="badge bg-primary me-2"
          >
            {{ tag }}
            <i class="bi bi-x-circle ms-1" @click="removeTag(index)"></i>
          </span>
        </div>
      </div>

      <!-- Steps -->
      <div class="mb-3">
        <label for="steps" class="form-label">Steps</label>
        <div v-for="(step, index) in form.steps" :key="index" class="input-group mb-2">
          <input
            type="text"
            class="form-control"
            v-model="form.steps[index]"
          />
          <button
            type="button"
            class="btn btn-danger"
            @click="removeStep(index)"
          >
            Remove
          </button>
        </div>
        <button
          type="button"
          class="btn btn-secondary"
          @click="addStep"
        >
          Add Step
        </button>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary">Save Changes</button>
    </form>
  </div>
</template>


<style scoped>
.badge {
  cursor: pointer;
}

.badge .bi-x-circle {
  cursor: pointer;
}
</style>
