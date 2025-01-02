<script setup>
import {ref, watch} from "vue";


const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  alpinistData: {
    type: Object,
    default: () => ({first_name: "", last_name: "", patronymic: ""}),
  },
  clubs: {
    type: Array
  },
  mode: {
    type: String,
    default: "add",
  },

});


const emits = defineEmits(["update:modelValue", "submit-alpinist"]);

const formData = ref({...props.alpinistData});

watch(
    () => props.alpinistData,
    (newVal) => {
      formData.value = {...newVal};
    }
);


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-alpinist", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Добавить альпиниста" : "Редактировать альпиниста" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.last_name" label="Фамилия" required></v-text-field>
          <v-text-field v-model="formData.first_name" label="Имя" required></v-text-field>
          <v-text-field v-model="formData.patronymic" label="Отчество" required></v-text-field>
          <v-select
              v-model="formData.club"
              :items="clubs"
              item-title="name"
              item-value="id"
              label="Клуб"/>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
