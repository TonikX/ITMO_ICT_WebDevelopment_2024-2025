<template>
  <v-container>
    <v-card>
      <v-card-title>
        <span class="text-h5">Преподаватели</span>
        <v-spacer />
        <v-btn color="primary" @click="showDialog = true">
          <v-icon start icon="mdi-plus" />
          Добавить преподавателя
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Поиск -->
        <v-text-field
          v-model="search"
          label="Поиск по ФИО, должности"
          prepend-icon="mdi-magnify"
          clearable
          class="mb-4"
        />

        <!-- Таблица преподавателей -->
        <v-data-table
          :headers="headers"
          :items="teachers.teachers.value"
          :loading="teachers.isLoading.value"
          :search="search"
          items-per-page="10"
        >
          <template #item.classroom_info="{ item }">
            {{ item.classroom_info || 'Не назначен' }}
          </template>

          <template #item.actions="{ item }">
            <v-btn icon="mdi-pencil" size="small" variant="text" @click="editTeacher(item)" />
            <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="deleteTeacher(item.teacher_id)" />
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Диалог добавления/редактирования преподавателя -->
    <v-dialog v-model="showDialog" max-width="600px">
      <v-card>
        <v-card-title>
          {{ editingTeacher ? 'Редактировать преподавателя' : 'Добавить преподавателя' }}
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveTeacher">
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="teacherForm.last_name"
                  label="Фамилия*"
                  required
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="teacherForm.first_name"
                  label="Имя*"
                  required
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="teacherForm.patronymic"
                  label="Отчество"
                />
              </v-col>
            </v-row>

            <v-text-field
              v-model="teacherForm.position"
              label="Должность*"
              required
            />

            <v-text-field
              v-model="teacherForm.degree"
              label="Учёная степень"
            />

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="teacherForm.phone"
                  label="Телефон"
                  type="tel"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="teacherForm.email"
                  label="Email"
                  type="email"
                />
              </v-col>
            </v-row>

            <!-- Добавляем выбор аудитории -->
            <v-select
              v-model="teacherForm.classroom"
              :items="classrooms.classrooms.value"
              item-title="classroom_number"
              item-value="classroom_id"
              label="Закрепленный кабинет"
              clearable
              :loading="classrooms.isLoading.value"
              hint="Выберите кабинет, закрепленный за преподавателем"
              persistent-hint
            />

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
import { useTeachers } from '@/composables/useTeachers'
import { useClassrooms } from '@/composables/useClassrooms'

const teachers = useTeachers()
const classrooms = useClassrooms()

const search = ref('')
const showDialog = ref(false)
const editingTeacher = ref(null)
const saving = ref(false)

const teacherForm = reactive({
  last_name: '',
  first_name: '',
  patronymic: '',
  position: 'Преподаватель',
  degree: '',
  phone: '',
  email: '',
  classroom: null
})

const headers = [
  { title: 'ФИО', key: 'full_name' },
  { title: 'Должность', key: 'position' },
  { title: 'Учёная степень', key: 'degree' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Email', key: 'email' },
  { title: 'Кабинет', key: 'classroom_info' },
  { title: 'Дисциплин', key: 'subject_count', align: 'center' },
  { title: 'Групп', key: 'group_count', align: 'center' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' }
]

const editTeacher = (teacher) => {
  editingTeacher.value = teacher
  Object.assign(teacherForm, {
    last_name: teacher.last_name,
    first_name: teacher.first_name,
    patronymic: teacher.patronymic || '',
    position: teacher.position,
    degree: teacher.degree || '',
    phone: teacher.phone || '',
    email: teacher.email || '',
    classroom: teacher.classroom
  })
  showDialog.value = true
}

const saveTeacher = async () => {
  saving.value = true
  try {
    if (editingTeacher.value) {
      await teachers.updateTeacher(editingTeacher.value.teacher_id, teacherForm)
    } else {
      await teachers.createTeacher(teacherForm)
    }
    closeDialog()
    await teachers.fetchTeachers()
  } catch (error) {
    console.error('Ошибка сохранения:', error)
  } finally {
    saving.value = false
  }
}

const deleteTeacher = async (id) => {
  if (confirm('Вы уверены, что хотите удалить преподавателя?')) {
    await teachers.deleteTeacher(id)
    await teachers.fetchTeachers()
  }
}

const closeDialog = () => {
  showDialog.value = false
  editingTeacher.value = null
  Object.assign(teacherForm, {
    last_name: '',
    first_name: '',
    patronymic: '',
    position: 'Преподаватель',
    degree: '',
    phone: '',
    email: '',
    classroom: null
  })
}

onMounted(async () => {
  await Promise.all([
    teachers.fetchTeachers(),
    classrooms.fetchClassrooms()
  ])
})
</script>