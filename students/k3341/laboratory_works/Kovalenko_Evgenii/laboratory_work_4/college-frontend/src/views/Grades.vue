<template>
  <v-container>
    <v-card>
      <v-card-title>
        <span class="text-h5">Оценки студентов</span>
        <v-spacer />
        <v-btn color="primary" @click="showDialog = true">
          <v-icon start icon="mdi-plus" />
          Добавить оценку
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Фильтры -->
        <v-row class="mb-4">
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.student_id"
              :items="students.students.value"
              item-title="full_name"
              item-value="student_id"
              label="Студент"
              clearable
              :loading="students.isLoading.value"
              @update:model-value="fetchGrades"
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.subject_id"
              :items="subjects.subjects.value"
              item-title="subject_name"
              item-value="subject_id"
              label="Дисциплина"
              clearable
              :loading="subjects.isLoading.value"
              @update:model-value="fetchGrades"
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.semester"
              :items="semesterOptions"
              label="Семестр"
              clearable
              @update:model-value="fetchGrades"
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="filters.academic_year"
              label="Учебный год"
              type="number"
              clearable
              @update:model-value="fetchGrades"
            />
          </v-col>
        </v-row>

        <!-- Таблица оценок -->
        <div v-if="grades.error.value" class="mb-4">
          <v-alert type="error">
            {{ grades.error.value }}
          </v-alert>
        </div>

        <v-data-table
          :headers="headers"
          :items="grades.grades.value"
          :loading="grades.isLoading.value"
          :items-per-page="20"
        >
          <template #item.grade_value="{ item }">
            <v-chip :color="getGradeColor(item.grade_value)" size="small">
              {{ item.grade_value }}
            </v-chip>
          </template>

          <template #item.grade_type_display="{ item }">
            {{ item.grade_type_display || item.grade_type }}
          </template>

          <template #item.semester_display="{ item }">
            {{ item.semester_display || (item.semester === 1 ? 'Осенний' : 'Весенний') }}
          </template>

          <template #item.date_received="{ item }">
            {{ formatDate(item.date_received) }}
          </template>

          <template #item.actions="{ item }">
            <v-btn
              icon="mdi-pencil"
              size="small"
              variant="text"
              @click="editGrade(item)"
            />
            <v-btn
              icon="mdi-delete"
              size="small"
              variant="text"
              color="error"
              @click="deleteGrade(item.grade_id)"
            />
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Диалог добавления/редактирования оценки -->
    <v-dialog v-model="showDialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingGrade ? 'Редактировать оценку' : 'Добавить оценку' }}
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveGrade">
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="gradeForm.student"
                  :items="students.students.value"
                  item-title="full_name"
                  item-value="student_id"
                  label="Студент*"
                  required
                  :loading="students.isLoading.value"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="gradeForm.subject"
                  :items="subjects.subjects.value"
                  item-title="subject_name"
                  item-value="subject_id"
                  label="Дисциплина*"
                  required
                  :loading="subjects.isLoading.value"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="gradeForm.grade_value"
                  label="Оценка*"
                  type="number"
                  step="0.1"
                  min="2.0"
                  max="5.0"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="gradeForm.grade_type"
                  :items="gradeTypeOptions"
                  label="Тип оценки*"
                  required
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="gradeForm.semester"
                  :items="semesterOptions"
                  label="Семестр*"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="gradeForm.academic_year"
                  label="Учебный год*"
                  type="number"
                  min="2000"
                  max="2100"
                  required
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="gradeForm.teacher"
                  :items="teachers.teachers.value"
                  item-title="full_name"
                  item-value="teacher_id"
                  label="Преподаватель*"
                  required
                  :loading="teachers.isLoading.value"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="gradeForm.date_received"
                  label="Дата получения"
                  type="date"
                />
              </v-col>
            </v-row>

            <v-card-actions>
              <v-spacer />
              <v-btn color="error" @click="closeDialog">Отмена</v-btn>
              <v-btn color="primary" type="submit" :loading="saving">
                Сохранить
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useGrades } from '@/composables/useGrades'
import { useStudents } from '@/composables/useStudents'
import { useTeachers } from '@/composables/useTeachers'
import { useSubjects } from '@/composables/useSubjects'

const grades = useGrades()
const students = useStudents()
const teachers = useTeachers()
const subjects = useSubjects()

const showDialog = ref(false)
const editingGrade = ref(null)
const saving = ref(false)

const filters = reactive({
  student_id: null,
  subject_id: null,
  semester: null,
  academic_year: null
})

const gradeForm = reactive({
  student: null,
  subject: null,
  grade_value: 3.0,
  grade_type: 'exam',
  semester: 1,
  academic_year: new Date().getFullYear(),
  teacher: null,
  date_received: new Date().toISOString().split('T')[0]
})

const semesterOptions = [
  { title: 'Осенний', value: 1 },
  { title: 'Весенний', value: 2 }
]

const gradeTypeOptions = [
  { title: 'Экзамен', value: 'exam' },
  { title: 'Зачёт', value: 'test' },
  { title: 'Курсовая работа', value: 'coursework' },
  { title: 'Практика', value: 'practice' },
  { title: 'Модульный контроль', value: 'test_module' }
]

const headers = [
  { title: 'Студент', key: 'student_name' },
  { title: 'Группа', key: 'group_name' },
  { title: 'Дисциплина', key: 'subject_name' },
  { title: 'Оценка', key: 'grade_value', align: 'center' },
  { title: 'Тип', key: 'grade_type_display' },
  { title: 'Семестр', key: 'semester_display' },
  { title: 'Учебный год', key: 'academic_year', align: 'center' },
  { title: 'Дата', key: 'date_received' },
  { title: 'Преподаватель', key: 'teacher_name' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' }
]

const getGradeColor = (grade) => {
  if (grade >= 4.5) return 'success'
  if (grade >= 3.5) return 'warning'
  return 'error'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('ru-RU')
}

const fetchGrades = async () => {
  const params = {}
  if (filters.student_id) params.student = filters.student_id
  if (filters.subject_id) params.subject = filters.subject_id
  if (filters.semester) params.semester = filters.semester
  if (filters.academic_year) params.academic_year = filters.academic_year
  
  await grades.fetchGrades(params)
}

const editGrade = (grade) => {
  editingGrade.value = grade
  Object.assign(gradeForm, {
    student: grade.student,
    subject: grade.subject,
    grade_value: grade.grade_value,
    grade_type: grade.grade_type,
    semester: grade.semester,
    academic_year: grade.academic_year,
    teacher: grade.teacher,
    date_received: grade.date_received?.split('T')[0] || new Date().toISOString().split('T')[0]
  })
  showDialog.value = true
}

const saveGrade = async () => {
  saving.value = true
  try {
    const result = editingGrade.value 
      ? await grades.updateGrade(editingGrade.value.grade_id, gradeForm)
      : await grades.createGrade(gradeForm)
    
    if (result.success) {
      closeDialog()
      await fetchGrades()
    } else {
      alert('Ошибка сохранения: ' + JSON.stringify(result.error))
    }
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    alert('Произошла ошибка при сохранении')
  } finally {
    saving.value = false
  }
}

const deleteGrade = async (id) => {
  if (confirm('Вы уверены, что хотите удалить эту оценку?')) {
    const result = await grades.deleteGrade(id)
    if (result.success) {
      await fetchGrades()
    } else {
      alert('Ошибка удаления: ' + JSON.stringify(result.error))
    }
  }
}

const closeDialog = () => {
  showDialog.value = false
  editingGrade.value = null
  Object.assign(gradeForm, {
    student: null,
    subject: null,
    grade_value: 3.0,
    grade_type: 'exam',
    semester: 1,
    academic_year: new Date().getFullYear(),
    teacher: null,
    date_received: new Date().toISOString().split('T')[0]
  })
}

onMounted(async () => {
  try {
    await Promise.all([
      fetchGrades(),
      students.fetchStudents(),
      teachers.fetchTeachers(),
      subjects.fetchSubjects()
    ])
  } catch (error) {
    console.error('Ошибка загрузки данных:', error)
  }
})
</script>