<template>
  <div class="student-grades-view">
    <div class="header">
      <button @click="goBack" class="back-btn">← Назад</button>
      <h1>Оценки студента</h1>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка оценок...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadGrades" class="retry-btn">Повторить</button>
    </div>

    <div v-else class="grades-container">
      <!-- Информация о студенте -->
      <div class="student-header">
        <h2>{{ student.full_name || 'Студент' }}</h2>
        <p>Группа: {{ student.group_name }}</p>
      </div>


      <!-- Статистика -->
      <div class="stats-summary">
        <div class="stat-item">
          <span class="stat-label">Всего оценок:</span>
          <span class="stat-value">{{ filteredGrades.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Средний балл:</span>
          <span class="stat-value">{{ averageGrade.toFixed(2) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Отличных (5):</span>
          <span class="stat-value grade-5">{{ gradeCounts[5] || 0 }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Хороших (4):</span>
          <span class="stat-value grade-4">{{ gradeCounts[4] || 0 }}</span>
        </div>
      </div>

      <!-- Таблица оценок -->
      <div class="grades-table-container">
        <table class="grades-table">
          <thead>
          <tr>
            <th>Дата</th>
            <th>Предмет</th>
            <th>Оценка</th>
            <th>Тип</th>
            <th>Семестр</th>
            <th>Преподаватель</th>
            <th>Комментарий</th>
            <th v-if="canEdit">Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="grade in filteredGrades" :key="grade.id" :class="`grade-${grade.grade}`">
            <td>{{ formatDate(grade.date) }}</td>
            <td>{{ grade.subject_name }}</td>
            <td>
                <span class="grade-badge" :class="`grade-${grade.grade}`">
                  {{ grade.grade_display }}
                </span>
            </td>
            <td>
              <span class="type-badge">{{ grade.grade_type_display }}</span>
            </td>
            <td>{{ grade.semester }}</td>
            <td>{{ grade.teacher_name }}</td>
            <td class="comments-cell">
              {{ grade.comments || '-' }}
            </td>
            <td v-if="canEdit" class="actions-cell">
              <button @click="editGrade(grade)" class="action-btn edit-btn">✏️</button>
              <button @click="deleteGrade(grade)" class="action-btn delete-btn">🗑️</button>
            </td>
          </tr>

          <tr v-if="!filteredGrades.length">
            <td colspan="8" class="no-data">
              Оценки не найдены
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <!-- Форма добавления/редактирования оценки -->
      <div v-if="canEdit" class="grade-form-section">
        <h3>{{ editingGrade ? 'Редактировать оценку' : 'Добавить новую оценку' }}</h3>
        <form @submit.prevent="saveGrade" class="grade-form">
          <div class="form-row">
            <div class="form-group">
              <label>Предмет *</label>
              <select v-model="newGrade.subject" required>
                <option value="">Выберите предмет</option>
                <!-- Используем subject.id как значение -->
                <option v-for="subject in availableSubjects" :key="subject.id" :value="subject.id">
                  {{ subject.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Оценка *</label>
              <select v-model="newGrade.grade" required>
                <option value="">Выберите оценку</option>
                <option value="5">5 (Отлично)</option>
                <option value="4">4 (Хорошо)</option>
                <option value="3">3 (Удовлетворительно)</option>
                <option value="2">2 (Неудовлетворительно)</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Тип оценки *</label>
              <select v-model="newGrade.grade_type" required>
                <option value="current">Текущая</option>
                <option value="semester">Семестровая</option>
                <option value="exam">Экзамен</option>
                <option value="credit">Зачёт</option>
              </select>
            </div>

            <div class="form-group">
              <label>Семестр *</label>
              <select v-model="newGrade.semester" required>
                <option value="">Выберите семестр</option>
                <option v-for="n in 8" :key="n" :value="n">{{ n }}</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Дата *</label>
              <input
                  v-model="newGrade.date"
                  type="date"
                  required
              >
            </div>

            <div class="form-group">
              <label>Преподаватель</label>
              <select v-model="newGrade.teacher">
                <option value="">Выберите преподавателя</option>
                <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
                  {{ teacher.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Комментарий</label>
            <textarea
                v-model="newGrade.comments"
                rows="3"
                placeholder="Комментарий к оценке..."
            ></textarea>
          </div>

          <div class="form-actions">
            <button type="submit" :disabled="saving" class="btn-primary">
              {{ saving ? 'Сохранение...' : (editingGrade ? 'Сохранить изменения' : 'Добавить оценку') }}
            </button>
            <button v-if="editingGrade" type="button" @click="cancelEdit" class="btn-secondary">
              Отмена
            </button>
            <button type="button" @click="resetForm" class="btn-secondary">
              Сбросить
            </button>
          </div>

          <div v-if="formError" class="error-message">
            {{ formError }}
          </div>

          <div v-if="formSuccess" class="success-message">
            {{ formSuccess }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, computed, onMounted, watch} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import api from '@/api'

export default {
  name: 'StudentGradesView',

  setup() {
    const route = useRoute()
    const router = useRouter()

    const studentId = ref(route.params.id)
    const loading = ref(true)
    const error = ref('')
    const grades = ref([])
    const student = ref({})
    const subjects = ref([])
    const teachers = ref([])

    // Фильтры
    const selectedSemester = ref('')
    const selectedSubject = ref('')
    const selectedGradeType = ref('')

    // Форма
    const newGrade = ref({
      student: studentId.value,
      subject: '',
      grade: '',
      grade_type: 'current',
      semester: '',
      date: new Date().toISOString().split('T')[0],
      teacher: '',
      comments: ''
    })

    const editingGrade = ref(null)
    const saving = ref(false)
    const formError = ref('')
    const formSuccess = ref('')

    // Функция загрузки данных студента
    const loadStudentInfo = async () => {
      try {
        console.log('Загрузка студента с ID:', studentId.value)
        const studentResponse = await api.get(`students/search/?id=${studentId.value}`)
        console.log('Ответ API (студент):', studentResponse.data)

        if (studentResponse.data && studentResponse.data.length > 0) {
          const studentData = studentResponse.data[0]
          student.value = {
            full_name: studentData.full_name || `${studentData.surname} ${studentData.name} ${studentData.middle_name || ''}`.trim(),
            group_name: studentData.group_name || '—',
            id: studentData.id,
            group: studentData.group,
            enrollment_date: studentData.enrollment_date,
            status: studentData.status,
            status_display: studentData.status_display
          }
        } else {
          student.value = {
            full_name: `Студент (ID: ${studentId.value})`,
            group_name: 'Не найден'
          }
        }
      } catch (err) {
        console.error('Ошибка загрузки студента:', err)
        student.value = {
          full_name: `Студент (ID: ${studentId.value})`,
          group_name: 'Ошибка загрузки'
        }
      }
    }

    // Загрузка всех данных
    const loadGrades = async () => {
      loading.value = true
      error.value = ''

      try {
        // Сбрасываем данные
        grades.value = []
        subjects.value = []

        // Загружаем данные студента
        await loadStudentInfo()

        // Загружаем оценки студента
        console.log('Загрузка оценок для студента:', studentId.value)
        const gradesResponse = await api.get(`students/${studentId.value}/grades/`)
        console.log('Ответ API (оценки):', gradesResponse.data)

        if (gradesResponse.data && gradesResponse.data.length > 0) {
          // Обрабатываем данные оценок
          grades.value = gradesResponse.data.map(grade => ({
            ...grade,
            subject_id: grade.subject, // сохраняем ID предмета
            subject_name: grade.subject_name
          }))

          // Извлекаем уникальные предметы из оценок
          const uniqueSubjectsMap = new Map()
          grades.value.forEach(grade => {
            if (grade.subject_id && grade.subject_name) {
              uniqueSubjectsMap.set(grade.subject_id, {
                id: grade.subject_id,
                name: grade.subject_name
              })
            }
          })

          subjects.value = Array.from(uniqueSubjectsMap.values())
        } else {
          grades.value = []
          subjects.value = []
        }

        // Загружаем преподавателей
        try {
          const teachersResponse = await api.get('teachers/active/')
          teachers.value = teachersResponse.data
        } catch (err) {
          console.warn('Не удалось загрузить преподавателей:', err)
          teachers.value = []
        }

      } catch (err) {
        console.error('Ошибка загрузки оценок:', err)
        error.value = err.response?.data?.detail || 'Не удалось загрузить оценки'
      } finally {
        loading.value = false
      }
    }

    // Следим за изменением studentId
    watch(() => route.params.id, (newId) => {
      console.log('ID студента изменился:', newId)
      if (newId && newId !== studentId.value) {
        studentId.value = newId
        newGrade.value.student = newId
        loadGrades()
      }
    })

    // Вычисляемые свойства
    const semesters = computed(() => {
      const semestersSet = new Set()
      grades.value.forEach(grade => {
        if (grade.semester) semestersSet.add(grade.semester)
      })
      return Array.from(semestersSet).sort()
    })

    const filteredGrades = computed(() => {
      return grades.value.filter(grade => {
        if (selectedSemester.value && grade.semester != selectedSemester.value) return false
        if (selectedSubject.value && grade.subject_id != selectedSubject.value) return false
        if (selectedGradeType.value && grade.grade_type != selectedGradeType.value) return false
        return true
      })
    })

    const averageGrade = computed(() => {
      if (!filteredGrades.value.length) return 0
      const sum = filteredGrades.value.reduce((acc, grade) => acc + grade.grade, 0)
      return sum / filteredGrades.value.length
    })

    const gradeCounts = computed(() => {
      const counts = {2: 0, 3: 0, 4: 0, 5: 0}
      filteredGrades.value.forEach(grade => {
        if (counts[grade.grade] !== undefined) {
          counts[grade.grade]++
        }
      })
      return counts
    })

    const availableSubjects = computed(() => {
      const studentSubjectIds = new Set(grades.value.map(g => g.subject_id))
      return subjects.value.filter(subject => !studentSubjectIds.has(subject.id))
    })

    const canEdit = computed(() => {
      return true
    })

    // Методы
    const formatDate = (dateString) => {
      if (!dateString) return 'Н/Д'
      return new Date(dateString).toLocaleDateString('ru-RU')
    }

    const filterGrades = () => {
      // Фильтрация происходит автоматически через computed
    }

    const editGrade = (grade) => {
      editingGrade.value = grade
      newGrade.value = {
        student: studentId.value,
        subject: grade.subject_id,
        grade: grade.grade.toString(),
        grade_type: grade.grade_type,
        semester: grade.semester.toString(),
        date: grade.date,
        teacher: grade.teacher || '',
        comments: grade.comments || ''
      }
    }

    const deleteGrade = async (grade) => {
      if (!confirm('Удалить эту оценку?')) return

      try {
        await api.delete(`grades/${grade.id}/delete/`)
        await loadGrades()
        formSuccess.value = 'Оценка удалена'
        setTimeout(() => formSuccess.value = '', 3000)
      } catch (err) {
        formError.value = err.response?.data?.error || 'Ошибка удаления оценки'
      }
    }

    const saveGrade = async () => {
      saving.value = true
      formError.value = ''
      formSuccess.value = ''

      try {
        if (editingGrade.value) {
          await api.put(`grades/${editingGrade.value.id}/update/`, newGrade.value)
          formSuccess.value = 'Оценка обновлена'
        } else {
          await api.post('grades/create/', newGrade.value)
          formSuccess.value = 'Оценка добавлена'
        }

        resetForm()
        await loadGrades()

        setTimeout(() => formSuccess.value = '', 3000)
      } catch (err) {
        console.error('Ошибка сохранения оценки:', err)
        formError.value = err.response?.data?.detail || err.response?.data?.error || 'Ошибка сохранения оценки'
      } finally {
        saving.value = false
      }
    }

    const cancelEdit = () => {
      editingGrade.value = null
      resetForm()
    }

    const resetForm = () => {
      newGrade.value = {
        student: studentId.value,
        subject: '',
        grade: '',
        grade_type: 'current',
        semester: '',
        date: new Date().toISOString().split('T')[0],
        teacher: '',
        comments: ''
      }
      editingGrade.value = null
      formError.value = ''
    }

    const goBack = () => {
      router.go(-1)
    }

    onMounted(() => {
      loadGrades()
    })

    return {
      studentId,
      loading,
      error,
      grades,
      student,
      subjects,
      teachers,
      selectedSemester,
      selectedSubject,
      selectedGradeType,
      newGrade,
      editingGrade,
      saving,
      formError,
      formSuccess,
      semesters,
      filteredGrades,
      averageGrade,
      gradeCounts,
      availableSubjects,
      canEdit,
      loadGrades,
      formatDate,
      filterGrades,
      editGrade,
      deleteGrade,
      saveGrade,
      cancelEdit,
      resetForm,
      goBack
    }
  }
}
</script>

<style scoped>
.student-grades-view {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  min-height: 100vh;
  background: #f8f9fa;
}

.header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e9ecef;
}

.back-btn {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(102, 126, 234, 0.2);
}

.back-btn:hover {
  background: #5a67d8;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
}

h1 {
  color: #2c3e50;
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

/* Состояния загрузки и ошибок */
.loading, .error {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  margin: 2rem 0;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading p {
  color: #667eea;
  font-size: 1.1rem;
  font-weight: 500;
}

.error {
  color: #e74c3c;
  background: #fff5f5;
  border: 1px solid #ffe3e3;
}

.error p {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.retry-btn {
  padding: 0.75rem 1.5rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: #c0392b;
}

/* Информация о студенте */
.student-header {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
  border-left: 5px solid #667eea;
}

.student-header h2 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
  font-weight: 600;
}

.student-header p {
  color: #666;
  margin: 0;
  font-size: 1.1rem;
}

/* Фильтры */
.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.filter-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.95rem;
}

.filter-group select {
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  color: #333;
  transition: all 0.3s ease;
  cursor: pointer;
}

.filter-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-group select:hover {
  border-color: #adb5bd;
}

/* Статистика */
.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-item {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
}

.stat-label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.stat-value.grade-5 {
  color: #27ae60;
}

.stat-value.grade-4 {
  color: #f39c12;
}

.stat-value.grade-3 {
  color: #3498db;
}

.stat-value.grade-2 {
  color: #e74c3c;
}

/* Таблица оценок */
.grades-table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 3rem;
}

.grades-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.grades-table th {
  background: #f8f9fa;
  padding: 1.25rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e9ecef;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.grades-table td {
  padding: 1.25rem 1rem;
  border-bottom: 1px solid #f1f3f5;
  vertical-align: middle;
}

.grades-table tr:hover {
  background: #f8f9fa;
}

.grades-table tr.grade-5 {
  background: rgba(39, 174, 96, 0.05);
}

.grades-table tr.grade-4 {
  background: rgba(243, 156, 18, 0.05);
}

.grades-table tr.grade-3 {
  background: rgba(52, 152, 219, 0.05);
}

.grades-table tr.grade-2 {
  background: rgba(231, 76, 60, 0.05);
}

/* Бейджи оценок */
.grade-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.9rem;
  min-width: 40px;
  text-align: center;
}

.grade-badge.grade-5 {
  background: #27ae60;
  color: white;
}

.grade-badge.grade-4 {
  background: #f39c12;
  color: white;
}

.grade-badge.grade-3 {
  background: #3498db;
  color: white;
}

.grade-badge.grade-2 {
  background: #e74c3c;
  color: white;
}

/* Бейджи типов оценок */
.type-badge {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
  background: #e3f2fd;
  color: #1976d2;
}

.comments-cell {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.comments-cell:hover {
  white-space: normal;
  overflow: visible;
  position: relative;
  z-index: 1;
  background: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  border-radius: 8px;
}

/* Кнопки действий в таблице */
.actions-cell {
  min-width: 100px;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.edit-btn:hover {
  background: #e3f2fd;
  color: #1976d2;
  transform: scale(1.1);
}

.delete-btn:hover {
  background: #fdedec;
  color: #e74c3c;
  transform: scale(1.1);
}

.no-data {
  text-align: center;
  padding: 3rem;
  color: #95a5a6;
  font-style: italic;
  font-size: 1.1rem;
}

/* Форма добавления/редактирования оценки */
.grade-form-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
  margin-top: 2rem;
}

.grade-form-section h3 {
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f3f5;
}

.grade-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.95rem;
}

.form-group select,
.form-group input,
.form-group textarea {
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  color: #333;
  transition: all 0.3s ease;
}

.form-group select:focus,
.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1.5rem;
  border-top: 2px solid #f1f3f5;
}

.btn-primary,
.btn-secondary {
  padding: 0.875rem 1.75rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #667eea;
  color: white;
  box-shadow: 0 2px 5px rgba(102, 126, 234, 0.2);
}

.btn-primary:hover:not(:disabled) {
  background: #5a67d8;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
  transform: translateY(-2px);
}

/* Сообщения об ошибках и успехах */
.error-message,
.success-message {
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-weight: 500;
}

.error-message {
  background: #fdedec;
  color: #e74c3c;
  border: 1px solid #fadbd8;
}

.success-message {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

/* Адаптивность */
@media (max-width: 768px) {
  .student-grades-view {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .filters {
    grid-template-columns: 1fr;
  }

  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
  }

  .grades-table {
    display: block;
    overflow-x: auto;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }

  .action-buttons {
    flex-direction: column;
    gap: 0.5rem;
  }

  .action-btn {
    width: 35px;
    height: 35px;
  }
}

@media (max-width: 480px) {
  .stats-summary {
    grid-template-columns: 1fr;
  }

  .student-header h2 {
    font-size: 1.4rem;
  }

  .grade-form-section {
    padding: 1rem;
  }

  .grade-form-section h3 {
    font-size: 1.3rem;
  }
}

/* Анимации */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.grades-container {
  animation: fadeIn 0.5s ease-out;
}

/* Кастомный скроллбар */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Печать */
@media print {
  .back-btn,
  .filters,
  .grade-form-section,
  .action-buttons,
  .form-actions {
    display: none !important;
  }

  .student-grades-view {
    background: white;
    padding: 0;
  }

  .grades-table {
    box-shadow: none;
    border: 1px solid #ddd;
  }

  .grades-table th {
    background: #f5f5f5 !important;
    -webkit-print-color-adjust: exact;
  }
}
</style>