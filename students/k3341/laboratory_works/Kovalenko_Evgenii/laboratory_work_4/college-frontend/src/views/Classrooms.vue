<template>
  <v-container>
    <v-card>
      <v-card-title>
        <span class="text-h5">Аудитории</span>
        <v-spacer />
        <v-btn color="primary" @click="showDialog = true">
          <v-icon start icon="mdi-plus" />
          Добавить аудиторию
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="classrooms.classrooms.value"
          :loading="classrooms.isLoading.value"
          items-per-page="10"
        >
          <template #item.is_occupied="{ item }">
            <v-icon :color="item.is_occupied ? 'error' : 'success'">
              {{ item.is_occupied ? 'mdi-close-circle' : 'mdi-check-circle' }}
            </v-icon>
            <span class="ml-2">{{ item.is_occupied ? 'Занята' : 'Свободна' }}</span>
          </template>

          <template #item.actions="{ item }">
            <v-btn icon="mdi-pencil" size="small" variant="text" @click="editClassroom(item)" />
            <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="deleteClassroom(item.classroom_id)" />
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Диалог -->
    <v-dialog v-model="showDialog" max-width="600px">
      <v-card>
        <v-card-title>{{ editingClassroom ? 'Редактировать' : 'Добавить' }} аудиторию</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="saveClassroom">
            <v-text-field v-model="classroomForm.classroom_number" label="Номер аудитории*" required />
            <v-text-field v-model="classroomForm.building" label="Корпус*" required />
            <v-text-field v-model="classroomForm.capacity" label="Вместимость" type="number" min="1" />
            <v-textarea v-model="classroomForm.equipment" label="Оборудование" rows="2" />
            
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
import { useClassrooms } from '@/composables/useClassrooms'

const classrooms = useClassrooms()
const showDialog = ref(false)
const editingClassroom = ref(null)
const saving = ref(false)

const headers = [
  { title: 'Номер аудитории', key: 'classroom_number' },
  { title: 'Корпус', key: 'building' },
  { title: 'Вместимость', key: 'capacity', align: 'center' },
  { title: 'Оборудование', key: 'equipment' },
  { title: 'Статус', key: 'is_occupied', align: 'center' },
  { title: 'Преподаватель', key: 'teacher_name' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' }
]

const classroomForm = reactive({
  classroom_number: '',
  building: '',
  capacity: 30,
  equipment: ''
})

const editClassroom = (classroom) => {
  editingClassroom.value = classroom
  Object.assign(classroomForm, classroom)
  showDialog.value = true
}

const saveClassroom = async () => {
  saving.value = true
  try {
    if (editingClassroom.value) {
      await classrooms.updateClassroom(editingClassroom.value.classroom_id, classroomForm)
    } else {
      await classrooms.createClassroom(classroomForm)
    }
    closeDialog()
    await classrooms.fetchClassrooms()
  } catch (error) {
    console.error('Ошибка:', error)
  } finally {
    saving.value = false
  }
}

const deleteClassroom = async (id) => {
  if (confirm('Удалить аудиторию?')) {
    await classrooms.deleteClassroom(id)
    await classrooms.fetchClassrooms()
  }
}

const closeDialog = () => {
  showDialog.value = false
  editingClassroom.value = null
  Object.assign(classroomForm, {
    classroom_number: '',
    building: '',
    capacity: 30,
    equipment: ''
  })
}

onMounted(() => classrooms.fetchClassrooms())
</script>