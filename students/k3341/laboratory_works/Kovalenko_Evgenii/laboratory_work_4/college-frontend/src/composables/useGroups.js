import { ref } from 'vue'
import { groupAPI } from '@/api/endpoints'

export function useGroups() {
  const groups = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchGroups = async (params = {}) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await groupAPI.getAll(params)
      groups.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data || 'Ошибка загрузки групп'
    } finally {
      isLoading.value = false
    }
  }

  const createGroup = async (data) => {
    isLoading.value = true
    try {
      const response = await groupAPI.create(data)
      groups.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const updateGroup = async (id, data) => {
    isLoading.value = true
    try {
      const response = await groupAPI.update(id, data)
      const index = groups.value.findIndex(g => g.group_id === id)
      if (index !== -1) {
        groups.value[index] = response.data
      }
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const deleteGroup = async (id) => {
    isLoading.value = true
    try {
      await groupAPI.delete(id)
      groups.value = groups.value.filter(g => g.group_id !== id)
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  return {
    groups,
    isLoading,
    error,
    fetchGroups,
    createGroup,
    updateGroup,
    deleteGroup
  }
}