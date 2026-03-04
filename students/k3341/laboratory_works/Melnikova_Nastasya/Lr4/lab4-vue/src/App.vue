<template>
  <v-app>
    <v-app-bar class="appbar" flat density="comfortable">
      <v-container class="d-flex align-center py-0">
        <div class="brand d-flex align-center">
          <v-icon class="mr-2" icon="mdi-hotel" />
          <span class="text-h6 font-weight-bold">Hotel Admin</span>
        </div>

        <v-spacer />

        <!-- NAV -->
        <v-btn-toggle class="navToggle" divided mandatory>
          <v-btn to="/" exact>Home</v-btn>
          <v-btn to="/rooms">Rooms</v-btn>
          <v-btn to="/stays">Bookings</v-btn>
        </v-btn-toggle>

        <v-spacer />

        <template v-if="!auth.isAuthenticated">
          <v-btn class="pill" variant="elevated" color="white" to="/login">
            Login
          </v-btn>
        </template>

        <template v-else>
          <v-chip class="mr-3" variant="tonal" color="white">
            {{ auth.user?.username || "user" }}
          </v-chip>

          <v-btn class="pill mr-2" variant="elevated" color="white" to="/profile">
            Profile
          </v-btn>

          <v-btn class="pill" variant="elevated" color="white" @click="onLogout">
            Logout
          </v-btn>
        </template>
      </v-container>
    </v-app-bar>

    <v-main class="page">
      <v-container class="py-8">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "./stores/auth";

const router = useRouter();
const auth = useAuthStore();

async function onLogout() {
  await auth.logout();
  router.push("/login");
}
</script>

<style scoped>
.appbar {
  background: linear-gradient(90deg, #ff8c00, #ffa726);
  color: white;
}
.brand { letter-spacing: 0.2px; }
.page { background: #f6f7fb; }
.pill { border-radius: 999px; }
.navToggle :deep(.v-btn) {
  border-radius: 999px !important;
}
</style>






