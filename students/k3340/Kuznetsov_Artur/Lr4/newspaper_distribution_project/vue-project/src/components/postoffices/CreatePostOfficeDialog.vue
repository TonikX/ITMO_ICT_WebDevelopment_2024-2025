<script setup>
import {ref} from 'vue'
import axiosClient from '@/services/axiosClient'

const emit = defineEmits(['update:modelValue', 'post-office-created'])

const formData = ref({
  number: '',
  address: ''
})

function closeDialog() {
  emit('update:modelValue', false)
}

async function handleCreate() {
  try {
    await axiosClient.post('/postoffices/create/', formData.value)
    emit('post-office-created')
    closeDialog()
  } catch (error) {
    console.error('Ошибка создания почтового отделения:', error)
  }
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeDialog" max-width="600">
    <v-card>
      <v-card-title>Добавить почтовое отделение</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleCreate">
          <v-text-field
            v-model="formData.number" label="Номер" type="number" required
          ></v-text-field>
          <v-text-field
            v-model="formData.address" label="Адрес" required
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="handleCreate">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
