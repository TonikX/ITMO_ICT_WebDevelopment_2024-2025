<script setup>
import {ref, watch} from 'vue'
import axiosClient from '@/services/axiosClient'

const props = defineProps({
  modelValue: Boolean,
  postOfficeId: Number
})

const emit = defineEmits(['update:modelValue', 'deleted'])

const localOpen = ref(props.modelValue)

watch(
  () => props.modelValue,
  (val) => {
    localOpen.value = val
  }
)

function closeDialog() {
  emit('update:modelValue', false)
}

async function handleDelete() {
  if (!props.postOfficeId) return
  try {
    await axiosClient.delete(`/postoffices/delete/${props.postOfficeId}/`)
    emit('deleted')
    closeDialog()
  } catch (error) {
    console.error('Ошибка удаления почтового отделения:', error)
  }
}
</script>

<template>
  <v-dialog v-model="localOpen" max-width="400" @update:model-value="closeDialog">
    <v-card>
      <v-card-title>Удалить почтовое отделение?</v-card-title>
      <v-card-actions>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="error" @click="handleDelete">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
