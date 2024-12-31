<script setup>
import {ref} from "vue";
import StudentModal from "@/components/student/StudentModal.vue";

defineProps({
  students: Array,
  groups: Array,
});
const emits = defineEmits(["delete-student", "update-student"]);

const isEditModalVisible = ref(false);
const selectedStudent = ref({});

function handleEdit(student) {
  selectedStudent.value = {...student};
  isEditModalVisible.value = true;
}

function handleUpdateStudent(student) {
  emits("update-student", student);
  isEditModalVisible.value = false
}
</script>

<template>
  <div class="student-list">
    <template v-for="student in students" :key="student.id">
      <v-card class="student-card" width="600">
        <v-card-title>
          {{ student.second_name }} {{ student.first_name }} {{ student.patronymic ?? "" }}
        </v-card-title>
        <v-card-subtitle>Класс {{ student.group.group_grade }}{{ student.group.group_name }}</v-card-subtitle>
        <v-card-actions class="student-card-actions">
          <v-btn @click="handleEdit(student)" color="primary" class="action-btn">Редактировать</v-btn>
          <v-btn @click="$emit('delete-student', student.id)" color="error" class="action-btn">Удалить</v-btn>
          <v-btn :to="`/students/${student.id}`" color="success" class="action-btn">Посмотреть оценки</v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <StudentModal
        v-model="isEditModalVisible"
        :studentData="selectedStudent"
        :groups="groups"
        mode="edit"
        @submit-student="handleUpdateStudent"
    />
  </div>
</template>

<style scoped>
.student-card {
  margin-bottom: 16px;
}

.student-card-actions {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.action-btn {
  flex: 1; /* Чтобы кнопки имели одинаковую ширину */
  text-transform: none; /* Убрать CAPSLOCK текста */
}
</style>
