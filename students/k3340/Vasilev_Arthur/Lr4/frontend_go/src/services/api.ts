import axios, { type AxiosInstance } from 'axios'

const API_BASE_URL = 'http://localhost:8080/api/v1'

class ApiService {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Добавляем JWT токен к каждому запросу
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Обработка ошибок
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Токен недействителен, удаляем его
          localStorage.removeItem('auth_token')
          localStorage.removeItem('user')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Аутентификация (JWT)
  async login(username: string, password: string) {
    const response = await this.api.post('/auth/login', {
      username_or_email: username,
      password,
    })
    // Go API возвращает: { token, token_type, expires_at, user }
    return {
      token: response.data.token,
      user: response.data.user
    }
  }

  async register(username: string, password: string, email: string, first_name?: string, last_name?: string) {
    const response = await this.api.post('/auth/register', {
      username,
      email,
      password,
      first_name,
      last_name,
    })
    // Go API возвращает: { token, token_type, expires_at, user }
    return {
      token: response.data.token,
      user: response.data.user
    }
  }

  async getCurrentUser() {
    const response = await this.api.get('/auth/me')
    return response.data
  }

  // Газеты (Newspapers)
  async getNewspapers(params?: { page?: number; page_size?: number }) {
    const response = await this.api.get('/newspapers')
    // Go API не использует пагинацию, возвращает массив напрямую
    return { results: response.data, count: response.data.length }
  }

  async getNewspaper(id: number) {
    const response = await this.api.get(`/newspapers/${id}`)
    return response.data
  }

  async createNewspaper(data: {
    title: string
    publication_index: string
    editor_first_name: string
    editor_last_name: string
    editor_middle_name?: string
    price_per_copy: string
  }) {
    const response = await this.api.post('/newspapers', {
      ...data,
      price_per_copy: parseFloat(data.price_per_copy)
    })
    return response.data
  }

  async updateNewspaper(id: number, data: Partial<{
    title: string
    publication_index: string
    editor_first_name: string
    editor_last_name: string
    editor_middle_name: string
    price_per_copy: string
  }>) {
    const updateData = { ...data }
    if (updateData.price_per_copy) {
      updateData.price_per_copy = parseFloat(updateData.price_per_copy) as any
    }
    const response = await this.api.put(`/newspapers/${id}`, updateData)
    return response.data
  }

  async deleteNewspaper(id: number) {
    const response = await this.api.delete(`/newspapers/${id}`)
    return response.data
  }

  async getNewspaperFullDetail(id: number) {
    const response = await this.api.get(`/newspapers/${id}/full-detail`)
    return response.data
  }

  async getNewspapersByName(name: string) {
    const response = await this.api.get('/newspapers/by-name', { params: { name } })
    return response.data
  }

  async getNewspaperInfo(params: { id?: number; name?: string }) {
    const response = await this.api.get('/newspapers/info', { params })
    return response.data
  }

  // Типографии (Printing Houses)
  async getPrintingHouses(params?: { page?: number; page_size?: number }) {
    const response = await this.api.get('/printing-houses')
    return { results: response.data, count: response.data.length }
  }

  async getPrintingHouse(id: number) {
    const response = await this.api.get(`/printing-houses/${id}`)
    return response.data
  }

  async createPrintingHouse(data: {
    name: string
    address: string
    is_active: boolean
  }) {
    const response = await this.api.post('/printing-houses', data)
    return response.data
  }

  async updatePrintingHouse(id: number, data: Partial<{
    name: string
    address: string
    is_active: boolean
  }>) {
    const response = await this.api.put(`/printing-houses/${id}`, data)
    return response.data
  }

  async deletePrintingHouse(id: number) {
    const response = await this.api.delete(`/printing-houses/${id}`)
    return response.data
  }

  async getPrintingHouseFullDetail(id: number) {
    const response = await this.api.get(`/printing-houses/${id}/full-detail`)
    return response.data
  }

  async getLargestCirculationEditor(id: number) {
    const response = await this.api.get(`/printing-houses/${id}/largest-circulation-editor`)
    return response.data
  }

  async getPrintingHousesReport() {
    const response = await this.api.get('/printing-houses/report')
    return response.data
  }

  // Почтовые отделения (Post Offices)
  async getPostOffices(params?: { page?: number; page_size?: number }) {
    const response = await this.api.get('/post-offices')
    return { results: response.data, count: response.data.length }
  }

  async getPostOffice(id: number) {
    const response = await this.api.get(`/post-offices/${id}`)
    return response.data
  }

  async createPostOffice(data: {
    number: string
    address: string
  }) {
    const response = await this.api.post('/post-offices', data)
    return response.data
  }

  async updatePostOffice(id: number, data: Partial<{
    number: string
    address: string
  }>) {
    const response = await this.api.put(`/post-offices/${id}`, data)
    return response.data
  }

  async deletePostOffice(id: number) {
    const response = await this.api.delete(`/post-offices/${id}`)
    return response.data
  }

  async getPostOfficeFullDetail(id: number) {
    const response = await this.api.get(`/post-offices/${id}/full-detail`)
    return response.data
  }

  async getPostOfficesByPrice(min_price: number) {
    const response = await this.api.get('/post-offices/by-price', { params: { min_price } })
    return response.data
  }

  async getPostOfficesLowQuantity(max_quantity: number) {
    // Этого эндпоинта нет в Go API, возвращаем пустой массив
    return []
  }

  // Распределения (Distributions)
  async getDistributions(params?: { page?: number; page_size?: number }) {
    const response = await this.api.get('/distributions')
    return { results: response.data, count: response.data.length }
  }

  async getDistribution(id: number) {
    const response = await this.api.get(`/distributions/${id}`)
    return response.data
  }

  async createDistribution(data: {
    post_office: number
    newspaper: number
    printing_house: number
    quantity: number
  }) {
    const response = await this.api.post('/distributions', {
      post_office_id: data.post_office,
      newspaper_id: data.newspaper,
      printing_house_id: data.printing_house,
      quantity: data.quantity
    })
    return response.data
  }

  async updateDistribution(id: number, data: Partial<{
    post_office: number
    newspaper: number
    printing_house: number
    quantity: number
  }>) {
    const updateData: any = {}
    if (data.quantity !== undefined) {
      updateData.quantity = data.quantity
    }
    const response = await this.api.put(`/distributions/${id}`, updateData)
    return response.data
  }

  async deleteDistribution(id: number) {
    const response = await this.api.delete(`/distributions/${id}`)
    return response.data
  }

  async getDistributionByNewspaperAndAddress(params: {
    newspaper_id?: number
    newspaper_name?: string
    address: string
  }) {
    // Этого эндпоинта нет в Go API, возвращаем пустой массив
    return []
  }

  // Метод для прямого доступа к axios instance
  get axiosInstance(): AxiosInstance {
    return this.api
  }

  // PrintingRuns (Тиражи / Публикации)
  async getPrintingRuns(params?: { page?: number; page_size?: number }) {
    const response = await this.api.get('/printing-runs')
    return { results: response.data, count: response.data.length }
  }

  async getPrintingRun(id: number) {
    const response = await this.api.get(`/printing-runs/${id}`)
    return response.data
  }

  async createPrintingRun(data: {
    printing_house_id: number
    newspaper_id: number
    circulation: number
  }) {
    const response = await this.api.post('/printing-runs', data)
    return response.data
  }

  async updatePrintingRun(id: number, data: Partial<{
    circulation: number
  }>) {
    const response = await this.api.put(`/printing-runs/${id}`, data)
    return response.data
  }

  async deletePrintingRun(id: number) {
    const response = await this.api.delete(`/printing-runs/${id}`)
    return response.data
  }
}

export default new ApiService()