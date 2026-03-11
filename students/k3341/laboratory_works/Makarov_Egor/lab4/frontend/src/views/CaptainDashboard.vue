<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { api } from '../api'

const auth = useAuthStore()
const $api = computed(() => api(auth.token))

// --- state ---
const team       = ref(null)   // моя команда или null
const tasks      = ref([])
const solutions  = ref([])
const loading    = ref(true)
const error      = ref(null)
const msg        = ref('')
const msgType    = ref('success')

// формы
const teamForm   = ref({ name: '', motto: '', selected_task_id: null })
const memberForm = ref({ full_name: '', email: '', role_in_team: '' })
const solForm    = ref({ title: '', description: '', repo_url: '', submit: false })
const editingTeam = ref(false)
const showSolForm = ref(false)

function flash(text, type = 'success') {
  msg.value = text; msgType.value = type
  setTimeout(() => (msg.value = ''), 3500)
}

async function load() {
  loading.value = true; error.value = null
  try {
    const [tr, ta, so] = await Promise.all([
      $api.value.get('/api/teams/?page_size=100'),
      $api.value.get('/api/tasks/?page_size=100'),
      $api.value.get('/api/solutions/?page_size=100'),
    ])
    tasks.value    = tr2arr(ta)
    solutions.value= tr2arr(so)
    const myTeams  = tr2arr(tr)
    team.value     = myTeams[0] ?? null
    if (team.value) {
      teamForm.value = {
        name: team.value.name,
        motto: team.value.motto,
        selected_task_id: team.value.selected_task?.id ?? null,
      }
    }
  } catch(e) { error.value = e.message }
  finally { loading.value = false }
}

function tr2arr(data) { return Array.isArray(data) ? data : (data?.results ?? []) }

// --- Team CRUD ---
async function createTeam() {
  try {
    const t = await $api.value.post('/api/teams/', teamForm.value)
    team.value = t
    flash('Команда создана!')
    await load()
  } catch(e) { flash(e.message, 'error') }
}

async function saveTeam() {
  try {
    const t = await $api.value.patch(`/api/teams/${team.value.id}/`, teamForm.value)
    team.value = t
    editingTeam.value = false
    flash('Команда обновлена!')
    await load()
  } catch(e) { flash(e.message, 'error') }
}

// --- Members ---
async function addMember() {
  if (!memberForm.value.full_name) return
  const existing = team.value.members.map(m => ({
    full_name: m.full_name, email: m.email, role_in_team: m.role_in_team
  }))
  try {
    await $api.value.patch(`/api/teams/${team.value.id}/`, {
      member_items: [...existing, { ...memberForm.value }]
    })
    memberForm.value = { full_name: '', email: '', role_in_team: '' }
    flash('Участник добавлен!')
    await load()
  } catch(e) { flash(e.message, 'error') }
}

async function removeMember(idx) {
  const members = team.value.members
    .filter((_, i) => i !== idx)
    .map(m => ({ full_name: m.full_name, email: m.email, role_in_team: m.role_in_team }))
  try {
    await $api.value.patch(`/api/teams/${team.value.id}/`, { member_items: members })
    flash('Участник удалён')
    await load()
  } catch(e) { flash(e.message, 'error') }
}

// --- Solution ---
const mySolution = computed(() =>
  solutions.value.find(s => s.team?.id === team.value?.id) ?? null
)

async function submitSolution() {
  const body = {
    ...solForm.value,
    task_id: team.value.selected_task?.id,
  }
  try {
    if (mySolution.value) {
      await $api.value.patch(`/api/solutions/${mySolution.value.id}/`, body)
      flash('Решение обновлено!')
    } else {
      await $api.value.post('/api/solutions/', body)
      flash(body.submit ? 'Решение отправлено!' : 'Черновик сохранён!')
    }
    showSolForm.value = false
    await load()
  } catch(e) { flash(e.message, 'error') }
}

function startEditSol() {
  if (mySolution.value) {
    solForm.value = {
      title: mySolution.value.title,
      description: mySolution.value.description,
      repo_url: mySolution.value.repo_url,
      submit: false,
    }
  } else {
    solForm.value = { title: '', description: '', repo_url: '', submit: false }
  }
  showSolForm.value = true
}

const selectedTask = computed(() =>
  tasks.value.find(t => t.id === team.value?.selected_task?.id) ??
  team.value?.selected_task ?? null
)

onMounted(load)
</script>

<template>
  <div class="dash-content">
    <div v-if="loading" class="state-box"><div class="big-spinner"></div></div>
    <div v-else-if="error" class="state-box error-state">{{ error }}</div>

    <template v-else>
      <!-- Flash -->
      <div v-if="msg" :class="['flash', msgType]">{{ msg }}</div>

      <!-- === Создать команду === -->
      <section v-if="!team" class="card">
        <h2 class="section-title">Создать команду</h2>
        <div class="form-grid">
          <div class="field">
            <label>Название команды *</label>
            <input v-model="teamForm.name" placeholder="DreamTeam" required />
          </div>
          <div class="field">
            <label>Девиз</label>
            <input v-model="teamForm.motto" placeholder="Ship it!" />
          </div>
          <div class="field full">
            <label>Выбрать задачу</label>
            <select v-model="teamForm.selected_task_id">
              <option :value="null">— не выбрана —</option>
              <option v-for="t in tasks" :key="t.id" :value="t.id">{{ t.title }}</option>
            </select>
          </div>
        </div>
        <button class="btn-primary" @click="createTeam" :disabled="!teamForm.name">
          Создать команду
        </button>
      </section>

      <!-- === Команда === -->
      <template v-else>

        <!-- Карточка команды -->
        <section class="card">
          <div class="section-head">
            <h2 class="section-title">Моя команда</h2>
            <button class="btn-edit" @click="editingTeam = !editingTeam">
              {{ editingTeam ? 'Отмена' : 'Редактировать' }}
            </button>
          </div>

          <div v-if="!editingTeam" class="info-grid">
            <div class="info-row"><span class="info-label">Название</span><span class="info-value">{{ team.name }}</span></div>
            <div class="info-row"><span class="info-label">Девиз</span><span class="info-value">{{ team.motto || '—' }}</span></div>
            <div class="info-row">
              <span class="info-label">Задача</span>
              <span class="info-value">{{ team.selected_task?.title || '— не выбрана —' }}</span>
            </div>
          </div>

          <div v-else class="form-grid">
            <div class="field">
              <label>Название</label>
              <input v-model="teamForm.name" />
            </div>
            <div class="field">
              <label>Девиз</label>
              <input v-model="teamForm.motto" />
            </div>
            <div class="field full">
              <label>Задача</label>
              <select v-model="teamForm.selected_task_id">
                <option :value="null">— не выбрана —</option>
                <option v-for="t in tasks" :key="t.id" :value="t.id">{{ t.title }}</option>
              </select>
            </div>
            <div class="field full">
              <button class="btn-primary" @click="saveTeam">Сохранить</button>
            </div>
          </div>
        </section>

        <!-- Участники -->
        <section class="card">
          <h2 class="section-title">Участники команды</h2>

          <div v-if="team.members.length" class="members-list">
            <div v-for="(m, i) in team.members" :key="i" class="member-row">
              <div class="member-info">
                <span class="member-name">{{ m.full_name }}</span>
                <span class="member-meta">{{ m.role_in_team || '—' }} · {{ m.email || '—' }}</span>
              </div>
              <button class="btn-icon danger" @click="removeMember(i)" title="Удалить">✕</button>
            </div>
          </div>
          <p v-else class="empty-hint">Участников пока нет</p>

          <div class="form-grid mt-16">
            <div class="field">
              <label>Полное имя *</label>
              <input v-model="memberForm.full_name" placeholder="Иванов Иван" />
            </div>
            <div class="field">
              <label>Email</label>
              <input v-model="memberForm.email" placeholder="ivan@example.com" />
            </div>
            <div class="field">
              <label>Роль в команде</label>
              <input v-model="memberForm.role_in_team" placeholder="Backend" />
            </div>
            <div class="field align-end">
              <button class="btn-secondary" @click="addMember" :disabled="!memberForm.full_name">
                + Добавить
              </button>
            </div>
          </div>
        </section>

        <!-- Выбранная задача -->
        <section v-if="selectedTask" class="card">
          <h2 class="section-title">Задача: {{ selectedTask.title }}</h2>
          <p class="task-desc">{{ selectedTask.description }}</p>

          <div v-if="selectedTask.consultation_url" class="resource-row">
            <a :href="selectedTask.consultation_url" target="_blank" class="resource-link consultation">
              📅 Записаться на консультацию
            </a>
          </div>

          <template v-if="selectedTask.resource_links?.length">
            <div class="resources-label">Ссылки</div>
            <div class="resources-wrap">
              <a v-for="l in selectedTask.resource_links" :key="l.id"
                 :href="l.url" target="_blank" class="resource-link">🔗 {{ l.title }}</a>
            </div>
          </template>

          <template v-if="selectedTask.resource_files?.length">
            <div class="resources-label">Файлы для скачивания</div>
            <div class="resources-wrap">
              <a v-for="f in selectedTask.resource_files" :key="f.id"
                 :href="f.file_url" target="_blank" class="resource-link">📄 {{ f.title }}</a>
            </div>
          </template>
        </section>

        <!-- Решение -->
        <section class="card">
          <div class="section-head">
            <h2 class="section-title">Решение</h2>
            <button
              v-if="!showSolForm && mySolution?.status !== 'SUBMITTED'"
              class="btn-edit"
              @click="startEditSol"
              :disabled="!team.selected_task"
            >
              {{ mySolution ? 'Редактировать' : 'Добавить решение' }}
            </button>
          </div>

          <div v-if="!team.selected_task && !mySolution" class="empty-hint">
            Сначала выберите задачу для команды
          </div>

          <div v-else-if="mySolution && !showSolForm" class="info-grid">
            <div class="info-row"><span class="info-label">Название</span><span class="info-value">{{ mySolution.title }}</span></div>
            <div class="info-row">
              <span class="info-label">Статус</span>
              <span :class="['badge', mySolution.status === 'SUBMITTED' ? 'badge-green' : 'badge-gray']">
                {{ mySolution.status === 'SUBMITTED' ? 'Отправлено' : 'Черновик' }}
              </span>
            </div>
            <div v-if="mySolution.repo_url" class="info-row">
              <span class="info-label">Репозиторий</span>
              <a :href="mySolution.repo_url" target="_blank" class="link">{{ mySolution.repo_url }}</a>
            </div>
            <div v-if="mySolution.description" class="field full">
              <label>Описание</label>
              <p class="task-desc">{{ mySolution.description }}</p>
            </div>
            <div v-if="mySolution.status === 'SUBMITTED'" class="empty-hint" style="padding:0">
              ✓ Решение отправлено — редактирование недоступно
            </div>
          </div>

          <div v-else-if="showSolForm">
            <div class="form-grid">
              <div class="field full">
                <label>Название решения *</label>
                <input v-model="solForm.title" placeholder="Наше решение" />
              </div>
              <div class="field full">
                <label>Описание</label>
                <textarea v-model="solForm.description" rows="4" placeholder="Опишите решение..."></textarea>
              </div>
              <div class="field full">
                <label>Ссылка на репозиторий</label>
                <input v-model="solForm.repo_url" placeholder="https://github.com/..." />
              </div>
              <div class="field full checkbox-row">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="solForm.submit" />
                  Отправить на рассмотрение (нельзя будет изменить)
                </label>
              </div>
            </div>
            <div class="form-actions">
              <button class="btn-primary" @click="submitSolution" :disabled="!solForm.title">
                {{ solForm.submit ? 'Отправить' : 'Сохранить черновик' }}
              </button>
              <button class="btn-secondary" @click="showSolForm = false">Отмена</button>
            </div>
          </div>

          <div v-else-if="!mySolution && team.selected_task" class="empty-hint">
            Решение ещё не добавлено
          </div>
        </section>

      </template>
    </template>
  </div>
</template>