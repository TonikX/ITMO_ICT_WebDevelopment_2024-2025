<template>
  <div class="subjects-view">
    <div class="header">
      <h1>📚 Дисциплины</h1>
      <div class="stats">
        <span class="stat-item">Всего: {{ subjects.length }}</span>
        <span class="stat-item">Часов всего: {{ totalHours }}</span>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка дисциплин...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadSubjects" class="retry-btn">Повторить</button>
    </div>

    <div v-else class="subjects-container">
      <!-- Фильтры -->
      <div class="filters">
        <div class="filter-group">
          <label>Курс:</label>
          <select v-model="selectedCourse" @change="onCourseChange">
            <option value="">Все курсы</option>
            <option v-for="course in courseOptions" :key="course.value" :value="course.value">
              {{ course.label }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label>Семестр:</label>
          <select v-model="selectedSemester" @change="filterSubjects" :disabled="!selectedCourse">
            <option value="">Все семестры</option>
            <option v-for="semester in semesterOptions" :key="semester.value" :value="semester.value">
              {{ semester.label }}
            </option>
          </select>
        </div>

        <div class="search-box">
          <input
            v-model="searchQuery"
            @input="filterSubjects"
            placeholder="Поиск по названию..."
            class="search-input"
          >
          <span class="search-icon">🔍</span>
        </div>

        <button @click="resetFilters" class="reset-btn">
          Сбросить фильтры
        </button>
      </div>

      <!-- Карточки предметов -->
      <div v-if="filteredSubjects.length > 0" class="subjects-grid">
        <div
          v-for="subject in paginatedSubjects"
          :key="subject.id"
          class="subject-card"
          :class="getSubjectCardClass(subject.course)"
        >
          <div class="subject-header">
            <div class="subject-course-badge">
              {{ subject.course }} курс
            </div>
            <div class="subject-semester-badge">
              {{ subject.semester }} семестр
            </div>
          </div>

          <div class="subject-content">
            <h3 class="subject-name">{{ subject.name }}</h3>

            <div class="subject-meta">
              <div class="meta-item">
                <span class="meta-icon">⏱️</span>
                <span class="meta-text">{{ subject.hours }} часов</span>
              </div>
              <div class="meta-item">
                <span class="meta-icon">📊</span>
                <span class="meta-text">Курс {{ subject.course }}</span>
              </div>
            </div>

            <div v-if="subject.description" class="subject-description">
              <p>{{ truncateDescription(subject.description) }}</p>
            </div>

          </div>
          <div class="subject-actions">
              <button @click="viewSubjectDetails(subject)" class="action-btn details-btn">
                Подробнее
              </button>
            </div>
        </div>
      </div>

      <!-- Сообщение, если нет результатов -->
      <div v-else class="no-results">
        <div class="no-results-icon">📚</div>
        <h3>Дисциплины не найдены</h3>
        <p>Попробуйте изменить параметры поиска или фильтры</p>
        <button @click="resetFilters" class="retry-btn">
          Сбросить фильтры
        </button>
      </div>

      <!-- Пагинация -->
      <div v-if="filteredSubjects.length > itemsPerPage" class="pagination">
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="page-btn"
        >
          ← Назад
        </button>

        <div class="page-info">
          Страница {{ currentPage }} из {{ totalPages }}
        </div>

        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="page-btn"
        >
          Далее →
        </button>
      </div>

      <!-- Статистика -->
      <div class="stats-summary">
        <div class="stat-card">
          <div class="stat-value">{{ subjectsByCourse[1] || 0 }}</div>
          <div class="stat-label">1 курс</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ subjectsByCourse[2] || 0 }}</div>
          <div class="stat-label">2 курс</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ subjectsByCourse[3] || 0 }}</div>
          <div class="stat-label">3 курс</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ subjectsByCourse[4] || 0 }}</div>
          <div class="stat-label">4 курс</div>
        </div>
      </div>

      <!-- Детальная информация (модальное окно) -->
      <div v-if="selectedSubject" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>📚 {{ selectedSubject.name }}</h3>
            <button @click="closeModal" class="close-btn">&times;</button>
          </div>

          <div class="modal-body">
            <div class="subject-details">
              <div class="detail-row">
                <span class="detail-label">Курс:</span>
                <span class="detail-value">{{ selectedSubject.course }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Семестр:</span>
                <span class="detail-value">{{ selectedSubject.semester }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Часы:</span>
                <span class="detail-value">{{ selectedSubject.hours }}</span>
              </div>

              <div v-if="selectedSubject.description" class="detail-row description-row">
                <span class="detail-label">Описание:</span>
                <p class="detail-description">{{ selectedSubject.description }}</p>
              </div>

              <div class="detail-row" v-if="selectedSubject.id">
                <span class="detail-label">ID предмета:</span>
                <span class="detail-value">{{ selectedSubject.id }}</span>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="closeModal" class="btn-secondary">
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/api'

export default {
  name: 'SubjectsView',

  setup() {
    // Реактивные данные
    const subjects = ref([])
    const loading = ref(true)
    const error = ref('')
    const searchQuery = ref('')
    const selectedCourse = ref('')
    const selectedSemester = ref('')
    const selectedSubject = ref(null)
    const currentPage = ref(1)
    const itemsPerPage = ref(12)

    // Опции для фильтров
    const courseOptions = [
      { value: 1, label: '1 курс' },
      { value: 2, label: '2 курс' },
      { value: 3, label: '3 курс' },
      { value: 4, label: '4 курс' }
    ]

    const semesterOptions = [
      { value: 1, label: '1 семестр' },
      { value: 2, label: '2 семестр' },
      { value: 3, label: '3 семестр' },
      { value: 4, label: '4 семестр' },
      { value: 5, label: '5 семестр' },
      { value: 6, label: '6 семестр' },
      { value: 7, label: '7 семестр' },
      { value: 8, label: '8 семестр' }
    ]

    // Загрузка данных
    const loadSubjects = async () => {
      loading.value = true
      error.value = ''

      try {
        const response = await api.get('subjects/all/')
        subjects.value = response.data
      } catch (err) {
        console.error('Ошибка загрузки дисциплин:', err)
        error.value = 'Не удалось загрузить список дисциплин'
      } finally {
        loading.value = false
      }
    }

    // Вычисляемые свойства
    const filteredSubjects = computed(() => {
      let filtered = subjects.value

      // Фильтр по курсу
      if (selectedCourse.value) {
        filtered = filtered.filter(subject => subject.course == selectedCourse.value)
      }

      // Фильтр по семестру
      if (selectedSemester.value) {
        filtered = filtered.filter(subject => subject.semester == selectedSemester.value)
      }

      // Поиск по названию
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(subject =>
          subject.name.toLowerCase().includes(query)
        )
      }

      return filtered
    })

    const totalHours = computed(() => {
      return subjects.value.reduce((sum, subject) => sum + subject.hours, 0)
    })

    const subjectsByCourse = computed(() => {
      const byCourse = {}
      subjects.value.forEach(subject => {
        byCourse[subject.course] = (byCourse[subject.course] || 0) + 1
      })
      return byCourse
    })

    const totalPages = computed(() => {
      return Math.ceil(filteredSubjects.value.length / itemsPerPage.value)
    })

    const paginatedSubjects = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return filteredSubjects.value.slice(start, end)
    })

    // Методы
    const onCourseChange = () => {
      selectedSemester.value = ''
      currentPage.value = 1
      filterSubjects()
    }

    const filterSubjects = () => {
      currentPage.value = 1
    }

    const resetFilters = () => {
      selectedCourse.value = ''
      selectedSemester.value = ''
      searchQuery.value = ''
      currentPage.value = 1
    }

    const getSubjectCardClass = (course) => {
      return `course-${course}`
    }

    const truncateDescription = (text, maxLength = 100) => {
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }

    const viewSubjectDetails = (subject) => {
      selectedSubject.value = subject
    }

    const viewRelatedGroups = (subject) => {
      console.log('Просмотр групп для предмета:', subject)
      // Здесь можно добавить навигацию на страницу с группами
    }

    const closeModal = () => {
      selectedSubject.value = null
    }

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
      }
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
      }
    }

    // Инициализация
    onMounted(() => {
      loadSubjects()
    })

    return {
      // Данные
      subjects,
      loading,
      error,
      searchQuery,
      selectedCourse,
      selectedSemester,
      selectedSubject,
      currentPage,
      itemsPerPage,
      courseOptions,
      semesterOptions,

      // Вычисляемые свойства
      filteredSubjects,
      totalHours,
      subjectsByCourse,
      totalPages,
      paginatedSubjects,

      // Методы
      loadSubjects,
      onCourseChange,
      filterSubjects,
      resetFilters,
      getSubjectCardClass,
      truncateDescription,
      viewSubjectDetails,
      viewRelatedGroups,
      closeModal,
      prevPage,
      nextPage
    }
  }
}
</script>

<style scoped>
.subjects-view {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
}

.header h1 {
  color: #2c3e50;
  border-bottom: 3px solid #667eea;
  padding-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stats {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.stat-item {
  background: #f8f9fa;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Фильтры */
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: flex-end;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 150px;
}

.filter-group label {
  font-weight: bold;
  font-size: 0.9rem;
  color: #2c3e50;
}

.filter-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.filter-group select:focus {
  outline: none;
  border-color: #667eea;
}

.filter-group select:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.search-box {
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
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.reset-btn {
  padding: 0.75rem 1.5rem;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.reset-btn:hover {
  background: #7f8c8d;
}

/* Сетка предметов */
.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.subject-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  border-top: 4px solid transparent;
}

.subject-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

/* Цвета по курсам */
.subject-card.course-1 { border-top-color: #667eea; }
.subject-card.course-2 { border-top-color: #48bb78; }
.subject-card.course-3 { border-top-color: #ed8936; }
.subject-card.course-4 { border-top-color: #9f7aea; }

.subject-header {
  display: flex;
  justify-content: space-between;
  padding: 1rem 1rem 0.5rem;
}

.subject-course-badge {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

.subject-semester-badge {
  background: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

.subject-content {
  padding: 1rem;
}

.subject-name {
  color: #2c3e50;
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  line-height: 1.4;
}

.subject-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.meta-icon {
  font-size: 0.9rem;
}

.subject-description {
  margin-bottom: 1rem;
}

.subject-description p {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}

.subject-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.details-btn {
  background: #e3f2fd;
  color: #1976d2;
}

.details-btn:hover {
  background: #bbdefb;
}

.groups-btn {
  background: #f3e5f5;
  color: #7b1fa2;
}

.groups-btn:hover {
  background: #e1bee7;
}

/* Нет результатов */
.no-results {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.no-results-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.no-results h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.no-results p {
  color: #666;
  margin-bottom: 1.5rem;
}

/* Пагинация */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
  padding: 1rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.page-btn {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.page-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.page-btn:not(:disabled):hover {
  background: #5a67d8;
}

.page-info {
  color: #666;
  font-weight: 500;
}

/* Статистика */
.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  text-align: center;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

/* Модальное окно */
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
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.subject-details {
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

.detail-label {
  font-weight: 600;
  color: #2c3e50;
}

.detail-value {
  color: #666;
  font-weight: 500;
}

.description-row {
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

.detail-description {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
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

.btn-secondary:hover {
  background: #7f8c8d;
}

/* Состояния загрузки и ошибки */
.loading, .error {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  color: #e53e3e;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
}

.retry-btn:hover {
  background: #c53030;
}

/* Адаптивность */
@media (max-width: 768px) {
  .subjects-view {
    padding: 1rem;
  }

  .filters {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group,
  .search-box {
    min-width: 100%;
  }

  .subjects-grid {
    grid-template-columns: 1fr;
  }

  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
  }

  .modal-content {
    margin: 1rem;
    width: calc(100% - 2rem);
  }
}

@media (max-width: 480px) {
  .stats-summary {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .pagination {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>