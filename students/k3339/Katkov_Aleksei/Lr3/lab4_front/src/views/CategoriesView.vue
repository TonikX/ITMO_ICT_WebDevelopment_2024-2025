<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="5">
        <v-card class="pa-4">
          <h2 class="mb-4">Категории</h2>

          <v-text-field v-model="title" label="Title" />
          <v-textarea v-model="description" label="Description" />

          <v-btn block class="mb-4" @click="create" :loading="creating">
            Создать категорию
          </v-btn>

          <v-alert v-if="error" type="error">{{ error }}</v-alert>
        </v-card>
      </v-col>

      <v-col cols="12" md="7">
        <v-card class="pa-4">
          <h3 class="mb-3">Список</h3>

          <v-list>
            <v-list-item v-for="c in categories" :key="c.id">
              <v-list-item-title>[{{ c.id }}] {{ c.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ c.description }}</v-list-item-subtitle>

              <template #append>
                <v-btn icon="mdi-delete" variant="text" @click="remove(c.id)" />
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>

    <v-card class="pa-4 mt-4">
      <h3 class="mb-3">Nested: категории + задачи</h3>
      <v-btn class="mb-3" @click="loadFull" :loading="loadingFull">
        Загрузить /api/categories/full/
      </v-btn>
      <pre style="white-space: pre-wrap">{{ fullJson }}</pre>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  getCategories,
  createCategory,
  deleteCategory,
  getCategoriesFull,
} from "../api/categories";

const categories = ref([]);
const loading = ref(false);
const creating = ref(false);
const error = ref("");

const title = ref("");
const description = ref("");

const loadingFull = ref(false);
const fullJson = ref("");

async function load() {
  error.value = "";
  loading.value = true;
  try {
    const res = await getCategories();
    categories.value = res.data;
  } catch {
    error.value = "Не удалось загрузить категории (сервер/токен).";
  } finally {
    loading.value = false;
  }
}

async function create() {
  error.value = "";
  creating.value = true;
  try {
    await createCategory({ title: title.value, description: description.value });
    title.value = "";
    description.value = "";
    await load();
  } catch {
    error.value = "Не удалось создать категорию.";
  } finally {
    creating.value = false;
  }
}

async function remove(id) {
  await deleteCategory(id);
  await load();
}

async function loadFull() {
  loadingFull.value = true;
  try {
    const res = await getCategoriesFull();
    fullJson.value = JSON.stringify(res.data, null, 2);
  } finally {
    loadingFull.value = false;
  }
}

onMounted(load);
</script>
