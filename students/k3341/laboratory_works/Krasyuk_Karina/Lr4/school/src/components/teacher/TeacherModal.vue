<script setup>
import {ref, watch} from "vue";


const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  teacherData: {
    type: Object,
    default: () => ({first_name: "", second_name: "", patronymic: "", room: ""}),
  },
  rooms: {
    type: Array
  },
  mode: {
    type: String,
    default: "add",
  },

});


const emits = defineEmits(["update:modelValue", "submit-teacher"]);

const formData = ref({...props.teacherData});

watch(
    () => props.teacherData,
    (newVal) => {
      formData.value = {...newVal};
    }
);


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-teacher", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Добавить учителя" : "Редактировать учителя" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.first_name" label="Фамилия" required></v-text-field>
          <v-text-field v-model="formData.second_name" label="Имя" required></v-text-field>
          <v-text-field v-model="formData.patronymic" label="Отчество" required></v-text-field>
          <v-select
              v-model="formData.room"
              :items="rooms"
              item-title="number"
              item-value="id"
              label="Закреплённый кабинет"/>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
