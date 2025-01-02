<script setup>
import {ref, watch} from "vue";


const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  startDate: {
    type: String,
    required: true,
  },
  endDate: {
    type: String,
    required: true
  },
  mode: {
    type: String,
    default: "add",
  },

});

const emits = defineEmits(["update:modelValue", "submit-date"]);

const formData = ref({
  fact_start_date: props.startDate,
  fact_end_date: props.endDate
});

watch(
    () => [props.startDate, props.endDate],
    ([newStartDate, newEndDate]) => {
      formData.value = {
        fact_start_date: newStartDate,
        fact_end_date: newEndDate,
      };
    }
);


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  console.log(formData.value)
  emits("submit-date", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>Изменить фактические даты</v-card-title>
      <v-card-text>
        <v-text-field
            label="Фактическое начало"
            v-model="formData.fact_start_date"
            type="date"
        ></v-text-field>
        <v-text-field
            label="Фактическое завершение"
            v-model="formData.fact_end_date"
            type="date"
        ></v-text-field>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
        <v-btn @click="closeModal">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
