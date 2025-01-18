import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/system/animals/'

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
const getAnimals = async (token) => {
  setAuthToken(token)
  const response = await apiClient.get('') // Используйте apiClient здесь
  return response.data
}

// Получение списка всех животных
const getAnimalsIn = async (token) => {
  setAuthToken(token)
  const response = await apiClient.get('animals_in/') // Используйте apiClient здесь
  return response.data
}

// Добавление нового животного
const addAnimal = async (animalData, token) => {
  setAuthToken(token)
  const response = await apiClient.post('', animalData) // Используйте apiClient здесь
  return response.data
}

// Обновление данных животного
const updateAnimal = async (id, animalData, token) => {
  setAuthToken(token)
  const response = await apiClient.put(`${id}/`, animalData) // Используйте apiClient здесь
  return response.data
}

// Удаление животного
const deleteAnimal = async (id, token) => {
  setAuthToken(token)
  const response = await apiClient.delete(`${id}/`) // Используйте apiClient здесь
  return response.data
}

const animalService = {
  getAnimals,
  addAnimal,
  updateAnimal,
  deleteAnimal,
  getAnimalsIn
}

export default animalService
