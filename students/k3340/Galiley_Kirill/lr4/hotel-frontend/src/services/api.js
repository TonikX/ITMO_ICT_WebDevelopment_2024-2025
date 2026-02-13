import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/v1/'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

export default {
  login(credentials) {
    return api.post('token/login/', credentials)
  },

  register(userData) {
    return api.post('users/', userData)
  },

  getRooms(params) {
    return api.get('rooms/', { params })
  },

  createRoom(data) {
    return api.post('rooms/', data)
  },

  getClients(params) {
    return api.get('clients/', { params })
  },

  createClient(data) {
    return api.post('clients/', data)
  },

  getStays() {
    return api.get('stays/')
  },

  createStay(data) {
    return api.post('stays/', {
      client_id: data.client,
      room_id: data.room,
      check_in: data.check_in,
      check_out: data.check_out,
    })
  },

  getFreeRooms() {
    return api.get('queries/free-rooms/')
  },

  getQuarterReport(quarter) {
    return api.get(`report/quarter/${quarter}/`)
  },
}
