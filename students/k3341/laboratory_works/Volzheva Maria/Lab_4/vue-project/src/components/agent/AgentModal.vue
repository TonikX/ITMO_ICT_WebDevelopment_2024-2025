<script setup>
import {ref, watch} from "vue";
const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  agentData: {
    type: Object,
    default: () => ({first_name: "", second_name: "", patronymic: "", passport: "", phone_number: ""}),
  },
  mode: {
    type: String,
    default: "add",
  },
});
const emits = defineEmits(["update:modelValue", "submit-agent"]);
const formData = ref({...props.agentData});
watch(
    () => props.agentData,
    (newVal) => {
      formData.value = {...newVal};
    }
);
function closeModal() {
  emits("update:modelValue", false);
}
function handleSubmit() {
  emits("submit-agent", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Добавить агента" : "Редактировать агента" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.first_name" label="Имя" required></v-text-field>
          <v-text-field v-model="formData.second_name" label="Фамилия"required></v-text-field>
          <v-text-field v-model="formData.patronymic" label="Отчество" required></v-text-field>
          <v-text-field v-model="formData.passport" label="Номер паспорта" required></v-text-field>
          <v-text-field v-model="formData.phone_number" label="Номер телефона" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="red" @click="closeModal">Отмена</v-btn>
        <v-btn color="green" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
