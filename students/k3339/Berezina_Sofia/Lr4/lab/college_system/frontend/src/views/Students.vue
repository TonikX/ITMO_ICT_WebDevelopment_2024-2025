<template>
  <div class="students-view">
    <h1>Студенты</h1>

    <div class="header-actions">
        <button @click="openCreateModal" class="btn-add">
          <span>+</span> Добавить студента
        </button>
    </div>

    <div class="controls">
      <div class="search-control">
        <input
            v-model="searchQuery"
            @input="searchStudents"
            placeholder="Поиск по имени, фамилии..."
            class="search-input"
        >
        <button @click="clearSearch" class="clear-btn">×</button>
      </div>

      <div class="filter-control">
        <label>Группа:</label>
        <select v-model="selectedGroup" @change="loadStudentsByGroup">
          <option value="">Все группы</option>
          <option v-for="group in groups" :key="group.id" :value="group.id">
            {{ group.name }}
          </option>
        </select>
      </div>

      <div class="filter-control">
        <label>Статус:</label>
        <select v-model="selectedStatus" @change="loadStudents">
          <option value="">Все статусы</option>
          <option value="active">Обучается</option>
          <option value="dropped">Отчислен</option>
          <option value="academic_leave">Академический отпуск</option>
          <option value="graduated">Выпустился</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Загрузка данных...</p>
    </div>

    <div v-else-if="error" class="error">
      <p>Ошибка: {{ error }}</p>
      <button @click="loadStudents" class="retry-btn">Повторить</button>
    </div>

    <div v-else class="students-content">
      <div class="stats-summary">
        <div class="stat-item">
          <span class="stat-label">Всего студентов:</span>
          <span class="stat-value">{{ totalStudents }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Обучаются:</span>
          <span class="stat-value active">{{ activeStudentsCount }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Отчислены:</span>
          <span class="stat-value dropped">{{ droppedStudentsCount }}</span>
        </div>
      </div>

      <div class="students-table-container">
        <table class="students-table">
          <thead>
          <tr>
            <th @click="sortBy('surname')" class="sortable">
              ФИО
              <span v-if="sortField === 'surname'" class="sort-indicator">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
            </th>
            <th>Группа</th>
            <th>Дата поступления</th>
            <th>Статус</th>
            <th>Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="student in sortedStudents" :key="student.id" :class="`status-${student.status}`">
            <td>
              <div class="student-name">
                <strong>{{ student.full_name }}</strong>
              </div>
            </td>
            <td>
                <span class="group-badge">
                  {{ student.group_name }}
                </span>
            </td>
            <td>
              {{ formatDate(student.enrollment_date) }}
            </td>
            <td>
                <span :class="`status-badge status-${student.status}`">
                  {{ student.status_display }}
                </span>
            </td>
            <td>
              <div class="action-buttons">
                <button
                    @click="viewStudentDetails(student)"
                    class="action-btn view-btn"
                    title="Просмотр"
                >
                  👁️
                </button>
                <button
                    @click="viewStudentGrades(student)"
                    class="action-btn grades-btn"
                    title="Оценки"
                    v-if="student.status === 'active'"
                >
                  📊
                </button>
                <button
                    @click="viewStudentStats(student)"
                    class="action-btn stats-btn"
                    title="Статистика"
                    v-if="student.status === 'active'"
                >
                  📈
                </button>
                <button
                    @click="editStudent(student)"
                    class="action-btn edit-btn"
                    title="Редактировать"
                >
                  ✏️
                </button>
                <button
                    @click="confirmDelete(student)"
                    class="action-btn delete-btn"
                    title="Удалить"
                >
                  🗑️
                </button>
              </div>
            </td>
          </tr>

          <tr v-if="!students.length">
            <td colspan="5" class="no-data">
              Студенты не найдены
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <div v-if="students.length" class="pagination">
        <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="page-btn"
        >
          ← Назад
        </button>

        <span class="page-info">
          Страница {{ currentPage }} из {{ totalPages }}
        </span>

        <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="page-btn"
        >
          Вперёд →
        </button>
      </div>

      <!-- Модальное окно деталей студента -->
      <div v-if="selectedStudent" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>Детальная информация</h2>
            <button @click="closeModal" class="close-btn">×</button>
          </div>

          <div class="modal-body">
            <div class="student-detail-card">
              <div class="detail-row">
                <strong>ФИО:</strong>
                <span>{{ selectedStudent.full_name }}</span>
              </div>
              <div class="detail-row">
                <strong>Группа:</strong>
                <span>{{ selectedStudent.group_name }}</span>
              </div>
              <div class="detail-row">
                <strong>Дата поступления:</strong>
                <span>{{ formatDate(selectedStudent.enrollment_date) }}</span>
              </div>
              <div class="detail-row">
                <strong>Статус:</strong>
                <span :class="`status-badge status-${selectedStudent.status}`">
                  {{ selectedStudent.status_display }}
                </span>
              </div>
              <div v-if="selectedUserAccount" class="detail-row">
                <strong>Учетная запись:</strong>
                <span>{{ selectedUserAccount.username }}</span>
              </div>

              <div v-if="studentStats" class="stats-section">
                <h3>Статистика успеваемости</h3>
                <div class="stats-grid">
                  <div class="stat-card">
                    <div class="stat-value">{{ studentStats.average_grade || 'Н/Д' }}</div>
                    <div class="stat-label">Средний балл</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-value">{{ studentStats.total_grades || 0 }}</div>
                    <div class="stat-label">Всего оценок</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="closeModal" class="btn-secondary">Закрыть</button>
            <button
                @click="editStudent(selectedStudent)"
                class="btn-edit"
            >
              Редактировать
            </button>
            <button
                @click="viewStudentGrades(selectedStudent)"
                class="btn-primary"
                v-if="selectedStudent.status === 'active'"
            >
              Посмотреть оценки
            </button>
          </div>
        </div>
      </div>

      <!-- Модальное окно создания/редактирования студента -->
      <div v-if="showStudentModal" class="modal-overlay" @click="closeStudentModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ isEditMode ? 'Редактировать студента' : 'Добавить нового студента' }}</h2>
            <button @click="closeStudentModal" class="close-btn">×</button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="saveStudent" class="student-form">
              <div class="form-group">
                <label for="surname">Фамилия *</label>
                <input
                    id="surname"
                    v-model="studentForm.surname"
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
                    v-model="studentForm.name"
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
                    v-model="studentForm.middle_name"
                    type="text"
                    placeholder="Введите отчество"
                >
              </div>

              <div class="form-group">
                <label for="group">Группа *</label>
                <select
                    id="group"
                    v-model="studentForm.group"
                    required
                    :class="{ 'error-input': formErrors.group }"
                >
                  <option value="">Выберите группу</option>
                  <option v-for="group in groups" :key="group.id" :value="group.id">
                    {{ group.name }}
                  </option>
                </select>
                <span v-if="formErrors.group" class="error-text">{{ formErrors.group }}</span>
              </div>

              <div class="form-group">
                <label for="enrollment_date">Дата поступления *</label>
                <input
                    id="enrollment_date"
                    v-model="studentForm.enrollment_date"
                    type="date"
                    required
                    :class="{ 'error-input': formErrors.enrollment_date }"
                >
                <span v-if="formErrors.enrollment_date" class="error-text">{{ formErrors.enrollment_date }}</span>
              </div>

              <div class="form-group" v-if="isEditMode">
                <label for="status">Статус</label>
                <select
                    id="status"
                    v-model="studentForm.status"
                >
                  <option value="active">Обучается</option>
                  <option value="dropped">Отчислен</option>
                  <option value="academic_leave">Академический отпуск</option>
                  <option value="graduated">Выпустился</option>
                </select>
              </div>

              <div class="form-group">
                <label for="email">Email</label>
                <input
                    id="email"
                    v-model="studentForm.email"
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
                    v-model="studentForm.phone"
                    type="tel"
                    placeholder="Введите телефон"
                >
              </div>

              <div class="form-group" v-if="!isEditMode">
                <label for="create_account">
                  <input
                      id="create_account"
                      v-model="studentForm.create_account"
                      type="checkbox"
                  >
                  Создать учетную запись
                </label>
              </div>

              <div v-if="studentForm.create_account" class="account-fields">
                <div class="form-group">
                  <label for="username">Имя пользователя *</label>
                  <input
                      id="username"
                      v-model="studentForm.username"
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
                      v-model="studentForm.password"
                      type="password"
                      required
                      placeholder="Введите пароль"
                      :class="{ 'error-input': formErrors.password }"
                  >
                  <span v-if="formErrors.password" class="error-text">{{ formErrors.password }}</span>
                </div>
              </div>
            </form>
          </div>

          <div class="modal-footer">
            <button @click="closeStudentModal" class="btn-secondary">Отмена</button>
            <button @click="saveStudent" class="btn-primary" :disabled="saving">
              {{ saving ? 'Сохранение...' : (isEditMode ? 'Сохранить изменения' : 'Добавить студента') }}
            </button>
          </div>
        </div>
      </div>

      <!-- Модальное окно подтверждения удаления -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
        <div class="modal-content delete-modal" @click.stop>
          <div class="modal-header">
            <h2>Подтверждение удаления</h2>
            <button @click="closeDeleteModal" class="close-btn">×</button>
          </div>

          <div class="modal-body">
            <div class="delete-warning">
              <div class="warning-icon">⚠️</div>
              <p>
                Вы уверены, что хотите удалить студента
                <strong>{{ studentToDelete?.full_name }}</strong>?
              </p>
              <p v-if="studentToDelete?.status === 'active'" class="warning-text">
                <strong>Внимание:</strong> Студент находится в статусе "Обучается".
                Удаление приведет к отчислению студента.
              </p>
              <p>Это действие нельзя отменить.</p>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="closeDeleteModal" class="btn-secondary">Отмена</button>
            <button @click="deleteStudent" class="btn-danger" :disabled="deleting">
              {{ deleting ? 'Удаление...' : 'Удалить' }}
            </button>
          </div>
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
  name: 'StudentsView',

  setup() {
    const router = useRouter()

    // Реактивные данные
    const students = ref([])
    const groups = ref([])
    const loading = ref(false)
    const error = ref('')
    const searchQuery = ref('')
    const selectedGroup = ref('')
    const selectedStatus = ref('active')
    const selectedStudent = ref(null)
    const studentStats = ref(null)
    const sortField = ref('surname')
    const sortDirection = ref('asc')
    const currentPage = ref(1)
    const itemsPerPage = 20

    // Модальные окна
    const showStudentModal = ref(false)
    const showDeleteModal = ref(false)
    const isEditMode = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    const studentToDelete = ref(null)

    // Форма студента
    const studentForm = ref({
      surname: '',
      name: '',
      middle_name: '',
      group: '',
      enrollment_date: new Date().toISOString().split('T')[0], // Сегодняшняя дата
      status: 'active',
      email: '',
      phone: '',
      create_account: false,
      username: '',
      password: ''
    })

    const formErrors = ref({})

    // Инициализация формы
    const initStudentForm = () => {
      studentForm.value = {
        surname: '',
        name: '',
        middle_name: '',
        group: '',
        enrollment_date: new Date().toISOString().split('T')[0],
        status: 'active',
        email: '',
        phone: '',
        create_account: false,
        username: '',
        password: ''
      }
      formErrors.value = {}
    }

    // Загрузка данных
    const loadStudents = async () => {
      loading.value = true
      error.value = ''

      try {
        // Если выбрана группа, используем endpoint группы
        if (selectedGroup.value) {
          await loadStudentsByGroup()
          return
        }

        let url = 'students/search/'
        const params = []

        // Только поиск по имени
        if (searchQuery.value) {
          params.push(`search=${searchQuery.value}`)
        }

        if (params.length) {
          url += `?${params.join('&')}`
        }

        const response = await api.get(url)
        let allStudents = response.data

        // Фильтрация по статусу на фронтенде
        if (selectedStatus.value) {
          allStudents = allStudents.filter(
              student => student.status === selectedStatus.value
          )
        }

        students.value = allStudents
      } catch (err) {
        console.error('Ошибка загрузки студентов:', err)
        error.value = err.message || 'Не удалось загрузить данные'
      } finally {
        loading.value = false
      }
    }

    const loadGroups = async () => {
      try {
        const response = await api.get('groups/')
        groups.value = response.data
      } catch (err) {
        console.error('Ошибка загрузки групп:', err)
      }
    }

    const loadStudentsByGroup = async () => {
      if (selectedGroup.value) {
        try {
          const response = await api.get(`groups/${selectedGroup.value}/students/`)
          let groupStudents = response.data

          // Фильтрация по статусу
          if (selectedStatus.value) {
            groupStudents = groupStudents.filter(
                student => student.status === selectedStatus.value
            )
          }

          // Фильтрация по поиску
          if (searchQuery.value) {
            const query = searchQuery.value.toLowerCase()
            groupStudents = groupStudents.filter(student =>
                student.full_name.toLowerCase().includes(query) ||
                (student.surname && student.surname.toLowerCase().includes(query)) ||
                (student.name && student.name.toLowerCase().includes(query)) ||
                (student.middle_name && student.middle_name.toLowerCase().includes(query))
            )
          }

          students.value = groupStudents

        } catch (err) {
          console.error('Ошибка загрузки студентов группы:', err)
          error.value = 'Не удалось загрузить студентов группы'
        }
      } else {
        // Если группа не выбрана, загружаем всех студентов с учетом фильтров
        loadStudents()
      }
    }

    const loadStudentStats = async (studentId) => {
      try {
        const response = await api.get(`students/${studentId}/stats/`)
        studentStats.value = response.data
      } catch (err) {
        console.error('Ошибка загрузки статистики:', err)
        studentStats.value = null
      }
    }

    // CRUD операции
    const openCreateModal = () => {
      isEditMode.value = false
      initStudentForm()
      showStudentModal.value = true
    }

    const editStudent = (student) => {
      isEditMode.value = true

      // Заполняем форму данными студента
      studentForm.value = {
        id: student.id,
        surname: student.surname || '',
        name: student.name || '',
        middle_name: student.middle_name || '',
        group: student.group || '',
        enrollment_date: student.enrollment_date ? student.enrollment_date.split('T')[0] : '',
        status: student.status || 'active',
        email: student.email || '',
        phone: student.phone || '',
        create_account: false,
        username: '',
        password: ''
      }

      formErrors.value = {}
      showStudentModal.value = true
      closeModal() // Закрываем модалку деталей если открыта
    }

    const saveStudent = async () => {
      saving.value = true
      formErrors.value = {}

      try {
        const data = {
          surname: studentForm.value.surname,
          name: studentForm.value.name,
          middle_name: studentForm.value.middle_name,
          group: studentForm.value.group,
          enrollment_date: studentForm.value.enrollment_date,
          status: studentForm.value.status,
          email: studentForm.value.email || null,
          phone: studentForm.value.phone || null
        }

        // Добавляем данные для создания учетной записи если нужно
        if (studentForm.value.create_account && !isEditMode.value) {
          data.user_account = {
            username: studentForm.value.username,
            password: studentForm.value.password,
            email: studentForm.value.email
          }
        }

        if (isEditMode.value) {
          // Обновление существующего студента
          await api.put(`student/update/${studentForm.value.id}/`, data)
        } else {
          // Создание нового студента
          await api.post('student/create/', data)
        }

        // Обновляем список студентов
        await loadStudents()

        // Закрываем модальное окно
        closeStudentModal()

        // Показываем сообщение об успехе
        alert(isEditMode.value ? 'Студент успешно обновлен!' : 'Студент успешно добавлен!')

      } catch (err) {
        console.error('Ошибка сохранения студента:', err)

        if (err.response && err.response.data) {
          // Обрабатываем ошибки валидации
          const errors = err.response.data
          for (const key in errors) {
            formErrors.value[key] = Array.isArray(errors[key]) ? errors[key][0] : errors[key]
          }

          if (!Object.keys(formErrors.value).length) {
            alert(err.response.data.detail || 'Ошибка при сохранении студента')
          }
        } else {
          alert('Ошибка при сохранении студента')
        }
      } finally {
        saving.value = false
      }
    }

    const confirmDelete = (student) => {
      studentToDelete.value = student
      showDeleteModal.value = true
    }

    const deleteStudent = async () => {
      if (!studentToDelete.value) return

      deleting.value = true

      try {
        await api.delete(`student/delete/${studentToDelete.value.id}/`)

        // Обновляем список студентов
        await loadStudents()

        // Закрываем модальное окно
        closeDeleteModal()

        // Показываем сообщение об успехе
        alert('Студент успешно удален!')

      } catch (err) {
        console.error('Ошибка удаления студента:', err)
        alert(err.response?.data?.detail || 'Ошибка при удалении студента')
      } finally {
        deleting.value = false
      }
    }

    // Закрытие модальных окон
    const closeStudentModal = () => {
      showStudentModal.value = false
      initStudentForm()
    }

    const closeDeleteModal = () => {
      showDeleteModal.value = false
      studentToDelete.value = null
    }

    // Поиск с задержкой
    let searchTimeout = null
    const searchStudents = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        currentPage.value = 1
        // Если выбрана группа, фильтруем на фронтенде
        if (selectedGroup.value) {
          loadStudentsByGroup()
        } else {
          loadStudents()
        }
      }, 500)
    }

    const clearSearch = () => {
      searchQuery.value = ''
      selectedGroup.value = ''
      selectedStatus.value = 'active'
      loadStudents()
    }

    // Сортировка
    const sortBy = (field) => {
      if (sortField.value === field) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortField.value = field
        sortDirection.value = 'asc'
      }
    }

    const sortedStudents = computed(() => {
      const sorted = [...students.value]

      if (sortField.value === 'surname') {
        sorted.sort((a, b) => {
          const nameA = a.full_name.toLowerCase()
          const nameB = b.full_name.toLowerCase()
          return sortDirection.value === 'asc'
              ? nameA.localeCompare(nameB)
              : nameB.localeCompare(nameA)
        })
      } else if (sortField.value === 'enrollment_date') {
        sorted.sort((a, b) => {
          const dateA = new Date(a.enrollment_date)
          const dateB = new Date(b.enrollment_date)
          return sortDirection.value === 'asc'
              ? dateA - dateB
              : dateB - dateA
        })
      }

      return sorted
    })

    // Пагинация
    const totalPages = computed(() => {
      return Math.ceil(sortedStudents.value.length / itemsPerPage)
    })

    const paginatedStudents = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return sortedStudents.value.slice(start, end)
    })

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
      }
    }

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
      }
    }

    // Статистика
    const totalStudents = computed(() => students.value.length)

    const activeStudentsCount = computed(() => {
      return students.value.filter(s => s.status === 'active').length
    })

    const droppedStudentsCount = computed(() => {
      return students.value.filter(s => s.status === 'dropped').length
    })

    // Работа с данными
    const formatDate = (dateString) => {
      if (!dateString) return 'Н/Д'
      return new Date(dateString).toLocaleDateString('ru-RU')
    }

    const viewStudentDetails = async (student) => {
      selectedStudent.value = student
      await loadStudentStats(student.id)
    }

    const viewStudentGrades = (student) => {
      router.push(`/students/${student.id}/grades`)
    }

    const viewStudentStats = (student) => {
      router.push(`/students/${student.id}/stats`)
    }

    const closeModal = () => {
      selectedStudent.value = null
      studentStats.value = null
    }

    const selectedUserAccount = computed(() => {
      return selectedStudent.value?.user_account || null
    })

    // Инициализация
    onMounted(() => {
      loadStudents()
      loadGroups()
    })

    return {
      // Данные
      students: paginatedStudents,
      groups,
      loading,
      error,
      searchQuery,
      selectedGroup,
      selectedStatus,
      selectedStudent,
      studentStats,
      sortField,
      sortDirection,
      currentPage,

      // Модальные окна и формы
      showStudentModal,
      showDeleteModal,
      isEditMode,
      studentForm,
      formErrors,
      saving,
      deleting,
      studentToDelete,

      // Вычисляемые свойства
      totalStudents,
      activeStudentsCount,
      droppedStudentsCount,
      sortedStudents: paginatedStudents,
      totalPages,
      selectedUserAccount,

      // Методы
      loadStudents,
      loadStudentsByGroup,
      searchStudents,
      clearSearch,
      sortBy,
      nextPage,
      prevPage,
      formatDate,
      viewStudentDetails,
      viewStudentGrades,
      viewStudentStats,
      closeModal,

      // CRUD методы
      openCreateModal,
      editStudent,
      saveStudent,
      confirmDelete,
      deleteStudent,
      closeStudentModal,
      closeDeleteModal
    }
  }
}
</script>

<style scoped>
.students-view {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
  border-bottom: 3px solid #667eea;
  padding-bottom: 0.5rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

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
}

.btn-add span {
  font-size: 1.2rem;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.search-control {
  display: flex;
  flex: 1;
  min-width: 300px;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 15px 0 0 15px;
  font-size: 1rem;
}

.clear-btn {
  padding: 0 1rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 0 15px 15px 0;
  cursor: pointer;
  font-size: 1.2rem;
}

.filter-control {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 150px;
}

.filter-control label {
  font-weight: bold;
  font-size: 0.9rem;
  color: #666;
}

.filter-control select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 15px;
  font-size: 1rem;
  background: white;
}

/* Статистика */
.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-item {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.stat-label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
}

.stat-value.active {
  color: #27ae60;
}

.stat-value.dropped {
  color: #e74c3c;
}

/* Таблица */
.students-table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 2rem;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

.students-table th {
  background: #667eea;
  color: white;
  padding: 1rem;
  text-align: center;
  font-weight: 600;
}

.students-table th.sortable {
  cursor: pointer;
  user-select: none;
}

.students-table th.sortable:hover {
  background: #5a67d8;
}

.sort-indicator {
  margin-left: 0.5rem;
  font-size: 0.8em;
}

.students-table td {
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.students-table tr:hover {
  background: #f8f9fa;
}

.students-table tr.status-dropped {
  background: #fff5f5;
}

.students-table tr.status-academic_leave {
  background: #fff9e6;
}

.students-table tr.status-graduated {
  background: #f0fff4;
}

/* Элементы таблицы */
.student-name strong {
  display: block;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.student-details {
  font-size: 0.85rem;
  color: #666;
}

.group-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-dropped {
  background: #f8d7da;
  color: #721c24;
}

.status-academic_leave {
  background: #fff3cd;
  color: #856404;
}

.status-graduated {
  background: #d1ecf1;
  color: #0c5460;
}

/* Кнопки действий */
.action-buttons {
  display: flex;
  justify-content: space-between;
}

.action-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
  background: transparent;
}

.view-btn:hover {
  background: #e3f2fd;
  color: #1976d2;
}

.grades-btn:hover {
  background: #f3e5f5;
  color: #7b1fa2;
}

.stats-btn:hover {
  background: #e8f5e8;
  color: #388e3c;
}

.schedule-btn:hover {
  background: #fff3e0;
  color: #f57c00;
}

/* Пагинация */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
}

.page-btn {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
}

.page-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-weight: 500;
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
  max-width: 600px;
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

.student-detail-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.detail-row:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.stats-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid #667eea;
}

.stats-section h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.stat-card .stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-card .stat-label {
  font-size: 0.85rem;
  color: #666;
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

/* Состояния загрузки и ошибки */
.loading {
  text-align: center;
  padding: 3rem;
  color: #667eea;
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
  text-align: center;
  padding: 3rem;
  color: #e74c3c;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
}

.edit-btn:hover {
  background: #e3f2fd;
  color: #2196f3;
}

/* Стили для формы */
.student-form {
  display: flex;
  flex-direction: column;
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

/* Стили для кнопок */
.btn-edit {
  padding: 0.75rem 1.5rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.3s;
}

.btn-edit:hover {
  background: #2980b9;
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

/* Адаптивность формы */
@media (max-width: 768px) {
  .student-form {
    gap: 0.75rem;
  }

  .form-group input,
  .form-group select {
    padding: 0.5rem;
  }
}

/* Адаптивность */
@media (max-width: 768px) {
  .controls {
    flex-direction: column;
  }

  .search-control,
  .filter-control {
    min-width: 100%;
  }

  .stats-summary {
    grid-template-columns: 1fr;
  }

  .students-table {
    display: block;
    overflow-x: auto;
  }

  .modal-content {
    margin: 1rem;
    width: calc(100% - 2rem);
  }

  .detail-row {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>