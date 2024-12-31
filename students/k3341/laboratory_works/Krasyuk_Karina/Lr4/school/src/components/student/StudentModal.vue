<script setup>
import {ref, watch} from "vue";


const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  studentData: {
    type: Object,
    default: () => ({first_name: "", second_name: "", patronymic: ""}),
  },
  groups: {
    type: Array
  },
  mode: {
    type: String,
    default: "add",
  },

});


const emits = defineEmits(["update:modelValue", "submit-student"]);

const formData = ref({...props.studentData});

watch(
    () => props.studentData,
    (newVal) => {
      formData.value = {...newVal};
    }
);


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-student", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Добавить ученика" : "Редактировать ученика" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.first_name" label="Фамилия" required></v-text-field>
          <v-text-field v-model="formData.second_name" label="Имя" required></v-text-field>
          <v-text-field v-model="formData.patronymic" label="Отчество" required></v-text-field>
          <v-select
              v-model="formData.group"
              :items="groups"
              :item-title="item => `${item.group_grade}${item.group_name}`"
              item-value="id"
              label="Класс"/>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
