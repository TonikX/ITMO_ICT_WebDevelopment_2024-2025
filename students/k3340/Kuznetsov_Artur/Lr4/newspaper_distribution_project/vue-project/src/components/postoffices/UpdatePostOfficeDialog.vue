<script setup>
import {ref, watch} from 'vue'
import axiosClient from '@/services/axiosClient'

const props = defineProps({
  modelValue: Boolean,
  postOfficeData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'updated'])

const localOpen = ref(props.modelValue)
const formData = ref({})

// Синхронизируем данные с пропсами
watch(
  () => props.postOfficeData,
  (newVal) => {
    formData.value = {...newVal}
  },
  {immediate: true}
)

watch(
  () => props.modelValue,
  (val) => {
    localOpen.value = val
  }
)

function closeDialog() {
  emit('update:modelValue', false)
}

async function handleUpdate() {
  try {
    const pk = formData.value.id
    await axiosClient.put(`/postoffices/update/${pk}/`, formData.value)
    emit('updated')
    closeDialog()
  } catch (error) {
    console.error('Ошибка обновления почтового отделения:', error)
  }
}
</script>

<template>
  <v-dialog v-model="localOpen" max-width="600" @update:model-value="closeDialog">
    <v-card>
      <v-card-title>Изменить почтовое отделение</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleUpdate">
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
        <v-btn color="primary" @click="handleUpdate">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
