<script setup>
import {ref} from "vue";
defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  mountains: {
    type: Array,
    required: true
  }
});
const formData = ref({
  description: "",
  planned_start_date: "",
  planned_end_date: "",
  fact_start_date: null,
  fact_end_date: null,
  mountain: null
});

const emits = defineEmits(["update:modelValue", "submit"]);

function closeModal() {
  emits("update:modelValue", false);
  formData.value = {
    description: "",
    planned_start_date: "",
    planned_end_date: "",
    fact_start_date: null,
    fact_end_date: null,
    mountain: null
  };
}

function handleSubmit() {
  emits("submit", formData.value);
  closeModal();
}


</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>Добавить восхождение</v-card-title>
      <v-card-text>
        <v-select
            :items="mountains"
            label="Выберите вершину"
            item-title="name"
            item-value="id"
            v-model="formData.mountain"
            required
        />
        <v-textarea label="Описание" v-model="formData.description" />
        <v-text-field
            label="Запланированное начало"
            v-model="formData.planned_start_date"
            type="date"
        />
        <v-text-field
            label="Запланированное завершение"
            v-model="formData.planned_end_date"
            type="date"
        />
        <v-text-field
            label="Фактическое начало"
            v-model="formData.fact_start_date"
            type="date"
        />
        <v-text-field
            label="Фактическое завершение"
            v-model="formData.fact_end_date"
            type="date"
        />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="handleSubmit">Добавить</v-btn>
        <v-btn @click="closeModal">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>