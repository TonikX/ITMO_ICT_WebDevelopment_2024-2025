import { ref } from 'vue'
import { gradeAPI } from '@/api/endpoints'

export function useGrades() {
  const grades = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchGrades = async (params = {}) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await gradeAPI.getAll(params)
      grades.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data || 'Ошибка загрузки оценок'
    } finally {
      isLoading.value = false
    }
  }

  const createGrade = async (data) => {
    isLoading.value = true
    try {
      const response = await gradeAPI.create(data)
      grades.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const updateGrade = async (id, data) => {
    isLoading.value = true
    try {
      const response = await gradeAPI.update(id, data)
      const index = grades.value.findIndex(g => g.grade_id === id)
      if (index !== -1) {
        grades.value[index] = response.data
      }
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const deleteGrade = async (id) => {
    isLoading.value = true
    try {
      await gradeAPI.delete(id)
      grades.value = grades.value.filter(g => g.grade_id !== id)
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
      const response = await gradeAPI.getAll({ student: studentId })
      return { success: true, data: response.data.results || response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // Получение оценок по предмету
  const getSubjectGrades = async (subjectId) => {
    isLoading.value = true
    try {
      const response = await gradeAPI.getAll({ subject: subjectId })
      return { success: true, data: response.data.results || response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // Получение оценок за семестр
  const getGradesBySemester = async (semester, academicYear) => {
    isLoading.value = true
    try {
      const params = { semester }
      if (academicYear) params.academic_year = academicYear
      
      const response = await gradeAPI.getAll(params)
      return { success: true, data: response.data.results || response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // Расчет среднего балла студента
  const calculateStudentAverage = (studentId) => {
    const studentGrades = grades.value.filter(g => g.student === studentId)
    if (studentGrades.length === 0) return null
    
    const sum = studentGrades.reduce((total, grade) => total + parseFloat(grade.grade_value), 0)
    return (sum / studentGrades.length).toFixed(2)
  }

  // Расчет среднего балла по группе
  const calculateGroupAverage = (groupId) => {
    // Здесь нужна логика получения студентов группы и их оценок
    // Это упрощенная версия
    if (grades.value.length === 0) return null
    
    const sum = grades.value.reduce((total, grade) => total + parseFloat(grade.grade_value), 0)
    return (sum / grades.value.length).toFixed(2)
  }

  return {
    grades,
    isLoading,
    error,
    fetchGrades,
    createGrade,
    updateGrade,
    deleteGrade,
    getStudentGrades,
    getSubjectGrades,
    getGradesBySemester,
    calculateStudentAverage,
    calculateGroupAverage
  }
}