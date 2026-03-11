<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { api } from '../api'

const auth = useAuthStore()
const $api = computed(() => api(auth.token))

const tasks     = ref([])
const teams     = ref([])
const solutions = ref([])
const users     = ref([])
const loading   = ref(true)
const error     = ref(null)
const msg       = ref('')
const msgType   = ref('success')

// Формы
const taskForm  = ref({ title: '', description: '', curator: null, consultation_url: '' })
const showTaskForm = ref(false)
const editingTask  = ref(null)

function flash(text, type = 'success') {
  msg.value = text; msgType.value = type
  setTimeout(() => (msg.value = ''), 3000)
}
function tr2arr(d) { return Array.isArray(d) ? d : (d?.results ?? []) }

async function load() {
  loading.value = true; error.value = null
  try {
    const [ta, te, so, us] = await Promise.all([
      $api.value.get('/api/tasks/?page_size=100'),
      $api.value.get('/api/teams/?page_size=100'),
      $api.value.get('/api/solutions/?page_size=100'),
      $api.value.get('/auth/users/?page_size=100'),
    ])
    tasks.value     = tr2arr(ta)
    teams.value     = tr2arr(te)
    solutions.value = tr2arr(so)
    users.value     = tr2arr(us)
  } catch(e) { error.value = e.message }
  finally { loading.value = false }
}

// Только кураторы для выбора
const curators = computed(() =>
  users.value.filter(u => u.profile?.role === 'CURATOR' || u.role === 'CURATOR')
)

function startCreate() {
  taskForm.value = { title: '', description: '', curator: null, consultation_url: '' }
  editingTask.value = null
  showTaskForm.value = true
}

function startEdit(task) {
  taskForm.value = {
    title: task.title,
    description: task.description,
    curator: task.curator?.id ?? null,
    consultation_url: task.consultation_url || '',
  }
  editingTask.value = task
  showTaskForm.value = true
}

async function saveTask() {
  const body = { ...taskForm.value }
  if (!body.curator) body.curator = null
  try {
    if (editingTask.value) {
      await $api.value.patch(`/api/tasks/${editingTask.value.id}/`, body)
      flash('Задача обновлена!')
    } else {
      await $api.value.post('/api/tasks/', body)
      flash('Задача создана!')
    }
    showTaskForm.value = false
    await load()
  } catch(e) { flash(e.message, 'error') }
}

async function deleteTask(id) {
  if (!confirm('Удалить задачу?')) return
  try {
    await $api.value.del(`/api/tasks/${id}/`)
    flash('Задача удалена')
    await load()
  } catch(e) { flash(e.message, 'error') }
}

// Быстрое назначение куратора прямо из списка задач
const assignForms = ref({}) // { task_id: curator_id }

async function assignCurator(task) {
  try {
    await $api.value.patch(`/api/tasks/${task.id}/`, { curator: assignForms.value[task.id] || null })
    flash('Куратор назначен!')
    await load()
  } catch(e) { flash(e.message, 'error') }
}

onMounted(load)
</script>

<template>
  <div class="dash-content">
    <div v-if="loading" class="state-box"><div class="big-spinner"></div></div>
    <div v-else-if="error" class="state-box error-state">{{ error }}</div>

    <template v-else>
      <div v-if="msg" :class="['flash', msgType]">{{ msg }}</div>

      <!-- === Задачи === -->
      <section class="card">
        <div class="section-head">
          <h2 class="section-title">Задачи</h2>
          <button class="btn-edit" @click="startCreate">+ Создать задачу</button>
        </div>

        <!-- Форма создания/редактирования -->
        <div v-if="showTaskForm" class="inner-form">
          <div class="form-grid">
            <div class="field full">
              <label>Название *</label>
              <input v-model="taskForm.title" placeholder="Название задачи" />
            </div>
            <div class="field full">
              <label>Описание *</label>
              <textarea v-model="taskForm.description" rows="4" placeholder="Описание задачи..."></textarea>
            </div>
            <div class="field">
              <label>Куратор</label>
              <select v-model="taskForm.curator">
                <option :value="null">— не назначен —</option>
                <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
              </select>
            </div>
            <div class="field">
              <label>Ссылка на консультацию</label>
              <input v-model="taskForm.consultation_url" placeholder="https://zoom.us/..." />
            </div>
          </div>
          <div class="form-actions">
            <button class="btn-primary" @click="saveTask" :disabled="!taskForm.title || !taskForm.description">
              {{ editingTask ? 'Сохранить' : 'Создать' }}
            </button>
            <button class="btn-secondary" @click="showTaskForm = false">Отмена</button>
          </div>
        </div>

        <div v-if="!tasks.length" class="empty-hint">Задач пока нет</div>

        <div v-else class="admin-table-wrap">
          <table class="admin-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Название</th>
                <th>Куратор</th>
                <th>Команд</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in tasks" :key="task.id">
                <td class="id-cell">{{ task.id }}</td>
                <td>
                  <span class="table-title">{{ task.title }}</span>
                  <div class="tags-row mt-4">
                    <span v-for="tag in task.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
                  </div>
                </td>
                <td>
                  <div class="assign-row">
                    <select
                      v-model="assignForms[task.id]"
                      @vue:mounted="assignForms[task.id] = task.curator?.id ?? null"
                      class="assign-select"
                    >
                      <option :value="null">— нет —</option>
                      <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
                    </select>
                    <button class="btn-icon" @click="assignCurator(task)" title="Сохранить">✓</button>
                  </div>
                </td>
                <td class="center">{{ teams.filter(t => t.selected_task?.id === task.id).length }}</td>
                <td>
                  <div class="actions-row">
                    <button class="btn-icon" @click="startEdit(task)" title="Редактировать">✏</button>
                    <button class="btn-icon danger" @click="deleteTask(task.id)" title="Удалить">✕</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- === Команды (только просмотр) === -->
      <section class="card">
        <h2 class="section-title">Команды <span class="section-hint">только просмотр</span></h2>

        <div v-if="!teams.length" class="empty-hint">Команд пока нет</div>
        <div v-else class="admin-table-wrap">
          <table class="admin-table">
            <thead>
              <tr><th>#</th><th>Название</th><th>Капитан</th><th>Задача</th><th>Участников</th></tr>
            </thead>
            <tbody>
              <tr v-for="team in teams" :key="team.id">
                <td class="id-cell">{{ team.id }}</td>
                <td><span class="table-title">{{ team.name }}</span><br><span class="table-sub">{{ team.motto }}</span></td>
                <td>{{ team.captain?.username }}</td>
                <td>{{ team.selected_task?.title || '—' }}</td>
                <td class="center">{{ team.members?.length ?? 0 }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- === Решения (только просмотр) === -->
      <section class="card">
        <h2 class="section-title">Решения <span class="section-hint">только просмотр</span></h2>

        <div v-if="!solutions.length" class="empty-hint">Решений пока нет</div>
        <div v-else class="solutions-list">
          <div v-for="sol in solutions" :key="sol.id" class="solution-card inner">
            <div class="sol-header">
              <div>
                <h3 class="sol-title">{{ sol.title }}</h3>
                <div class="sol-meta">
                  <span class="meta-chip">🏷 {{ sol.task?.title }}</span>
                  <span class="meta-chip">👥 {{ sol.team?.name }}</span>
                  <span :class="['badge', sol.status === 'SUBMITTED' ? 'badge-green' : 'badge-gray']">
                    {{ sol.status === 'SUBMITTED' ? 'Отправлено' : 'Черновик' }}
                  </span>
                  <span v-if="sol.avg_score != null" class="score-badge sm">⭐ {{ sol.avg_score }}</span>
                </div>
              </div>
            </div>
            <a v-if="sol.repo_url" :href="sol.repo_url" target="_blank" class="resource-link">🔗 Репозиторий</a>
          </div>
        </div>
      </section>

    </template>
  </div>
</template>