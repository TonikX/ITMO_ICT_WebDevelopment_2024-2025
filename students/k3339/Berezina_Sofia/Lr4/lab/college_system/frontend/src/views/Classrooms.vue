<template>
  <div class="classrooms-view">
    <div class="header">
      <h1>Кабинеты</h1>
      <div class="search-box">
        <input
          v-model="searchQuery"
          @input="searchClassrooms"
          placeholder="Поиск по номеру или названию..."
          class="search-input"
        >
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка кабинетов...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadClassrooms" class="retry-btn">Повторить</button>
    </div>

    <div v-else class="classrooms-grid">
      <div v-for="classroom in filteredClassrooms" :key="classroom.id" class="classroom-card">
        <div class="classroom-header">
          <h3>Кабинет {{ classroom.room_number }}</h3>
          <span class="capacity-badge">{{ classroom.capacity || '?' }} мест</span>
        </div>

        <div class="classroom-body">
          <p v-if="classroom.name" class="classroom-name">
            {{ classroom.name }}
          </p>
          <p v-else class="no-name">Название не указано</p>

          <div class="classroom-details">
            <div class="detail-item">
              <span class="label">ID:</span>
              <span class="value">{{ classroom.id }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Номер:</span>
              <span class="value">{{ classroom.room_number }}</span>
            </div>
            <div v-if="classroom.capacity" class="detail-item">
              <span class="label">Вместимость:</span>
              <span class="value">{{ classroom.capacity }} чел.</span>
            </div>
          </div>
        </div>

        <div class="classroom-footer">
          <span class="status available">Доступен</span>
        </div>
      </div>

      <div v-if="!filteredClassrooms.length" class="no-data">
        Кабинеты не найдены
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiEndpoints } from '@/api'

export default {
  name: 'ClassroomsView',

  setup() {
    const router = useRouter()

    const classrooms = ref([])
    const loading = ref(true)
    const error = ref('')
    const searchQuery = ref('')

    const loadClassrooms = async () => {
      loading.value = true
      error.value = ''

      try {
        const response = await apiEndpoints.classrooms.list()
        classrooms.value = response.data
      } catch (err) {
        console.error('Ошибка загрузки кабинетов:', err)
        error.value = 'Не удалось загрузить список кабинетов'
      } finally {
        loading.value = false
      }
    }

    const filteredClassrooms = computed(() => {
      if (!searchQuery.value) return classrooms.value

      const query = searchQuery.value.toLowerCase()
      return classrooms.value.filter(classroom =>
        classroom.room_number.toString().includes(query) ||
        (classroom.name && classroom.name.toLowerCase().includes(query))
      )
    })

    const searchClassrooms = () => {
      // Поиск происходит автоматически через computed
    }

    const viewSchedule = (classroom) => {
      // Здесь можно перейти на страницу расписания для кабинета
      console.log('Просмотр расписания кабинета:', classroom)
    }

    onMounted(() => {
      loadClassrooms()
    })

    return {
      classrooms,
      loading,
      error,
      searchQuery,
      filteredClassrooms,
      loadClassrooms,
      searchClassrooms,
      viewSchedule
    }
  }
}
</script>

<style scoped>
.classrooms-view {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header h1 {
  color: #2c3e50;
  margin: 0;
}

.search-box {
  flex: 1;
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.classrooms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.classroom-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #f1f3f5;
}

.classroom-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.classroom-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.classroom-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.capacity-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.classroom-body {
  padding: 1.5rem;
}

.classroom-name {
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0 0 1rem 0;
  min-height: 24px;
}

.no-name {
  color: #95a5a6;
  font-style: italic;
  margin: 0 0 1rem 0;
  min-height: 24px;
}

.classroom-details {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

.detail-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.label {
  color: #666;
  font-size: 0.9rem;
}

.value {
  color: #2c3e50;
  font-weight: 500;
}

.classroom-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #f1f3f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status.available {
  background: #d4edda;
  color: #155724;
}

.schedule-btn {
  padding: 0.5rem 1rem;
  background: #48bb78;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background 0.3s ease;
}

.schedule-btn:hover {
  background: #38a169;
}

/* Состояния */
.loading, .error, .no-data {
  text-align: center;
  padding: 3rem;
  grid-column: 1 / -1;
}

.no-data {
  color: #95a5a6;
  font-style: italic;
}

@media (max-width: 768px) {
  .classrooms-view {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: 100%;
  }

  .classrooms-grid {
    grid-template-columns: 1fr;
  }
}
</style>