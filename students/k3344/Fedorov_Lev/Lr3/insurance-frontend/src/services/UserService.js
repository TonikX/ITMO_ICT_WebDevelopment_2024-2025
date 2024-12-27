import apiClient from '@/services/apiClient';

export default {
    async getProfile() {
        try {
            const response = await apiClient.get('/insurance/user/profile/');
            return response.data;
        } catch (error) {
            if (error.response && error.response.status === 401) {
                alert('Сессия истекла. Пожалуйста, войдите снова.');
                localStorage.removeItem('token');
                window.location.href = '/login';
            }
            throw error;
        }
    },
    async updateProfile(userData) {
        const response = await apiClient.patch('/insurance/profile/update-partial/', userData);
        return response.data;
    },
    async changePassword(passwordData) {
    const response = await apiClient.put('/insurance/profile/change-password/', passwordData);
    return response.data;
  }
};
