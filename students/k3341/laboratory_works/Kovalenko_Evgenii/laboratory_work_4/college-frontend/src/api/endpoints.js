import api from './index'

export const authAPI = {
  login(data) {
    return api.post('/auth/token/login/', data)
  },
  register(data) {
    return api.post('/auth/users/', data)
  },
  logout() {
    return api.post('/auth/token/logout/')
  },
  getCurrentUser() {
    return api.get('/auth/users/me/')
  },
  updateUser(id, data) {
    return api.put(`/auth/users/${id}/`, data)
  }
}

export const teacherAPI = {
  getAll(params) {
    return api.get('/teachers/', { params })
  },
  get(id) {
    return api.get(`/teachers/${id}/`)
  },
  create(data) {
    return api.post('/teachers/', data)
  },
  update(id, data) {
    return api.put(`/teachers/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/teachers/${id}/`)
  }
}

export const studentAPI = {
  getAll(params) {
    return api.get('/students/', { params })
  },
  get(id) {
    return api.get(`/students/${id}/`)
  },
  create(data) {
    return api.post('/students/', data)
  },
  update(id, data) {
    return api.put(`/students/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/students/${id}/`)
  },
  getByCourse(course) {
    return api.get(`/students/by_course/?course=${course}`)
  }
}

export const scheduleAPI = {
  getAll(params) {
    return api.get('/schedules/', { params })
  },
  get(id) {
    return api.get(`/schedules/${id}/`)
  },
  create(data) {
    return api.post('/schedules/', data)
  },
  update(id, data) {
    return api.put(`/schedules/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/schedules/${id}/`)
  }
}

export const gradeAPI = {
  getAll(params) {
    return api.get('/grades/', { params })
  },
  get(id) {
    return api.get(`/grades/${id}/`)
  },
  create(data) {
    return api.post('/grades/', data)
  },
  update(id, data) {
    return api.put(`/grades/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/grades/${id}/`)
  }
}

export const groupAPI = {
  getAll(params) {
    return api.get('/groups/', { params })
  },
  get(id) {
    return api.get(`/groups/${id}/`)
  },
  create(data) {
    return api.post('/groups/', data)
  },
  update(id, data) {
    return api.put(`/groups/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/groups/${id}/`)
  }
}

export const subjectAPI = {
  getAll(params) {
    return api.get('/subjects/', { params })
  },
  get(id) {
    return api.get(`/subjects/${id}/`)
  },
  create(data) {
    return api.post('/subjects/', data)
  },
  update(id, data) {
    return api.put(`/subjects/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/subjects/${id}/`)
  }
}

export const classroomAPI = {
  getAll(params) {
    return api.get('/classrooms/', { params })
  },
  get(id) {
    return api.get(`/classrooms/${id}/`)
  },
  create(data) {
    return api.post('/classrooms/', data)
  },
  update(id, data) {
    return api.put(`/classrooms/${id}/`, data)
  },
  delete(id) {
    return api.delete(`/classrooms/${id}/`)
  }
}

// Запросы должны быть без /api в начале, так как baseURL уже включает его
export const queriesAPI = {
  scheduleQuery(data) {
    return api.post('/queries/schedule/', data)
  },
  teachersByGroup(data) {
    return api.post('/queries/teachers-by-group/', data)
  },
  groupsBySubjectTeacher(data) {
    return api.post('/queries/groups-by-subject-teacher/', data)
  },
  groupSchedule(data) {
    return api.post('/queries/group-schedule/', data)
  },
  studentsByCourse(course) {
    return api.get(`/queries/students-by-course/${course}/`)
  },
  groupPerformance(data) {
    return api.post('/queries/group-performance/', data)
  }
}

// Статистика
export const statisticsAPI = {
  dashboardStats() {
    return api.get('/statistics/dashboard/')
  },
  courseStatistics() {
    return api.get('/statistics/courses/')
  }
}