<script setup>
import {ref, watch} from 'vue'
import axiosClient from '@/services/axiosClient'

const props = defineProps({
  modelValue: Boolean,
  editionData: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update:modelValue', 'updated'])

const formData = ref({})

watch(
  () => props.editionData,
  (newVal) => {
    formData.value = {...newVal}
  },
  {immediate: true}
)

function closeDialog() {
  emit('update:modelValue', false)
}

async function handleUpdate() {
  const pk = formData.value.id
  try {
    await axiosClient.put(`/editions/update/${pk}/`, {
      printing_house: formData.value.printing_house,
      newspaper: formData.value.newspaper,
      quantity: formData.value.quantity,
    })
    emit('updated')
    closeDialog()
  } catch (error) {
    console.error('Ошибка обновления тиража:', error)
  }
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeDialog" max-width="600">
    <v-card>
      <v-card-title>Изменить тираж</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleUpdate">
          <v-text-field
            v-model="formData.printing_house"
            label="ID типографии"
            type="number"
            required
          ></v-text-field>
          <v-text-field
            v-model="formData.newspaper"
            label="ID газеты"
            type="number"
            required
          ></v-text-field>
          <v-text-field
            v-model="formData.quantity"
            label="Количество"
            type="number"
            required
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="handleUpdate">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
