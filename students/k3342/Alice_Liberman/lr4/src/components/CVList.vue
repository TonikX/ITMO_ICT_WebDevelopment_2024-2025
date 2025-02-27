<script setup>
import {computed} from "vue";

const props = defineProps(['cv'])
const formattedCV = computed(() => {
  const content = props.cv.content_blob || "";
  return content.replace(/\\n/g, "<br>");
});
</script>

<template>
<div class="card mb-3">
  <div class="card-body">
    <h5 class="card-title">CV {{props.cv.id}}</h5>
    <p class="card-text">{{formattedCV}}</p>
    <router-link :to="`cvs/${props.cv.id}/edit`" class="btn btn-primary">Edit</router-link>
    <router-link :to="`cvs/${props.cv.id}/delete`" class="btn btn-danger">Delete</router-link>
  </div>
</div>
</template>

<style scoped>
</style>