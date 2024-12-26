import axios from 'axios'
import {tokenStore} from '@/stores/tokenStore'

const axiosClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})


axiosClient.interceptors.request.use((config) => {
  const store = tokenStore()
  if (store.token) {
    config.headers.Authorization = `Token ${store.token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export default axiosClient
