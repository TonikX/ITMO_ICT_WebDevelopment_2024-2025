import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/system/food/diets/'

const apiClient = axios.create({
  baseURL: API_URL,
})

// Установка токена в заголовки
const setAuthToken = (token) => {
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete apiClient.defaults.headers.common['Authorization']
  }
}
// Получение списка всех животных
const getDiets = async (token) => {
  setAuthToken(token)
  const response = await apiClient.get('') // Используйте apiClient здесь
  return response.data
}

// Добавление нового животного
const addDiet = async (dietData, token) => {
  setAuthToken(token)
  const response = await apiClient.post('', dietData) // Используйте apiClient здесь
  return response.data
}

// Обновление данных животного
const updateDiet = async (id, dietData, token) => {
  setAuthToken(token)
  const response = await apiClient.put(`${id}/`, dietData) // Используйте apiClient здесь
  return response.data
}

// Удаление животного
const deleteDiet = async (id, token) => {
  setAuthToken(token)
  const response = await apiClient.delete(`${id}/`) // Используйте apiClient здесь
  return response.data
}

const dietService = {
  getDiets,
  addDiet,
  updateDiet,
  deleteDiet,
}

export default dietService
