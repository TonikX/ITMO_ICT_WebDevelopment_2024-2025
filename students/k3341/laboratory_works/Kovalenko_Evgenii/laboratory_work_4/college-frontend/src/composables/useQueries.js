import { ref } from 'vue'
import { queriesAPI, statisticsAPI } from '@/api/endpoints'

export function useQueries() {
  const isLoading = ref(false)
  const error = ref(null)
  const queryResults = ref({})

  // запрос 1
  const scheduleQuery = async (data) => {
    isLoading.value = true
    try {
      const response = await queriesAPI.scheduleQuery(data)
      queryResults.value.schedule = response.data
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // запрос 2
  const getTeachersByGroup = async (data) => {
    isLoading.value = true
    try {
      const response = await queriesAPI.teachersByGroup(data)
      queryResults.value.teachersByGroup = response.data
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // запрос 3
  const getGroupsBySubjectTeacher = async (data) => {
    isLoading.value = true
    try {
      const response = await queriesAPI.groupsBySubjectTeacher(data)
      queryResults.value.groupsBySubjectTeacher = response.data
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // запрос 4
  const getGroupSchedule = async (data) => {
    isLoading.value = true
    try {
      const response = await queriesAPI.groupSchedule(data)
      queryResults.value.groupSchedule = response.data
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // запрос 5
  const getStudentsByCourse = async (course) => {
    isLoading.value = true
    try {
      const response = await queriesAPI.studentsByCourse(course)
      queryResults.value.studentsByCourse = response.data
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // сводная ведомость успеваемости за семестр по группе
  const getGroupPerformanceReport = async (data) => {
    isLoading.value = true
    try {
      const response = await queriesAPI.groupPerformance(data)
      queryResults.value.groupPerformance = response.data
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // получение статистики для дашборда
  const getDashboardStats = async () => {
    isLoading.value = true
    try {
      const response = await statisticsAPI.dashboardStats()
      queryResults.value.dashboardStats = response.data
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // получение статистики по курсам
  const getCourseStatistics = async () => {
    isLoading.value = true
    try {
      const response = await statisticsAPI.courseStatistics()
      queryResults.value.courseStatistics = response.data
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      isLoading.value = false
    }
  }

  // очистка результатов запросов
  const clearResults = () => {
    queryResults.value = {}
  }

  return {
    isLoading,
    error,
    queryResults,
    scheduleQuery,
    getTeachersByGroup,
    getGroupsBySubjectTeacher,
    getGroupSchedule,
    getStudentsByCourse,
    getGroupPerformanceReport,
    getDashboardStats,
    getCourseStatistics,
    clearResults
  }
}