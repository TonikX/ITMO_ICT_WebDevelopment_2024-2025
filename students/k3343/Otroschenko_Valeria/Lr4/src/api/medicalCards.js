import axiosInstance from './axiosInstance';

// Функция для создания новой медицинской карты

export const createMedicalCard = async (data) => {
    try {
        const response = await axiosInstance.post('/medical_cards/', {
            patient: {
                first_name: data.patient.first_name,
                last_name: data.patient.last_name,
                birth_date: data.patient.birth_date,
            },
            record_date: data.record_date,
            diagnosis: data.diagnosis
        });
        return response.data;
    } catch (error) {
        console.error('Ошибка при создании медицинской карты:', error);
        throw error;
    }
};


// Функция для получения всех медицинских карт
export const getMedicalCards = async () => {
    try {
        const response = await axiosInstance.get('/medical_cards/');
        return response.data;  // возвращаем данные карт
    } catch (error) {
        console.error('Ошибка при получении медицинских карт:', error);
        throw error;
    }
};


// Функция для удаления пациента и его медицинской карты
export const deleteMedicalCard = async (patientId) => {
    try {
        const response = await axiosInstance.delete(`/patients/${patientId}/`);  // Удаляем пациента по его ID
        return response.data;
    } catch (error) {
        console.error('Ошибка при удалении пациента и медицинской карты:', error);
        throw error;
    }
};
