<script setup>
import {ref, watch} from "vue";


const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  manufacturerData: {
    type: Object,
    default: () => ({name: "", country: ""}),
  },
  mode: {
    type: String,
    default: "add",
  },
});

const formData = ref({
  name: "",

})
const emits = defineEmits(["update:modelValue", "submit-manufacturer"]);


watch(
    () => props.manufacturerData,
    (newVal) => {
      formData.value = {...newVal};
    }
);


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-manufacturer", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ "Добавить производителя" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.name" label="Название" required></v-text-field>
          <v-text-field v-model="formData.country" label="Страна" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
