import { api } from './api'

export const animalService = {
  async getAll() {
    const token = localStorage.getItem('access_token')
    console.log('🔑 Токен в getAll:', token)  // <-- смотрим, что приходит
    const response = await api.get('animals/', {
      headers: { Authorization: `JWT ${token}` }
    })
    return response.data
  },
  async getById(id) {
    const token = localStorage.getItem('access_token')
    console.log('🔑 Токен в getById:', token)
    const response = await api.get(`animals/${id}/`, {
      headers: { Authorization: `JWT ${token}` }
    })
    return response.data
  },
  async create(data) {
    const token = localStorage.getItem('access_token')
    console.log('🔑 Токен в create:', token)
    const response = await api.post('animals/', data, {
      headers: { Authorization: `JWT ${token}` }
    })
    return response.data
  },
  async update(id, data) {
    const token = localStorage.getItem('access_token')
    console.log('🔑 Токен в update:', token)
    const response = await api.put(`animals/${id}/`, data, {
      headers: { Authorization: `JWT ${token}` }
    })
    return response.data
  },
  async delete(id) {
    const token = localStorage.getItem('access_token')
    console.log('🔑 Токен в delete:', token)
    await api.delete(`animals/${id}/`, {
      headers: { Authorization: `JWT ${token}` }
    })
  },
}