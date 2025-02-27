<template>
  <div class="card shadow-sm my-4">
    <div class="card-header bg-success text-white">
      <h5 class="mb-0">Job Application #{{ props.application.id }}</h5>
    </div>
    <div class="card-body row">
      <div class="col">
        <div class="mb-3">
          <h6 class="card-subtitle text-muted">Applicant Information</h6>
          <ul class="list-unstyled mb-0">
            <li><strong>Username:</strong> {{ props.application.applicant.username }}</li>
            <li><strong>Email:</strong> {{ props.application.applicant.email || "N/A" }}</li>
          </ul>
        </div>

        <div class="mb-3">
          <h6><strong>Message:</strong></h6>
          <p class="card-text" style="white-space: pre;">{{ props.application.message }}</p>
        </div>

        <div class="mb-3">
          <h6><strong>CV Content:</strong></h6>
          <p class="bg-light p-2 rounded border" v-html="formattedCV"></p>
        </div>
      </div>
      <div class="col">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed} from "vue";

const props = defineProps(["application"]);

const formattedCV = computed(() => {
  const content = props.application.CV.content_blob || "";
  return content.replace(/\\n/g, "<br>");
});
</script>

<style scoped>
p {
  white-space: pre-wrap;
}
</style>
