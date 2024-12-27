import apiClient from '@/services/apiClient';

export default {
  async getEmployees(params = {}) {
    const response = await apiClient.get('/insurance/employees/', { params });
    return response.data;
  },

  async getOrganizations() {
    const response = await apiClient.get('/insurance/organizations/');
    return response.data;
  },

  async getEmployeeById(id) {
    const response = await apiClient.get(`/insurance/employees/${id}/`);
    return response.data;
  },

  async updateEmployee(id, data) {
    const response = await apiClient.patch(`/insurance/employees/${id}/`, data);
    return response.data;
  },

  async fireEmployee(id) {
    const response = await apiClient.post(`/insurance/employees/${id}/fire_employee/`);
    return response.data;
  }
};
