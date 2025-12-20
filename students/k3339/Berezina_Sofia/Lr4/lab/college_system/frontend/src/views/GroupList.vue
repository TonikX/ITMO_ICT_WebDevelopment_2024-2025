<template>
  <div class="groups-view">
    <h1>Группы студентов</h1>

    <div class="controls">
      <select v-model="selectedCourse" @change="loadGroups">
        <option value="">Выберите курс</option>
        <option v-for="course in [1,2,3,4]" :key="course" :value="course">
          {{ course }} курс
        </option>
      </select>
    </div>

    <div v-if="loading" class="loading">Загрузка групп...</div>

    <div v-else-if="groups.length" class="groups-grid">
      <div v-for="group in groups" :key="group.id" class="group-card">
        <h3>{{ group.name }}</h3>
        <p><strong>Курс:</strong> {{ group.course_display }}</p>
        <p><strong>Специальность:</strong> {{ group.specialty }}</p>
        <p><strong>Куратор:</strong> {{ group.curator_name || 'Не назначен' }}</p>
        <p><strong>Год создания:</strong> {{ group.created_year }}</p>

        <div class="group-actions">
          <router-link :to="`/groups/${group.id}/students`" class="btn">
            👨‍🎓 Студенты
          </router-link>
          <router-link :to="`/groups/${group.id}/schedule`" class="btn">
            📅 Расписание
          </router-link>
        </div>
      </div>
    </div>

    <div v-else class="no-data">
      <p v-if="selectedCourse">Нет групп на {{ selectedCourse }} курсе</p>
      <p v-else>Выберите курс для отображения групп</p>
    </div>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'GroupsView',

  data() {
    return {
      selectedCourse: '',
      groups: [],
      loading: false
    }
  },

  methods: {
    async loadGroups() {
      if (!this.selectedCourse) {
        this.groups = []
        return
      }

      this.loading = true
      try {
        const response = await api.get(`groups/course/${this.selectedCourse}/`)
        this.groups = response.data
      } catch (error) {
        console.error('Ошибка загрузки групп:', error)
        this.groups = []
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.groups-view {
  padding: 2rem;
}

.controls {
  margin: 2rem 0;
}

.controls select {
  padding: 0.5rem;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.group-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.group-card h3 {
  color: #667eea;
  margin-top: 0;
}

.group-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-size: 0.9rem;
}

.btn:hover {
  background: #5a67d8;
}

.loading, .no-data {
  text-align: center;
  padding: 3rem;
  color: #666;
}
</style>