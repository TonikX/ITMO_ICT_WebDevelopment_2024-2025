<script setup>
import {ref, watch} from 'vue'
import axiosClient from '@/services/axiosClient'

const props = defineProps({
  modelValue: Boolean,
  newspaperData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'updated'])

const localOpen = ref(props.modelValue)
const formData = ref({})

watch(
  () => props.newspaperData,
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
    await axiosClient.put(`/newspapers/update/${pk}/`, {
      name: formData.value.name,
      index: formData.value.index,
      price: formData.value.price,
      editor: formData.value.editor
    })
    emit('updated')
    closeDialog()
  } catch (error) {
    console.error('Ошибка обновления газеты:', error)
  }
}
</script>

<template>
  <v-dialog v-model="localOpen" max-width="600" @update:model-value="closeDialog">
    <v-card>
      <v-card-title>Изменить газету</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleUpdate">
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
        <v-btn color="primary" @click="handleUpdate">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
