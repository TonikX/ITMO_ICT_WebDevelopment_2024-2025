import { ref } from 'vue'
import { classroomAPI } from '@/api/endpoints'

export function useClassrooms() {
  const classrooms = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchClassrooms = async (params = {}) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await classroomAPI.getAll(params)
      classrooms.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data || 'Ошибка загрузки аудиторий'
    } finally {
      isLoading.value = false
    }
  }

  const createClassroom = async (data) => {
    isLoading.value = true
    try {
      const response = await classroomAPI.create(data)
      classrooms.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const updateClassroom = async (id, data) => {
    isLoading.value = true
    try {
      const response = await classroomAPI.update(id, data)
      const index = classrooms.value.findIndex(c => c.classroom_id === id)
      if (index !== -1) {
        classrooms.value[index] = response.data
      }
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const deleteClassroom = async (id) => {
    isLoading.value = true
    try {
      await classroomAPI.delete(id)
      classrooms.value = classrooms.value.filter(c => c.classroom_id !== id)
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  return {
    classrooms,
    isLoading,
    error,
    fetchClassrooms,
    createClassroom,
    updateClassroom,
    deleteClassroom
  }
}