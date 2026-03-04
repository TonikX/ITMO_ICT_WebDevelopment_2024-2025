<template>
  <v-container class="d-flex justify-center">
    <v-card class="pa-6" style="max-width: 720px; width: 100%;">
      <h2 class="mb-6">Profile</h2>

      <v-alert v-if="loading" type="info" variant="tonal" class="mb-4">
        Loading user...
      </v-alert>

      <div v-if="auth.user">
        <div class="mb-6">
          <b>Current username:</b> {{ auth.user.username }}
        </div>

        <h3 class="mb-2">Update username</h3>
        <v-text-field v-model="newUsername" label="New username" />

        <v-btn
          color="primary"
          class="mb-8"
          @click="updateUsername"
          :loading="savingUser"
        >
          Save username
        </v-btn>

        <h3 class="mb-2">Change password</h3>

        <v-text-field
          v-model="currentPassword"
          label="Current password"
          type="password"
        />

        <v-text-field
          v-model="newPassword"
          label="New password"
          type="password"
        />

        <v-btn color="primary" @click="changePassword" :loading="savingPass">
          Change password
        </v-btn>
      </div>

      <v-alert v-if="msg" type="success" class="mt-4" variant="tonal">
        {{ msg }}
      </v-alert>

      <v-alert v-if="err" type="error" class="mt-4" variant="tonal">
        {{ err }}
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();

const loading = ref(false);
const savingUser = ref(false);
const savingPass = ref(false);

const newUsername = ref("");

const currentPassword = ref("");
const newPassword = ref("");

const msg = ref("");
const err = ref("");

onMounted(async () => {
  msg.value = "";
  err.value = "";
  loading.value = true;

  try {
    await auth.fetchUser();
    newUsername.value = auth.user?.username || "";
  } catch (e) {
    err.value = "Не удалось загрузить пользователя";
  } finally {
    loading.value = false;
  }
});

async function updateUsername() {
  msg.value = "";
  err.value = "";
  savingUser.value = true;

  try {
    await auth.updateUser({ username: newUsername.value });
    msg.value = "Username updated";
  } catch (e) {
    const data = e?.response?.data;
    err.value =
      (data && (data.username?.[0] || data.detail)) ||
      "Не получилось обновить username";
  } finally {
    savingUser.value = false;
  }
}

async function changePassword() {
  msg.value = "";
  err.value = "";

  if (!currentPassword.value || !newPassword.value) {
    err.value = "Введите текущий и новый пароль";
    return;
  }

  savingPass.value = true;

  try {
    // важно: Djoser требует current_password + new_password
    await auth.changePassword(currentPassword.value, newPassword.value);

    msg.value = "Пароль успешно изменён";
    currentPassword.value = "";
    newPassword.value = "";
  } catch (e) {
    const data = e?.response?.data;

    err.value =
      (data && (data.current_password?.[0] || data.new_password?.[0] || data.detail)) ||
      "Не удалось сменить пароль";
  } finally {
    savingPass.value = false;
  }
}
</script>

<style>
</style>