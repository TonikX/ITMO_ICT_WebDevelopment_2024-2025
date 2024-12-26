import axios from 'axios';
import { Dog, Owner, Expert, Show, Participation, Grade } from '../shared/types';

export const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/api/',
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Token ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            console.error('Unauthorized! Redirecting to login...');
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// --------- Owners ---------
export const fetchOwners = async (search: string = ''): Promise<Owner[]> => {
    const response = await api.get('owners/', {
        params: {
            search,
        },
    });
    return response.data;
};

export const createOwner = async (data: Partial<Owner>): Promise<Owner> => {
    const response = await api.post('owners/', data);
    return response.data;
};

export const updateOwner = async (id: string, data: Partial<Owner>): Promise<Owner> => {
    const response = await api.put(`owners/${id}/`, data);
    return response.data;
};

export const deleteOwner = async (id: string): Promise<void> => {
    await api.delete(`owners/${id}/`);
};

// --------- Dogs ---------
export const fetchDogs = async (search: string = ''): Promise<Dog[]> => {
    const response = await api.get('dogs/', {
        params: {
            search,
        },
    });
    return response.data;
};
export const createDog = async (data: Partial<Dog>): Promise<Dog> => {
    const response = await api.post('dogs/', data);
    return response.data;
};

export const updateDog = async (data: Partial<Dog>): Promise<Dog> => {
    const response = await api.put('dogs/', data);
    return response.data;
};

export const disqualifyDog = async (id: string): Promise<{status: string}> => {
    const response = await api.post(`dogs/${id}/disqualify/`);
    return response.data;
};

export const deleteDog = async (id: string): Promise<{status: string}> => {
    const response = await api.delete(`dogs/${id}/`);
    return response.data;
};

// --------- Shows ---------
export const fetchShows = async (search: string = ''): Promise<Show[]> => {
    const response = await api.get('shows/', {
        params: { search },
    });
    return response.data;
};

export const createShow = async (data: Partial<Show>): Promise<Show> => {
    const response = await api.post('shows/', data);
    return response.data;
};

export const updateShow = async (id: string, data: Partial<Show>): Promise<Show> => {
    const response = await api.put(`shows/${id}/`, data);
    return response.data;
};

export const deleteShow = async (id: string): Promise<void> => {
    await api.delete(`shows/${id}/`);
};

// --------- Experts ---------
export const fetchExperts = async (search: string = ''): Promise<Expert[]> => {
    const response = await api.get('experts/', {
        params: { search },
    });
    return response.data;
};

export const createExpert = async (data: Partial<Expert>): Promise<Expert> => {
    const response = await api.post('experts/', data);
    return response.data;
};

export const updateExpert = async (id: string, data: Partial<Expert>): Promise<Expert> => {
    const response = await api.put(`experts/${id}/`, data);
    return response.data;
};

export const deleteExpert = async (id: string): Promise<void> => {
    await api.delete(`experts/${id}/`);
};

// --------- Participation ---------
export const fetchParticipations = async (): Promise<Participation[]> => {
    const response = await api.get('participations/');
    return response.data;
};

export const createParticipation = async (data: Partial<Participation>): Promise<Participation> => {
    const response = await api.post('participations/', data);
    return response.data;
};

// --------- Grade ---------
export const createGrade = async (data: Partial<Grade>): Promise<Grade> => {
    const response = await api.post('grades/', data);
    return response.data;
};
