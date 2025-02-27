// src/store/slices/aircraftSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8080/backend_war/api';

export const fetchAircrafts = createAsyncThunk(
    'aircrafts/fetchAll',
    async (_, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_URL}/aircrafts`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data; // список Aircraft
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Fetch aircrafts failed');
        }
    }
);

export const createAircraft = createAsyncThunk(
    'aircrafts/create',
    async (aircraftData, { rejectWithValue }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`${API_URL}/aircrafts`, aircraftData, {
                headers: { Authorization: `Bearer ${token}` },
            });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Create aircraft failed');
        }
    }
);

// Добавьте другие экшены (update, delete) при необходимости

const initialState = {
    aircrafts: [],
    loading: false,
    error: null,
};

const aircraftSlice = createSlice({
    name: 'aircrafts',
    initialState,
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchAircrafts.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAircrafts.fulfilled, (state, action) => {
                state.loading = false;
                state.aircrafts = action.payload;
            })
            .addCase(fetchAircrafts.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.error || 'Fetch aircrafts failed';
            })
            .addCase(createAircraft.fulfilled, (state, action) => {
                state.aircrafts.push(action.payload);
            })
            .addCase(createAircraft.rejected, (state, action) => {
                state.error = action.payload?.error || 'Create aircraft failed';
            });
    },
});

export const { clearError } = aircraftSlice.actions;
export default aircraftSlice.reducer;
