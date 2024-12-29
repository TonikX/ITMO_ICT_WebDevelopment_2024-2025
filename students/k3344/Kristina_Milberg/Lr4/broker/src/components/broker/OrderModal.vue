<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  batch: {
    type: Object,
  }
});

const emits = defineEmits(["update:modelValue", "edit-batch"]);
console.log(props.batch)
const formData = ref({...props.batch});

watch(
    () => props.batch,
    (newVal) => {
      formData.value = {...newVal};
    },
    {immediate: true, deep: true}
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("edit-batch", {
    id: formData.value.id,
    quantity: Number(formData.value.quantity),
    price_per_unit: formData.value.pricePerUnit
  });
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" max-width="500">
    <v-card>
      <v-card-title>Изменить количество или цену</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.quantity" label="Количество" type="number" required></v-text-field>
          <v-text-field v-model="formData.pricePerUnit" label="Цена за единицу" type="number" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
