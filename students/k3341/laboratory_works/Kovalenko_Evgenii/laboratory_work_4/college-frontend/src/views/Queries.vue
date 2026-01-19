<template>
  <v-container>
    <v-card>
      <v-card-title>Специальные запросы</v-card-title>
      <v-card-text>
        <v-tabs v-model="tab">
          <v-tab value="1">Предмет в группе</v-tab>
          <v-tab value="2">Преподаватели группы</v-tab>
          <v-tab value="3">Группы преподавателя</v-tab>
          <v-tab value="4">Расписание группы</v-tab>
          <v-tab value="5">Статистика по курсу</v-tab>
        </v-tabs>
        
        <v-window v-model="tab" class="mt-4">
          <!-- Запрос 1: Какой предмет будет в заданной группе в заданный день недели на заданном уроке? -->
          <v-window-item value="1">
            <v-form @submit.prevent="executeQuery1" class="mt-4">
              <v-row>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="query1.group_id"
                    :items="groups.groups.value"
                    label="Группа"
                    item-title="group_name"
                    item-value="group_id"
                    required
                    :loading="groups.isLoading.value"
                    :disabled="groups.isLoading.value"
                  />
                </v-col>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="query1.day_of_week"
                    :items="days"
                    label="День недели"
                    item-title="title"
                    item-value="value"
                    required
                  />
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="query1.lesson_number"
                    label="Номер пары"
                    type="number"
                    min="1"
                    max="8"
                    required
                  />
                </v-col>
              </v-row>
              <v-btn 
                type="submit" 
                color="primary"
                :loading="queries.isLoading.value"
                :disabled="!query1.group_id || !query1.day_of_week || !query1.lesson_number"
              >
                Выполнить
              </v-btn>
            </v-form>
            
            <div v-if="queries.error.value" class="mt-4">
              <v-alert type="error">
                {{ queries.error.value }}
              </v-alert>
            </div>
            
            <v-data-table
              v-if="query1Result && query1Result.length > 0"
              :headers="queryHeaders"
              :items="query1Result"
              class="mt-4"
            >
              <template #no-data>
                <div class="text-center py-4">
                  <p>Введите параметры и нажмите "Выполнить"</p>
                </div>
              </template>
            </v-data-table>
            <div v-else-if="query1Result && query1Result.length === 0" class="text-center py-6">
              <v-icon size="64" color="grey">mdi-calendar-remove</v-icon>
              <p class="mt-2">Занятий не найдено</p>
            </div>
          </v-window-item>
          
          <!-- Запрос 2: Кто из преподавателей преподает в заданной группе? -->
          <v-window-item value="2">
            <v-form @submit.prevent="executeQuery2" class="mt-4">
              <v-row>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="query2.group_id"
                    :items="groups.groups.value"
                    label="Группа"
                    item-title="group_name"
                    item-value="group_id"
                    required
                    :loading="groups.isLoading.value"
                    :disabled="groups.isLoading.value"
                  />
                </v-col>
              </v-row>
              <v-btn 
                type="submit" 
                color="primary"
                :loading="queries.isLoading.value"
                :disabled="!query2.group_id"
              >
                Выполнить
              </v-btn>
            </v-form>
            
            <div v-if="queries.error.value" class="mt-4">
              <v-alert type="error">
                {{ queries.error.value }}
              </v-alert>
            </div>
            
            <div v-if="query2Result && query2Result.length > 0">
              <!-- Проверяем формат данных -->
              <div v-if="isNewFormat(query2Result[0])" class="mt-4">
                <v-data-table
                  :headers="teacherHeadersNew"
                  :items="query2Result"
                  class="mt-4"
                >
                  <template #item.teacher_name="{ item }">
                    {{ item.teacher_name || 'Не указано' }}
                  </template>
                  <template #item.position="{ item }">
                    {{ item.position || 'Не указано' }}
                  </template>
                  <template #item.subject_name="{ item }">
                    {{ item.subject_name || 'Не указано' }}
                  </template>
                  <template #item.subject_code="{ item }">
                    {{ item.subject_code || 'Не указано' }}
                  </template>
                </v-data-table>
              </div>
              <div v-else class="mt-4">
                <v-data-table
                  :headers="teacherHeadersOld"
                  :items="query2Result"
                  class="mt-4"
                >
                  <template #item.full_name="{ item }">
                    {{ item.full_name || 'Не указано' }}
                  </template>
                  <template #item.position="{ item }">
                    {{ item.position || 'Не указано' }}
                  </template>
                  <template #item.classroom_info="{ item }">
                    {{ item.classroom_info || 'Не указано' }}
                  </template>
                </v-data-table>
                <v-alert type="info" class="mt-4">
                  Для просмотра предметов, которые преподает преподаватель, создайте расписание для этой группы.
                </v-alert>
              </div>
            </div>
            <div v-else-if="query2Result && query2Result.length === 0" class="text-center py-6">
              <v-icon size="64" color="grey">mdi-account-question</v-icon>
              <p class="mt-2">Для этой группы нет преподавателей или расписания</p>
            </div>
          </v-window-item>
          
          <!-- Запрос 3: В каких группах преподает заданный предмет заданный преподаватель? -->
          <v-window-item value="3">
            <v-form @submit.prevent="executeQuery3" class="mt-4">
              <v-row>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="query3.teacher_id"
                    :items="teachers.teachers.value"
                    label="Преподаватель"
                    item-title="full_name"
                    item-value="teacher_id"
                    required
                    :loading="teachers.isLoading.value"
                    :disabled="teachers.isLoading.value"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="query3.subject_id"
                    :items="subjects.subjects.value"
                    label="Дисциплина"
                    item-title="subject_name"
                    item-value="subject_id"
                    required
                    :loading="subjects.isLoading.value"
                    :disabled="subjects.isLoading.value"
                  />
                </v-col>
              </v-row>
              <v-btn 
                type="submit" 
                color="primary"
                :loading="queries.isLoading.value"
                :disabled="!query3.teacher_id || !query3.subject_id"
              >
                Выполнить
              </v-btn>
            </v-form>
            
            <div v-if="queries.error.value" class="mt-4">
              <v-alert type="error">
                {{ queries.error.value }}
              </v-alert>
            </div>
            
            <v-data-table
              v-if="query3Result && query3Result.length > 0"
              :headers="groupHeaders"
              :items="query3Result"
              class="mt-4"
            >
              <template #no-data>
                <div class="text-center py-4">
                  <p>Введите параметры и нажмите "Выполнить"</p>
                </div>
              </template>
            </v-data-table>
            <div v-else-if="query3Result && query3Result.length === 0" class="text-center py-6">
              <v-icon size="64" color="grey">mdi-account-group</v-icon>
              <p class="mt-2">Группы не найдены</p>
            </div>
          </v-window-item>
          
          <!-- Запрос 4: Расписание на заданный день недели для указанной группы -->
          <v-window-item value="4">
            <v-form @submit.prevent="executeQuery4" class="mt-4">
              <v-row>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="query4.group_id"
                    :items="groups.groups.value"
                    label="Группа"
                    item-title="group_name"
                    item-value="group_id"
                    required
                    :loading="groups.isLoading.value"
                    :disabled="groups.isLoading.value"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="query4.day_of_week"
                    :items="days"
                    label="День недели"
                    item-title="title"
                    item-value="value"
                    required
                  />
                </v-col>
              </v-row>
              <v-btn 
                type="submit" 
                color="primary"
                :loading="queries.isLoading.value"
                :disabled="!query4.group_id || !query4.day_of_week"
              >
                Выполнить
              </v-btn>
            </v-form>
            
            <div v-if="queries.error.value" class="mt-4">
              <v-alert type="error">
                {{ queries.error.value }}
              </v-alert>
            </div>
            
            <v-data-table
              v-if="query4Result && query4Result.length > 0"
              :headers="scheduleHeaders"
              :items="query4Result"
              class="mt-4"
            >
              <template #no-data>
                <div class="text-center py-4">
                  <p>Введите параметры и нажмите "Выполнить"</p>
                </div>
              </template>
            </v-data-table>
            <div v-else-if="query4Result && query4Result.length === 0" class="text-center py-6">
              <v-icon size="64" color="grey">mdi-calendar-blank</v-icon>
              <p class="mt-2">Расписание не найдено</p>
            </div>
          </v-window-item>
          
          <!-- Запрос 5: Сколько студентов обучается на каждом курсе -->
          <v-window-item value="5">
            <v-form @submit.prevent="executeQuery5" class="mt-4">
              <v-row>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="query5.course"
                    :items="courseOptions"
                    label="Курс"
                    item-title="title"
                    item-value="value"
                    required
                  />
                </v-col>
              </v-row>
              <v-btn 
                type="submit" 
                color="primary"
                :loading="queries.isLoading.value"
                :disabled="!query5.course"
              >
                Выполнить
              </v-btn>
            </v-form>
            
            <div v-if="queries.error.value" class="mt-4">
              <v-alert type="error">
                {{ queries.error.value }}
              </v-alert>
            </div>
            
            <!-- Результат для запроса 5 -->
            <v-card v-if="query5Result" class="mt-4">
              <v-card-title>
                <v-icon start icon="mdi-school" />
                Статистика по курсу
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Курс</v-list-item-title>
                    <v-list-item-subtitle class="text-right">
                      {{ query5Result.course || '—' }}
                    </v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-divider />
                  
                  <v-list-item>
                    <v-list-item-title>Всего активных студентов</v-list-item-title>
                    <v-list-item-subtitle class="text-right">
                      <v-chip color="primary" size="small">
                        {{ query5Result.total_active_students || 0 }}
                      </v-chip>
                    </v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-title>Количество групп</v-list-item-title>
                    <v-list-item-subtitle class="text-right">
                      <v-chip color="secondary" size="small">
                        {{ query5Result.groups_count || 0 }}
                      </v-chip>
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
                
                <!-- Детальная информация по группам -->
                <v-card v-if="query5Result.groups && query5Result.groups.length > 0" class="mt-4" variant="outlined">
                  <v-card-title class="text-subtitle-1">
                    <v-icon start icon="mdi-account-multiple" size="small" />
                    Группы на курсе
                  </v-card-title>
                  <v-card-text>
                    <v-table>
                      <thead>
                        <tr>
                          <th>Группа</th>
                          <th class="text-center">Активных студентов</th>
                          <th class="text-center">Всего студентов</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="group in query5Result.groups" :key="group.group_id">
                          <td>{{ group.group_name }}</td>
                          <td class="text-center">
                            <v-chip color="success" size="small">
                              {{ group.active_students || 0 }}
                            </v-chip>
                          </td>
                          <td class="text-center">
                            <v-chip color="info" size="small">
                              {{ group.total_students || 0 }}
                            </v-chip>
                          </td>
                        </tr>
                      </tbody>
                    </v-table>
                  </v-card-text>
                </v-card>
                <div v-else class="text-center py-4">
                  <v-icon size="48" color="grey">mdi-account-group-off</v-icon>
                  <p class="mt-2">На этом курсе нет групп</p>
                </div>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQueries } from '@/composables/useQueries'
import { useGroups } from '@/composables/useGroups'
import { useTeachers } from '@/composables/useTeachers'
import { useSubjects } from '@/composables/useSubjects'

const queries = useQueries()
const groups = useGroups()
const teachers = useTeachers()
const subjects = useSubjects()

const tab = ref('1')

// данные для запросов
const query1 = ref({ group_id: null, day_of_week: null, lesson_number: 1 })
const query2 = ref({ group_id: null })
const query3 = ref({ teacher_id: null, subject_id: null })
const query4 = ref({ group_id: null, day_of_week: null })
const query5 = ref({ course: null })

const query1Result = ref(null)
const query2Result = ref(null)
const query3Result = ref(null)
const query4Result = ref(null)
const query5Result = ref(null)

const days = [
  { title: 'Понедельник', value: 1 },
  { title: 'Вторник', value: 2 },
  { title: 'Среда', value: 3 },
  { title: 'Четверг', value: 4 },
  { title: 'Пятница', value: 5 },
  { title: 'Суббота', value: 6 }
]

const courseOptions = [
  { title: '1 курс', value: 1 },
  { title: '2 курс', value: 2 },
  { title: '3 курс', value: 3 },
  { title: '4 курс', value: 4 },
  { title: '5 курс', value: 5 },
  { title: '6 курс', value: 6 }
]

const queryHeaders = [
  { title: 'Предмет', key: 'subject_name' },
  { title: 'Преподаватель', key: 'teacher_name' },
  { title: 'Кабинет', key: 'classroom_info' },
  { title: 'Номер пары', key: 'lesson_number', align: 'center' },
  { title: 'Семестр', key: 'semester_display' }
]

const teacherHeadersNew = [
  { title: 'Преподаватель', key: 'teacher_name' },
  { title: 'Должность', key: 'position' },
  { title: 'Предмет', key: 'subject_name' },
  { title: 'Код предмета', key: 'subject_code' }
]

const teacherHeadersOld = [
  { title: 'Преподаватель', key: 'full_name' },
  { title: 'Должность', key: 'position' },
  { title: 'Кабинет', key: 'classroom_info' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Email', key: 'email' }
]

const groupHeaders = [
  { title: 'Группа', key: 'group_name' },
  { title: 'Курс', key: 'course', align: 'center' }
]

const scheduleHeaders = [
  { title: 'Пара', key: 'lesson_number', align: 'center' },
  { title: 'Предмет', key: 'subject_name' },
  { title: 'Преподаватель', key: 'teacher_name' },
  { title: 'Кабинет', key: 'classroom_info' },
  { title: 'Семестр', key: 'semester_display' },
  { title: 'Тип недели', key: 'week_type' }
]

// Функция для определения формата данных
const isNewFormat = (item) => {
  // Проверяем, есть ли поле subject_name в данных
  return item && item.hasOwnProperty('subject_name')
}

// Функции выполнения запросов
const executeQuery1 = async () => {
  query1Result.value = null
  queries.clearResults()
  const result = await queries.scheduleQuery(query1.value)
  if (result.success) {
    query1Result.value = Array.isArray(result.data) ? result.data : [result.data]
    console.log('Результат запроса 1:', query1Result.value)
  } else {
    console.error('Ошибка запроса 1:', result.error)
  }
}

const executeQuery2 = async () => {
  query2Result.value = null
  queries.clearResults()
  const result = await queries.getTeachersByGroup(query2.value)
  if (result.success) {
    query2Result.value = Array.isArray(result.data) ? result.data : [result.data]
    console.log('Результат запроса 2 (сырые данные):', result.data)
    console.log('Результат запроса 2 (обработанные):', query2Result.value)
    
    // Если данных нет или они в неправильном формате, попробуем получить данные через расписание
    if (!query2Result.value || query2Result.value.length === 0 || !isNewFormat(query2Result.value[0])) {
      console.log('Данные в старом формате или пустые. Пробуем получить через расписание...')
      // Создаем временный запрос для получения расписания
      const tempResult = await queries.getGroupSchedule({
        group_id: query2.value.group_id,
        day_of_week: 1 // Понедельник для теста
      })
      
      if (tempResult.success && tempResult.data && tempResult.data.length > 0) {
        // Извлекаем уникальных преподавателей с предметами из расписания
        const uniqueTeachers = []
        const seen = new Set()
        
        tempResult.data.forEach(schedule => {
          const key = `${schedule.teacher}_${schedule.subject}`
          if (!seen.has(key)) {
            seen.add(key)
            uniqueTeachers.push({
              teacher_name: schedule.teacher_name,
              position: 'Преподаватель', // По умолчанию
              subject_name: schedule.subject_name,
              subject_code: schedule.subject || 'N/A'
            })
          }
        })
        
        if (uniqueTeachers.length > 0) {
          query2Result.value = uniqueTeachers
          console.log('Получены данные через расписание:', query2Result.value)
        }
      }
    }
  } else {
    console.error('Ошибка запроса 2:', result.error)
  }
}

const executeQuery3 = async () => {
  query3Result.value = null
  queries.clearResults()
  const result = await queries.getGroupsBySubjectTeacher(query3.value)
  if (result.success) {
    query3Result.value = Array.isArray(result.data) ? result.data : [result.data]
    console.log('Результат запроса 3:', query3Result.value)
  } else {
    console.error('Ошибка запроса 3:', result.error)
  }
}

const executeQuery4 = async () => {
  query4Result.value = null
  queries.clearResults()
  const result = await queries.getGroupSchedule(query4.value)
  if (result.success) {
    query4Result.value = Array.isArray(result.data) ? result.data : [result.data]
    console.log('Результат запроса 4:', query4Result.value)
  } else {
    console.error('Ошибка запроса 4:', result.error)
  }
}

const executeQuery5 = async () => {
  query5Result.value = null
  queries.clearResults()
  const result = await queries.getStudentsByCourse(query5.value.course)
  if (result.success) {
    query5Result.value = result.data
    console.log('Результат запроса 5:', result.data)
  } else {
    console.error('Ошибка запроса 5:', result.error)
  }
}

// Сброс результатов при смене вкладки
const resetAllQueries = () => {
  query1Result.value = null
  query2Result.value = null
  query3Result.value = null
  query4Result.value = null
  query5Result.value = null
  queries.clearResults()
}

onMounted(async () => {
  try {
    await Promise.all([
      groups.fetchGroups(),
      teachers.fetchTeachers(),
      subjects.fetchSubjects()
    ])
  } catch (error) {
    console.error('Ошибка загрузки данных:', error)
  }
})
</script>

<style scoped>
.v-data-table {
  margin-top: 20px;
}

.v-card {
  margin-top: 20px;
}
</style>