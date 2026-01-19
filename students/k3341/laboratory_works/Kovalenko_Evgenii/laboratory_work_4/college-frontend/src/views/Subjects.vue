<template>
  <v-container>
    <v-card>
      <v-card-title>
        <span class="text-h5">Дисциплины</span>
        <v-spacer />
        <v-btn color="primary" @click="showDialog = true">
          <v-icon start icon="mdi-plus" />
          Добавить дисциплину
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="subjects.subjects.value"
          :loading="subjects.isLoading.value"
          items-per-page="10"
        >
          <template #item.average_grade="{ item }">
            <v-chip v-if="item.average_grade" :color="getGradeColor(item.average_grade)" size="small">
              {{ item.average_grade }}
            </v-chip>
            <span v-else>—</span>
          </template>

          <template #item.actions="{ item }">
            <v-btn icon="mdi-pencil" size="small" variant="text" @click="editSubject(item)" />
            <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="deleteSubject(item.subject_id)" />
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Диалог -->
    <v-dialog v-model="showDialog" max-width="600px">
      <v-card>
        <v-card-title>{{ editingSubject ? 'Редактировать' : 'Добавить' }} дисциплину</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveSubject">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="subjectForm.subject_code" label="Код дисциплины*" required />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="subjectForm.subject_name" label="Название дисциплины*" required />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="subjectForm.hours_lecture" label="Лекционные часы*" type="number" min="0" required />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="subjectForm.hours_practice" label="Практические часы*" type="number" min="0" required />
              </v-col>
            </v-row>
            <!-- hours_total вычисляется на сервере, не отправляем -->
            
            <v-card-actions>
              <v-spacer />
              <v-btn color="error" @click="closeDialog">Отмена</v-btn>
              <v-btn color="primary" type="submit" :loading="saving">Сохранить</v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useSubjects } from '@/composables/useSubjects'

const subjects = useSubjects()
const showDialog = ref(false)
const editingSubject = ref(null)
const saving = ref(false)

const headers = [
  { title: 'Код дисциплины', key: 'subject_code' },
  { title: 'Название дисциплины', key: 'subject_name' },
  { title: 'Всего часов', key: 'hours_total', align: 'center' },
  { title: 'Лекции', key: 'hours_lecture', align: 'center' },
  { title: 'Практика', key: 'hours_practice', align: 'center' },
  { title: 'Преподавателей', key: 'teacher_count', align: 'center' },
  { title: 'Групп', key: 'group_count', align: 'center' },
  { title: 'Ср. оценка', key: 'average_grade', align: 'center' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' }
]

const subjectForm = reactive({
  subject_code: '',
  subject_name: '',
  hours_lecture: 36,
  hours_practice: 36
  // hours_total вычисляется сервером
})

const getGradeColor = (grade) => {
  if (grade >= 4.5) return 'success'
  if (grade >= 3.5) return 'warning'
  return 'error'
}

const editSubject = (subject) => {
  editingSubject.value = subject
  Object.assign(subjectForm, subject)
  showDialog.value = true
}

const saveSubject = async () => {
  saving.value = true
  try {
    if (editingSubject.value) {
      await subjects.updateSubject(editingSubject.value.subject_id, subjectForm)
    } else {
      await subjects.createSubject(subjectForm)
    }
    closeDialog()
    await subjects.fetchSubjects()
  } catch (error) {
    console.error('Ошибка:', error)
  } finally {
    saving.value = false
  }
}

const deleteSubject = async (id) => {
  if (confirm('Удалить дисциплину?')) {
    await subjects.deleteSubject(id)
    await subjects.fetchSubjects()
  }
}

const closeDialog = () => {
  showDialog.value = false
  editingSubject.value = null
  Object.assign(subjectForm, {
    subject_code: '',
    subject_name: '',
    hours_lecture: 36,
    hours_practice: 36
  })
}

onMounted(() => subjects.fetchSubjects())
</script>