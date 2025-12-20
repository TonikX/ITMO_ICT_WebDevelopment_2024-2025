<template>
  <div class="group-students-view">
    <div class="header">
      <button @click="goBack" class="back-btn">← Назад к группам</button>
      <h1>Студенты группы</h1>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка данных...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadData" class="retry-btn">Повторить</button>
    </div>

    <div v-else class="content">
      <!-- Информация о группе -->
      <div class="group-info-card">
        <h2>{{ group.name || 'Загрузка...' }}</h2>
        <div class="group-details">
          <p><strong>Курс:</strong> {{ group.course_display || 'Н/Д' }}</p>
          <p><strong>Специальность:</strong> {{ group.specialty || 'Н/Д' }}</p>
          <p><strong>Куратор:</strong> {{ group.curator_name || 'Не назначен' }}</p>
          <p><strong>Год создания:</strong> {{ group.created_year || 'Н/Д' }}</p>
          <p><strong>Количество студентов:</strong> {{ students.length }}</p>
        </div>
      </div>

      <!-- Поиск и фильтры -->
      <div class="controls">
        <div class="search-box">
          <input
              v-model="searchQuery"
              @input="filterStudents"
              placeholder="Поиск по имени или фамилии..."
              class="search-input"
          >
        </div>

        <div class="filter-control">
          <label>Статус:</label>
          <select v-model="selectedStatus" @change="filterStudents">
            <option value="">Все статусы</option>
            <option value="active">Обучается</option>
            <option value="dropped">Отчислен</option>
            <option value="academic_leave">Академический отпуск</option>
            <option value="graduated">Выпустился</option>
          </select>
        </div>
      </div>

      <!-- Таблица студентов -->
      <div class="students-table-container">
        <div class="table-header">
          <h3>Список студентов ({{ filteredStudents.length }})</h3>
          <div class="status-summary">
            <span class="status-badge active">{{ activeCount }} активных</span>
            <span class="status-badge dropped">{{ droppedCount }} отчислено</span>
            <span class="status-badge academic">{{ academicCount }} в академе</span>
          </div>
        </div>

        <table class="students-table">
          <thead>
          <tr>
            <th @click="sortBy('surname')" class="sortable">
              ФИО
              <span v-if="sortField === 'surname'" class="sort-indicator">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
            </th>
            <th>Дата поступления</th>
            <th>Статус</th>
            <th>Действия</th>
          </tr>
          </thead>
          <tbody>
          <!-- В шаблоне измените строку 153 -->
          <tr v-for="student in sortedStudents" :key="student.id" :class="`status-${student.status}`">
            <td>
              <div class="student-name">
                <strong>{{ student.full_name }}</strong>
                <div class="student-id">
                  ID: {{ student.id }}
                </div>
              </div>
            </td>
            <td>
              {{ formatDate(student.enrollment_date) }}
            </td>
            <td>
                <span :class="`status-badge status-${student.status}`">
                  {{ student.status_display }}
                </span>
            </td>
            <td>
              <div class="action-buttons">
                <button
                    @click="viewStudentDetails(student)"
                    class="action-btn view-btn"
                    title="Просмотр"
                >
                  👁️
                </button>
                <button
                    @click="viewStudentGrades(student)"
                    class="action-btn grades-btn"
                    title="Оценки"
                    v-if="student.status === 'active'"
                >
                  📊
                </button>
                <button
                    @click="viewStudentStats(student)"
                    class="action-btn stats-btn"
                    title="Статистика"
                    v-if="student.status === 'active'"
                >
                  📈
                </button>
              </div>
            </td>
          </tr>

          <tr v-if="!filteredStudents.length">
            <td colspan="4" class="no-data">
              Студенты не найдены
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <!-- Экспорт данных -->
      <div class="export-section">
        <button @click="exportToCSV" class="export-btn">
          📥 Экспорт в CSV
        </button>
        <button @click="printList" class="print-btn">
          🖨️ Печать списка
        </button>
      </div>

      <!-- Модальное окно деталей студента -->
      <div v-if="selectedStudent" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Информация о студенте</h3>
            <button @click="closeModal" class="close-btn">×</button>
          </div>

          <div class="modal-body">
            <div class="student-details-modal">
              <div class="detail-row">
                <strong>ФИО:</strong>
                <span>{{ selectedStudent.full_name }}</span>
              </div>
              <div class="detail-row">
                <strong>Группа:</strong>
                <span>{{ group.name }}</span>
              </div>
              <div class="detail-row">
                <strong>Дата поступления:</strong>
                <span>{{ formatDate(selectedStudent.enrollment_date) }}</span>
              </div>
              <div class="detail-row">
                <strong>Статус:</strong>
                <span :class="`status-badge status-${selectedStudent.status}`">
                  {{ selectedStudent.status_display }}
                </span>
              </div>
              <div class="detail-row">
                <strong>Учетная запись:</strong>
                <span>{{ selectedStudent.user_account ? 'Есть' : 'Нет' }}</span>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="closeModal" class="btn-secondary">Закрыть</button>
            <button
                @click="viewStudentGrades(selectedStudent)"
                class="btn-primary"
                v-if="selectedStudent.status === 'active'"
            >
              Посмотреть оценки
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, computed, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import api from '@/api'

export default {
  name: 'GroupStudentsView',

  setup() {
    const route = useRoute()
    const router = useRouter()

    const groupId = ref(route.params.groupId)
    const loading = ref(true)
    const error = ref('')
    const group = ref({})
    const students = ref([])
    const selectedStudent = ref(null)

    // Фильтры и сортировка
    const searchQuery = ref('')
    const selectedStatus = ref('')
    const sortField = ref('surname')
    const sortDirection = ref('asc')

    // Загрузка данных
    const loadData = async () => {
      loading.value = true
      error.value = ''

      try {
        // Загружаем информацию о группе
        const groupResponse = await api.get(`groups/${groupId.value}/detail/`)
        group.value = groupResponse.data

        // Загружаем студентов группы
        const studentsResponse = await api.get(`groups/${groupId.value}/students/`)
        students.value = studentsResponse.data

      } catch (err) {
        console.error('Ошибка загрузки данных:', err)
        error.value = err.response?.data?.detail || 'Не удалось загрузить данные группы'
      } finally {
        loading.value = false
      }
    }

    // Фильтрация и сортировка
    const filteredStudents = computed(() => {
      let filtered = students.value

      // Фильтр по поиску
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(student =>
            student.full_name.toLowerCase().includes(query) ||
            student.surname.toLowerCase().includes(query) ||
            student.name.toLowerCase().includes(query)
        )
      }

      // Фильтр по статусу
      if (selectedStatus.value) {
        filtered = filtered.filter(student => student.status === selectedStatus.value)
      }

      return filtered
    })

    const sortedStudents = computed(() => {
      const sorted = [...filteredStudents.value]

      if (sortField.value === 'surname') {
        sorted.sort((a, b) => {
          const nameA = a.surname.toLowerCase()
          const nameB = b.surname.toLowerCase()
          return sortDirection.value === 'asc'
              ? nameA.localeCompare(nameB)
              : nameB.localeCompare(nameA)
        })
      }

      return sorted
    })

    const sortBy = (field) => {
      if (sortField.value === field) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortField.value = field
        sortDirection.value = 'asc'
      }
    }

    // Статистика
    const activeCount = computed(() => {
      return students.value.filter(s => s.status === 'active').length
    })

    const droppedCount = computed(() => {
      return students.value.filter(s => s.status === 'dropped').length
    })

    const academicCount = computed(() => {
      return students.value.filter(s => s.status === 'academic_leave').length
    })

    // Методы
    const formatDate = (dateString) => {
      if (!dateString) return 'Н/Д'
      return new Date(dateString).toLocaleDateString('ru-RU')
    }

    const filterStudents = () => {
      // Фильтрация происходит автоматически через computed
    }

    const viewStudentDetails = (student) => {
      selectedStudent.value = student
    }

    const viewStudentGrades = (student) => {
      router.push(`/students/${student.id}/grades`)
    }

    const viewStudentStats = (student) => {
      router.push(`/students/${student.id}/stats`)
    }

    const closeModal = () => {
      selectedStudent.value = null
    }

    const goBack = () => {
      router.push('/groups')
    }

    const exportToCSV = () => {
      const headers = ['ФИО', 'Дата поступления', 'Статус', 'ID']
      const csvContent = [
        headers.join(','),
        ...students.value.map(student => [
          `"${student.full_name}"`,
          student.enrollment_date,
          student.status_display,
          student.id
        ].join(','))
      ].join('\n')

      const blob = new Blob([csvContent], {type: 'text/csv;charset=utf-8;'})
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `group_${groupId.value}_students.csv`
      link.click()
    }

    const printList = () => {
      window.print()
    }

    // Инициализация
    onMounted(() => {
      loadData()
    })

    return {
      // Реактивные данные
      groupId,
      loading,
      error,
      group,
      students: students, // оставляем оригинальный массив
      selectedStudent,
      searchQuery,
      selectedStatus,
      sortField,
      sortDirection,

      // Вычисляемые свойства
      activeCount,
      droppedCount,
      academicCount,
      filteredStudents,
      sortedStudents: sortedStudents, // добавляем явно

      // Методы
      loadData,
      formatDate,
      filterStudents,
      sortBy,
      viewStudentDetails,
      viewStudentGrades,
      viewStudentStats,
      closeModal,
      goBack,
      exportToCSV,
      printList
    }
  }
}
</script>

<style scoped>
.group-students-view {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.back-btn {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
}

.back-btn:hover {
  background: #5a67d8;
}

h1 {
  color: #2c3e50;
  margin: 0;
}

/* Информация о группе */
.group-info-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.group-info-card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.group-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.group-details p {
  margin: 0;
  color: #666;
}

.group-details strong {
  color: #2c3e50;
  margin-right: 0.5rem;
}

/* Контролы */
.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.search-box {
  display: flex;
  flex: 1;
  position: relative;
  min-width: 300px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.filter-control {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 150px;
}

.filter-control label {
  font-weight: bold;
  font-size: 0.9rem;
  color: #666;
}

.filter-control select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  background: white;
}

/* Таблица */
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.table-header h3 {
  color: #2c3e50;
  margin: 0;
}

.status-summary {
  display: flex;
  gap: 0.5rem;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.dropped {
  background: #f8d7da;
  color: #721c24;
}

.status-badge.academic {
  background: #fff3cd;
  color: #856404;
}

.students-table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 2rem;
  padding: 1.5rem;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
}

.students-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #666;
  border-bottom: 2px solid #e2e8f0;
}

.students-table th.sortable {
  cursor: pointer;
  user-select: none;
}

.students-table th.sortable:hover {
  background: #e9ecef;
}

.sort-indicator {
  margin-left: 0.5rem;
  font-size: 0.8em;
}

.students-table td {
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.students-table tr:hover {
  background: #f8f9fa;
}

.students-table tr.status-dropped {
  background: #fff5f5;
}

.students-table tr.status-academic_leave {
  background: #fff9e6;
}

.students-table tr.status-graduated {
  background: #f0fff4;
}

/* Элементы таблицы */
.student-name strong {
  display: block;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.student-id {
  font-size: 0.85rem;
  color: #666;
}

/* Кнопки действий */
.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
  background: transparent;
  min-width: 40px;
}

.view-btn:hover {
  background: #e3f2fd;
  color: #1976d2;
}

.grades-btn:hover {
  background: #f3e5f5;
  color: #7b1fa2;
}

.stats-btn:hover {
  background: #e8f5e8;
  color: #388e3c;
}

.schedule-btn:hover {
  background: #fff3e0;
  color: #f57c00;
}

/* Экспорт */
.export-section {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.export-btn, .print-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.export-btn {
  background: #48bb78;
  color: white;
}

.print-btn {
  background: #667eea;
  color: white;
}

.export-btn:hover {
  background: #38a169;
}

.print-btn:hover {
  background: #5a67d8;
}

/* Модальное окно (используйте стили из предыдущих компонентов) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 10px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.student-details-modal {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.detail-row:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
}

/* Состояния */
.loading, .error, .no-data {
  text-align: center;
  padding: 3rem;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error {
  color: #e53e3c;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #e53e3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.no-data {
  color: #666;
  font-style: italic;
}

/* Адаптивность */
@media (max-width: 768px) {
  .group-students-view {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .group-details {
    grid-template-columns: 1fr;
  }

  .controls {
    flex-direction: column;
  }

  .search-box,
  .filter-control {
    min-width: 100%;
  }

  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .modal-content {
    margin: 1rem;
    width: calc(100% - 2rem);
  }

  .action-buttons {
    flex-wrap: wrap;
  }

  .export-section {
    flex-direction: column;
  }
}
</style>