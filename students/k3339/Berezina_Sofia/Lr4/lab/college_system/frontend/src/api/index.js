import axios from 'axios'

// Базовый экземпляр axios
const api = axios.create({
  baseURL: 'http://localhost:8000/',
  headers: {
    'Content-Type': 'application/json',
  }
})

// Эндпоинты для аутентификации (DRF Token)
// ВНИМАНИЕ: Имя экспорта должно совпадать с импортом в auth.js
// В auth.js вы импортируете 'authApi', поэтому здесь должно быть 'authApi'
const authApi = {
  login: (credentials) => api.post('token/', credentials),
  logout: () => api.post('token/logout/'),
  getUser: () => api.get('me/'),
}

// Эндпоинты данных
const apiEndpoints = {
  // Кабинеты
  classrooms: {
    list: () => api.get('classrooms/'),
    search: (query) => api.get(`classrooms/?search=${query}`),
  },

  // Преподаватели
  teachers: {
    active: () => api.get('teachers/'),
  },

  // Группы
  groups: {
    byCourse: (course) => api.get(`groups/course/${course}/`),
    detail: (id) => api.get(`groups/${id}/detail/`),
    nested: (id, day = 1) => api.get(`groups/${id}/nested/?day=${day}`),
    students: (id) => api.get(`groups/${id}/students/`),
  },

  // Студенты
  students: {
    search: (query = '') => api.get(`students/search/?search=${query}`),
    byGroup: (groupId) => api.get(`groups/${groupId}/students/`),
    grades: (id) => api.get(`students/${id}/grades/`),
    stats: (id) => api.get(`students/${id}/stats/`),
  },

  // Расписание
  schedule: {
    group: (groupId) => api.get(`schedule/group/${groupId}/`),
  },

  // Дисциплины
  subjects: {
    byCourseSemester: (course, semester) => api.get(`subjects/course/${course}/semester/${semester}/`),
  },

  // Оценки
  grades: {
    create: (data) => api.post('grades/create/', data),
    update: (id, data) => api.put(`grades/${id}/update/`, data),
    delete: (id) => api.delete(`grades/${id}/delete/`),
  },
}

// Перехватчик для добавления токена
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

// Перехватчик для обработки ошибок
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Экспорты - имена должны совпадать с импортами в других файлах
export { authApi, apiEndpoints }
export default api