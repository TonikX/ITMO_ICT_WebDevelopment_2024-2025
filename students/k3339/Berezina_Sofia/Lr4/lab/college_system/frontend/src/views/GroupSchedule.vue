<template>
  <div class="schedule-view">
    <div class="header">
      <h1>Расписание занятий</h1>
    </div>

    <div class="controls">
      <div class="control-group">
        <label>Выберите группу:</label>
        <select v-model="selectedGroupId" @change="loadSchedule">
          <option value="">-- Выберите группу --</option>
          <option v-for="group in groups" :key="group.id" :value="group.id">
            {{ group.name }} ({{ group.course }} курс)
          </option>
        </select>
      </div>

      <div class="control-group">
        <label>Неделя:</label>
        <select v-model="weekType" @change="filterSchedule">
          <option value="all">Все недели</option>
          <option value="odd">Нечетная</option>
          <option value="even">Четная</option>
        </select>
      </div>

      <div class="control-group">
        <button @click="toggleToday" class="today-btn">
          {{ showTodayOnly ? 'Вся неделя' : 'Только сегодня' }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка расписания...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadSchedule" class="retry-btn">Повторить</button>
    </div>

    <div v-else-if="!selectedGroupId" class="no-group-selected">
      <p>Выберите группу для просмотра расписания</p>
    </div>

    <div v-else class="schedule-content">
      <div class="group-info">
        <h2>Расписание группы: {{ selectedGroup?.name }}</h2>
        <div class="group-stats">
          <span>📚 Предметов: {{ subjectsCount }}</span>
          <span>👨‍🏫 Преподавателей: {{ teachersCount }}</span>
          <span>🏫 Занятий: {{ schedule.length }}</span>
        </div>
      </div>

      <!-- ОБНОВЛЕННАЯ СТРУКТУРА СЕТКИ -->
      <div class="week-schedule">
        <!-- Первая строка: дни недели -->
        <!-- Пустая ячейка для первого столбца -->
        <div class="day-header header-corner"></div>

        <!-- Дни недели -->
        <div class="day-header" v-for="day in days" :key="day.value">
          <div class="day-name" :class="{ 'today': isToday(day.value) }">
            {{ day.name }}
            <span v-if="isToday(day.value)" class="today-badge">Сегодня</span>
          </div>
          <div class="day-date">
            {{ getDayDate(day.value) }}
          </div>
        </div>

        <!-- Строки с парами -->
        <div v-for="lesson in lessons" :key="lesson.number" class="lesson-row">
          <!-- Время пар (первый столбец) -->
          <div class="lesson-time">
            <div class="lesson-number">{{ lesson.number }} пара</div>
            <div class="lesson-hours">{{ lesson.time }}</div>
          </div>

          <!-- Ячейки для каждого дня недели -->
          <div
            class="lesson-slot"
            v-for="day in days"
            :key="`${day.value}-${lesson.number}`"
          >
            <div
              v-if="getLessonForDay(day.value, lesson.number)"
              class="lesson-card"
              :class="getLessonTypeClass(getLessonForDay(day.value, lesson.number).lesson_type)"
            >
              <div class="lesson-subject">
                <strong>{{ getLessonForDay(day.value, lesson.number).subject_name }}</strong>
              </div>
              <div class="lesson-type">
                {{ getLessonForDay(day.value, lesson.number).lesson_type_display }}
              </div>
              <div class="lesson-teacher">
                👨‍🏫 {{ getLessonForDay(day.value, lesson.number).teacher_name }}
              </div>
              <div class="lesson-room">
                🏫 Кабинет: {{ getLessonForDay(day.value, lesson.number).classroom_number }}
              </div>
              <div class="lesson-week" v-if="getLessonForDay(day.value, lesson.number).week_type !== 'both'">
                <span :class="getWeekTypeClass(getLessonForDay(day.value, lesson.number).week_type)">
                  {{ getWeekTypeDisplay(getLessonForDay(day.value, lesson.number).week_type) }}
                </span>
              </div>
            </div>
            <div v-else class="empty-slot">
              —
            </div>
          </div>
        </div>
      </div>

      <!-- Детальная информация -->
      <div class="detailed-schedule" v-if="filteredSchedule.length > 0">
        <h3>Подробное расписание</h3>
        <div class="schedule-table-container">
          <table class="schedule-table">
            <thead>
              <tr>
                <th>День</th>
                <th>Пара</th>
                <th>Предмет</th>
                <th>Тип</th>
                <th>Преподаватель</th>
                <th>Кабинет</th>
                <th>Неделя</th>
                <th>Период</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredSchedule" :key="item.id">
                <td>{{ item.day_display }}</td>
                <td>{{ item.lesson_number }}</td>
                <td>
                  <strong>{{ item.subject_name }}</strong>
                </td>
                <td>
                  <span :class="`type-badge ${item.lesson_type}`">
                    {{ item.lesson_type_display }}
                  </span>
                </td>
                <td>{{ item.teacher_name }}</td>
                <td>
                  <span class="room-badge">
                    {{ item.classroom_number }}
                  </span>
                </td>
                <td>
                  <span :class="`week-badge ${item.week_type}`">
                    {{ getWeekTypeDisplay(item.week_type) }}
                  </span>
                </td>
                <td>
                  <small>
                    {{ formatDate(item.start_date) }} - {{ formatDate(item.end_date) }}
                  </small>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Экспорт -->
      <div class="export-section">
        <button @click="exportToPDF" class="export-btn">
          📄 Экспорт в PDF
        </button>
        <button @click="exportToExcel" class="export-btn">
          📊 Экспорт в Excel
        </button>
        <button @click="printSchedule" class="export-btn">
          🖨️ Печать
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/api'

export default {
  name: 'ScheduleView',

  setup() {
    // Реактивные данные
    const groups = ref([])
    const schedule = ref([])
    const selectedGroupId = ref('')
    const selectedGroup = ref(null)
    const loading = ref(false)
    const error = ref('')
    const weekType = ref('all')
    const showTodayOnly = ref(false)

    // Дни недели
    const days = ref([
      { value: 1, name: 'Понедельник' },
      { value: 2, name: 'Вторник' },
      { value: 3, name: 'Среда' },
      { value: 4, name: 'Четверг' },
      { value: 5, name: 'Пятница' },
      { value: 6, name: 'Суббота' }
    ])

    // Время пар
    const lessons = ref([
      { number: 1, time: '8:30 - 10:00' },
      { number: 2, time: '10:10 - 11:40' },
      { number: 3, time: '12:10 - 13:40' },
      { number: 4, time: '14:00 - 15:30' },
      { number: 5, time: '15:40 - 17:10' },
      { number: 6, time: '17:20 - 18:50' }
    ])

    // Загрузка данных
    const loadGroups = async () => {
      try {
        // Пробуем загрузить все группы
        const response = await api.get('groups/')
        groups.value = response.data
      } catch (err) {
        console.error('Ошибка загрузки групп:', err)
        // Если нет endpoint для всех групп, загружаем по курсам
        await loadGroupsByCourses()
      }
    }

    const loadGroupsByCourses = async () => {
      const allGroups = []
      for (let course = 1; course <= 4; course++) {
        try {
          const response = await api.get(`groups/course/${course}/`)
          if (response.data) {
            allGroups.push(...response.data)
          }
        } catch (err) {
          console.warn(`Не удалось загрузить группы ${course} курса:`, err)
        }
      }
      groups.value = allGroups
    }

    const loadSchedule = async () => {
      if (!selectedGroupId.value) {
        schedule.value = []
        selectedGroup.value = null
        return
      }

      loading.value = true
      error.value = ''

      try {
        // Загружаем расписание для группы
        const response = await api.get(`schedule/group/${selectedGroupId.value}/`)
        schedule.value = response.data

        // Загружаем информацию о группе
        const groupResponse = await api.get(`groups/${selectedGroupId.value}/detail/`)
        selectedGroup.value = groupResponse.data

      } catch (err) {
        console.error('Ошибка загрузки расписания:', err)
        error.value = err.response?.data?.detail || 'Не удалось загрузить расписание'
      } finally {
        loading.value = false
      }
    }

    // Фильтрация
    const filteredSchedule = computed(() => {
      let filtered = schedule.value

      // Фильтр по типу недели
      if (weekType.value !== 'all') {
        filtered = filtered.filter(item => item.week_type === weekType.value || item.week_type === 'both')
      }

      // Фильтр по сегодняшнему дню
      if (showTodayOnly.value) {
        const today = new Date().getDay()
        // Преобразуем воскресенье (0) в 7 для совместимости
        const todayNumber = today === 0 ? 7 : today
        filtered = filtered.filter(item => item.day_of_week === todayNumber)
      }

      return filtered
    })

    // Статистика
    const subjectsCount = computed(() => {
      const uniqueSubjects = new Set(schedule.value.map(item => item.subject_id))
      return uniqueSubjects.size
    })

    const teachersCount = computed(() => {
      const uniqueTeachers = new Set(schedule.value.map(item => item.teacher_id))
      return uniqueTeachers.size
    })

    // Методы для работы с расписанием
    const getLessonForDay = (dayNumber, lessonNumber) => {
      return filteredSchedule.value.find(item =>
        item.day_of_week === dayNumber && item.lesson_number === lessonNumber
      )
    }

    const isToday = (dayNumber) => {
      const today = new Date().getDay()
      const todayNumber = today === 0 ? 7 : today
      return dayNumber === todayNumber && !showTodayOnly.value
    }

    const getDayDate = (dayNumber) => {
      if (!showTodayOnly.value) {
        const today = new Date()
        const currentDay = today.getDay()
        const currentDayNumber = currentDay === 0 ? 7 : currentDay
        const diff = dayNumber - currentDayNumber

        const targetDate = new Date(today)
        targetDate.setDate(today.getDate() + diff)

        return targetDate.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
      }
      return ''
    }

    const getLessonTypeClass = (type) => {
      const classes = {
        'lecture': 'lecture',
        'practice': 'practice',
        'lab': 'lab',
        'seminar': 'seminar'
      }
      return classes[type] || ''
    }

    const getWeekTypeClass = (type) => {
      return type === 'odd' ? 'odd-week' : 'even-week'
    }

    const getWeekTypeDisplay = (type) => {
      const types = {
        'odd': 'Нечетная',
        'even': 'Четная',
        'both': 'Каждую'
      }
      return types[type] || type
    }

    const formatDate = (dateString) => {
      if (!dateString) return '—'
      return new Date(dateString).toLocaleDateString('ru-RU')
    }

    const toggleToday = () => {
      showTodayOnly.value = !showTodayOnly.value
    }

    const filterSchedule = () => {
      // Фильтрация происходит автоматически через computed
    }

    // Экспорт
    const exportToPDF = () => {
      alert('Функция экспорта в PDF будет реализована позже')
      // Здесь будет логика экспорта в PDF
    }

    const exportToExcel = () => {
      const headers = ['День', 'Пара', 'Предмет', 'Тип', 'Преподаватель', 'Кабинет', 'Неделя', 'Начало', 'Конец']
      const csvContent = [
        headers.join(','),
        ...filteredSchedule.value.map(item => [
          `"${item.day_display}"`,
          item.lesson_number,
          `"${item.subject_name}"`,
          `"${item.lesson_type_display}"`,
          `"${item.teacher_name}"`,
          item.classroom_number,
          `"${getWeekTypeDisplay(item.week_type)}"`,
          item.start_date,
          item.end_date
        ].join(','))
      ].join('\n')

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `schedule_${selectedGroup.value?.name || 'group'}.csv`
      link.click()
    }

    const printSchedule = () => {
      window.print()
    }

    // Инициализация
    onMounted(() => {
      loadGroups()
    })

    return {
      // Данные
      groups,
      schedule: filteredSchedule,
      selectedGroupId,
      selectedGroup,
      loading,
      error,
      weekType,
      showTodayOnly,
      days,
      lessons,

      // Вычисляемые свойства
      subjectsCount,
      teachersCount,
      filteredSchedule,

      // Методы
      loadSchedule,
      getLessonForDay,
      isToday,
      getDayDate,
      getLessonTypeClass,
      getWeekTypeClass,
      getWeekTypeDisplay,
      formatDate,
      toggleToday,
      filterSchedule,
      exportToPDF,
      exportToExcel,
      printSchedule
    }
  }
}
</script>

<style scoped>
.schedule-view {
  padding: 2rem;
  max-width: 1800px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
}

.header h1 {
  color: #2c3e50;
  border-bottom: 3px solid #667eea;
  padding-bottom: 0.5rem;
}

/* Контролы */
.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.control-group {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-width: 200px;
}

.control-group label {
  font-weight: bold;
  color: #2c3e50;
  font-size: 0.9rem;
}

.control-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  background: white;
}

.today-btn {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  margin-top: 1.5rem;
}

.today-btn:hover {
  background: #5a67d8;
}

/* Информация о группе */
.group-info {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.group-info h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.group-stats {
  display: flex;
  gap: 2rem;
  color: #666;
}

.group-stats span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* ============= ИСПРАВЛЕННАЯ СЕТКА ============= */

.week-schedule {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 20px rgba(0,0,0,0.05);
  overflow: hidden;
  margin-bottom: 2rem;
  display: grid;
  grid-template-columns: 100px repeat(6, 1fr);
  grid-auto-rows: minmax(100px, auto);
}

/* Заголовок дней - первая строка */
.header-corner {
  grid-column: 1;
  grid-row: 1;
  background: #667eea;
  border-right: 1px solid rgba(255,255,255,0.1);
}

.day-header {
  background: #667eea;
  color: white;
  padding: 1rem;
  text-align: center;
  border-right: 1px solid rgba(255,255,255,0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.day-header:last-child {
  border-right: none;
}

.day-name {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
  position: relative;
}

.day-name.today {
  color: #ffeb3b;
}

.today-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #e53e3e;
  color: white;
  font-size: 0.7rem;
  padding: 0.1rem 0.4rem;
  border-radius: 10px;
}

.day-date {
  font-size: 0.85rem;
  opacity: 0.9;
}

/* Строки с парами */
.lesson-row {
  display: contents; /* Дети становятся частью основной сетки */
}

/* Ячейка времени (первый столбец каждой строки) */
.lesson-time {
  grid-column: 1;
  background: #f8f9fa;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0.5rem;
}

.lesson-number {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.lesson-hours {
  font-size: 0.85rem;
  color: #666;
}

/* Ячейки с уроками */
.lesson-slot {
  border-bottom: 1px solid #e2e8f0;
  border-right: 1px solid #e2e8f0;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

/* Убираем границу у последней колонки */
.lesson-slot:nth-child(7n) {
  border-right: none;
}

.lesson-card {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-height: 90px;
}

.lesson-card.lecture {
  border-left: 4px solid #667eea;
  background: #e3f2fd;
}

.lesson-card.practice {
  border-left: 4px solid #48bb78;
  background: #f0fff4;
}

.lesson-card.lab {
  border-left: 4px solid #ed8936;
  background: #fffaf0;
}

.lesson-card.seminar {
  border-left: 4px solid #9f7aea;
  background: #faf5ff;
}

.lesson-subject {
  font-size: 0.9rem;
  color: #2c3e50;
}

.lesson-type {
  font-size: 0.8rem;
  color: #666;
}

.lesson-teacher,
.lesson-room {
  font-size: 0.8rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.lesson-week {
  margin-top: auto;
}

.odd-week {
  display: inline-block;
  background: #c6f6d5;
  color: #22543d;
  padding: 0.1rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 500;
}

.even-week {
  display: inline-block;
  background: #fed7d7;
  color: #742a2a;
  padding: 0.1rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 500;
}

.empty-slot {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #cbd5e0;
  font-style: italic;
}

/* Детальное расписание */
.detailed-schedule {
  margin-top: 3rem;
}

.detailed-schedule h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.schedule-table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  overflow: hidden;
}

.schedule-table {
  width: 100%;
  border-collapse: collapse;
}

.schedule-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e2e8f0;
}

.schedule-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #edf2f7;
}

.schedule-table tr:hover {
  background: #f8f9fa;
}

.type-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

.type-badge.lecture {
  background: #e3f2fd;
  color: #1976d2;
}

.type-badge.practice {
  background: #f0fff4;
  color: #38a169;
}

.type-badge.lab {
  background: #fffaf0;
  color: #dd6b20;
}

.type-badge.seminar {
  background: #faf5ff;
  color: #805ad5;
}

.room-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #edf2f7;
  color: #2d3748;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

.week-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

.week-badge.odd {
  background: #c6f6d5;
  color: #22543d;
}

.week-badge.even {
  background: #fed7d7;
  color: #742a2a;
}

.week-badge.both {
  background: #e9d8fd;
  color: #553c9a;
}

/* Экспорт */
.export-section {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.export-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #667eea;
  color: white;
}

.export-btn:hover {
  background: #5a67d8;
}

/* Состояния */
.loading, .error, .no-group-selected {
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
  padding: 0.5rem 1.5rem;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.no-group-selected {
  color: #666;
}

/* Адаптивность */
@media (max-width: 1200px) {
  .week-schedule {
    overflow-x: auto;
    min-width: 1000px;
  }
}

@media (max-width: 768px) {
  .schedule-view {
    padding: 1rem;
  }

  .controls {
    flex-direction: column;
  }

  .control-group {
    min-width: 100%;
  }

  .group-stats {
    flex-direction: column;
    gap: 0.5rem;
  }

  .export-section {
    flex-direction: column;
  }

  .schedule-table {
    display: block;
    overflow-x: auto;
  }
}

@media print {
  .controls,
  .export-section,
  .today-btn {
    display: none !important;
  }

  .week-schedule {
    box-shadow: none;
    border: 1px solid #ddd;
  }

  .lesson-card {
    box-shadow: none;
    border: 1px solid #eee;
  }
}
</style>