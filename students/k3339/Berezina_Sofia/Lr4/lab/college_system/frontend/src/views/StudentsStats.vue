<template>
  <div class="student-stats-view">
    <div class="header">
      <button @click="goBack" class="back-btn">← Назад</button>
      <h1>Статистика успеваемости</h1>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка статистики...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadStats" class="retry-btn">Повторить</button>
    </div>

    <div v-else class="stats-container">
      <!-- Информация о студенте -->
      <div class="student-info-card">
        <h2>{{ student.full_name || 'Загрузка...' }}</h2>
        <div class="student-details">
          <p><strong>Группа:</strong> {{ student.group_name || 'Н/Д' }}</p>
        </div>
      </div>

      <!-- Основная статистика -->
      <div class="main-stats">
        <div class="stat-card primary">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.average_grade || 'Н/Д' }}</div>
            <div class="stat-label">Средний балл</div>
          </div>
        </div>

        <div class="stat-card secondary">
          <div class="stat-icon">📈</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.total_grades || 0 }}</div>
            <div class="stat-label">Всего оценок</div>
          </div>
        </div>

        <div class="stat-card success" v-if="stats.best_subject">
          <div class="stat-icon">🏆</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.best_subject }}</div>
            <div class="stat-label">Лучший предмет</div>
          </div>
        </div>

        <div class="stat-card warning" v-if="stats.worst_subject">
          <div class="stat-icon">📉</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.worst_subject }}</div>
            <div class="stat-label">Худший предмет</div>
          </div>
        </div>
      </div>

      <!-- Статус студента -->
      <div class="status-card" :class="`status-${stats.status || 'unknown'}`">
        <h3>Статус успеваемости</h3>
        <div class="status-value">
          {{ getStatusText(stats.status) }}
        </div>
      </div>

      <!-- Статистика по семестрам -->
      <div class="section" v-if="stats.grades_by_semester && Object.keys(stats.grades_by_semester).length">
        <h3>Средний балл по семестрам</h3>
        <div class="semester-stats">
          <div v-for="(grade, semester) in stats.grades_by_semester"
               :key="semester"
               class="semester-card">
            <div class="semester-name">{{ semester }}</div>
            <div class="semester-grade">{{ grade }}</div>
          </div>
        </div>
      </div>

      <!-- Статистика по предметам -->
      <div class="section" v-if="stats.grades_by_subject && stats.grades_by_subject.length">
        <h3>Успеваемость по предметам</h3>
        <div class="subjects-table">
          <table>
            <thead>
              <tr>
                <th>Предмет</th>
                <th>Средний балл</th>
                <th>Количество оценок</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="subject in stats.grades_by_subject" :key="subject.subject_id">
                <td>{{ subject.subject_name }}</td>
                <td>
                  <span class="grade-badge" :class="`grade-${Math.round(subject.average_grade)}`">
                    {{ subject.average_grade }}
                  </span>
                </td>
                <td>{{ subject.grades_count }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Пустой случай -->
      <div v-if="!stats || (!stats.total_grades && !stats.grades_by_subject?.length)" class="no-data">
        <p>У студента пока нет оценок</p>
        <router-link :to="`/students/${studentId}/grades`" class="btn-primary">
          Посмотреть оценки
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'

export default {
  name: 'StudentStatsView',

  setup() {
    const route = useRoute()
    const router = useRouter()

    const studentId = ref(route.params.id)
    const loading = ref(true)
    const error = ref('')
    const stats = ref({})
    const student = ref({})

    const loadStats = async () => {
      loading.value = true
      error.value = ''

      try {
        // Загружаем статистику
        const statsResponse = await api.get(`students/${studentId.value}/stats/`)
        stats.value = statsResponse.data

        // Загружаем информацию о студенте
        try {
          const studentResponse = await api.get(`students/search/?id=${studentId.value}`)
          if (studentResponse.data && studentResponse.data.length > 0) {
            student.value = studentResponse.data[0]
          }
        } catch (err) {
          console.warn('Не удалось загрузить данные студента:', err)
          student.value = { name: `Студент #${studentId.value}` }
        }
      } catch (err) {
        console.error('Ошибка загрузки статистики:', err)
        error.value = err.response?.data?.detail || 'Не удалось загрузить статистику'
      } finally {
        loading.value = false
      }
    }

    const getStatusText = (status) => {
      const statusMap = {
        'отличник': 'Отличник',
        'хорошист': 'Хорошист',
        'троечник': 'Троечник',
        'unknown': 'Не определен'
      }
      return statusMap[status] || status
    }

    const goBack = () => {
      router.go(-1)
    }

    onMounted(() => {
      loadStats()
    })

    return {
      studentId,
      loading,
      error,
      stats,
      student,
      loadStats,
      getStatusText,
      goBack
    }
  }
}
</script>

<style scoped>
.student-stats-view {
  padding: 2rem;
  max-width: 1200px;
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

/* Информация о студенте */
.student-info-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.student-info-card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.student-details {
  display: flex;
  gap: 2rem;
}

.student-details p {
  margin: 0;
  color: #666;
}

/* Основная статистика */
.main-stats {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  gap: 1rem;
  width: fit-content;
}

.stat-card.primary {
  border-left: 4px solid #667eea;
}

.stat-card.secondary {
  border-left: 4px solid #48bb78;
}

.stat-card.success {
  border-left: 4px solid #38a169;
}

.stat-card.warning {
  border-left: 4px solid #ed8936;
}

.stat-icon {
  font-size: 2rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  line-height: 1;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

/* Статус студента */
.status-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
  text-align: center;
}

.status-card h3 {
  color: #666;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  font-weight: normal;
}

.status-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.status-отличник { color: #38a169; }
.status-хорошист { color: #ed8936; }
.status-троечник { color: #e53e3e; }
.status-unknown { color: #718096; }

/* Семестры */
.section {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.section h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.semester-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.semester-card {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}

.semester-name {
  font-weight: 500;
  color: #666;
  margin-bottom: 0.5rem;
}

.semester-grade {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
}

/* Таблица предметов */
.subjects-table {
  overflow-x: auto;
}

.subjects-table table {
  width: 100%;
  border-collapse: collapse;
}

.subjects-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #666;
  border-bottom: 2px solid #e2e8f0;
}

.subjects-table td {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.subjects-table tr:hover {
  background: #f8f9fa;
}

.grade-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: bold;
  color: white;
  min-width: 50px;
  text-align: center;
}

.grade-5 { background: #38a169; }
.grade-4 { background: #ed8936; }
.grade-3 { background: #ecc94b; }
.grade-2 { background: #e53e3e; }

/* График */
.chart-container {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.chart-placeholder {
  text-align: center;
  padding: 2rem;
  color: #666;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  color: #e53e3e;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.no-data {
  color: #666;
}

.btn-primary {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: 500;
}

.btn-primary:hover {
  background: #5a67d8;
}

/* Адаптивность */
@media (max-width: 768px) {
  .student-stats-view {
    padding: 1rem;
  }

  .student-details {
    flex-direction: column;
    gap: 0.5rem;
  }

  .main-stats {
    grid-template-columns: 1fr;
  }

  .semester-stats {
    grid-template-columns: 1fr;
  }
}
</style>