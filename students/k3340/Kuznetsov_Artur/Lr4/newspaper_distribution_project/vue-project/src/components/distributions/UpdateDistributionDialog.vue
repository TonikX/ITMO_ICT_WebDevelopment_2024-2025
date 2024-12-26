<script setup>
import {ref, watch} from 'vue'
import axiosClient from '@/services/axiosClient'

const props = defineProps({
  modelValue: Boolean,
  distributionData: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'updated'])

const localOpen = ref(props.modelValue)
const formData = ref({})

watch(
  () => props.distributionData,
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
    await axiosClient.put(`/distributions/update/${pk}/`, formData.value)
    emit('updated')
    closeDialog()
  } catch (error) {
    console.error('Ошибка обновления поставки:', error)
  }
}
</script>

<template>
  <v-dialog v-model="localOpen" max-width="600" @update:model-value="closeDialog">
    <v-card>
      <v-card-title>Изменить поставку</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleUpdate">
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
        <v-btn color="primary" @click="handleUpdate">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
