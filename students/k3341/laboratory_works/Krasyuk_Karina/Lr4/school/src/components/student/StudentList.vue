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
      <v-card class="student-card" width="400">
        <template #title>{{ student.second_name }} {{ student.first_name }} {{ student.patronymic ?? "" }}</template>
        Класс {{ student.group.group_grade }}{{ student.group.group_name }}<br/>
        <v-card-actions>
          <v-btn @click="handleEdit(student)" color="primary">Редактировать</v-btn>
          <v-btn @click="$emit('delete-student', student.id)" color="secondary">Удалить</v-btn>
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
.student-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.student-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 16px;
}
</style>
