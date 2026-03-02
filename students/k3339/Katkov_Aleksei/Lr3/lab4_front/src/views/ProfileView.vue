<template>
  <v-container style="max-width: 700px">
    <v-snackbar v-model="snackbar.show" :timeout="2000" location="bottom right">
      {{ snackbar.text }}
    </v-snackbar>

    <v-card class="pa-4">
      <h2 class="mb-4">Профиль</h2>

      <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

      <div v-if="user">
        <div class="mb-4">
          <div>id: {{ user.id }}</div>
          <div>username: {{ user.username }}</div>
          <div v-if="user.email !== undefined">email: {{ user.email || "-" }}</div>
        </div>

        <v-text-field v-model="form.username" label="Новый username" />
        <v-text-field
          v-if="user.email !== undefined"
          v-model="form.email"
          label="Новый email"
        />

        <div class="d-flex ga-3 mt-3">
          <v-btn color="primary" @click="save" :loading="saving">
            Сохранить
          </v-btn>
        </div>
      </div>

      <div v-else>
        <div v-if="loading">Загрузка...</div>
        <div v-else>Не удалось загрузить профиль</div>
      </div>
    </v-card>
  </v-container>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { http } from "../api/http";

const user = ref(null);
const error = ref("");
const loading = ref(false);
const saving = ref(false);

const snackbar = ref({ show: false, text: "" });

const form = reactive({
  username: "",
  email: "",
});

function notify(text) {
  snackbar.value.text = text;
  snackbar.value.show = true;
}

function fillFormFromUser(u) {
  form.username = u?.username || "";
  form.email = u?.email || "";
}

async function load() {
  error.value = "";
  loading.value = true;
  try {
    const res = await http.get("/auth/users/me/");
    user.value = res.data;
    fillFormFromUser(res.data);
  } catch (e) {
    error.value = "Не удалось получить данные пользователя (токен/сервер).";
  } finally {
    loading.value = false;
  }
}

async function save() {
  if (!user.value) return;

  const payload = {};
  const newUsername = form.username.trim();

  if (newUsername && newUsername !== user.value.username) payload.username = newUsername;

  if (user.value.email !== undefined) {
    const newEmail = form.email.trim();
    if (newEmail !== (user.value.email || "")) payload.email = newEmail;
  }

  if (Object.keys(payload).length === 0) return notify("Нечего сохранять");

  error.value = "";
  saving.value = true;
  try {
    const res = await http.patch("/auth/users/me/", payload);
    user.value = res.data;
    fillFormFromUser(res.data);
    notify("Данные профиля сохранены");
  } catch (e) {
    const data = e?.response?.data;

    if (typeof data === "string") {
      error.value = data;
    } else if (data && typeof data === "object") {
      const msg = Object.entries(data)
        .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(", ") : String(v)}`)
        .join(" | ");
      error.value = msg || "Не удалось сохранить изменения.";
    } else {
      error.value = "Не удалось сохранить изменения.";
    }
  } finally {
    saving.value = false;
  }
}

onMounted(load);
</script>
