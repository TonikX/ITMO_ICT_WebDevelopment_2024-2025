<template>
  <h1 class="mt-4 mb-2">{{ props.dayName }}</h1>
  <div v-if="!scheduleRecords.length">
    <h3>Уроков не найдено</h3>
  </div>
  <div v-for="scheduleRecord in scheduleRecords" :key="scheduleRecord.id">
    <v-card class="mb-2">
      <v-card-title>
        {{ scheduleRecord.lesson_number }}. {{ scheduleRecord.subject.name }}
      </v-card-title>
      <div class="d-flex align-center justify-space-between w-100">
        <div class="ms-3 mb-4 d-flex">
          <v-chip class="me-3" color="primary">
            Класс: {{ scheduleRecord.student_class.class_name }}
          </v-chip>
          <v-chip class="me-3" color="secondary"
            >Кабинет №{{ scheduleRecord.room_number_id }}
          </v-chip>
          <v-chip class="me-3">
            Учитель:
            {{ scheduleRecord.teacher.last_name }}
            {{ scheduleRecord.teacher.first_name }}
            {{ scheduleRecord.teacher.patronymic }}
          </v-chip>
        </div>
        <div class="d-flex me-4 mb-4">
          <v-btn
            color="primary"
            class="me-3"
            variant="tonal"
            size="small"
            @click="editHandler(scheduleRecord)"
            >Изменить</v-btn
          >
          <v-btn
            color="error"
            variant="tonal"
            size="small"
            @click="deleteHandler(scheduleRecord)"
            >Удалить</v-btn
          >
        </div>
      </div>
    </v-card>
  </div>
</template>

<script setup>
const props = defineProps(["dayName", "scheduleRecords", "editHandler", "deleteHandler"]);
</script>
