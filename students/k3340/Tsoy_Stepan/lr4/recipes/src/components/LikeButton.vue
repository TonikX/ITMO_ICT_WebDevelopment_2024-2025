<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import api from "@/services/AxiosService";

const route = useRoute();
const like = ref<boolean>(false);
const error = ref<string | null>(null);

async function fetchStatus() {
  try {
    const recipeId = route.params.id;
    const response = await api.get<boolean>(`recipes/${recipeId}/like`);
    like.value = response.data;
  } catch (e) {
    error.value = "Failed to load like status.";
  }
}

async function toggleLike() {
  try {
    const recipeId = route.params.id;
    await api.post(`recipes/${recipeId}/like/`);
    like.value = !like.value;
  } catch (e) {
    error.value = "Failed to update like status.";
  }
}

const buttonClass = computed(() => ({
  "btn": true,
  "btn-outline-danger": !like.value,
  "btn-danger": like.value,
}));

onMounted(() => {
  fetchStatus();
});
</script>

<template>
  <div>
    <button :class="buttonClass" @click="toggleLike">
      <span v-if="like">❤️ Liked</span>
      <span v-else>🤍 Like</span>
    </button>
    <p v-if="error" class="text-danger mt-2">{{ error }}</p>
  </div>
</template>

<style scoped>
button {
  font-size: 1.2rem;
  padding: 8px 16px;
  border-radius: 8px;
  transition: background 0.2s ease-in-out;
}
</style>
