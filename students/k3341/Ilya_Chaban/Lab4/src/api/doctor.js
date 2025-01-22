import axiosInstance from './axiosInstance';

// Получение списка докторов
export const getDoctors = async () => {
    try {
        const response = await axiosInstance.get('/doctors/');
        return response.data; // Возвращаем массив докторов
    } catch (error) {
        console.error("Error fetching doctors:", error);
        throw error; // Пробрасываем ошибку дальше для обработки
    }
};

// Добавление нового доктора
export const addDoctor = async (doctorData) => {
    try {
        const response = await axiosInstance.post('/doctors/', doctorData);
        return response.data; // Возвращаем данные добавленного врача
    } catch (error) {
        console.error("Error adding doctor:", error);
        throw error; // Пробрасываем ошибку дальше для обработки
    }
};

// Удаление доктора по id
export const deleteDoctor = async (doctorId) => {
    try {
        const response = await axiosInstance.delete(`/doctors/${doctorId}/`);
        return response.data; // Возвращаем данные ответа
    } catch (error) {
        console.error("Error deleting doctor:", error);
        throw error; // Пробрасываем ошибку дальше для обработки
    }
};
