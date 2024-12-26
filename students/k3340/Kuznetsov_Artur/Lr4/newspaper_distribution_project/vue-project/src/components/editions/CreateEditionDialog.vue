<script setup>
import {ref} from 'vue'
import axiosClient from '@/services/axiosClient'

const emit = defineEmits(['update:modelValue', 'edition-created'])

const formData = ref({
  printing_house: null,
  newspaper: null,
  quantity: 0,
})

function closeDialog() {
  emit('update:modelValue', false)
}

async function handleCreate() {
  try {
    await axiosClient.post('/editions/create/', formData.value)
    emit('edition-created')
    closeDialog()
  } catch (error) {
    console.error('Ошибка создания тиража:', error)
  }
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeDialog" max-width="600">
    <v-card>
      <v-card-title>Добавить тираж</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleCreate">
          <v-text-field
            v-model="formData.printing_house" label="ID типографии" type="number" required
          ></v-text-field>
          <v-text-field
            v-model="formData.newspaper" label="ID газеты" type="number" required
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
