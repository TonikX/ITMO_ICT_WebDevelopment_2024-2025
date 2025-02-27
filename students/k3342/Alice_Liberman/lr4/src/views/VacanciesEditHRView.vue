<template>
  <div class="card shadow-sm p-4">
    <!-- Show loading spinner if data is still being fetched -->
    <div v-if="dLoading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Form to edit vacancy -->
    <div v-else>
      <h5 class="card-title">Edit Vacancy</h5>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axiosInstance from "@/services/axios.js";
import { useRoute } from "vue-router";

const route = useRoute();
const vacancyID = route.params.vacancyID;

const initialData = ref(null);
const dErrors = ref(null);
const dLoading = ref(true);

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
    await axiosInstance.patch(`vacancies/${vacancyID}/edit/`, updatedData);
    alert("Vacancy updated successfully!");
  } catch (error) {
    console.error("Error updating vacancy:", error);
    alert("Failed to update the vacancy.");
  }
};

onMounted(async () => {
  try {
    const response = await axiosInstance.get(`vacancies/${vacancyID}`);
    if (response.status === 200) {
      initialData.value = response.data.vacancy;

      formData.value = {
        title: initialData.value.title,
        salary: initialData.value.salary,
        description: initialData.value.description,
      };
      tagsInput.value = initialData.value.tags ? initialData.value.tags.join(", ") : "";
      skillsInput.value = initialData.value.skills ? initialData.value.skills.join(", ") : "";

      dLoading.value = false;
    } else {
      dErrors.value = true;
    }
  } catch (error) {
    console.error("Error fetching vacancy:", error);
    dErrors.value = true;
    dLoading.value = false;
  }
});
</script>

<style scoped>
.card {
  border-radius: 8px;
}
</style>
