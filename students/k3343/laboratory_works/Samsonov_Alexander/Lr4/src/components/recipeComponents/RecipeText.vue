<script setup>
import {ref} from "vue";

const props = defineProps(["recipeInfo"])
const recipeInfo = ref(props.recipeInfo)
</script>

<template>
  <p v-html="recipeInfo.content_json.text" style="white-space: pre-line;"/>
</template>

<style scoped>

</style>