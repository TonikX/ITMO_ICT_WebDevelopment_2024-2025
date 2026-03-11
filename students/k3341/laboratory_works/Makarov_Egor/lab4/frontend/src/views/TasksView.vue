<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth     = useAuthStore()
const router   = useRouter()
const tasks    = ref([])
const loading  = ref(true)
const error    = ref(null)
const expanded = ref(null)

async function fetchTasks() {
  loading.value = true; error.value = null
  try {
    const res = await fetch('http://localhost:8000/api/tasks/?page_size=100', {
      headers: { Authorization: `Token ${auth.token}` },
    })
    if (!res.ok) throw new Error('Не удалось загрузить задачи')
    const data = await res.json()
    tasks.value = Array.isArray(data) ? data : (data.results ?? [])
  } catch(e) { error.value = e.message }
  finally    { loading.value = false }
}

function toggleExpand(id) { expanded.value = expanded.value === id ? null : id }
async function handleLogout() { await auth.logout(); router.push('/login') }

onMounted(fetchTasks)
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
      <div style="margin-left:auto">
        <button class="btn-logout" @click="handleLogout">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Выйти
        </button>
      </div>
    </header>

    <main class="tasks-main">
      <div class="tasks-header">
        <h1>Задачи хакатона</h1>
        <span class="tasks-count" v-if="!loading">{{ tasks.length }} задач</span>
      </div>

      <div v-if="loading" class="state-box"><div class="big-spinner"></div><p>Загружаем задачи...</p></div>

      <div v-else-if="error" class="state-box">
        <div class="state-icon error-icon">!</div>
        <p>{{ error }}</p>
        <button class="btn-primary" @click="fetchTasks">Повторить</button>
      </div>

      <div v-else-if="tasks.length === 0" class="state-box">
        <div class="state-icon">∅</div>
        <p>Задачи ещё не добавлены</p>
      </div>

      <div v-else class="tasks-list">
        <article v-for="task in tasks" :key="task.id" class="task-card" :class="{ expanded: expanded === task.id }">
          <div class="task-card-header" @click="toggleExpand(task.id)">
            <div class="task-card-left">
              <span class="task-num">#{{ task.id }}</span>
              <div>
                <h2 class="task-title">{{ task.title }}</h2>
                <div class="task-meta">
                  <span v-if="task.curator" class="meta-item">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                    {{ task.curator.username }}
                  </span>
                  <span class="meta-item">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                    {{ new Date(task.created_at).toLocaleDateString('ru-RU') }}
                  </span>
                </div>
              </div>
            </div>
            <div class="task-card-right">
              <div class="tags-row">
                <span v-for="tag in task.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
              </div>
              <div class="expand-btn" :class="{ rotated: expanded === task.id }">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
            </div>
          </div>

          <div v-if="expanded === task.id" class="task-body">
            <p class="task-description">{{ task.description }}</p>
            <div class="task-resources">
              <a v-if="task.consultation_url" :href="task.consultation_url" target="_blank" rel="noopener" class="resource-link consultation">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                Записаться на консультацию
              </a>
              <template v-if="task.resource_links?.length">
                <div class="resources-label">Ссылки</div>
                <div class="resources-grid">
                  <a v-for="link in task.resource_links" :key="link.id" :href="link.url" target="_blank" rel="noopener" class="resource-link">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                    {{ link.title }}
                  </a>
                </div>
              </template>
              <template v-if="task.resource_files?.length">
                <div class="resources-label">Файлы</div>
                <div class="resources-grid">
                  <a v-for="file in task.resource_files" :key="file.id" :href="file.file_url" target="_blank" rel="noopener" class="resource-link">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                    {{ file.title }}
                  </a>
                </div>
              </template>
            </div>
          </div>
        </article>
      </div>
    </main>
  </div>
</template>

<style scoped>
.tasks-main {
  flex: 1;
  max-width: 800px; margin: 0 auto;
  padding: 40px 24px 60px;
  width: 100%;
}
.tasks-header { display: flex; align-items: baseline; gap: 14px; margin-bottom: 28px; }
.tasks-header h1 { font-family: 'Unbounded', sans-serif; font-size: 24px; font-weight: 600; }
.tasks-count { font-size: 13px; color: var(--text-muted); }

.state-box { display: flex; flex-direction: column; align-items: center; gap: 16px; padding: 80px 0; color: var(--text-muted); }
.state-icon { width: 48px; height: 48px; border-radius: 12px; background: var(--surface2); border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; font-size: 20px; color: var(--text-muted); }
.error-icon { color: var(--error); border-color: rgba(248,113,113,0.3); background: rgba(248,113,113,0.1); }

.tasks-list { display: flex; flex-direction: column; gap: 8px; }
.task-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; transition: border-color 0.2s; }
.task-card:hover, .task-card.expanded { border-color: rgba(91,110,245,0.4); }
.task-card-header { display: flex; align-items: center; justify-content: space-between; padding: 18px 20px; cursor: pointer; gap: 16px; }
.task-card-left { display: flex; align-items: flex-start; gap: 14px; min-width: 0; }
.task-num { font-family: 'Unbounded', sans-serif; font-size: 11px; color: var(--accent); background: var(--accent-glow); border: 1px solid rgba(91,110,245,0.3); border-radius: 6px; padding: 3px 7px; flex-shrink: 0; margin-top: 2px; }
.task-title { font-size: 15px; font-weight: 500; margin-bottom: 5px; }
.task-meta { display: flex; gap: 14px; flex-wrap: wrap; }
.meta-item { display: flex; align-items: center; gap: 4px; font-size: 12px; color: var(--text-muted); }
.task-card-right { display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
.tags-row { display: flex; flex-wrap: wrap; gap: 6px; justify-content: flex-end; }
.tag { font-size: 11px; color: var(--text-muted); background: var(--surface2); border: 1px solid var(--border); border-radius: 5px; padding: 2px 8px; }
.expand-btn { color: var(--text-muted); transition: transform 0.2s; flex-shrink: 0; }
.expand-btn.rotated { transform: rotate(180deg); }

.task-body { padding: 0 20px 20px; border-top: 1px solid var(--border); padding-top: 18px; }
.task-description { font-size: 14px; color: var(--text); line-height: 1.7; white-space: pre-line; margin-bottom: 18px; }
.task-resources { display: flex; flex-direction: column; gap: 10px; }
.resources-label { font-size: 11px; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; }
.resources-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.resource-link { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; color: var(--accent); background: var(--accent-glow); border: 1px solid rgba(91,110,245,0.3); border-radius: 8px; padding: 6px 12px; text-decoration: none; transition: background 0.2s; }
.resource-link:hover { background: rgba(91,110,245,0.3); }
.resource-link.consultation { background: rgba(52,211,153,0.1); border-color: rgba(52,211,153,0.3); color: var(--success); }
.resource-link.consultation:hover { background: rgba(52,211,153,0.2); }
</style>