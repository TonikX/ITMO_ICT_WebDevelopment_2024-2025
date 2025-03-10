<template>
  <v-dialog v-model="internalDialog" max-width="400px">
    <v-card>
      <v-card-title class="headline">
        Вы уверены, что хотите удалить эту статью?
      </v-card-title>
      <v-card-actions>
        <v-btn color="red-lighten-3" text @click="cancel">Отмена</v-btn>
        <v-btn color="indigo-lighten-3" text @click="confirm">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { watch, ref } from "vue";

// Props
const props = defineProps({
  modelValue: Boolean,
});

// Emits
const emit = defineEmits(["update:modelValue", "confirm-delete", "cancel-delete"]);

// Локальное состояние
const internalDialog = ref(props.modelValue);

// Обновляем локальное состояние при изменении props
watch(
  () => props.modelValue,
  (newValue) => {
    internalDialog.value = newValue;
  }
);

// Сохраняем изменения в родительском компоненте
watch(
  () => internalDialog.value,
  (newValue) => {
    emit("update:modelValue", newValue);
  }
);

// Действия
const cancel = () => {
  emit("cancel-delete");
  internalDialog.value = false;
};

const confirm = () => {
  emit("confirm-delete");
  internalDialog.value = false;
};
</script>
