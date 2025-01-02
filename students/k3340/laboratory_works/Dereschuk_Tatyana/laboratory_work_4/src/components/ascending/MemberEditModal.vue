<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  alpinistData: {
    type: Object,
    default: () => ({alpinist: null, result: null, emergency_situations: null})
  }
});
const formData = ref({...props.alpinistData});

const emits = defineEmits(["update:modelValue", "submit"]);

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
  emits("submit", formData.value);
  closeModal();
}


</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>Редактировать участника</v-card-title>
      <v-card-text>
        <v-select
            label="Альпинист"
            :item-title="alpinist => `${alpinist.last_name} ${alpinist.first_name} ${alpinist.patronymic}`"
            item-value="id"
            v-model="formData.alpinist"
            disabled
            required
        />
        <v-select v-model="formData.result"
                  :items="[
              { text: 'Успех', value: 's' },
              { text: 'Неудача', value: 'f' },
              { text: 'ЧС', value: 'e' },
              { text: 'Другое', value: 'o' },
            ]"
                  item-value="value"
                  item-title="text"
                  label="Результат"/>
        <v-select
            :items="[
              { text: 'Травма', value: 't' },
              { text: 'Смерть', value: 'l' },
              { text: 'Пропал', value: 'm' },
            ]"
            item-value="value"
            item-title="text"
            label="Чрезвычайные ситуации"
            v-model="formData.emergency_situations"
        />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="handleSubmit">Добавить</v-btn>
        <v-btn @click="closeModal">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>