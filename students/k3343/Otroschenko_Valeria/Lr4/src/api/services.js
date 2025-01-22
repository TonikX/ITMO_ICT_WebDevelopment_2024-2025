import axiosInstance from './axiosInstance';

// Получение списка сервисов
export const getServices = async () => {
    const response = await axiosInstance.get('/service/');
    return response.data;
};

// Создание нового сервиса
export const createService = async (serviceData) => {
    const response = await axiosInstance.post('/service/', serviceData);
    return response.data;
};

// Обновление данных сервиса
export const updateService = async (serviceData) => {
    const response = await axiosInstance.put(`/service/${serviceData.id}/`, serviceData);
    return response.data;
};

// Удаление сервиса
export const deleteService = async (id) => {
    await axiosInstance.delete(`/service/${id}/`);
};
