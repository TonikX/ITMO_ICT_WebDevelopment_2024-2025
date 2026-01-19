import { ref } from 'vue'
import { scheduleAPI } from '@/api/endpoints'

export function useSchedule() {
  const schedules = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchSchedules = async (params = {}) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await scheduleAPI.getAll(params)
      schedules.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data || 'Ошибка загрузки расписания'
    } finally {
      isLoading.value = false
    }
  }

  const createSchedule = async (data) => {
    isLoading.value = true
    try {
      const response = await scheduleAPI.create(data)
      schedules.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const updateSchedule = async (id, data) => {
    isLoading.value = true
    try {
      const response = await scheduleAPI.update(id, data)
      const index = schedules.value.findIndex(s => s.schedule_id === id)
      if (index !== -1) {
        schedules.value[index] = response.data
      }
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  const deleteSchedule = async (id) => {
    isLoading.value = true
    try {
      await scheduleAPI.delete(id)
      schedules.value = schedules.value.filter(s => s.schedule_id !== id)
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // Получение расписания для конкретной группы
  const getGroupSchedule = async (groupId) => {
    isLoading.value = true
    try {
      const response = await scheduleAPI.getAll({ group: groupId })
      return { success: true, data: response.data.results || response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // Получение расписания для конкретного преподавателя
  const getTeacherSchedule = async (teacherId) => {
    isLoading.value = true
    try {
      const response = await scheduleAPI.getAll({ teacher: teacherId })
      return { success: true, data: response.data.results || response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // Получение расписания на конкретный день недели
  const getScheduleByDay = async (dayOfWeek, params = {}) => {
    isLoading.value = true
    try {
      const response = await scheduleAPI.getAll({ ...params, day_of_week: dayOfWeek })
      return { success: true, data: response.data.results || response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  return {
    schedules,
    isLoading,
    error,
    fetchSchedules,
    createSchedule,
    updateSchedule,
    deleteSchedule,
    getGroupSchedule,
    getTeacherSchedule,
    getScheduleByDay
  }
}