<template>
  <v-item-group selected-class="bg-primary" v-if="post">
    <v-container>
      <v-btn
        icon
        @click="goBack"
        class="mb-4"
      >
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>

      <v-card-subtitle class="text-overline text-h6 my-1">
        {{ formatDate(post.created_at) }}
      </v-card-subtitle>
      <v-card-title class="my-6 text-h4 font-weight-black">
        {{ post.title }}
      </v-card-title>

      <v-card-actions v-if="post.author.id == user.id">
        <v-btn
          color="indigo-lighten-3"
          text="Редактировать"
          @click="openEditDialog"
        >
          Редактировать
        </v-btn>
        <v-btn color="red-lighten-3" text="Удалить" @click="openDeleteDialog">
          Удалить
        </v-btn>
      </v-card-actions>

      <v-card-text class="text-overline text-h6 pb-0">
        Категория: {{ post.category }}
      </v-card-text>
      <v-card-text v-if="author" class="text-overline text-h6 pt-0">
        Автор: {{ author }}
      </v-card-text>
      <v-img
        v-if="post.image_url"
        height="400px"
        :src="post.image_url"
        class="mb-3"
        rounded="xl"
        cover
      ></v-img>
      <v-card-text v-html="post.content"></v-card-text>
    </v-container>

    <EditDialog
      v-model:modelValue="editDialog"
      :post="selectedPost"
      @save-post="handleSaveEdit"
      @cancel-edit="closeEditDialog"
    />
    <DeleteDialog
      v-model:modelValue="deleteDialog"
      @confirm-delete="handleConfirmDelete"
      @cancel-delete="closeDeleteDialog"
    />
  </v-item-group>
</template>

<script setup>
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import { useAppStore } from "@/stores/app";
import { onMounted, ref, computed } from "vue";

import EditDialog from "@/components/edit-dialog.vue";
import DeleteDialog from "@/components/delete-dialog.vue";

const route = useRoute();
const router = useRouter();
const store = useAppStore();

const postId = route.params.id;

const post = ref(null);
const user = computed(() => JSON.parse(store.user));
const author = computed(() =>
  user.id == post?.author?.id ? "Вы" : post.author.username
);

const editDialog = ref(false);
const deleteDialog = ref(false);

const editedPost = ref({
  title: "",
  content: "",
});

const formatDate = (date) => {
  const d = new Date(date);
  return d.toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
};

const openEditDialog = () => {
  editedPost.value.title = post.value.title;
  editedPost.value.content = post.value.content;
  editDialog.value = true;
};
const closeEditDialog = () => (editDialog.value = false);

const openDeleteDialog = () => (deleteDialog.value = true);
const closeDeleteDialog = () => (deleteDialog.value = false);

const handleSaveEdit = async (updatedPost) => {
  await store.updatePost(postId, updatedPost);
  post.value = await store.fetchPost(postId);
  closeEditDialog();
};

const handleConfirmDelete = async () => {
  await store.deletePost(postId);
  closeDeleteDialog();
  router.push("/blogs/all");
};

const goBack = () => {
  router.go(-1); // Возвращает на предыдущую страницу
};

onMounted(async () => {
  post.value = await store.fetchPost(postId);
});
</script>
