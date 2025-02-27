<template xmlns="http://www.w3.org/1999/html">
  <div class="container">
    <h1 class="mb-4">Job Listings {{isHR ? `at ${company}`: ''}}</h1>
    <h2>found {{ response.count }} vacancies</h2>

    <div class="row">
      <JobListCard :job="vacancy" v-for="vacancy in response.results" v-if="response" class="col-4 my-2"/>
      <p v-else>Loading</p>
    </div>
    <div v-if="isHR">
      <router-link to="hr/vacancies/create" class="btn btn-primary">Create new vacancy</router-link>
    </div>
  </div>
  <nav aria-label="Page navigation">
    <ul class="pagination justify-content-center">

      <li class="page-item" :class="{ disabled: !pagination.previous }">
        <button
            class="page-link"
            :disabled="!pagination.previous"
            @click="navigate(pageNumber-=1)"
        >
          Previous
        </button>
      </li>
      <li class="page-item page-link">
        {{ pageNumber }}
      </li>

      <li class="page-item" :class="{ disabled: !pagination.next }">
        <button
            class="page-link"
            :disabled="!pagination.next"
            @click="navigate(pageNumber+=1)"
        >
          Next
        </button>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import JobListCard from "@/components/JobListCard.vue";
import {company, isHR} from "../stores/globalState.js";

const response = ref('')
const pageNumber = ref(1);
const pagination = ref({count: 0, next: null, previous: null});

async function navigate(pageNumber) {
  response.value = (await axiosInstance.get(`/vacancies?page=${pageNumber}`)).data
  pagination.value = {
    count: response.value.count,
    next: response.value.next,
    previous: response.value.previous,
  };
}

onMounted(async () => {
  response.value = (await axiosInstance.get("/vacancies")).data
  pagination.value = {
    count: response.value.count,
    next: response.value.next,
    previous: response.value.previous,
  };
})
</script>