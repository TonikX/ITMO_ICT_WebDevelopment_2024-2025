import axiosInstance from './axiosInstance';

export const getPatients = async () => {
    const response = await axiosInstance.get('/patients/');
    return response.data;
};

export const getDoctors = async () => {
    const response = await axiosInstance.get('/doctors/');
    return response.data;
};

export const getCabinets = async () => {
    const response = await axiosInstance.get('/cabinets/');
    return response.data;
};

export const getServices = async () => {
    try {
        const response = await axiosInstance.get('/service/');
        return response.data;
    } catch (error) {
        console.error("Error fetching services:", error);
        throw error;
    }
};
