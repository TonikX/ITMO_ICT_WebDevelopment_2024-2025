<template>
  <v-container>
    <v-card>
      <v-card-title>
        <span class="text-h5">Группы</span>
        <v-spacer />
        <v-btn color="primary" @click="addGroup">
          <v-icon start icon="mdi-plus" />
          Добавить группу
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="groups.groups.value"
          :loading="groups.isLoading.value"
          :items-per-page="10"
        >
          <template #item.student_count="{ item }">
            <v-chip size="small" color="primary">
              {{ item.student_count || 0 }}
            </v-chip>
          </template>

          <template #item.active_student_count="{ item }">
            <v-chip size="small" color="success">
              {{ item.active_student_count || 0 }}
            </v-chip>
          </template>

          <template #item.actions="{ item }">
            <v-btn 
              icon="mdi-pencil" 
              size="small" 
              variant="text" 
              @click="editGroup(item)" 
              title="Редактировать"
            />
            <v-btn 
              icon="mdi-delete" 
              size="small" 
              variant="text" 
              color="error" 
              @click="deleteGroup(item.group_id)"
              title="Удалить"
            />
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Диалог добавления/редактирования группы -->
    <v-dialog v-model="showDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ dialogTitle }}</span>
        </v-card-title>
        
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveGroup">
            <v-text-field 
              v-model="groupForm.group_name" 
              label="Название группы*" 
              :rules="[v => !!v || 'Название группы обязательно']"
              required 
            />
            <v-text-field 
              v-model="groupForm.course" 
              label="Курс*" 
              type="number" 
              min="1" 
              max="6" 
              :rules="[
                v => !!v || 'Курс обязателен',
                v => (v >= 1 && v <= 6) || 'Курс должен быть от 1 до 6'
              ]"
              required 
            />
            
            <v-alert 
              v-if="errorMessage" 
              type="error" 
              density="compact" 
              class="mt-4"
            >
              {{ errorMessage }}
            </v-alert>

            <v-card-actions class="mt-4">
              <v-spacer />
              <v-btn color="error" @click="closeDialog" :disabled="saving">
                Отмена
              </v-btn>
              <v-btn 
                color="primary" 
                type="submit" 
                :loading="saving"
                :disabled="!groupForm.group_name || !groupForm.course"
              >
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useGroups } from '@/composables/useGroups'

const groups = useGroups()
const showDialog = ref(false)
const editingGroup = ref(null)
const saving = ref(false)
const formRef = ref(null)
const errorMessage = ref('')

const headers = [
  { title: 'Название группы', key: 'group_name' },
  { title: 'Курс', key: 'course', align: 'center' },
  { title: 'Всего студентов', key: 'student_count', align: 'center' },
  { title: 'Активных', key: 'active_student_count', align: 'center' },
  { title: 'Действия', key: 'actions', sortable: false, align: 'end' }
]

const groupForm = reactive({
  group_name: '',
  course: 1
})

// Исправлено: правильный вычисляемый заголовок
const dialogTitle = computed(() => {
  return editingGroup.value ? 'Редактировать группу' : 'Добавить группу'
})

const addGroup = () => {
  editingGroup.value = null
  resetForm()
  showDialog.value = true
}

const editGroup = (group) => {
  editingGroup.value = group
  Object.assign(groupForm, {
    group_name: group.group_name,
    course: group.course
  })
  showDialog.value = true
}

const saveGroup = async () => {
  errorMessage.value = ''
  
  // Валидация формы
  if (!groupForm.group_name.trim()) {
    errorMessage.value = 'Название группы не может быть пустым'
    return
  }
  
  if (!groupForm.course || groupForm.course < 1 || groupForm.course > 6) {
    errorMessage.value = 'Курс должен быть от 1 до 6'
    return
  }
  
  saving.value = true
  
  try {
    const result = editingGroup.value
      ? await groups.updateGroup(editingGroup.value.group_id, groupForm)
      : await groups.createGroup(groupForm)
    
    if (result.success) {
      closeDialog()
      await groups.fetchGroups()
    } else {
      // Отображаем ошибку от сервера
      errorMessage.value = formatErrorMessage(result.error)
    }
  } catch (error) {
    console.error('Ошибка при сохранении группы:', error)
    errorMessage.value = 'Произошла ошибка при сохранении'
  } finally {
    saving.value = false
  }
}

const formatErrorMessage = (error) => {
  if (typeof error === 'string') return error
  if (error && typeof error === 'object') {
    // Обработка ошибок Django REST framework
    if (error.non_field_errors) {
      return Array.isArray(error.non_field_errors) 
        ? error.non_field_errors.join(', ') 
        : error.non_field_errors
    }
    if (error.detail) return error.detail
    
    // Собираем ошибки полей
    const fieldErrors = []
    for (const [field, messages] of Object.entries(error)) {
      if (Array.isArray(messages)) {
        fieldErrors.push(`${field}: ${messages.join(', ')}`)
      } else {
        fieldErrors.push(`${field}: ${messages}`)
      }
    }
    return fieldErrors.join('; ')
  }
  return 'Неизвестная ошибка'
}

const deleteGroup = async (id) => {
  if (confirm('Вы уверены, что хотите удалить группу?')) {
    const result = await groups.deleteGroup(id)
    if (result.success) {
      await groups.fetchGroups()
    } else {
      alert('Ошибка удаления: ' + formatErrorMessage(result.error))
    }
  }
}

const resetForm = () => {
  groupForm.group_name = ''
  groupForm.course = 1
  errorMessage.value = ''
  if (formRef.value) {
    formRef.value.resetValidation()
  }
}

const closeDialog = () => {
  showDialog.value = false
  editingGroup.value = null
  resetForm()
}

onMounted(() => groups.fetchGroups())
</script>

<style scoped>
.v-data-table {
  margin-top: 20px;
}
</style>