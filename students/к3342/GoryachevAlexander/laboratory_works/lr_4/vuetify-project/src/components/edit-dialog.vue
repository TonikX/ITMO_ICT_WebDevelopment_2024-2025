<template>
  <v-dialog v-model="internalDialog" max-width="600px">
    <v-card>
      <v-card-title>Редактирование статьи</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="internalPost.title"
          label="Заголовок"
          outlined
        ></v-text-field>

        <v-textarea
          v-model="internalPost.content"
          label="Содержание"
          outlined
        ></v-textarea>

        <!-- Добавление поля для image_url -->
        <v-text-field
          v-model="internalPost.image_url"
          label="Изображение (URL)"
          outlined
        ></v-text-field>

        <!-- Добавление поля для category -->
        <v-text-field
          v-model="internalPost.category"
          label="Категория"
          outlined
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red-lighten-3" text @click="cancel">Отмена</v-btn>
        <v-btn color="indigo-lighten-3" text @click="save">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { watch, ref } from "vue";

// Props
const props = defineProps({
  modelValue: Boolean,
  post: Object,
});

// Emits
const emit = defineEmits(["update:modelValue", "save-post", "cancel-edit"]);

// Локальное состояние
const internalDialog = ref(props.modelValue);
const internalPost = ref({ ...props.post });

// Синхронизация modelValue
watch(
  () => props.modelValue,
  (newValue) => {
    internalDialog.value = newValue;
  }
);

watch(
  () => internalDialog.value,
  (newValue) => {
    emit("update:modelValue", newValue);
  }
);

// Обновление локального поста при изменении входного post
watch(
  () => props.post,
  (newValue) => {
    internalPost.value = { ...newValue };
  }
);

// Действия
const cancel = () => {
  emit("cancel-edit");
  internalDialog.value = false;
};

const save = () => {
  emit("save-post", { ...internalPost.value });
  internalDialog.value = false;
};
</script>
