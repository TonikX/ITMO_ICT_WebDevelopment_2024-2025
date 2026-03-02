<template>
  <v-container>
    <v-snackbar v-model="snackbar.show" :timeout="2000" location="bottom right">
      {{ snackbar.text }}
    </v-snackbar>

    <h2 class="mb-4">Задачи</h2>

    <!-- Создание задачи + создание тега -->
    <v-card class="pa-4 mb-6">
      <v-text-field v-model="title" label="Название" />
      <v-textarea v-model="description" label="Описание" />

      <v-select
        v-model="status"
        :items="['todo','in_progress','done']"
        label="Статус"
        class="mt-2"
      />

      <v-select
        v-model="category"
        :items="categories"
        item-title="title"
        item-value="id"
        label="Категория"
        class="mt-2"
      />

      <v-select
        v-model="selectedTags"
        :items="tags"
        item-title="name"
        item-value="id"
        label="Теги"
        multiple
        chips
        closable-chips
        class="mt-2"
      />

      <v-btn color="primary" class="mt-4" @click="create" :loading="creating">
        Создать задачу
      </v-btn>

      <v-divider class="my-5" />

      <v-text-field v-model="newTagName" label="Новый тег" />
      <v-btn variant="outlined" class="mt-2" @click="addTag" :loading="tagCreating">
        Добавить тег
      </v-btn>
    </v-card>

    <!-- Список задач -->
    <v-card>
      <v-list>
        <v-list-item v-for="t in tasks" :key="t.id">
          <v-list-item-title>
            [{{ t.id }}] {{ t.title }}
          </v-list-item-title>

          <v-list-item-subtitle>
            Категория: {{ categoryTitle(t.category) }}
          </v-list-item-subtitle>

          <v-list-item-subtitle v-if="t.tags && t.tags.length">
            Теги: {{ tagsTitleList(t.tags) }}
          </v-list-item-subtitle>

          <div class="d-flex align-center ga-3 mt-3">
            <v-select
              :model-value="t.status"
              :items="['todo','in_progress','done']"
              density="compact"
              variant="outlined"
              hide-details
              style="max-width: 220px"
              @update:model-value="(val) => changeStatus(t.id, val)"
            />

            <v-btn
              variant="text"
              color="error"
              @click="removeTask(t.id)"
              :loading="deletingId === t.id"
            >
              Удалить
            </v-btn>
          </div>
        </v-list-item>

        <v-list-item v-if="!tasks.length">
          <v-list-item-title>Задач пока нет</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getTasks, createTask, updateTask, deleteTask } from "../api/tasks";
import { getCategories } from "../api/categories";
import { getTags, createTag } from "../api/tags";

const tasks = ref([]);
const categories = ref([]);
const tags = ref([]);

const title = ref("");
const description = ref("");
const status = ref("todo");
const category = ref(null);
const selectedTags = ref([]);

const newTagName = ref("");

const snackbar = ref({ show: false, text: "" });

const creating = ref(false);
const tagCreating = ref(false);
const deletingId = ref(null);

function notify(text) {
  snackbar.value.text = text;
  snackbar.value.show = true;
}

async function loadAll() {
  const [c, tg, t] = await Promise.all([getCategories(), getTags(), getTasks()]);
  categories.value = c.data;
  tags.value = tg.data;
  tasks.value = t.data;
}

function categoryTitle(id) {
  const c = categories.value.find((x) => x.id === id);
  return c ? c.title : String(id);
}

function tagsTitleList(tagIds) {
  const list = tagIds
    .map((id) => tags.value.find((x) => x.id === id)?.name)
    .filter(Boolean);

  return list.length ? list.join(", ") : tagIds.join(", ");
}

async function addTag() {
  const name = newTagName.value.trim();
  if (!name) return notify("Введите имя тега");

  tagCreating.value = true;
  try {
    await createTag({ name });
    newTagName.value = "";
    await loadAll();
    notify("Тег создан");
  } catch (e) {
    notify("Не удалось создать тег (возможно, уже существует)");
  } finally {
    tagCreating.value = false;
  }
}

async function create() {
  if (!title.value.trim()) return notify("Введите название");
  if (!category.value) return notify("Выберите категорию");

  creating.value = true;
  try {
    await createTask({
      title: title.value.trim(),
      description: description.value,
      status: status.value,
      category: category.value,
      tags: selectedTags.value,
    });

    title.value = "";
    description.value = "";
    status.value = "todo";
    category.value = null;
    selectedTags.value = [];

    await loadAll();
    notify("Задача создана");
  } catch (e) {
    notify("Не удалось создать задачу");
  } finally {
    creating.value = false;
  }
}

async function changeStatus(taskId, newStatus) {
  try {
    await updateTask(taskId, { status: newStatus });
    await loadAll();
    notify("Статус обновлён");
  } catch (e) {
    notify("Не удалось обновить статус");
  }
}

async function removeTask(taskId) {
  deletingId.value = taskId;
  try {
    await deleteTask(taskId);
    await loadAll();
    notify("Задача удалена");
  } catch (e) {
    notify("Не удалось удалить задачу");
  } finally {
    deletingId.value = null;
  }
}

onMounted(loadAll);
</script>
