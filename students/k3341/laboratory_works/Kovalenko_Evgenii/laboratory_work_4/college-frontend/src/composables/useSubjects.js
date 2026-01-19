import { ref } from 'vue'
import { subjectAPI } from '@/api/endpoints'

export function useSubjects() {
  const subjects = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchSubjects = async (params = {}) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await subjectAPI.getAll(params)
      subjects.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data || 'Ошибка загрузки предметов'
    } finally {
      isLoading.value = false
    }
  }

  const createSubject = async (data) => {
    isLoading.value = true
    try {
      const response = await subjectAPI.create(data)
      subjects.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const updateSubject = async (id, data) => {
    isLoading.value = true
    try {
      const response = await subjectAPI.update(id, data)
      const index = subjects.value.findIndex(s => s.subject_id === id)
      if (index !== -1) {
        subjects.value[index] = response.data
      }
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const deleteSubject = async (id) => {
    isLoading.value = true
    try {
      await subjectAPI.delete(id)
      subjects.value = subjects.value.filter(s => s.subject_id !== id)
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  return {
    subjects,
    isLoading,
    error,
    fetchSubjects,
    createSubject,
    updateSubject,
    deleteSubject
  }
}