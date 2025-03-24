import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/bus/';

// Получаем токен из localStorage
const getAuthToken = () => localStorage.getItem('authToken');

// Функция для добавления токена в заголовки
const getAuthHeaders = () => ({
  headers: {
    'Authorization': `Token ${getAuthToken()}`,
  }
});

// Водители
export const getDrivers = () => axios.get(`${API_URL}drivers/`, getAuthHeaders());
export const addDriver = (driver) => axios.post(`${API_URL}drivers/`, driver, getAuthHeaders());
export const getDriverById = (id) => axios.get(`${API_URL}drivers/${id}/`, getAuthHeaders());
export const updateDriver = (id, driver) => axios.put(`${API_URL}drivers/${id}/`, driver, getAuthHeaders());
export const deleteDriver = (id) => axios.delete(`${API_URL}drivers/${id}/`, getAuthHeaders());

// Маршруты
export const getRoutes = () => axios.get(`${API_URL}routes/`, getAuthHeaders());
export const addRoute = (route) => axios.post(`${API_URL}routes/`, route, getAuthHeaders());
export const getRouteById = (id) => axios.get(`${API_URL}routes/${id}/`, getAuthHeaders());
export const updateRoute = (id, route) => axios.put(`${API_URL}routes/${id}/`, route, getAuthHeaders());
export const deleteRoute = (id) => axios.delete(`${API_URL}routes/${id}/`, getAuthHeaders());

// Автобусы
export const getBuses = () => axios.get(`${API_URL}buses/`, getAuthHeaders());
export const addBus = (bus) => axios.post(`${API_URL}buses/`, bus, getAuthHeaders());
export const getBusById = (id) => axios.get(`${API_URL}buses/${id}/`, getAuthHeaders());
export const updateBus = (id, bus) => axios.put(`${API_URL}buses/${id}/`, bus, getAuthHeaders());
export const deleteBus = (id) => axios.delete(`${API_URL}buses/${id}/`, getAuthHeaders());

// Категории автобусов
export const getBusCategories = () => axios.get(`${API_URL}bus-categories/`, getAuthHeaders());
export const addBusCategory = (category) => axios.post(`${API_URL}bus-categories/`, category, getAuthHeaders());
export const getBusCategoryById = (id) => axios.get(`${API_URL}bus-categories/${id}/`, getAuthHeaders());
export const updateBusCategory = (id, category) => axios.put(`${API_URL}bus-categories/${id}/`, category, getAuthHeaders());
export const deleteBusCategory = (id) => axios.delete(`${API_URL}bus-categories/${id}/`, getAuthHeaders());

// Смены
export const getShifts = () => axios.get(`${API_URL}shifts/`, getAuthHeaders());
export const getShiftById = (id) => axios.get(`${API_URL}shifts/${id}/`, getAuthHeaders());
export const addShift = (shift) => axios.post(`${API_URL}shifts/`, shift, getAuthHeaders());
export const updateShift = (id, shift) => axios.put(`${API_URL}shifts/${id}/`, shift, getAuthHeaders());
export const deleteShift = (id) => axios.delete(`${API_URL}shifts/${id}/`, getAuthHeaders());

// Продолжительность маршрутов
export const getTotalRouteDuration = () => axios.get(`${API_URL}routes/total-duration/`, getAuthHeaders());

// Количество водителей по классам
export const getDriverCategoryCount = () => axios.get(`${API_URL}drivers/category-count/`, getAuthHeaders());

// Отчет
export const getParkStatusReport = () => axios.get(`${API_URL}reports/park-status/`, getAuthHeaders());
