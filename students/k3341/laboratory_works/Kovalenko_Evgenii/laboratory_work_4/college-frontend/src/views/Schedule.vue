<template>
  <v-container>
    <v-card>
      <v-card-title>
        <span class="text-h5">Расписание занятий</span>
        <v-spacer />
        <v-btn color="primary" @click="showDialog = true">
          <v-icon start icon="mdi-plus" />
          Добавить занятие
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Фильтры -->
        <v-row class="mb-4">
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.group_id"
              :items="groups.groups.value"
              item-title="group_name"
              item-value="group_id"
              label="Группа"
              clearable
              :loading="groups.isLoading.value"
              @update:model-value="fetchSchedules"
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.teacher_id"
              :items="teachers.teachers.value"
              item-title="full_name"
              item-value="teacher_id"
              label="Преподаватель"
              clearable
              :loading="teachers.isLoading.value"
              @update:model-value="fetchSchedules"
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.day_of_week"
              :items="dayOptions"
              label="День недели"
              clearable
              @update:model-value="fetchSchedules"
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="filters.semester"
              :items="semesterOptions"
              label="Семестр"
              clearable
              @update:model-value="fetchSchedules"
            />
          </v-col>
        </v-row>

        <!-- Таблица расписания -->
        <div v-if="schedule.error.value" class="mb-4">
          <v-alert type="error">
            {{ schedule.error.value }}
          </v-alert>
        </div>

        <v-data-table
          :headers="headers"
          :items="schedule.schedules.value"
          :loading="schedule.isLoading.value"
          :items-per-page="20"
        >
          <template #item.day_of_week_display="{ item }">
            {{ item.day_of_week_display || (item.day_of_week === 1 ? 'Понедельник' : 
                                            item.day_of_week === 2 ? 'Вторник' :
                                            item.day_of_week === 3 ? 'Среда' :
                                            item.day_of_week === 4 ? 'Четверг' :
                                            item.day_of_week === 5 ? 'Пятница' : 'Суббота') }}
          </template>

          <template #item.semester_display="{ item }">
            {{ item.semester_display || (item.semester === 1 ? 'Осенний' : 'Весенний') }}
          </template>

          <template #item.actions="{ item }">
            <v-btn
              icon="mdi-pencil"
              size="small"
              variant="text"
              @click="editSchedule(item)"
            />
            <v-btn
              icon="mdi-delete"
              size="small"
              variant="text"
              color="error"
              @click="deleteSchedule(item.schedule_id)"
            />
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Диалог добавления/редактирования расписания -->
    <v-dialog v-model="showDialog" max-width="800px">
      <v-card>
        <v-card-title>
          {{ editingSchedule ? 'Редактировать занятие' : 'Добавить занятие' }}
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveSchedule">
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="scheduleForm.group"
                  :items="groups.groups.value"
                  item-title="group_name"
                  item-value="group_id"
                  label="Группа*"
                  required
                  :loading="groups.isLoading.value"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="scheduleForm.subject"
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
                <v-select
                  v-model="scheduleForm.teacher"
                  :items="teachers.teachers.value"
                  item-title="full_name"
                  item-value="teacher_id"
                  label="Преподаватель*"
                  required
                  :loading="teachers.isLoading.value"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="scheduleForm.classroom"
                  :items="classrooms.classrooms.value"
                  item-title="classroom_number"
                  item-value="classroom_id"
                  label="Кабинет"
                  :loading="classrooms.isLoading.value"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="4">
                <v-select
                  v-model="scheduleForm.day_of_week"
                  :items="dayOptions"
                  label="День недели*"
                  required
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="scheduleForm.lesson_number"
                  label="Номер пары*"
                  type="number"
                  min="1"
                  max="8"
                  required
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                  v-model="scheduleForm.semester"
                  :items="semesterOptions"
                  label="Семестр*"
                  required
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="scheduleForm.academic_year"
                  label="Учебный год*"
                  type="number"
                  min="2000"
                  max="2100"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="scheduleForm.week_type"
                  :items="weekTypeOptions"
                  label="Тип недели"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="scheduleForm.start_date"
                  label="Дата начала"
                  type="date"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="scheduleForm.end_date"
                  label="Дата окончания"
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
import { useSchedule } from '@/composables/useSchedule'
import { useGroups } from '@/composables/useGroups'
import { useTeachers } from '@/composables/useTeachers'
import { useSubjects } from '@/composables/useSubjects'
import { useClassrooms } from '@/composables/useClassrooms'

const schedule = useSchedule()
const groups = useGroups()
const teachers = useTeachers()
const subjects = useSubjects()
const classrooms = useClassrooms()

const showDialog = ref(false)
const editingSchedule = ref(null)
const saving = ref(false)

const filters = reactive({
  group_id: null,
  teacher_id: null,
  day_of_week: null,
  semester: null
})

const scheduleForm = reactive({
  group: null,
  subject: null,
  teacher: null,
  classroom: null,
  day_of_week: 1,
  lesson_number: 1,
  semester: 1,
  academic_year: new Date().getFullYear(),
  week_type: 'all',
  start_date: new Date().toISOString().split('T')[0],
  end_date: null
})

const dayOptions = [
  { title: 'Понедельник', value: 1 },
  { title: 'Вторник', value: 2 },
  { title: 'Среда', value: 3 },
  { title: 'Четверг', value: 4 },
  { title: 'Пятница', value: 5 },
  { title: 'Суббота', value: 6 }
]

const semesterOptions = [
  { title: 'Осенний', value: 1 },
  { title: 'Весенний', value: 2 }
]

const weekTypeOptions = [
  { title: 'Все недели', value: 'all' },
  { title: 'Чётная', value: 'odd' },
  { title: 'Нечётная', value: 'even' }
]

const headers = [
  { title: 'Группа', key: 'group_name' },
  { title: 'Дисциплина', key: 'subject_name' },
  { title: 'Преподаватель', key: 'teacher_name' },
  { title: 'Кабинет', key: 'classroom_info' },
  { title: 'День', key: 'day_of_week_display' },
  { title: 'Пара', key: 'lesson_number', align: 'center' },
  { title: 'Семестр', key: 'semester_display' },
  { title: 'Учебный год', key: 'academic_year', align: 'center' },
  { title: 'Тип недели', key: 'week_type' },
  { title: 'Дата начала', key: 'start_date' },
  { title: 'Дата окончания', key: 'end_date' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' }
]

const fetchSchedules = async () => {
  const params = {}
  if (filters.group_id) params.group = filters.group_id
  if (filters.teacher_id) params.teacher = filters.teacher_id
  if (filters.day_of_week) params.day_of_week = filters.day_of_week
  if (filters.semester) params.semester = filters.semester
  
  await schedule.fetchSchedules(params)
}

const editSchedule = (scheduleItem) => {
  editingSchedule.value = scheduleItem
  Object.assign(scheduleForm, {
    group: scheduleItem.group,
    subject: scheduleItem.subject,
    teacher: scheduleItem.teacher,
    classroom: scheduleItem.classroom,
    day_of_week: scheduleItem.day_of_week,
    lesson_number: scheduleItem.lesson_number,
    semester: scheduleItem.semester,
    academic_year: scheduleItem.academic_year,
    week_type: scheduleItem.week_type || 'all',
    start_date: scheduleItem.start_date?.split('T')[0] || new Date().toISOString().split('T')[0],
    end_date: scheduleItem.end_date?.split('T')[0] || null
  })
  showDialog.value = true
}

const saveSchedule = async () => {
  saving.value = true
  try {
    const result = editingSchedule.value 
      ? await schedule.updateSchedule(editingSchedule.value.schedule_id, scheduleForm)
      : await schedule.createSchedule(scheduleForm)
    
    if (result.success) {
      closeDialog()
      await fetchSchedules()
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

const deleteSchedule = async (id) => {
  if (confirm('Вы уверены, что хотите удалить это занятие?')) {
    const result = await schedule.deleteSchedule(id)
    if (result.success) {
      await fetchSchedules()
    } else {
      alert('Ошибка удаления: ' + JSON.stringify(result.error))
    }
  }
}

const closeDialog = () => {
  showDialog.value = false
  editingSchedule.value = null
  Object.assign(scheduleForm, {
    group: null,
    subject: null,
    teacher: null,
    classroom: null,
    day_of_week: 1,
    lesson_number: 1,
    semester: 1,
    academic_year: new Date().getFullYear(),
    week_type: 'all',
    start_date: new Date().toISOString().split('T')[0],
    end_date: null
  })
}

onMounted(async () => {
  try {
    await Promise.all([
      fetchSchedules(),
      groups.fetchGroups(),
      teachers.fetchTeachers(),
      subjects.fetchSubjects(),
      classrooms.fetchClassrooms()
    ])
  } catch (error) {
    console.error('Ошибка загрузки данных:', error)
  }
})
</script>