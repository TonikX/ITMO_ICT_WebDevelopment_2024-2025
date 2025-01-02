<script setup>
import {ref, watch} from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },

  groupData: {
    type: Object,
    default: () => ({group_result: "", description_of_result: ""}),
  },

  mode: {
    type: String,
    default: "add",
  }
})

const emits = defineEmits(["update:modelValue", "submit"]);

const formData = ref({...props.groupData});

watch(
    () => props.groupData,
    (newVal) => {
      formData.value = {...newVal};
    }
);

function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  console.log(formData.value)
  emits("submit", formData.value);
  closeModal();
}

</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Добавить группу" : "Редактировать группу" }}</v-card-title>
      <v-card-text>
        <v-select
            v-model="formData.group_result"
            :items="[
              { text: 'Успех', value: 's' },
              { text: 'Неудача', value: 'f' },
              { text: 'Другое', value: 'o' },
            ]"
            item-value="value"
            item-title="text"
            label="Результат группы"/>
        <v-textarea label="Описание результата" v-model="formData.description_of_result" />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
        <v-btn @click="closeModal">Отмена</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>