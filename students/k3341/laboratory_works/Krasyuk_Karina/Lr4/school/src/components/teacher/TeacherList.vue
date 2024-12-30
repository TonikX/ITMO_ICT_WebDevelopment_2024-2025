<script setup>
import {ref} from "vue";
import TeacherModal from "@/components/teacher/TeacherModal.vue";

defineProps({
  teachers: Array,
  rooms: Array,
});
const emits = defineEmits(["delete-teacher", "update-teacher"]);

const isEditModalVisible = ref(false);
const selectedTeacher = ref({});

function handleEdit(teacher) {
  selectedTeacher.value = {...teacher};
  isEditModalVisible.value = true;
}

function handleUpdateTeacher(teacher) {
  emits("update-teacher", teacher);
  isEditModalVisible.value = false;
}
</script>

<template>
  <div class="teacher-list">
    <template v-for="teacher in teachers" :key="teacher.id">
      <v-card class="teacher-card" width="400">
        <template #title>{{ teacher.second_name }} {{ teacher.first_name }} {{ teacher.patronymic ?? "" }}</template>
        <template v-if="teacher.room" #text>
          Закреплённый кабинет {{ teacher.room.number }}<br/>
        </template>
        <v-card-actions>
          <v-btn @click="handleEdit(teacher)" color="primary">Редактировать</v-btn>
          <v-btn @click="$emit('delete-teacher', teacher.id)" color="secondary">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <TeacherModal
        v-model="isEditModalVisible"
        :teacherData="selectedTeacher"
        :rooms="rooms"
        mode="edit"
        @submit-teacher="handleUpdateTeacher"
    />
  </div>
</template>

<style scoped>
.teacher-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.teacher-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 16px;
}
</style>
