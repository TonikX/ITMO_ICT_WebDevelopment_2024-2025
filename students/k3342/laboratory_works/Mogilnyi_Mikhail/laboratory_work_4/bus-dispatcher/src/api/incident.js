import axios from 'axios';

const API_URL = 'http://localhost:8000/manage';

export const getIncidents = () => axios.get(`${API_URL}/incidents/`);

export const getIncidentById = (id) => axios.get(`${API_URL}/incidents/${id}/`);

export const createIncident = (incidentData) => axios.post(`${API_URL}/incidents/create/`, incidentData);

export const updateIncident = (id, incidentData) => axios.put(`${API_URL}/incidents/${id}/update/`, incidentData);

export const deleteIncident = (id) => axios.delete(`${API_URL}/incidents/${id}/delete/`);
