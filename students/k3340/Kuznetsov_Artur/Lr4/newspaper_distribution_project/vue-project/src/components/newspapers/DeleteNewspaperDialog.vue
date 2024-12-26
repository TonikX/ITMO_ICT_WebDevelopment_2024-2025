<script setup>
import axiosClient from '@/services/axiosClient'
import {ref, watch} from 'vue'

const props = defineProps({
  modelValue: Boolean,
  newspaperId: Number
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
  if (!props.newspaperId) return
  try {
    await axiosClient.delete(`/newspapers/delete/${props.newspaperId}/`)
    emit('deleted')
    closeDialog()
  } catch (error) {
    console.error('Ошибка удаления газеты:', error)
  }
}
</script>

<template>
  <v-dialog v-model="localOpen" max-width="400" @update:model-value="closeDialog">
    <v-card>
      <v-card-title>Удалить газету?</v-card-title>
      <v-card-actions>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="error" @click="handleDelete">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
