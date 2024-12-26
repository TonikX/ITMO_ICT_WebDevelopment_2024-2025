<script setup>
import {ref} from 'vue'
import axiosClient from '@/services/axiosClient'

const emit = defineEmits(['update:modelValue', 'newspaper-created'])

const formData = ref({
  name: '',
  index: '',
  price: '',
  editor: null
})

function closeDialog() {
  emit('update:modelValue', false)
}

async function handleCreate() {
  try {
    await axiosClient.post('/newspapers/create/', formData.value)
    emit('newspaper-created')
    closeDialog()
  } catch (error) {
    console.error('Ошибка создания газеты:', error)
  }
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeDialog" max-width="600">
    <v-card>
      <v-card-title>Добавить газету</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleCreate">
          <v-text-field
            v-model="formData.name" label="Название" required
          ></v-text-field>
          <v-text-field
            v-model="formData.index" label="Индекс" required
          ></v-text-field>
          <v-text-field
            v-model="formData.price" label="Цена" type="number" required
          ></v-text-field>
          <v-text-field
            v-model="formData.editor" label="ID редактора" type="number" required
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

<style scoped>
</style>
