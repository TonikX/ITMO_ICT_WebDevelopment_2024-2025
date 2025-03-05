<script setup lang="ts">
import { defineProps } from "vue";
import { useRouter } from "vue-router";

const props = defineProps<{ recipeId: number; canEdit: boolean }>();
const router = useRouter();

const navigateToEdit = () => {
  router.push(`/recipes/${props.recipeId}/edit`);
};

const navigateToDelete = () => {
  router.push(`/recipes/${props.recipeId}/delete`);
};
</script>

<template>
  <div v-if="canEdit" class="d-flex gap-2 mt-3">
    <button class="btn btn-warning" @click="navigateToEdit">✏️ Edit</button>
    <button class="btn btn-danger" @click="navigateToDelete">🗑️ Delete</button>
  </div>
</template>

<style scoped>
button {
  min-width: 100px;
}
</style>
