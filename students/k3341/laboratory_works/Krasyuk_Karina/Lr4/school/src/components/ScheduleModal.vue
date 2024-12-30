<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  lesson: {
    type: Object,
    default: () => ({
      day_of_week: "",
      number_of_lesson: "",
      time: "",
      subject: null,
      teacher: null,
      room: null,
      group: null
    }),
  },
  subjects: {
    type: Array,
    default: () => []
  },
  teachers: {
    type: Array,
    default: () => []
  },
  rooms: {
    type: Array,
    default: () => []
  },
  groups: {
    type: Array,
    default: () => []
  },
  mode: {
    type: String,
    default: "add",
  },
});

const emits = defineEmits(["update:modelValue", "save-lesson"]);

const formData = ref({ ...props.lesson });

watch(
    () => props.lesson,
    (newVal) => {
      formData.value = {...newVal};
    },
    { immediate: true, deep: true },
);

function closeModal() {
  emits("update:modelValue", false);
}


function saveLesson() {
  const preparedData = {
    ...formData.value,
    subject: formData.value.subject?.id || formData.value.subject,
    teacher: formData.value.teacher?.id || formData.value.teacher,
    room: formData.value.room?.id || formData.value.room,
    group: formData.value.group?.id || formData.value.group,
  };
  emits("save-lesson", preparedData);
  closeModal();
}

</script>

<template>
  <v-dialog :model-value="modelValue" max-width="600px" @update:model-value="closeModal">
    <v-card>
      <v-card-title>{{ mode === "add" ? "Добавить урок" : "Редактировать урок" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="saveLesson">
          <v-select
              v-model="formData.day_of_week"
              :items="[
              { text: 'Понедельник', value: 'mon' },
              { text: 'Вторник', value: 'tue' },
              { text: 'Среда', value: 'wed' },
              { text: 'Четверг', value: 'thu' },
              { text: 'Пятница', value: 'fri' },
              { text: 'Суббота', value: 'sat' },
              { text: 'Воскресенье', value: 'sun' },
            ]"
              item-title="text"
              item-value="value"
              label="День недели"
              required
          />
          <v-text-field
              v-model="formData.number_of_lesson"
              label="Номер урока"
              type="number"
              required
          />
          <v-text-field
              v-model="formData.time"
              label="Время"
              required
          />
          <v-select
              v-model="formData.subject"
              label="Предмет"
              :items="subjects"
              item-title="subject_name"
              item-value="id"
              required
          />
          <v-select
              v-model="formData.teacher"
              label="Учитель"
              :items="teachers"
              :item-title="item => `${item.second_name} ${item.first_name} ${item.patronymic}`"
              item-value="id"
              required
          />
          <v-select
              v-model="formData.room"
              label="Кабинет"
              :items="rooms"
              item-title="number"
              item-value="id"
              required
          />
          <v-select
              v-model="formData.group"
              :items="groups"
              item-title="label"
              item-value="id"
              label="Класс"
              required
          />

        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="saveLesson">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
</style>
