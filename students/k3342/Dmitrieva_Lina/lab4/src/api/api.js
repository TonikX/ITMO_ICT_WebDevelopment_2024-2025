import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token"); // Получение токена из localStorage
  if (token) {
    config.headers["Authorization"] = `Token ${token}`;
  }
  return config;
});

export const getNewspapers = () => apiClient.get('/newspapers/');
export const addNewspaper = (data) => apiClient.post('/newspapers/', data);
export const updateNewspaper = (id, data) => apiClient.put(`/newspapers/${id}/`, data);
export const deleteNewspaper = (id) => apiClient.delete(`/newspapers/${id}/`);

export const getPrintShops = () => apiClient.get('/printshops/');
export const addPrintShop = (data) => apiClient.post('/printshops/', data);
export const updatePrintShop = (id, data) => apiClient.put(`/printshops/${id}/`, data);
export const deletePrintShop = (id) => apiClient.delete(`/printshops/${id}/`);

export const getPostalOffices = () => apiClient.get('/postaloffices/');

export const registerUser = (data) => apiClient.post("/auth/users/", data);

export const getDeliveries = () => apiClient.get("/deliveries/");
export const addDelivery = (data) => apiClient.post("/deliveries/", data);
export const updateDelivery = (id, data) => apiClient.put(`/deliveries/${id}/`, data);
export const deleteDelivery = (id) => apiClient.delete(`/deliveries/${id}/`);

export const getEmployees = () => apiClient.get("/employees/");
export const createEmployee = (data) => apiClient.post("/employees/", data);
export const updateEmployee = (id, data) => apiClient.put(`/employees/${id}/`, data);
export const deleteEmployee = (id) => apiClient.delete(`/employees/${id}/`);


export const fetchReport = (queryType, config = {}) => {
  return apiClient.get(`/newspaper-analytics/`, { params: { query_type: queryType, ...config.params } });
};


export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("username");
  window.location.href = "/login";
}

// Функция для входа
export const loginUser = async (data) => {
  try {
    const response = await apiClient.post("/auth/token/login/", data);
    const token = response.data.auth_token;

    // Сохраняем токен в localStorage
    localStorage.setItem("token", token);

    const userResponse = await apiClient.get("/auth/users/me/");
    localStorage.setItem("role", userResponse.data.role || "user");
    localStorage.setItem("username", userResponse.data.username);

    window.location.href = "/";
  } catch (error) {
    console.error("Ошибка при входе:", error);
    throw error;
  }
};
