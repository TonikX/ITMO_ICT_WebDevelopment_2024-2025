<template>
  <div class="card shadow-sm my-4">
    <div class="card-header bg-primary text-white">
      <h5 class="mb-0">{{ vacancy.title }}</h5>
    </div>
    <div class="card-body">
      <h6 class="card-subtitle text-muted mb-2">{{ vacancy.company }}</h6>
      <div class="mb-3">
        <span class="badge bg-info me-1" v-for="tag in vacancy.tags" :key="tag">{{ tag }}</span>
      </div>
      <div class="mb-3">
        <strong>Skills:</strong>
        <ul class="list-inline mb-0">
          <li class="list-inline-item" v-for="skill in vacancy.skills" :key="skill">
            <span class="badge bg-secondary">{{ skill }}</span>
          </li>
        </ul>
      </div>
      <div class="mb-3">
        <strong>Salary:</strong> ${{ vacancy.salary }}
      </div>
      <p class="card-text">
        <strong>Description: </strong>{{ vacancy.description }}</p>
    </div>
    <div class="card-footer text-end" v-if="isHR">
      <div class="d-flex justify-content-end">
        <router-link :to="`/hr/vacancies/${vacancy.id}/edit`" class="btn btn-primary btn-sm me-2">Edit</router-link>

        <router-link :to="`/hr/vacancies/${vacancy.id}/delete`" class="btn btn-danger btn-sm">Delete</router-link>
      </div>
    </div>
    <div v-else>
      <router-link :to="`/vacancies/${vacancy.id}/apply`" class="btn btn-outline-primary btn-sm">Apply Now</router-link>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import {isHR} from "@/stores/globalState.js";

const props = defineProps(["vacancy"]);
const vacancy = ref(props.vacancy);
</script>

<style scoped>
.card {
  border-radius: 8px;
}

.card-header {
  font-weight: bold;
}
</style>
