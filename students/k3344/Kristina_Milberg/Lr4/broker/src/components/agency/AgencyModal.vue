<script setup>
import {ref, watch} from "vue";


const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  agencyData: {
    type: Object,
    default: () => ({name: "", country: "", contact_number: "", address: "", legal_address: ""}),
  },
  mode: {
    type: String,
    default: "add",
  },
});


const emits = defineEmits(["update:modelValue", "agency-client"]);

const formData = ref({...props.agencyData});

watch(
    () => props.agencyData,
    (newVal) => {
      formData.value = {...newVal};
    }
);


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-agency", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Добавить агенство" : "Редактировать агенство" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.name" label="Название" required></v-text-field>
          <v-text-field v-model="formData.country" label="Страна" required></v-text-field>
          <v-text-field v-model="formData.contact_number" label="Контактный номер" required></v-text-field>
          <v-text-field v-model="formData.address" label="Адрес" required></v-text-field>
          <v-text-field v-model="formData.legal_address" label="Юридический адрес" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
