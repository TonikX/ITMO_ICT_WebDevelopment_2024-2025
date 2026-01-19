import { ref } from 'vue'
import { studentAPI } from '@/api/endpoints'

export function useStudents() {
  const students = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchStudents = async (params = {}) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await studentAPI.getAll(params)
      students.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data || 'Ошибка загрузки студентов'
    } finally {
      isLoading.value = false
    }
  }

  const fetchStudent = async (id) => {
    isLoading.value = true
    try {
      const response = await studentAPI.get(id)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const createStudent = async (data) => {
    isLoading.value = true
    try {
      const response = await studentAPI.create(data)
      students.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const updateStudent = async (id, data) => {
    isLoading.value = true
    try {
      const response = await studentAPI.update(id, data)
      const index = students.value.findIndex(s => s.student_id === id)
      if (index !== -1) {
        students.value[index] = response.data
      }
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const deleteStudent = async (id) => {
    isLoading.value = true
    try {
      await studentAPI.delete(id)
      students.value = students.value.filter(s => s.student_id !== id)
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // Получение оценок студента
  const getStudentGrades = async (studentId) => {
    isLoading.value = true
    try {
      const response = await studentAPI.get(studentId)
      return { success: true, grades: response.data.grades || [] }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // Получение студентов по курсу
  const getStudentsByCourse = async (course) => {
    isLoading.value = true
    try {
      const response = await studentAPI.getByCourse(course)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  return {
    students,
    isLoading,
    error,
    fetchStudents,
    fetchStudent,
    createStudent,
    updateStudent,
    deleteStudent,
    getStudentGrades,
    getStudentsByCourse
  }
}