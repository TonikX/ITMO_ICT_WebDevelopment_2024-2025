<template>
  <div class="dashboard">
    <div class="header">
      <h1>Панель управления</h1>
      <div class="user-info">
        <span>Привет, {{ user?.username }}!</span>
        <button @click="logout" class="logout-btn">Выйти</button>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <h3>Всего групп</h3>
        <p class="stat-number">{{ stats.groupsCount || 0 }}</p>
      </div>

      <div class="stat-card">
        <h3>Активных студентов</h3>
        <p class="stat-number">{{ stats.studentsCount || 0 }}</p>
      </div>

      <div class="stat-card">
        <h3>Преподавателей</h3>
        <p class="stat-number">{{ stats.teachersCount || 0 }}</p>
      </div>

      <div class="stat-card">
        <h3>Предметов</h3>
        <p class="stat-number">{{ stats.subjectsCount || 0 }}</p>
      </div>
    </div>

    <div class="sections">
      <div class="section">
        <h2>Быстрые действия</h2>
        <div class="action-buttons">
          <router-link to="/groups" class="action-btn">
            Группы
          </router-link>
          <router-link to="/classrooms" class="action-btn">
            Кабинеты
          </router-link>
          <router-link to="/students" class="action-btn">
            Студенты
          </router-link>
          <router-link to="/teachers" class="action-btn">
            Учителя
          </router-link>
          <router-link to="/subjects" class="action-btn">
            Предметы
          </router-link>
          <router-link to="/schedule/group/<int:group_id>/" class="action-btn">
            Расписание
          </router-link>
        </div>
      </div>


    </div>
  </div>


</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/api'

export default {
  name: 'DashboardView',

  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    return { authStore, router }
  },

  data() {
    return {
      loading: true,
      stats: {},
      recentGrades: []
    }
  },

  computed: {
    user() {
      return this.authStore.user
    }
  },

  async mounted() {
    await this.loadData()
  },

  methods: {
    async loadData() {
      this.loading = true
      try {
        // Загружаем статистику (нужно будет создать эндпоинт или вычислять на клиенте)
        this.stats = {
          groupsCount: 12,
          studentsCount: 350,
          teachersCount: 45,
          subjectsCount: 28
        }

        // Загружаем последние оценки (если есть доступ)
        try {
          // Пример: получаем оценки первого студента для демонстрации
          const response = await api.get('students/1/grades/')
          this.recentGrades = response.data.slice(0, 5)
        } catch (error) {
          console.log('Нет доступа к оценкам или данных нет')
        }
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.authStore.logout()
      this.router.push('/login')
    }
  }
}
</script>



<style scoped>
.dashboard {
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
  margin: 0.5rem 0;
}

.sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.section {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.action-btn {
  display: block;
  padding: 1rem;
  background: #667eea;
  color: white;
  text-align: center;
  text-decoration: none;
  border-radius: 15px;
  transition: background 0.3s;
}

.action-btn:hover {
  background: #5a67d8;
}

.data-list ul {
  list-style: none;
  padding: 0;
}

.data-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.quick-access {
  margin-top: 2rem;
}

.access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}
</style>