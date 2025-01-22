import axiosInstance from './axiosInstance';

export const getAppointments = async () => {
    const response = await axiosInstance.get('/appointments/');
    return response.data;
};

export const addAppointment = async (appointmentData) => {
    try {
        const response = await axiosInstance.post('/appointments/', appointmentData);
        return response.data;
    } catch (error) {
        console.error("Error adding appointment:", error);
        throw error;
    }
};

export const deleteAppointment = async (appointmentId) => {
    try {
        const response = await axiosInstance.delete(`/appointments/${appointmentId}/`);
        return response.data;
    } catch (error) {
        console.error("Error deleting appointment:", error);
        throw error;
    }
};


export const updateAppointment = async (appointmentId, updatedData) => {
    try {
        const response = await axiosInstance.put(`/appointments/${appointmentId}/`, updatedData);
        return response.data;
    } catch (error) {
        console.error("Error updating appointment:", error);
        throw error;
    }
};
