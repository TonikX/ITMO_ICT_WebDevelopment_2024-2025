<script setup>
import axiosClient from '@/services/axiosClient'
import {ref, watch} from 'vue'

const props = defineProps({
  modelValue: Boolean,
  printingHouseId: Number
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
  if (!props.printingHouseId) return
  try {
    await axiosClient.delete(`/printinghouses/delete/${props.printingHouseId}/`)
    emit('deleted')
    closeDialog()
  } catch (error) {
    console.error('Ошибка удаления типографии:', error)
  }
}
</script>

<template>
  <v-dialog v-model="localOpen" max-width="400" @update:model-value="closeDialog">
    <v-card>
      <v-card-title>Удалить типографию?</v-card-title>
      <v-card-actions>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="error" @click="handleDelete">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
