<template>
  <div>
    <div v-if="isHR">
      <div class="container">
        <section class="bg-dark text-white text-center py-5">
          <div class="container">
            <h1 class="display-4">Welcome, HR from {{company}}</h1>
            <p class="lead">Manage top talent and streamline your hiring process.</p>
            <router-link to="/vacancies" class="btn btn-primary btn-lg mt-3">View Candidates</router-link>
          </div>
        </section>
      </div>
    </div>
    <div v-else>
      <section class="bg-primary text-white text-center py-5">
        <div class="container">
          <h1 class="display-4">Welcome to JobHunter</h1>
          <p class="lead">Find your dream job with ease and confidence.</p>
          <router-link to="/vacancies" class="btn btn-light btn-lg mt-3">Start Exploring Jobs</router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import {company, isHR} from "../stores/globalState.js";
</script>
