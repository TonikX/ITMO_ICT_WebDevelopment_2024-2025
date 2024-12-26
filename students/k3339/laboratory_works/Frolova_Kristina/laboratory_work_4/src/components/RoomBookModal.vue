<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  room: {
    type: Object,
    required: true,
  },
  clients: {
    type: Array,
    default: () => [],
  }
});

const emits = defineEmits(["update:modelValue", "save-booking"]);

const formData = ref({
  client: "",
  arrival_date: "",
  departure_date: "",
});


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("save-booking", { ...formData.value, room: props.room.id });
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" max-width="500">
    <v-card>
      <v-card-title>Забронировать комнату</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-select
              v-model="formData.client"
              :items="clients"
              item-title="full_name"
              item-value="id"
              label="Клиент"
              required/>
          <v-text-field v-model="formData.arrival_date" label="Дата заезда" type="date" required></v-text-field>
          <v-text-field v-model="formData.departure_date" label="Дата выезда" type="date" required></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
