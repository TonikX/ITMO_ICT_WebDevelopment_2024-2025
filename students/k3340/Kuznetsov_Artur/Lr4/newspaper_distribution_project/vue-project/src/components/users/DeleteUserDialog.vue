<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
});
const emits = defineEmits(["update:modelValue", "confirm-delete"]);

function closeModal() {
  emits("update:modelValue", false);
}

function confirmDelete() {
  emits("confirm-delete");
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="400">
    <v-card>
      <v-card-title>Удалить пользователя?</v-card-title>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Оставить</v-btn>
        <v-btn color="error" @click="confirmDelete">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
