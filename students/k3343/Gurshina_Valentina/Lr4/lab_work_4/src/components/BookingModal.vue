<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  booking: {
    type: Object,
    default: () => ({
      client: "",
      room: "",
      arrival_date: "",
      departure_date: "",
    }),
  },
  clients: {
    type: Array,
    default: () => [],
  },
  rooms: {
    type: Array,
    default: () => [],
  }
});

const emits = defineEmits(["update:modelValue", "save-booking"]);

const formData = ref({});

watch(
    () => props.booking,
    (newVal) => {
      formData.value = {...newVal};
    },
    {immediate: true, deep: true}
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  console.log(formData.value)
  emits("save-booking", {...formData.value, client: formData.value.client});
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" max-width="500">
    <v-card>
      <v-card-title>
        {{ booking?.id ? "Редактировать бронирование" : "Добавить бронирование" }}
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-select
              v-model="formData.client"
              :items="clients"
              item-title="full_name"
              item-value="id"
              label="Гость"
              required/>
          <v-select
              v-model="formData.room"
              :items="rooms"
              item-title="id"
              item-value="id"
              label="Номер"
              required/>
          <v-text-field
              v-model="formData.arrival_date"
              label="Дата заезда"
              type="date"
              required
          ></v-text-field>
          <v-text-field
              v-model="formData.departure_date"
              label="Дата выезда"
              type="date"
              required
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
