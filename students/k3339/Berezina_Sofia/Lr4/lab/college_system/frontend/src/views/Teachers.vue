<template>
  <div class="teachers-view">
    <div class="header">
      <h1>Преподаватели</h1>
      <div class="header-actions">
        <button @click="openCreateModal" class="btn-add">
          <span>+</span> Добавить преподавателя
        </button>
      </div>
      <div class="stats">
        <span class="stat-item">Всего: {{ teachers.length }}</span>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка преподавателей...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadTeachers" class="retry-btn">Повторить</button>
    </div>

    <div v-else class="teachers-container">
      <!-- Фильтры -->
      <div class="filters">
        <div class="search-box">
          <input
              v-model="searchQuery"
              @input="filterTeachers"
              placeholder="Поиск по фамилии или имени..."
              class="search-input"
          >
        </div>

        <div class="filter-control">
          <label>Должность:</label>
          <select v-model="selectedPosition" @change="filterTeachers">
            <option value="">Все должности</option>
            <option v-for="position in positions" :key="position" :value="position">
              {{ getPositionDisplay(position) }}
            </option>
          </select>
        </div>
      </div>

      <!-- Таблица преподавателей -->
      <div class="teachers-table-container">
        <table class="teachers-table">
          <thead>
          <tr>
            <th @click="sortBy('surname')" class="sortable">
              ФИО
              <span v-if="sortField === 'surname'" class="sort-indicator">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
            </th>
            <th>Должность</th>
            <th>Кабинет</th>
            <th>Статус</th>
            <th>Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="teacher in sortedTeachers" :key="teacher.id">
            <td>
              <div class="teacher-name">
                <strong>{{ teacher.surname }} {{ teacher.name }} {{ teacher.middle_name }}</strong>
                <div class="teacher-id">ID: {{ teacher.id }}</div>
              </div>
            </td>
            <td>
                <span class="position-badge">
                  {{ teacher.position_display }}
                </span>
            </td>
            <td>
                <span v-if="teacher.classroom_display" class="classroom-info">
                  {{ teacher.classroom_display }}
                </span>
              <span v-else class="no-classroom">Не назначен</span>
            </td>
            <td>
              <span v-if="teacher.is_active" class="status-badge active">Активен</span>
              <span v-else class="status-badge non-active">Уволен</span>
            </td>

            <td>
              <div class="action-buttons">
                <button
                    @click="editTeacher(teacher)"
                    class="action-btn edit-btn"
                    title="Редактировать"
                >
                  ✏️
                </button>
                <button
                    @click="confirmDelete(teacher)"
                    class="action-btn delete-btn"
                    title="Удалить"
                >
                  🗑️
                </button>
              </div>
            </td>

          </tr>

          <tr v-if="!filteredTeachers.length">
            <td colspan="5" class="no-data">
              Преподаватели не найдены
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <!-- Статистика -->
      <div class="stats-summary">
        <div class="stat-card">
          <div class="stat-value">{{ teachers.length }}</div>
          <div class="stat-label">Всего преподавателей</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ professorCount }}</div>
          <div class="stat-label">Профессоров</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ associateProfessorCount }}</div>
          <div class="stat-label">Доцентов</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ withClassroomCount }}</div>
          <div class="stat-label">С кабинетом</div>
        </div>
      </div>
    </div>

    <!-- Модальное окно создания/редактирования преподавателя -->
    <div v-if="showTeacherModal" class="modal-overlay" @click="closeTeacherModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ isEditMode ? 'Редактировать преподавателя' : 'Добавить нового преподавателя' }}</h2>
          <button @click="closeTeacherModal" class="close-btn">×</button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="saveTeacher" class="teacher-form">
            <div class="form-row">
              <div class="form-group">
                <label for="surname">Фамилия *</label>
                <input
                    id="surname"
                    v-model="teacherForm.surname"
                    type="text"
                    required
                    placeholder="Введите фамилию"
                    :class="{ 'error-input': formErrors.surname }"
                >
                <span v-if="formErrors.surname" class="error-text">{{ formErrors.surname }}</span>
              </div>

              <div class="form-group">
                <label for="name">Имя *</label>
                <input
                    id="name"
                    v-model="teacherForm.name"
                    type="text"
                    required
                    placeholder="Введите имя"
                    :class="{ 'error-input': formErrors.name }"
                >
                <span v-if="formErrors.name" class="error-text">{{ formErrors.name }}</span>
              </div>

              <div class="form-group">
                <label for="middle_name">Отчество</label>
                <input
                    id="middle_name"
                    v-model="teacherForm.middle_name"
                    type="text"
                    placeholder="Введите отчество"
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="position">Должность *</label>
                <select
                    id="position"
                    v-model="teacherForm.position"
                    required
                    :class="{ 'error-input': formErrors.position }"
                >
                  <option value="">Выберите должность</option>
                  <option value="преподаватель">Преподаватель</option>
                  <option value="старший преподаватель">Старший преподаватель</option>
                  <option value="доцент">Доцент</option>
                  <option value="профессор">Профессор</option>
                  <option value="заведующий кафедрой">Заведующий кафедрой</option>
                </select>
                <span v-if="formErrors.position" class="error-text">{{ formErrors.position }}</span>
              </div>

              <div class="form-group">
                <label for="classroom">Кабинет</label>
                <input
                    id="classroom"
                    v-model="teacherForm.classroom"
                    type="text"
                    placeholder="Например: 101, 202А"
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="email">Email</label>
                <input
                    id="email"
                    v-model="teacherForm.email"
                    type="email"
                    placeholder="Введите email"
                    :class="{ 'error-input': formErrors.email }"
                >
                <span v-if="formErrors.email" class="error-text">{{ formErrors.email }}</span>
              </div>

              <div class="form-group">
                <label for="phone">Телефон</label>
                <input
                    id="phone"
                    v-model="teacherForm.phone"
                    type="tel"
                    placeholder="Введите телефон"
                >
              </div>
            </div>

            <div class="form-group" v-if="!isEditMode">
              <label for="create_account">
                <input
                    id="create_account"
                    v-model="teacherForm.create_account"
                    type="checkbox"
                >
                Создать учетную запись
              </label>
            </div>

            <div v-if="teacherForm.create_account && !isEditMode" class="account-fields">
              <div class="form-row">
                <div class="form-group">
                  <label for="username">Имя пользователя *</label>
                  <input
                      id="username"
                      v-model="teacherForm.username"
                      type="text"
                      required
                      placeholder="Введите имя пользователя"
                      :class="{ 'error-input': formErrors.username }"
                  >
                  <span v-if="formErrors.username" class="error-text">{{ formErrors.username }}</span>
                </div>

                <div class="form-group">
                  <label for="password">Пароль *</label>
                  <input
                      id="password"
                      v-model="teacherForm.password"
                      type="password"
                      required
                      placeholder="Введите пароль"
                      :class="{ 'error-input': formErrors.password }"
                  >
                  <span v-if="formErrors.password" class="error-text">{{ formErrors.password }}</span>
                </div>
              </div>
            </div>

            <div class="form-group" v-if="isEditMode">
              <label for="is_active">Статус</label>
              <select
                  id="is_active"
                  v-model="teacherForm.is_active"
              >
                <option :value="true">Активен</option>
                <option :value="false">Уволен</option>
              </select>
            </div>
          </form>
        </div>

        <div class="modal-footer">
          <button @click="closeTeacherModal" class="btn-secondary">Отмена</button>
          <button @click="saveTeacher" class="btn-primary" :disabled="saving">
            {{ saving ? 'Сохранение...' : (isEditMode ? 'Сохранить изменения' : 'Добавить преподавателя') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content delete-modal" @click.stop>
        <div class="modal-header">
          <h2>{{ getDeleteModalTitle() }}</h2>
          <button @click="closeDeleteModal" class="close-btn">×</button>
        </div>

        <div class="modal-body">
          <div class="delete-warning">
            <div class="warning-icon">⚠️</div>
            <p>
              {{ getDeleteMessage() }}
            </p>

            <p v-if="teacherToDelete?.is_active" class="warning-text">
              <strong>Внимание:</strong> Преподаватель активен. Это действие уволит преподавателя (изменит статус на
              "Уволен").
            </p>

            <p v-if="!teacherToDelete?.is_active" class="warning-text">
              <strong>Внимание:</strong> Преподаватель уже уволен.
              Это действие <strong>полностью удалит</strong> запись о преподавателе из базы данных.
            </p>

            <p>Это действие нельзя отменить.</p>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeDeleteModal" class="btn-secondary">Отмена</button>
          <button @click="deleteTeacher" class="btn-danger" :disabled="deleting">
            {{ getDeleteButtonText() }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, computed, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import api from '@/api'

export default {
  name: 'TeachersView',

  setup() {
    const router = useRouter()

    const teachers = ref([])
    const loading = ref(true)
    const error = ref('')
    const searchQuery = ref('')
    const selectedPosition = ref('')
    const sortField = ref('surname')
    const sortDirection = ref('asc')

    // Модальные окна
    const showTeacherModal = ref(false)
    const showDeleteModal = ref(false)
    const isEditMode = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    const teacherToDelete = ref(null)

    // Форма преподавателя
    const teacherForm = ref({
      surname: '',
      name: '',
      middle_name: '',
      position: '',
      classroom: '',
      email: '',
      phone: '',
      is_active: true,
      create_account: false,
      username: '',
      password: ''
    })

    const formErrors = ref({})

    // Инициализация формы
    const initTeacherForm = () => {
      teacherForm.value = {
        surname: '',
        name: '',
        middle_name: '',
        position: '',
        classroom: '',
        email: '',
        phone: '',
        is_active: true,
        create_account: false,
        username: '',
        password: ''
      }
      formErrors.value = {}
    }

    const loadTeachers = async () => {
      loading.value = true
      error.value = ''

      try {
        const response = await api.get('teachers/')
        teachers.value = response.data
      } catch (err) {
        console.error('Ошибка загрузки преподавателей:', err)
        error.value = 'Не удалось загрузить список преподавателей'
      } finally {
        loading.value = false
      }
    }

    // CRUD операции
    const openCreateModal = () => {
      isEditMode.value = false
      initTeacherForm()
      showTeacherModal.value = true
    }

    const editTeacher = (teacher) => {
      isEditMode.value = true

      // Заполняем форму данными преподавателя
      teacherForm.value = {
        id: teacher.id,
        surname: teacher.surname || '',
        name: teacher.name || '',
        middle_name: teacher.middle_name || '',
        position: teacher.position || '',
        classroom: teacher.classroom || '',
        email: teacher.email || '',
        phone: teacher.phone || '',
        is_active: teacher.is_active || true,
        create_account: false,
        username: '',
        password: ''
      }

      formErrors.value = {}
      showTeacherModal.value = true
    }

    const saveTeacher = async () => {
      saving.value = true
      formErrors.value = {}

      try {
        // Подготавливаем данные в формате, ожидаемом сервером
        const data = {
          surname: teacherForm.value.surname.trim(),
          name: teacherForm.value.name.trim(),
          position: teacherForm.value.position,
          is_active: teacherForm.value.is_active
        }

        // Добавляем отчество если есть
        if (teacherForm.value.middle_name?.trim()) {
          data.middle_name = teacherForm.value.middle_name.trim()
        }

        // Добавляем кабинет если есть (нужно передавать ID кабинета)
        if (teacherForm.value.classroom?.trim()) {
          // Здесь нужно получить ID кабинета по номеру
          // Или изменить логику на сервере
          // Пока оставляем как есть, сервер должен обработать
          // data.classroom = teacherForm.value.classroom.trim()
        }

        // Добавляем данные для создания учетной записи если нужно
        if (teacherForm.value.create_account && !isEditMode.value) {
          const userData = {
            username: teacherForm.value.username.trim(),
            password: teacherForm.value.password
          }

          // Добавляем email если указан
          if (teacherForm.value.email?.trim()) {
            userData.email = teacherForm.value.email.trim()
          }

          // Добавляем телефон если указан
          if (teacherForm.value.phone?.trim()) {
            userData.phone = teacherForm.value.phone.trim()
          }

          data.user_account = userData
        }

        let response
        if (isEditMode.value) {
          // Обновление существующего преподавателя
          response = await api.put(`teacher/update/${teacherForm.value.id}/`, data)
        } else {
          // Создание нового преподавателя
          response = await api.post('teacher/create/', data)
        }

        // Обновляем список преподавателей
        await loadTeachers()

        // Закрываем модальное окно
        closeTeacherModal()

        // Показываем сообщение об успехе
        alert(isEditMode.value ? 'Преподаватель успешно обновлен!' : 'Преподаватель успешно добавлен!')

      } catch (err) {
        console.error('Ошибка сохранения преподавателя:', err)

        if (err.response && err.response.data) {
          // Обрабатываем ошибки валидации
          const errors = err.response.data
          for (const key in errors) {
            formErrors.value[key] = Array.isArray(errors[key]) ? errors[key][0] : errors[key]
          }

          if (!Object.keys(formErrors.value).length) {
            alert(err.response.data.detail || 'Ошибка при сохранении преподавателя')
          }
        } else {
          alert('Ошибка при сохранении преподавателя')
        }
      } finally {
        saving.value = false
      }
    }

    const confirmDelete = (teacher) => {
      teacherToDelete.value = teacher
      showDeleteModal.value = true
    }

    // Получение заголовка модального окна удаления
    const getDeleteModalTitle = () => {
      if (!teacherToDelete.value) return 'Подтверждение удаления'

      if (!teacherToDelete.value.is_active) {
        return 'Подтверждение удаления из базы'
      }
      return 'Подтверждение увольнения'
    }

    // Получение текста сообщения
    const getDeleteMessage = () => {
      if (!teacherToDelete.value) return ''

      const isActive = teacherToDelete.value.is_active
      const name = `${teacherToDelete.value.surname} ${teacherToDelete.value.name}`

      if (!isActive) {
        return `Вы уверены, что хотите полностью удалить из базы данных уволенного преподавателя "${name}"?`
      } else {
        return `Вы уверены, что хотите уволить преподавателя "${name}"?`
      }
    }

    // Получение текста кнопки удаления
    const getDeleteButtonText = () => {
      if (deleting.value) return 'Удаление...'

      if (!teacherToDelete.value) return 'Удалить'

      if (!teacherToDelete.value.is_active) {
        return 'Удалить из базы'
      }
      return 'Уволить'
    }

    const deleteTeacher = async () => {
      if (!teacherToDelete.value) return

      deleting.value = true

      try {
        const teacher = teacherToDelete.value

        // Используем эндпоинт удаления
        await api.delete(`teacher/delete/${teacher.id}/`)

        // Обновляем список преподавателей
        await loadTeachers()

        // Закрываем модальное окно
        closeDeleteModal()

        // Показываем сообщение об успехе
        if (!teacher.is_active) {
          alert('Преподаватель полностью удален из базы данных!')
        } else {
          alert('Преподаватель успешно уволен!')
        }

      } catch (err) {
        console.error('Ошибка удаления преподавателя:', err)
        alert(err.response?.data?.detail || 'Ошибка при удалении преподавателя')
      } finally {
        deleting.value = false
      }
    }

    // Закрытие модальных окон
    const closeTeacherModal = () => {
      showTeacherModal.value = false
      initTeacherForm()
    }

    const closeDeleteModal = () => {
      showDeleteModal.value = false
      teacherToDelete.value = null
    }

    // Вычисляемые свойства
    const positions = computed(() => {
      const uniquePositions = [...new Set(teachers.value.map(t => t.position))]
      return uniquePositions.sort()
    })

    const filteredTeachers = computed(() => {
      let filtered = teachers.value

      // Фильтр по поиску
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(teacher =>
            teacher.surname.toLowerCase().includes(query) ||
            teacher.name.toLowerCase().includes(query) ||
            (teacher.middle_name && teacher.middle_name.toLowerCase().includes(query))
        )
      }

      // Фильтр по должности
      if (selectedPosition.value) {
        filtered = filtered.filter(teacher => teacher.position === selectedPosition.value)
      }

      return filtered
    })

    const sortedTeachers = computed(() => {
      const sorted = [...filteredTeachers.value]

      if (sortField.value === 'surname') {
        sorted.sort((a, b) => {
          const nameA = a.surname.toLowerCase()
          const nameB = b.surname.toLowerCase()
          return sortDirection.value === 'asc'
              ? nameA.localeCompare(nameB)
              : nameB.localeCompare(nameA)
        })
      }

      return sorted
    })

    const professorCount = computed(() => {
      return teachers.value.filter(t => t.position === 'профессор').length
    })

    const associateProfessorCount = computed(() => {
      return teachers.value.filter(t => t.position === 'доцент').length
    })

    const withClassroomCount = computed(() => {
      return teachers.value.filter(t => t.classroom).length
    })

    // Методы
    const getPositionDisplay = (position) => {
      const positionsMap = {
        'преподаватель': 'Преподаватель',
        'старший преподаватель': 'Старший преподаватель',
        'доцент': 'Доцент',
        'профессор': 'Профессор',
        'заведующий кафедрой': 'Заведующий кафедрой'
      }
      return positionsMap[position] || position
    }

    const sortBy = (field) => {
      if (sortField.value === field) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortField.value = field
        sortDirection.value = 'asc'
      }
    }

    const filterTeachers = () => {
      // Фильтрация происходит автоматически через computed
    }

    onMounted(() => {
      loadTeachers()
    })

    return {
      teachers,
      loading,
      error,
      searchQuery,
      selectedPosition,
      sortField,
      sortDirection,
      positions,
      filteredTeachers,
      sortedTeachers,
      professorCount,
      associateProfessorCount,
      withClassroomCount,

      // Модальные окна и формы
      showTeacherModal,
      showDeleteModal,
      isEditMode,
      teacherForm,
      formErrors,
      saving,
      deleting,
      teacherToDelete,

      loadTeachers,
      getPositionDisplay,
      sortBy,
      filterTeachers,

      // CRUD методы
      openCreateModal,
      editTeacher,
      saveTeacher,
      confirmDelete,
      deleteTeacher,
      closeTeacherModal,
      closeDeleteModal,
      getDeleteModalTitle,
      getDeleteMessage,
      getDeleteButtonText
    }
  }
}
</script>

<style scoped>
.teachers-view {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
}

.header h1 {
  color: #2c3e50;
  border-bottom: 3px solid #667eea;
  padding-bottom: 0.5rem;
}

.stats {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.stat-item {
  background: #f8f9fa;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Фильтры */
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.search-box {
  flex: 1;
  position: relative;
  min-width: 300px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.2s;
  height: 100%;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}


.filter-control {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 200px;
}

.filter-control label {
  font-weight: bold;
  font-size: 0.9rem;
  color: #2c3e50;
}

.filter-control select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.filter-control select:focus {
  outline: none;
  border-color: #667eea;
}

/* Таблица преподавателей */
.teachers-table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 2rem;
}

.teachers-table {
  width: 100%;
  border-collapse: collapse;
}

.teachers-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e2e8f0;
}

.teachers-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.teachers-table th.sortable:hover {
  background: #e9ecef;
}

.sort-indicator {
  margin-left: 0.5rem;
  font-size: 0.8em;
  color: #667eea;
}

.teachers-table td {
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.teachers-table tr:hover {
  background: #f8f9fa;
}

/* Элементы таблицы */
.teacher-name strong {
  display: block;
  color: #2c3e50;
  margin-bottom: 0.25rem;
  font-size: 1.05rem;
}

.teacher-id {
  font-size: 0.85rem;
  color: #666;
}

.position-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
  background: #e3f2fd;
  color: #1976d2;
}

.classroom-info {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f0fff4;
  color: #38a169;
  border-radius: 15px;
  font-size: 0.9rem;
}

.no-classroom {
  color: #a0aec0;
  font-style: italic;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.non-active {
  background: #f8d7da;
  color: #721c24;
}

/* Кнопки действий */
.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
  background: transparent;
  min-width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}


.no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
  background: #f8f9fa;
}

/* Статистика */
.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

/* Состояния */
.loading, .error {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error {
  color: #e53e3e;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.retry-btn:hover {
  background: #c53030;
}

/* Адаптивность */
@media (max-width: 768px) {
  .teachers-view {
    padding: 1rem;
  }

  .filters {
    flex-direction: column;
  }

  .search-box,
  .filter-control {
    min-width: 100%;
  }

  .teachers-table {
    display: block;
    overflow-x: auto;
  }

  .action-buttons {
    flex-wrap: wrap;
  }

  .stats-summary {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-summary {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-value {
    font-size: 2rem;
  }

  .teachers-table th,
  .teachers-table td {
    padding: 0.75rem 0.5rem;
    font-size: 0.9rem;
  }
}

/* Стили для разных должностей */
.position-badge {
  background: #e3f2fd;
  color: #1976d2;
}

.position-badge[data-position="профессор"] {
  background: #ffebee;
  color: #c62828;
}

.position-badge[data-position="доцент"] {
  background: #f3e5f5;
  color: #7b1fa2;
}

.position-badge[data-position="старший преподаватель"] {
  background: #e8f5e8;
  color: #2e7d32;
}

.position-badge[data-position="заведующий кафедрой"] {
  background: #e3f2fd;
  color: #1565c0;
}

/* Анимации */
.teachers-table tr {
  transition: background-color 0.2s, transform 0.2s;
}

.teachers-table tr:hover {
  transform: translateX(2px);
}

/* Стили для кнопки редактирования */
.edit-btn:hover {
  background: #e3f2fd;
  color: #2196f3;
}

/* Стили для формы */
.teacher-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #333;
  font-size: 0.95rem;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.error-input {
  border-color: #e74c3c !important;
}

.error-text {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.account-fields {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

/* Стили для чекбокса */
.form-group label[for="create_account"] {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.form-group input[type="checkbox"] {
  width: auto;
}

/* Модальное окно */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 10px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
}

.btn-danger {
  padding: 0.75rem 1.5rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.3s;
}

.btn-danger:hover {
  background: #c0392b;
}

.btn-danger:disabled {
  background: #eaa29b;
  cursor: not-allowed;
}

/* Стили для модалки удаления */
.delete-modal {
  max-width: 500px;
}

.delete-warning {
  text-align: center;
  padding: 1rem;
}

.warning-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.warning-text {
  color: #e74c3c;
  font-size: 0.9rem;
  margin: 0.5rem 0;
  padding: 0.75rem;
  background: #fff5f5;
  border-radius: 8px;
  border-left: 4px solid #e74c3c;
}

.warning-text strong {
  color: #c0392b;
}

/* Кнопка добавления в хедере */
.btn-add {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  margin-top: 2rem;
}

.btn-add span {
  font-size: 1.2rem;
}

.btn-add:hover {
  background: #5a67d8;
}

.header-actions {
  margin-bottom: 1rem;
}

/* Адаптивность формы */
@media (max-width: 768px) {
  .teacher-form {
    gap: 1rem;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .form-group input,
  .form-group select {
    padding: 0.5rem;
  }

  .modal-content {
    margin: 1rem;
    width: calc(100% - 2rem);
  }

  .delete-modal {
    max-width: 100%;
  }
}
</style>