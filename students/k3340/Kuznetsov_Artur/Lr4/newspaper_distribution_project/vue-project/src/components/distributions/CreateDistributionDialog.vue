<script setup>
import {ref} from 'vue'
import axiosClient from '@/services/axiosClient'

const emit = defineEmits(['update:modelValue', 'distribution-created'])

const formData = ref({
  newspaper: null,
  printing_house: null,
  post_office: null,
  quantity: null
})

function closeDialog() {
  emit('update:modelValue', false)
}

async function handleCreate() {
  try {
    await axiosClient.post('/distributions/create/', formData.value)
    emit('distribution-created')
    closeDialog()
  } catch (error) {
    console.error('Ошибка создания поставки:', error)
  }
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeDialog" max-width="600">
    <v-card>
      <v-card-title>Добавить поставку</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleCreate">
          <v-text-field
            v-model="formData.newspaper" label="ID газеты" type="number" required
          ></v-text-field>
          <v-text-field
            v-model="formData.printing_house" label="ID типографии" type="number" required
          ></v-text-field>
          <v-text-field
            v-model="formData.post_office" label="ID почтового отделения" type="number" required
          ></v-text-field>
          <v-text-field
            v-model="formData.quantity" label="Количество" type="number" required
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
