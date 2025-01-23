// api/patients.js
import axiosInstance from './axiosInstance';

// Получение списка пациентов
export const getPatients = async () => {
    const response = await axiosInstance.get('/patients/');
    return response.data;
};

// Создание нового пациента
export const createPatient = async (patientData) => {
    const response = await axiosInstance.post('/patients/', patientData);
    return response.data;
};

// Обновление данных пациента
export const updatePatient = async (patientData) => {
    const response = await axiosInstance.put(`/patients/${patientData.id}/`, patientData);
    return response.data;
};

// Удаление пациента
export const deletePatient = async (id) => {
    await axiosInstance.delete(`/patients/${id}/`);
};
