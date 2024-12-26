<script setup>
import {ref} from 'vue'
import axiosClient from '@/services/axiosClient'

const emit = defineEmits(['update:modelValue', 'printinghouse-created'])

const formData = ref({
  name: '',
  address: '',
  is_active: true
})

function closeDialog() {
  emit('update:modelValue', false)
}

async function handleCreate() {
  try {
    await axiosClient.post('/printinghouses/create/', formData.value)
    emit('printinghouse-created')
    closeDialog()
  } catch (error) {
    console.error('Ошибка создания типографии:', error)
  }
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeDialog" max-width="600">
    <v-card>
      <v-card-title>Добавить типографию</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleCreate">
          <v-text-field
            v-model="formData.name" label="Название" required
          ></v-text-field>
          <v-text-field
            v-model="formData.address" label="Адрес" required
          ></v-text-field>
          <v-switch
            v-model="formData.is_active" label="Типография активна? (Нет/Да)"
          ></v-switch>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="handleCreate">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
