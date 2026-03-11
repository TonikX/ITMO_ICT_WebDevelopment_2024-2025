<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { api } from '../api'

const auth = useAuthStore()
const $api = computed(() => api(auth.token))

const solutions   = ref([])
const evaluations = ref([])
const loading     = ref(true)
const error       = ref(null)
const msg         = ref('')
const msgType     = ref('success')

// форма оценки
const evalForms = ref({}) // { solution_id: { score, comment, open } }

function flash(text, type = 'success') {
  msg.value = text; msgType.value = type
  setTimeout(() => (msg.value = ''), 3000)
}

function tr2arr(d) { return Array.isArray(d) ? d : (d?.results ?? []) }

async function load() {
  loading.value = true; error.value = null
  try {
    const [sol, ev] = await Promise.all([
      $api.value.get('/api/solutions/?page_size=100'),
      $api.value.get('/api/evaluations/?page_size=100'),
    ])
    solutions.value   = tr2arr(sol)
    evaluations.value = tr2arr(ev)
  } catch(e) { error.value = e.message }
  finally { loading.value = false }
}

function myEval(solutionId) {
  return evaluations.value.find(
    e => e.solution === solutionId && e.jury_member?.id === auth.user?.id
  ) ?? null
}

function openEval(solutionId) {
  const existing = myEval(solutionId)
  evalForms.value[solutionId] = {
    score: existing?.score ?? 5,
    comment: existing?.comment ?? '',
    open: true,
  }
}

function closeEval(solutionId) {
  if (evalForms.value[solutionId]) evalForms.value[solutionId].open = false
}

async function saveEval(solution) {
  const f = evalForms.value[solution.id]
  const existing = myEval(solution.id)
  try {
    if (existing) {
      await $api.value.patch(`/api/evaluations/${existing.id}/`, {
        score: f.score, comment: f.comment
      })
      flash('Оценка обновлена!')
    } else {
      await $api.value.post('/api/evaluations/', {
        solution: solution.id,
        score: f.score,
        comment: f.comment,
      })
      flash('Оценка добавлена!')
    }
    closeEval(solution.id)
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

      <div v-if="!solutions.length" class="state-box">
        <p style="color:var(--text-muted)">Решений пока нет</p>
      </div>

      <div class="solutions-list">
        <div v-for="sol in solutions" :key="sol.id" class="card solution-card">
          <div class="sol-header">
            <div>
              <h3 class="sol-title">{{ sol.title }}</h3>
              <div class="sol-meta">
                <span class="meta-chip">🏷 {{ sol.task?.title }}</span>
                <span class="meta-chip">👥 {{ sol.team?.name }}</span>
                <span :class="['badge', sol.status === 'SUBMITTED' ? 'badge-green' : 'badge-gray']">
                  {{ sol.status === 'SUBMITTED' ? 'Отправлено' : 'Черновик' }}
                </span>
              </div>
            </div>
            <div class="eval-summary">
              <template v-if="myEval(sol.id)">
                <span class="score-badge">{{ myEval(sol.id).score }}/10</span>
                <button class="btn-edit" @click="openEval(sol.id)">Изменить</button>
              </template>
              <button v-else class="btn-edit" @click="openEval(sol.id)">+ Оценить</button>
            </div>
          </div>

          <p v-if="sol.description" class="sol-desc">{{ sol.description }}</p>
          <a v-if="sol.repo_url" :href="sol.repo_url" target="_blank" class="resource-link">
            🔗 Репозиторий
          </a>

          <!-- Форма оценки -->
          <div v-if="evalForms[sol.id]?.open" class="eval-form">
            <div class="score-row">
              <label>Оценка (0–10)</label>
              <div class="score-buttons">
                <button
                  v-for="n in 11" :key="n-1"
                  :class="['score-btn', evalForms[sol.id].score === n-1 ? 'active' : '']"
                  @click="evalForms[sol.id].score = n-1"
                >{{ n-1 }}</button>
              </div>
            </div>
            <div class="field">
              <label>Комментарий</label>
              <textarea v-model="evalForms[sol.id].comment" rows="3" placeholder="Комментарий к оценке..."></textarea>
            </div>
            <div class="form-actions">
              <button class="btn-primary" @click="saveEval(sol)">Сохранить оценку</button>
              <button class="btn-secondary" @click="closeEval(sol.id)">Отмена</button>
            </div>
          </div>

          <!-- Все оценки по этому решению -->
          <div v-if="evaluations.filter(e => e.solution === sol.id).length" class="all-evals">
            <div class="resources-label">Оценки жюри</div>
            <div v-for="e in evaluations.filter(ev => ev.solution === sol.id)" :key="e.id" class="eval-row">
              <span class="eval-who">{{ e.jury_member?.username }}</span>
              <span class="score-badge sm">{{ e.score }}/10</span>
              <span v-if="e.comment" class="eval-comment">{{ e.comment }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>