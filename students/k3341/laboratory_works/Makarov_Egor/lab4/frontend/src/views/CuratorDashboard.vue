<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { api } from '../api'

const auth = useAuthStore()
const $api = computed(() => api(auth.token))

const myTask    = ref(null)
const solutions = ref([])
const loading   = ref(true)
const error     = ref(null)
const msg       = ref('')
const msgType   = ref('success')

// формы
const linkForm  = ref({ title: '', url: '' })
const consultForm = ref('')
const showConsult = ref(false)

function flash(text, type = 'success') {
  msg.value = text; msgType.value = type
  setTimeout(() => (msg.value = ''), 3000)
}
function tr2arr(d) { return Array.isArray(d) ? d : (d?.results ?? []) }

async function load() {
  loading.value = true; error.value = null
  try {
    const [tasks, sols] = await Promise.all([
      $api.value.get('/api/tasks/?page_size=100'),
      $api.value.get('/api/solutions/?page_size=100'),
    ])
    const allTasks = tr2arr(tasks)
    // Куратор видит только ту задачу, которая закреплена за ним
    myTask.value   = allTasks[0] ?? null
    solutions.value = tr2arr(sols)
    if (myTask.value) consultForm.value = myTask.value.consultation_url || ''
  } catch(e) { error.value = e.message }
  finally { loading.value = false }
}

// Ссылка на консультацию
async function saveConsult() {
  try {
    // Патч задачи — но куратор не может патчить Task напрямую, это делает ADMIN.
    // Однако consultation_url — часть TaskWriteSerializer и доступна ADMIN.
    // Обходим: куратор может обновить через TaskResourceLink.
    // По факту в текущем бэке consultation_url доступен только ADMIN,
    // поэтому просто покажем поле, но кнопку сделаем недоступной с подсказкой.
    flash('Ссылку на консультацию добавляет только администратор', 'error')
    showConsult.value = false
  } catch(e) { flash(e.message, 'error') }
}

// Resource links
async function addLink() {
  if (!linkForm.value.title || !linkForm.value.url || !myTask.value) return
  try {
    await $api.value.post('/api/task-resource-links/', {
      task: myTask.value.id,
      title: linkForm.value.title,
      url: linkForm.value.url,
    })
    linkForm.value = { title: '', url: '' }
    flash('Ссылка добавлена!')
    await load()
  } catch(e) { flash(e.message, 'error') }
}

async function deleteLink(id) {
  try {
    await $api.value.del(`/api/task-resource-links/${id}/`)
    flash('Ссылка удалена')
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

      <div v-if="!myTask" class="state-box">
        <p style="color:var(--text-muted)">Вам ещё не назначена задача</p>
      </div>

      <template v-else>
        <!-- Моя задача -->
        <section class="card">
          <h2 class="section-title">Моя задача</h2>
          <div class="info-grid">
            <div class="info-row"><span class="info-label">Название</span><span class="info-value">{{ myTask.title }}</span></div>
            <div class="info-row">
              <span class="info-label">Консультация</span>
              <span class="info-value">
                <a v-if="myTask.consultation_url" :href="myTask.consultation_url" target="_blank" class="link">
                  {{ myTask.consultation_url }}
                </a>
                <span v-else class="empty-hint" style="padding:0">Ссылка не указана (устанавливает администратор)</span>
              </span>
            </div>
          </div>
          <p class="task-desc mt-16">{{ myTask.description }}</p>
        </section>

        <!-- Ресурсные ссылки -->
        <section class="card">
          <h2 class="section-title">Ссылки для участников</h2>

          <div v-if="myTask.resource_links?.length" class="members-list">
            <div v-for="l in myTask.resource_links" :key="l.id" class="member-row">
              <div class="member-info">
                <span class="member-name">{{ l.title }}</span>
                <a :href="l.url" target="_blank" class="link member-meta">{{ l.url }}</a>
              </div>
              <button class="btn-icon danger" @click="deleteLink(l.id)">✕</button>
            </div>
          </div>
          <p v-else class="empty-hint">Ссылок пока нет</p>

          <div class="form-grid mt-16">
            <div class="field">
              <label>Название ссылки *</label>
              <input v-model="linkForm.title" placeholder="Документация" />
            </div>
            <div class="field">
              <label>URL *</label>
              <input v-model="linkForm.url" placeholder="https://..." />
            </div>
            <div class="field align-end">
              <button class="btn-secondary" @click="addLink" :disabled="!linkForm.title || !linkForm.url">
                + Добавить ссылку
              </button>
            </div>
          </div>
        </section>

        <!-- Решения по моей задаче -->
        <section class="card">
          <h2 class="section-title">Решения команд</h2>

          <div v-if="!solutions.length" class="empty-hint">Решений пока нет</div>

          <div v-else class="solutions-list">
            <div v-for="sol in solutions" :key="sol.id" class="solution-card inner">
              <div class="sol-header">
                <div>
                  <h3 class="sol-title">{{ sol.title }}</h3>
                  <div class="sol-meta">
                    <span class="meta-chip">👥 {{ sol.team?.name }}</span>
                    <span :class="['badge', sol.status === 'SUBMITTED' ? 'badge-green' : 'badge-gray']">
                      {{ sol.status === 'SUBMITTED' ? 'Отправлено' : 'Черновик' }}
                    </span>
                  </div>
                </div>
              </div>
              <p v-if="sol.description" class="sol-desc">{{ sol.description }}</p>
              <a v-if="sol.repo_url" :href="sol.repo_url" target="_blank" class="resource-link">
                🔗 Репозиторий
              </a>
            </div>
          </div>
        </section>
      </template>
    </template>
  </div>
</template>