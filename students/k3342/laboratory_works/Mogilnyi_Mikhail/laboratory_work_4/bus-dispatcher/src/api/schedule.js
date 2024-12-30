import axios from 'axios';

const API_URL = 'http://localhost:8000/manage';

export const getSchedules = () => axios.get(`${API_URL}/schedules`);

export const getScheduleById = (id) => axios.get(`${API_URL}/schedules/${id}`);

export const getDrivers = () => axios.get(`${API_URL}/drivers`);

export const getBuses = () => axios.get(`${API_URL}/buses`);

export const getRoutes = () => axios.get(`${API_URL}/routes`);

export const createSchedule = (scheduleData) => axios.post(`${API_URL}/schedules/create/`, scheduleData);

export const updateSchedule = (id, scheduleData) => axios.put(`${API_URL}/update-schedule/${id}/`, scheduleData);

export const deleteSchedule = (id) => axios.delete(`${API_URL}/delete-schedule/${id}/`);
