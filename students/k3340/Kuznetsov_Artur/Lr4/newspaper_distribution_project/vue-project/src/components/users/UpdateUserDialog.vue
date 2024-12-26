<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  userData: {
    type: Object,
    default: () => ({
      username: "",
      email: "",
      first_name: "",
      last_name: "",
      patronymic: "",
      role: "user",
    }),
  },
});

const emits = defineEmits(["update:modelValue", "submit-user"]);

const formData = ref({...props.userData});

watch(
  () => props.userData,
  (newVal) => {
    formData.value = {...newVal};
  }
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("submit-user", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="600">
    <v-card>
      <v-card-title>Редактировать пользователя</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field
            v-model="formData.username" label="Имя пользователя" required
          ></v-text-field>
          <v-text-field
            v-model="formData.email" label="Email" required
          ></v-text-field>
          <v-text-field
            v-model="formData.first_name" label="Имя" required
          ></v-text-field>
          <v-text-field
            v-model="formData.last_name" label="Фамилия" required
          ></v-text-field>
          <v-text-field
            v-model="formData.patronymic" label="Отчество" required
          ></v-text-field>
          <v-select
            v-model="formData.role" :items="['user', 'editor', 'admin']" label="Роль" required
          ></v-select>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
