<script setup>
import axiosClient from '@/services/axiosClient'

const props = defineProps({
  modelValue: Boolean,
  editionId: Number,
})

const emit = defineEmits(['update:modelValue', 'deleted'])

function closeDialog() {
  emit('update:modelValue', false)
}

async function handleDelete() {
  if (!props.editionId) return
  try {
    await axiosClient.delete(`/editions/delete/${props.editionId}/`)
    emit('deleted')
    closeDialog()
  } catch (error) {
    console.error('Ошибка удаления тиража:', error)
  }
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeDialog" max-width="400">
    <v-card>
      <v-card-title>Удалить тираж?</v-card-title>
      <v-card-actions>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="error" @click="handleDelete">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
