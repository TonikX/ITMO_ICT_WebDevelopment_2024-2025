<template>
  <v-container>
    <v-card>
      <v-card-title>
        <span class="text-h5">Отчеты и ведомости</span>
      </v-card-title>

      <v-card-text>
        <v-tabs v-model="activeTab">
          <v-tab value="performance">Ведомость успеваемости</v-tab>
          <v-tab value="statistics">Статистика</v-tab>
        </v-tabs>

        <v-window v-model="activeTab" class="mt-4">
          <!-- Вкладка 1: Ведомость успеваемости -->
          <v-window-item value="performance">
            <v-card variant="outlined">
              <v-card-text>
                <v-form @submit.prevent="generatePerformanceReport">
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-select
                        v-model="reportForm.group_id"
                        :items="groups.groups.value"
                        item-title="group_name"
                        item-value="group_id"
                        label="Группа*"
                        required
                        :loading="groups.isLoading.value"
                        :disabled="groups.isLoading.value || groups.groups.value.length === 0"
                      />
                      <div v-if="groups.groups.value.length === 0" class="text-caption text-red mt-1">
                        Нет доступных групп. Сначала создайте группы в системе.
                      </div>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-select
                        v-model="reportForm.semester"
                        :items="semesterOptions"
                        label="Семестр*"
                        required
                      />
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="reportForm.academic_year"
                        label="Учебный год*"
                        type="number"
                        min="2000"
                        max="2100"
                        required
                      />
                    </v-col>
                  </v-row>
                  <v-btn 
                    color="primary" 
                    type="submit" 
                    :loading="loading"
                    :disabled="!reportForm.group_id"
                  >
                    Сформировать отчет
                  </v-btn>
                </v-form>

                <!-- Результаты отчета -->
                <div v-if="performanceReport" class="mt-6">
                  <v-card>
                    <v-card-title>
                      Ведомость успеваемости группы {{ performanceReport.group?.name || 'Неизвестная группа' }}
                    </v-card-title>
                    <v-card-text>
                      <!-- Общая статистика -->
                      <div v-if="performanceReport.statistics" class="mb-6">
                        <v-row>
                          <v-col cols="12" md="3" v-for="stat in generalStats" :key="stat.title">
                            <v-card>
                              <v-card-text class="text-center">
                                <div class="text-h6">{{ stat.value }}</div>
                                <div class="text-caption">{{ stat.title }}</div>
                              </v-card-text>
                            </v-card>
                          </v-col>
                        </v-row>
                      </div>

                      <!-- Статистика по предметам -->
                      <div v-if="performanceReport.subject_stats && performanceReport.subject_stats.length > 0">
                        <h4 class="text-h6 mb-4">Статистика по предметам:</h4>
                        <v-table>
                          <thead>
                            <tr>
                              <th>Дисциплина</th>
                              <th>Средний балл</th>
                              <th>Всего оценок</th>
                              <th>5</th>
                              <th>4</th>
                              <th>3</th>
                              <th>2</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="subject in performanceReport.subject_stats" :key="subject.subject_id">
                              <td>{{ subject.subject_name }}</td>
                              <td>
                                <v-chip :color="getGradeColor(subject.average_grade)" size="small">
                                  {{ subject.average_grade?.toFixed(2) || '—' }}
                                </v-chip>
                              </td>
                              <td>{{ subject.total_grades || 0 }}</td>
                              <td>{{ subject.grade_distribution?.['5'] || 0 }}</td>
                              <td>{{ subject.grade_distribution?.['4'] || 0 }}</td>
                              <td>{{ subject.grade_distribution?.['3'] || 0 }}</td>
                              <td>{{ subject.grade_distribution?.['2'] || 0 }}</td>
                            </tr>
                          </tbody>
                        </v-table>
                      </div>
                      <div v-else class="text-center py-4">
                        <v-icon size="64" color="grey">mdi-book-open</v-icon>
                        <p class="mt-2">Нет данных по предметам</p>
                      </div>

                      <!-- Статистика по студентам -->
                      <div v-if="performanceReport.student_stats && performanceReport.student_stats.length > 0">
                        <h4 class="text-h6 mt-6 mb-4">Успеваемость студентов:</h4>
                        <v-table>
                          <thead>
                            <tr>
                              <th>Студент</th>
                              <th>Средний балл</th>
                              <th>Всего оценок</th>
                              <th>Долги</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="student in performanceReport.student_stats" :key="student.student_id">
                              <td>{{ student.student_name }}</td>
                              <td>
                                <v-chip 
                                  :color="student.average_grade ? getGradeColor(student.average_grade) : 'default'" 
                                  size="small"
                                >
                                  {{ student.average_grade ? student.average_grade.toFixed(2) : '—' }}
                                </v-chip>
                              </td>
                              <td>{{ student.total_grades || 0 }}</td>
                              <td>
                                <v-icon :color="student.has_debt ? 'error' : 'success'">
                                  {{ student.has_debt ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                                </v-icon>
                                <span class="ml-2">{{ student.has_debt ? 'Есть долги' : 'Нет долгов' }}</span>
                              </td>
                            </tr>
                          </tbody>
                        </v-table>
                      </div>
                      <div v-else class="text-center py-4">
                        <v-icon size="64" color="grey">mdi-account-group</v-icon>
                        <p class="mt-2">Нет данных о студентах</p>
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
                <div v-else-if="loading" class="text-center py-6">
                  <v-progress-circular indeterminate />
                  <p class="mt-2">Формирование отчета...</p>
                </div>
              </v-card-text>
            </v-card>
          </v-window-item>

          <!-- Вкладка 2: Статистика -->
          <v-window-item value="statistics">
            <v-card variant="outlined">
              <v-card-text>
                <v-btn color="primary" @click="loadStatistics" :loading="loading">
                  Загрузить статистику
                </v-btn>

                <div v-if="dashboardStats" class="mt-6">
                  <v-row>
                    <!-- Карточки статистики -->
                    <v-col cols="12" md="3" v-for="stat in dashboardCards" :key="stat.title">
                      <v-card>
                        <v-card-text class="text-center">
                          <v-icon size="48" :color="stat.color" class="mb-2">
                            {{ stat.icon }}
                          </v-icon>
                          <div class="text-h4">{{ stat.value }}</div>
                          <div class="text-caption">{{ stat.title }}</div>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>

                  <!-- Статусы студентов -->
                  <v-row class="mt-6">
                    <v-col cols="12" md="6">
                      <v-card>
                        <v-card-title>Статусы студентов</v-card-title>
                        <v-card-text>
                          <v-list v-if="dashboardStats.students">
                            <v-list-item v-if="dashboardStats.students.active !== undefined">
                              <v-list-item-title>Активных</v-list-item-title>
                              <v-list-item-subtitle>{{ dashboardStats.students.active }}</v-list-item-subtitle>
                            </v-list-item>
                            <v-list-item v-if="dashboardStats.students.inactive !== undefined">
                              <v-list-item-title>Неактивных</v-list-item-title>
                              <v-list-item-subtitle>{{ dashboardStats.students.inactive }}</v-list-item-subtitle>
                            </v-list-item>
                            <v-list-item v-if="dashboardStats.students.expelled !== undefined">
                              <v-list-item-title>Отчисленных</v-list-item-title>
                              <v-list-item-subtitle>{{ dashboardStats.students.expelled }}</v-list-item-subtitle>
                            </v-list-item>
                            <v-list-item v-if="dashboardStats.students.academic_leave !== undefined">
                              <v-list-item-title>В академе</v-list-item-title>
                              <v-list-item-subtitle>{{ dashboardStats.students.academic_leave }}</v-list-item-subtitle>
                            </v-list-item>
                          </v-list>
                          <div v-else class="text-center py-4">
                            <p>Нет данных о статусах студентов</p>
                          </div>
                        </v-card-text>
                      </v-card>
                    </v-col>
                    
                    <!-- Статистика по группам -->
                    <v-col cols="12" md="6">
                      <v-card>
                        <v-card-title>Статистика по группам</v-card-title>
                        <v-card-text>
                          <v-list v-if="groups.groups.value.length > 0">
                            <v-list-item v-for="group in groups.groups.value.slice(0, 5)" :key="group.group_id">
                              <v-list-item-title>{{ group.group_name }}</v-list-item-title>
                              <v-list-item-subtitle>{{ group.course }} курс • {{ group.student_count || 0 }} студентов</v-list-item-subtitle>
                            </v-list-item>
                          </v-list>
                          <div v-else class="text-center py-4">
                            <p>Нет данных о группах</p>
                          </div>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>
                <div v-else-if="loading" class="text-center py-6">
                  <v-progress-circular indeterminate />
                  <p class="mt-2">Загрузка статистики...</p>
                </div>
                <div v-else class="text-center py-6">
                  <v-icon size="64" color="grey">mdi-chart-bar</v-icon>
                  <p class="mt-2">Нажмите "Загрузить статистику" для получения данных</p>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useQueries } from '@/composables/useQueries'
import { useGroups } from '@/composables/useGroups'

const queries = useQueries()
const groups = useGroups()

const activeTab = ref('performance')
const loading = ref(false)
const performanceReport = ref(null)
const dashboardStats = ref(null)

const reportForm = reactive({
  group_id: null,
  semester: 1,
  academic_year: new Date().getFullYear()
})

const semesterOptions = [
  { title: 'Осенний', value: 1 },
  { title: 'Весенний', value: 2 }
]

const generalStats = computed(() => {
  if (!performanceReport.value || !performanceReport.value.statistics) return []
  
  const stats = performanceReport.value.statistics
  return [
    { title: 'Всего студентов', value: stats.total_students || 0 },
    { title: 'С оценками', value: stats.students_with_grades || 0 },
    { title: 'Средний балл группы', value: stats.group_average_grade ? stats.group_average_grade.toFixed(2) : '—' },
    { title: 'С долгами', value: stats.students_with_debt || 0 }
  ]
})

const dashboardCards = computed(() => {
  if (!dashboardStats.value) return []
  
  return [
    { 
      title: 'Всего студентов', 
      value: dashboardStats.value.students?.total || 0,
      icon: 'mdi-account-group',
      color: 'blue'
    },
    { 
      title: 'Активных студентов', 
      value: dashboardStats.value.students?.active || 0,
      icon: 'mdi-account-check',
      color: 'green'
    },
    { 
      title: 'Преподавателей', 
      value: dashboardStats.value.teachers?.total || 0,
      icon: 'mdi-account-tie',
      color: 'orange'
    },
    { 
      title: 'Групп', 
      value: dashboardStats.value.groups?.total || 0,
      icon: 'mdi-account-multiple',
      color: 'purple'
    }
  ]
})

const getGradeColor = (grade) => {
  if (!grade || grade === 0) return 'default'
  if (grade >= 4.5) return 'success'
  if (grade >= 3.5) return 'warning'
  return 'error'
}

const generatePerformanceReport = async () => {
  if (!reportForm.group_id) {
    alert('Выберите группу для формирования отчета')
    return
  }
  
  loading.value = true
  performanceReport.value = null
  
  try {
    const result = await queries.getGroupPerformanceReport(reportForm)
    if (result.success) {
      performanceReport.value = result.data
    } else {
      console.error('Ошибка формирования отчета:', result.error)
      alert('Не удалось сформировать отчет. Проверьте данные и попробуйте снова.')
    }
  } catch (error) {
    console.error('Ошибка формирования отчета:', error)
    alert('Произошла ошибка при формировании отчета.')
  } finally {
    loading.value = false
  }
}

const loadStatistics = async () => {
  loading.value = true
  dashboardStats.value = null
  
  try {
    const result = await queries.getDashboardStats()
    if (result.success) {
      dashboardStats.value = result.data
    } else {
      console.error('Ошибка загрузки статистики:', result.error)
      alert('Не удалось загрузить статистику.')
    }
  } catch (error) {
    console.error('Ошибка загрузки статистики:', error)
    alert('Произошла ошибка при загрузке статистики.')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await groups.fetchGroups()
})
</script>

<style scoped>
.v-alert {
  margin-top: 10px;
}
.text-red {
  color: #f44336;
}
</style>