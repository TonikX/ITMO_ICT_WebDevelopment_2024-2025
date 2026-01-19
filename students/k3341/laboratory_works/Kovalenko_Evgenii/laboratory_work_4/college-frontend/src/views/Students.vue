<template>
  <v-container>
    <v-card>
      <v-card-title>
        <span class="text-h5">Студенты</span>
        <v-spacer />
        <v-btn color="primary" @click="showDialog = true">
          <v-icon start icon="mdi-plus" />
          Добавить студента
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Фильтры -->
        <v-row class="mb-4">
          <v-col cols="12" md="4">
            <v-text-field
              v-model="filters.last_name"
              label="Фамилия"
              clearable
              @update:model-value="fetchStudents"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="filters.status"
              :items="statusOptions"
              label="Статус"
              clearable
              @update:model-value="fetchStudents"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="filters.course"
              :items="courseOptions"
              label="Курс"
              clearable
              @update:model-value="fetchStudents"
            />
          </v-col>
        </v-row>

        <!-- Таблица студентов -->
        <v-data-table
          :headers="headers"
          :items="students.students.value"
          :loading="students.isLoading.value"
          :search="search"
          items-per-page="10"
        >
          <template #item.status="{ item }">
            <v-chip :color="getStatusColor(item.status)" size="small">
              {{ getStatusText(item.status) }}
            </v-chip>
          </template>

          <template #item.average_grade="{ item }">
            <v-chip v-if="item.average_grade" :color="getGradeColor(item.average_grade)" size="small">
              {{ item.average_grade }}
            </v-chip>
            <span v-else>—</span>
          </template>

          <template #item.actions="{ item }">
            <v-btn
              icon="mdi-pencil"
              size="small"
              variant="text"
              @click="editStudent(item)"
            />
            <v-btn
              icon="mdi-delete"
              size="small"
              variant="text"
              color="error"
              @click="deleteStudent(item.student_id)"
            />
            <v-btn
              icon="mdi-school"
              size="small"
              variant="text"
              color="info"
              @click="viewGrades(item)"
            />
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Диалог добавления/редактирования студента -->
    <v-dialog v-model="showDialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingStudent ? 'Редактировать студента' : 'Добавить студента' }}
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveStudent">
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="studentForm.last_name"
                  label="Фамилия*"
                  required
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="studentForm.first_name"
                  label="Имя*"
                  required
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="studentForm.patronymic"
                  label="Отчество"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="studentForm.group"
                  :items="groups.groups.value"
                  item-title="group_name"
                  item-value="group_id"
                  label="Группа*"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="studentForm.status"
                  :items="statusOptions"
                  label="Статус*"
                  required
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="studentForm.phone"
                  label="Телефон"
                  type="tel"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="studentForm.email"
                  label="Email"
                  type="email"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="studentForm.enrollment_date"
                  label="Дата зачисления"
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

    <!-- Диалог просмотра оценок -->
    <v-dialog v-model="showGradesDialog" max-width="800px">
      <StudentGradesDialog
        :student="selectedStudent"
        @close="showGradesDialog = false"
      />
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useStudents } from '@/composables/useStudents'
import { useGroups } from '@/composables/useGroups'
import StudentGradesDialog from '@/components/students/StudentGradesDialog.vue'

const students = useStudents()
const groups = useGroups()

const search = ref('')
const showDialog = ref(false)
const showGradesDialog = ref(false)
const editingStudent = ref(null)
const saving = ref(false)
const selectedStudent = ref(null)

const filters = reactive({
  last_name: '',
  status: '',
  course: ''
})

const studentForm = reactive({
  last_name: '',
  first_name: '',
  patronymic: '',
  group: null,
  status: 'active',
  phone: '',
  email: '',
  enrollment_date: new Date().toISOString().split('T')[0]
})

const statusOptions = [
  { title: 'Активен', value: 'active' },
  { title: 'Отчислен', value: 'expelled' },
  { title: 'Академический отпуск', value: 'academic' }
]

const courseOptions = computed(() => {
  return [...new Set(groups.groups.value.map(g => g.course))]
    .sort()
    .map(c => ({ title: `${c} курс`, value: c }))
})

const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Группа', key: 'group_name' },
  { title: 'Курс', key: 'course', align: 'center' },
  { title: 'Дата зачисления', key: 'enrollment_date' },
  { title: 'Статус', key: 'status' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Email', key: 'email' },
  { title: 'Ср. балл', key: 'average_grade', align: 'center' },
  { title: 'Оценок', key: 'total_grades', align: 'center' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' }
]

const getStatusColor = (status) => {
  const colors = {
    active: 'success',
    expelled: 'error',
    academic: 'warning'
  }
  return colors[status] || 'default'
}

const getStatusText = (status) => {
  const texts = {
    active: 'Активен',
    expelled: 'Отчислен',
    academic: 'Академический отпуск'
  }
  return texts[status] || status
}

// Добавляем недостающую функцию
const getGradeColor = (grade) => {
  if (!grade) return 'default'
  if (grade >= 4.5) return 'success'
  if (grade >= 3.5) return 'warning'
  return 'error'
}

const fetchStudents = async () => {
  const params = {}
  if (filters.last_name) params.last_name = filters.last_name
  if (filters.status) params.status = filters.status
  if (filters.course) params.course = filters.course
  
  await students.fetchStudents(params)
}

const editStudent = (student) => {
  editingStudent.value = student
  Object.assign(studentForm, {
    ...student,
    enrollment_date: student.enrollment_date?.split('T')[0] || new Date().toISOString().split('T')[0]
  })
  showDialog.value = true
}

const saveStudent = async () => {
  saving.value = true
  try {
    if (editingStudent.value) {
      await students.updateStudent(editingStudent.value.student_id, studentForm)
    } else {
      await students.createStudent(studentForm)
    }
    closeDialog()
    await fetchStudents()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
  } finally {
    saving.value = false
  }
}

const deleteStudent = async (id) => {
  if (confirm('Вы уверены, что хотите удалить студента?')) {
    await students.deleteStudent(id)
    await fetchStudents()
  }
}

const viewGrades = (student) => {
  selectedStudent.value = student
  showGradesDialog.value = true
}

const closeDialog = () => {
  showDialog.value = false
  editingStudent.value = null
  Object.assign(studentForm, {
    last_name: '',
    first_name: '',
    patronymic: '',
    group: null,
    status: 'active',
    phone: '',
    email: '',
    enrollment_date: new Date().toISOString().split('T')[0]
  })
}

onMounted(async () => {
  await fetchStudents()
  await groups.fetchGroups()
})
</script>