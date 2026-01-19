import { ref } from 'vue'
import { teacherAPI } from '@/api/endpoints'

export function useTeachers() {
  const teachers = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchTeachers = async (params = {}) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await teacherAPI.getAll(params)
      teachers.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data || 'Ошибка загрузки'
    } finally {
      isLoading.value = false
    }
  }

  const createTeacher = async (data) => {
    isLoading.value = true
    try {
      const response = await teacherAPI.create(data)
      teachers.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const updateTeacher = async (id, data) => {
    isLoading.value = true
    try {
      const response = await teacherAPI.update(id, data)
      const index = teachers.value.findIndex(t => t.teacher_id === id)
      if (index !== -1) {
        teachers.value[index] = response.data
      }
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const deleteTeacher = async (id) => {
    isLoading.value = true
    try {
      await teacherAPI.delete(id)
      teachers.value = teachers.value.filter(t => t.teacher_id !== id)
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  return {
    teachers,
    isLoading,
    error,
    fetchTeachers,
    createTeacher,
    updateTeacher,
    deleteTeacher
  }
}