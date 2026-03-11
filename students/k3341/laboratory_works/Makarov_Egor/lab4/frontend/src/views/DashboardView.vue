<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import CaptainDashboard from './CaptainDashboard.vue'
import JuryDashboard    from './JuryDashboard.vue'
import CuratorDashboard from './CuratorDashboard.vue'
import AdminDashboard   from './AdminDashboard.vue'

const auth   = useAuthStore()
const router = useRouter()

const role = computed(() => auth.profile?.role ?? null)

const roleLabel = {
  ADMIN:   'Администратор',
  JURY:    'Жюри',
  CURATOR: 'Куратор',
  CAPTAIN: 'Капитан',
}

const dashComponent = computed(() => {
  if (role.value === 'ADMIN')   return AdminDashboard
  if (role.value === 'JURY')    return JuryDashboard
  if (role.value === 'CURATOR') return CuratorDashboard
  if (role.value === 'CAPTAIN') return CaptainDashboard
  return null
})

const pageTitle = computed(() => {
  if (role.value === 'ADMIN')   return 'Панель администратора'
  if (role.value === 'JURY')    return 'Оценка решений'
  if (role.value === 'CURATOR') return 'Кабинет куратора'
  if (role.value === 'CAPTAIN') return 'Кабинет капитана'
  return 'Личный кабинет'
})

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="app-layout">
    <header class="navbar">
      <div class="navbar-brand">
        <div class="logo-mark">H</div>
        <span>Hackathon</span>
      </div>
      <nav class="navbar-links">
        <router-link to="/dashboard">Кабинет</router-link>
        <router-link to="/tasks">Задачи</router-link>
        <router-link to="/profile">Профиль</router-link>
      </nav>
      <div class="navbar-right">
        <span class="role-pill">{{ roleLabel[role] ?? role }}</span>
        <span class="nav-username">{{ auth.user?.username }}</span>
        <button class="btn-logout" @click="handleLogout">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Выйти
        </button>
      </div>
    </header>

    <main class="dash-main">
      <div class="dash-inner">
        <h1 class="dash-title">{{ pageTitle }}</h1>

        <div v-if="!role" class="state-box">
          <div class="big-spinner"></div>
          <p>Загрузка профиля...</p>
        </div>
        <component :is="dashComponent" v-else />
      </div>
    </main>
  </div>
</template>

<style scoped>
.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}

.role-pill {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent);
  background: var(--accent-glow);
  border: 1px solid rgba(91,110,245,0.3);
  border-radius: 20px;
  padding: 3px 10px;
}

.nav-username {
  font-size: 13px;
  color: var(--text-muted);
}

.dash-main {
  flex: 1;
  background:
    radial-gradient(ellipse 50% 40% at 70% 0%, rgba(91,110,245,0.08), transparent),
    var(--bg);
  padding: 40px 24px 60px;
}

.dash-inner {
  max-width: 860px;
  margin: 0 auto;
}

.dash-title {
  font-family: 'Unbounded', sans-serif;
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 28px;
}
</style>