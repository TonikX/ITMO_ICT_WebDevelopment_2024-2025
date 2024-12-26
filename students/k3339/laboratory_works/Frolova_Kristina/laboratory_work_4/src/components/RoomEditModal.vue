<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  room: {
    type: Object,
    default: () => ({
      id: null,
      type: "",
      floor: "",
      cost: "",
      phone_number: "",
    }),
  },
});

const emits = defineEmits(["update:modelValue", "save-room"]);

const formData = ref({});

watch(
    () => props.room,
    (newVal) => {
      formData.value = { ...newVal };
    },
    { immediate: true, deep: true }
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("save-room", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" max-width="500">
    <v-card>
      <v-card-title>Редактировать комнату</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-select
              v-model="formData.type"
              label="Тип комнаты"
              :items="[
              { title: 'Одиночная', value: 's' },
              { title: 'Двухместная', value: 'd' },
              { title: 'Трёхместная', value: 't' }]"
              required>
          </v-select>
          <v-text-field v-model="formData.floor" label="Этаж" type="number" required></v-text-field>
          <v-text-field v-model="formData.cost" label="Стоимость" type="number" required></v-text-field>
          <v-text-field v-model="formData.phone_number" label="Телефон" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
