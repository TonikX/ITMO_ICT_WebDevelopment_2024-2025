<template>
  <div class="card shadow-sm p-4">
    <h5 class="card-title">Create Vacancy</h5>
    <form @submit.prevent="handleSubmit">
      <!-- Title -->
      <div class="mb-3">
        <label for="title" class="form-label">Title</label>
        <input
            type="text"
            id="title"
            v-model="formData.title"
            class="form-control"
            required
        />
      </div>

      <!-- Tags -->
      <div class="mb-3">
        <label for="tags" class="form-label">Tags (comma-separated)</label>
        <input
            type="text"
            id="tags"
            v-model="tagsInput"
            class="form-control"
            placeholder="Enter tags separated by commas"
        />
      </div>

      <!-- Skills -->
      <div class="mb-3">
        <label for="skills" class="form-label">Skills (comma-separated)</label>
        <input
            type="text"
            id="skills"
            v-model="skillsInput"
            class="form-control"
            placeholder="Enter skills separated by commas"
        />
      </div>

      <!-- Salary -->
      <div class="mb-3">
        <label for="salary" class="form-label">Salary</label>
        <input
            type="number"
            id="salary"
            v-model.number="formData.salary"
            class="form-control"
            min="0"
            required
        />
      </div>

      <!-- Description -->
      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
            id="description"
            v-model="formData.description"
            class="form-control"
            rows="4"
            required
        ></textarea>
      </div>

      <!-- Submit Button -->
      <div class="text-end">
        <button type="submit" class="btn btn-success">Save Changes</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import {ref} from "vue";
import axiosInstance from "@/services/axios.js";
import router from "@/router/index.js";

const formData = ref({
  title: "",
  salary: 0,
  description: "",
});

const tagsInput = ref("");
const skillsInput = ref("");

const handleSubmit = async () => {
  const updatedData = {
    ...formData.value,
    tags: tagsInput.value.split(",").map((tag) => tag.trim()).filter(Boolean),
    skills: skillsInput.value.split(",").map((skill) => skill.trim()).filter(Boolean),
  };

  try {
    await axiosInstance.post(`vacancies/`, updatedData);
    alert("Vacancy created successfully!");
    router.push({path: '/vacancies', replace: true});
  } catch (error) {
    console.error("Error creating vacancy:", error);
    alert("Failed to create the vacancy.");
  }
};

</script>

<style scoped>
.card {
  border-radius: 8px;
}
</style>
