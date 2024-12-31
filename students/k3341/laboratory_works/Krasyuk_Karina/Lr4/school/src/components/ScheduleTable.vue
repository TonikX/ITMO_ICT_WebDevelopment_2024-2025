<script setup>
import { daysOfWeek } from "@/utils/enums.js";

const props = defineProps({
  schedule: {
    type: Array,
    required: true,
  },
});

defineEmits(["edit-lesson", "edit-lesson"]);

function getLesson(day, lessonNumber) {
  return props.schedule.find(
      item => item.day_of_week === day && item.number_of_lesson === lessonNumber
  );
}
</script>

<template>
  <table>
    <thead>
    <tr>
      <th>Время</th>
      <th v-for="day in daysOfWeek" :key="day.value">{{ day.label }}</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="lessonNumber in 10" :key="lessonNumber">
      <td>{{ lessonNumber }}</td>
      <td v-for="day in daysOfWeek" :key="day.value">
        <div v-if="getLesson(day.value, lessonNumber)">
          <strong>{{ getLesson(day.value, lessonNumber).subject.subject_name }}</strong><br />
          {{ getLesson(day.value, lessonNumber).teacher.first_name }}
          {{ getLesson(day.value, lessonNumber).teacher.second_name }}<br />
          Кабинет: {{ getLesson(day.value, lessonNumber).room.number }}<br />
          <v-btn color="primary" @click="$emit('edit-lesson', getLesson(day.value, lessonNumber))">Редактировать</v-btn>
          <v-btn color="error" @click="$emit('delete-lesson', getLesson(day.value, lessonNumber).id)">Удалить</v-btn>
        </div>
      </td>
    </tr>
    </tbody>
  </table>
</template>

<style scoped>
</style>
