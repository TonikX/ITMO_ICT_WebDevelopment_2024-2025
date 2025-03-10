<template>
  <div class="container mt-4">
    <h1>User Details</h1>
    <hr />

    <div v-if="user" class="card">
      <div class="card-body">
        <h2 class="card-title">{{ user.username }}</h2>
        <p class="card-text">
          <strong>Email:</strong> {{ user.email || "Not provided" }}<br />
          <strong>First Name:</strong> {{ user.first_name || "Not provided" }}<br />
          <strong>Last Name:</strong> {{ user.last_name || "Not provided" }}<br />
          <strong>Role:</strong> {{ user.is_superuser ? "Admin" : "User" }}
        </p>
      </div>
    </div>

    <div v-else class="alert alert-info">
      {{ loading ? "Loading user details..." : "Failed to load user details." }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { UserInfo } from "@/composables/AccountActions.ts";
import api from "@/services/axios.ts";

const route = useRoute();
const user = ref<UserInfo | null>(null);
const loading = ref(true);

onMounted(async () => {
  try {
    const response = await api.get<UserInfo>(`/fitness/current-user/`);
    user.value = response.data;
  } catch (error) {
    console.error("Failed to fetch user details:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.card {
  max-width: 600px;
  margin: 0 auto;
}
</style>