<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between align-center">
      <span>Оценки студента: {{ student?.full_name }}</span>
      <v-btn icon @click="$emit('close')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>
    
    <v-card-text>
      <div v-if="grades.isLoading.value" class="text-center py-6">
        <v-progress-circular indeterminate />
      </div>
      
      <div v-else-if="gradesList.length === 0" class="text-center py-6">
        <v-icon size="64" color="grey">mdi-school-outline</v-icon>
        <div class="text-h6 mt-4">Нет оценок</div>
      </div>
      
      <v-table v-else>
        <thead>
          <tr>
            <th>Дисциплина</th>
            <th>Оценка</th>
            <th>Тип</th>
            <th>Семестр</th>
            <th>Учебный год</th>
            <th>Дата</th>
            <th>Преподаватель</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="grade in gradesList" :key="grade.grade_id">
            <td>{{ grade.subject_name }}</td>
            <td>
              <v-chip :color="getGradeColor(grade.grade_value)" size="small">
                {{ grade.grade_value }}
              </v-chip>
            </td>
            <td>{{ getGradeTypeText(grade.grade_type) }}</td>
            <td>{{ grade.semester === 1 ? 'Осенний' : 'Весенний' }}</td>
            <td>{{ grade.academic_year }}</td>
            <td>{{ formatDate(grade.date_received) }}</td>
            <td>{{ grade.teacher_name }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
    
    <v-card-actions>
      <v-spacer />
      <v-btn color="primary" @click="$emit('close')">Закрыть</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useGrades } from '@/composables/useGrades'

const props = defineProps({
  student: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])

const grades = useGrades()
const gradesList = ref([])

const getGradeColor = (grade) => {
  if (grade >= 4.5) return 'success'
  if (grade >= 3.5) return 'warning'
  return 'error'
}

const getGradeTypeText = (type) => {
  const typeMap = {
    exam: 'Экзамен',
    test: 'Зачёт',
    coursework: 'Курсовая',
    practice: 'Практика',
    test_module: 'Модуль'
  }
  return typeMap[type] || type
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('ru-RU')
}

onMounted(async () => {
  if (props.student?.student_id) {
    const result = await grades.getStudentGrades(props.student.student_id)
    if (result.success) {
      gradesList.value = result.data
    }
  }
})
</script>