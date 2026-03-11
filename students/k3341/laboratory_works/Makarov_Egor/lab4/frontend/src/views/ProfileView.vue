<script setup>
import { ref, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth   = useAuthStore()
const router = useRouter()

const editing  = ref(false)
const success  = ref(false)
const fullName = ref('')
const organization = ref('')

const roleLabels = {
  ADMIN: 'Главный администратор', JURY: 'Жюри',
  CURATOR: 'Куратор', CAPTAIN: 'Капитан',
}
const roleLabel = computed(() => roleLabels[auth.profile?.role] || auth.profile?.role || '—')

watch(() => auth.profile, (p) => {
  if (p) { fullName.value = p.full_name || ''; organization.value = p.organization || '' }
}, { immediate: true })

function startEdit()  { editing.value = true;  success.value = false; auth.error = null }
function cancelEdit() { editing.value = false; fullName.value = auth.profile?.full_name || ''; organization.value = auth.profile?.organization || '' }

async function saveProfile() {
  const ok = await auth.updateProfile({ full_name: fullName.value, organization: organization.value })
  if (ok) { editing.value = false; success.value = true; setTimeout(() => (success.value = false), 3000) }
}

async function handleLogout() { await auth.logout(); router.push('/login') }
</script>

<template>
  <div class="app-layout">
    <header class="navbar">
      <div class="navbar-brand"><div class="logo-mark">H</div><span>Hackathon</span></div>
      <nav class="navbar-links">
        <router-link to="/dashboard">Кабинет</router-link>
        <router-link to="/tasks">Задачи</router-link>
        <router-link to="/profile">Профиль</router-link>
      </nav>
      <div style="margin-left:auto;display:flex;align-items:center;gap:12px;">
        <button class="btn-logout" @click="handleLogout">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Выйти
        </button>
      </div>
    </header>

    <div class="profile-page">
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar">{{ auth.user?.username?.[0]?.toUpperCase() || '?' }}</div>
          <div class="profile-title">
            <h1>{{ auth.user?.username }}</h1>
            <span class="role-badge">{{ roleLabel }}</span>
          </div>
        </div>

        <div class="profile-section">
          <h2>Учётные данные</h2>
          <div class="info-grid">
            <div class="info-row">
              <span class="info-label">Email</span>
              <span class="info-value">{{ auth.user?.email || '—' }}</span>
            </div>
          </div>
        </div>

        <div class="profile-section">
          <div class="section-head">
            <h2>Профиль</h2>
            <button v-if="!editing" class="btn-edit" @click="startEdit">Редактировать</button>
          </div>

          <div v-if="!editing" class="info-grid">
            <div class="info-row"><span class="info-label">Полное имя</span><span class="info-value">{{ auth.profile?.full_name || '—' }}</span></div>
            <div class="info-row"><span class="info-label">Организация</span><span class="info-value">{{ auth.profile?.organization || '—' }}</span></div>
          </div>

          <form v-else class="edit-form" @submit.prevent="saveProfile">
            <div class="field"><label>Полное имя</label><input v-model="fullName" placeholder="Иванов Иван Иванович" /></div>
            <div class="field"><label>Организация</label><input v-model="organization" placeholder="Название организации" /></div>
            <div v-if="auth.error" class="error-msg">{{ auth.error }}</div>
            <div class="edit-actions">
              <button type="submit" class="btn-primary" :disabled="auth.loading">
                <span v-if="auth.loading" class="spinner"></span><span v-else>Сохранить</span>
              </button>
              <button type="button" class="btn-secondary" @click="cancelEdit">Отмена</button>
            </div>
          </form>

          <div v-if="success" class="success-msg">✓ Профиль обновлён</div>
        </div>
      </div>
    </div>
  </div>
</template>